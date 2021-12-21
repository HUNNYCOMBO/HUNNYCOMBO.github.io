---
layout: single
title:  "토비의 스프링 vol.1 5장"
categories: spring
tags: [spring, 서비스 추상화]
toc: true
author_profile: false
sidebar:
    nav: "docs"
search: true
---

## 서비스 추상화
5장에서는 지금까지 만든 DAO에 트랜잭션을 적용해보면서 스프링이 어떻게 성격이 비슷한 여러 종류의 기술을 추상화하고 이를 일관된 방법으로 사용하게 하는지 살펴봅니다.  

### 1. 사용자 레벨 관리 추가
우리는 단순히 UserDao를 이용한 CRUD기능을 만들었습니다. 이번에는 정기적으로 사용자의 활동내용윽 참고해서 레벨을 조정해주는 기능을 추가해봅니다.  
구현해야할 비지니스 로직은 다음과 같습니다.  

- 사용자 레벨은 BASIC, SILVER, GOLD 입니다.
- 가입 후 50회 이상 로그인하면 BASIC 에서 SILVER 레벨이 됩니다.
- SILVER 레벨 이면서 30번 이상 추천을 받으면 GOLD 레벨이 됩니다.
- 사용자 레벨의 변경 작업은 일정한 주기를 가지고 일괄적으로 진행됩니다.

#### 1-1. 필드 추가
DB는 varchar타입으로 선언하는 방법도있지만 각 레벨을 숫자화 해서 넣는 것이 더 편합니다. 이에 맞춰 User에 추가할 프로퍼티 역시 int 값이 되어야 하지만, 다른 종류의 정보를 넣는 실수를 해도 컴파일러가 체크하지 못하는 단점이 있습니다.  
그래서 자바 5 이상에서 제공하는 enum을 이용하는게 안전하고 편리합니다.  

```java
package springbook.user.domain;

public enum Level {
	BASIC(1), SILVER(2), GOLD(3);
    // 3개의 이넘 오브젝트. 들어갈 수 있는 값이 고정됐습니다.

	private final int value;
		
	Level(int value) {
		this.value = value;
        // DB에 저장할 값을 넣어줄 생성자 입니다.
	}

	public int intValue() {
		return value;
        // 값을 가져옵니다.
	}
	
	public static Level valueOf(int value) {
        // 값으로부터 Level 타입 오브젝트를 가져옵니다.
		switch(value) {
		case 1: return BASIC;
		case 2: return SILVER;
		case 3: return GOLD;
		default: throw new AssertionError("Unknown value: " + value);
		}
	}
}

```

다음은 User 클래스에 필드를 추가합니다. 로그인 횟수와, 추천수도 추가합니다.  

```java
public class User {
	String id;
	String name;
	String password;
	Level level;
	int login;
	int recommend;
	
	public User() {
	}
	
	public User(String id, String name, String password, Level level,
			int login, int recommend) { //생성자도 수정합니다.
		this.id = id;
		this.name = name;
		this.password = password;
		this.level = level;
		this.login = login;
		this.recommend = recommend;
	}


	public String getId() {
        ...
```

UserDaoJdbc와 테스트에도 필드를 추가해야합니다.

```java
// 픽스처 역시 수정합니다.

private void checkSameUser(User user1, User user2) {
		assertThat(user1.getId(), is(user2.getId()));
		assertThat(user1.getName(), is(user2.getName()));
		assertThat(user1.getPassword(), is(user2.getPassword()));
        // 아래부터 새로운 필드가 제대로 반영되었는지 비교하는 점검합니다.
		assertThat(user1.getLevel(), is(user2.getLevel()));
		assertThat(user1.getLogin(), is(user2.getLogin()));
		assertThat(user1.getRecommend(), is(user2.getRecommend()));

        // addAndGet() 에서 이 메소드를 사용하도록 합니다.
	}

// 클라이언트에서 테스트가성공하도록 변경합니다.
// enum을 이용한 set만 주의합니다.

// user를 get()
user.setLevel(Level.valueOf(rs.getInt("level")));

// update()
user.getLvel().intValue();
```

눈여겨볼 것은 Level 타입의 필드를 사용하는 부분입니다. enum 은 오브젝트이므로 DB에 저장될 수 있는 타입이 아닙니다. 따라서 정수형으로 변환해줘야 합니다.  
반대로 조회했을 떄는 valueOf()를 이용해 int의 값을 Level 타입 오브젝트로 만들어서 setLevl()에 넣어줍니다.

#### 1-2. 사용자 수정 기능 추가
사용자의 기본키인 id를 제외한 나머지 필드는 수정될 가능성이 많습니다. 이를 수정하는 테스트 메소드 먼저 만듭니다.  
User를 수정했을 때 원하는 로우가 수정됐는지 확인하기 위해, 변경한 로우 1개와 변경하지 않은 로우만 두고, checkSameUser()를 실행합니다.  
아래는 이를 성공시킬 udpate() 입니다.

```java
// 테스트
	@Test
	public void update() {
		dao.deleteAll();
		
		dao.add(user1);		// 수정할 사용자
		dao.add(user2);		// 수정하지 않을 사용자
		
		user1.setName("수정");
		user1.setPassword("springno6");
		user1.setLevel(Level.GOLD);
		user1.setLogin(1000);
		user1.setRecommend(999);
		
		dao.update(user1);
		
		User user1update = dao.get(user1.getId());
		checkSameUser(user1, user1update);
		User user2same = dao.get(user2.getId());
		checkSameUser(user2, user2same);
	}

// 메소드
public void update(User user) {
		this.jdbcTemplate.update(
				"update users set name = ?, password = ?, level = ?, login = ?, " +
				"recommend = ? where id = ? ", user.getName(), user.getPassword(), 
		user.getLevel().intValue(), user.getLogin(), user.getRecommend(),
		user.getId());
		
	}
```

#### 1-3. UserService.upgradeLevels()
사용자 관리 로직을 담을 클래스로 UserService를 만듭니다. UserService 클래스는 UserDao타입의 빈을 주입받아 사용합니다. 또한 UserSerivce의 테스트 클래스도 생성합니다.  
레벨 관리 기능을 구현하기는 어렵지 않습니다. UserDao의 getAll()메소드로 사용자를 모두 가져온 후, 사용자 별로 레벨 관리 작업을 진행하면서 UserDao의 update()를 호출해 DB에 결과를 저장하면 됩니다.  

```java
// xml 설정
<bean id = "userService" class="">
	<property name="userDao" ref="userDao" />
	// bean이름이 userDao인것을 userDao필드에 주입합니다.

public class UserService {
	private UserDao userDao;

	public void setUserDao(UserDao userDao){
		this.userDao = userDao;
	}

	public void upgradeLevels() {
		List<User> users = userDao.getAll();  
		for(User user : users) {  
			Boolean changed = null;
			// 변화를 확인하는 플래그 입니다.
			if (user.getLevel() == Level.BASIC && user.getLogin() >= 50) {  
				user.setLevel(Level.SILVER);
				changed = true;
				// 실버 업그레이드 조건에 맞으면 플래그를 트루로 줍니다.
			}
			else if(골드 업그레이드 조건){
				...
			}
			else if(user.getLevel() == Level.SILVER){changed == false;} // 골드레벨은 변화가 없습니다.
			else {changed == false;}	// 일치하는 조건이 없다면 false로 줍니다.

			if(changed){userDao.update(user);} // 레벨변경이 있었다면 update()를 호출합니다.
		}
	}
}

// 테스트 메소드
@RunWith(SpringJUnit4ClassRunner.class)
@ContextConfiguration(locations="/test-applicationContext.xml")
public class UserServiceTest {
	@Autowired 	UserService userService;	
	// userService는 스프링 빈이므로 테스트 컨텍스트를 통해 주입받을 수 있습니다.
	@Autowired UserDao userDao;
	
	List<User> users;	// test fixture
	
	@Before
	public void setUp() {
		users = Arrays.asList(	//배열을 리스트로 만들어주는 메소드 입니다.
				new User("bumjin", "name1", "p1", Level.BASIC, 49, 0),
				new User("joytouch", "name2", "p2", Level.BASIC, 50, 0),
				new User("erwins", "name3", "p3", Level.SILVER, 60, 29),
				new User("madnite1", "name4", "p4", Level.SILVER, 60, 30),
				new User("green", "name5", "p5", Level.GOLD, 100, 100)
				// 테스트는 업그레이드가 되는 경우와, 안되는 경우, GOLD일 때 5가지 경우로 테스트합니다.
				);
	}

	@Test
	public void upgradeLevels() {
		userDao.deleteAll();
		for(User user : users) userDao.add(user);
		
		userService.upgradeLevels();
		
		checkLevelUpgraded(users.get(0), Level.BASIC);
		checkLevelUpgraded(users.get(1), Level.SILVER);
		checkLevelUpgraded(users.get(2), Level.SIVER);
		checkLevelUpgraded(users.get(3), Level.GOLD);
		checkLevelUpgraded(users.get(4), Level.GOLD);
```

#### 5-4. UserService.add()
아직 남은 부분이 있습니다. 처음 가입하는 사용자는 기본적으로 BASIC 레벨이어야 한다는 것입니다. 이 로직을 담기위해서 적합한 부분은 UserService입니다.  
UserService에도 add()를 만들어두고 사용자가 등록될 때 적용할 만한 비지니스 로직을 담당하게 합니다.  
테스트 케이스는 레벨이 미리 정해진 경우와 레벨이 비어있는 경우로 두고 진행합니다.  

```java
@Test
public void add(){
	userDao.deleteAll();

	User userWithLevel = users.get(4);	//미리 정해진 경우 초기화 하지 않습니다.
	User userWithoutLevel = users.get(0);
	userIwthoutLevel.setLevel(null);	//레벨이 비어있는 사용자는 BASIC으로 설정합니다.

	userService.add(userWithLevel);
	UserService.add(userWithoutLevel);

	User userWithLevelRead = userDao.get(userWithLevel.getId());
	User userWithoutLevelRead = userDao.get(userWithoutLevel.getId());
	// DB에 저장된 결과를 가져와 확인합니다.

	assertThat(userWithLevelRead.getLevel(), is(userWithLevel.getLevel())); 
	assertThat(userWithoutLevelRead.getLevel(), is(Level.BASIC));
}

// 구현한 add()
public void add(User user){
	if (user.getLevel() == null) user.setLevel(Level.BASIC);
	userDao.add(user);
}
```
테스트는 성공이지만 DAO와 DB까지 동원되는 점이 불편합니다. 간결하게 만드는 법은 뒤에서 다시 다뤄봅니다.  

#### 1-5. 코드개선
UserService의 upgradeLevels()를 살펴보면 if블록들이 읽기 불편합니다. 또, 업그레이드 조건이 변경됐을 때, 조건문을 수정해줘야 합니다. 또, 레벨과 업그레이드를 동시에 비교하는 부분도 추후 레벨이 추가해야 되면 문제가 될 수 있습니다.  
이 코드를 리팩토링 해봅니다. 자주 변경될 가능성이 있는 구체적인 내용과 로직을 분리합니다.  

```java
public void upgradeLevels() {
		List<User> users = userDao.getAll();  
		for(User user : users) {  
			if (canUpgradeLevel(user)) {  
				// 주어진 user에 업그레이드가 가능하면 true를 리턴하게 합니다.
				upgradeLevel(user);  
			}
		}
	}

private boolean canUpgradeLevel(User user) {
		Level currentLevel = user.getLevel(); 
		switch(currentLevel) {                                   
		case BASIC: return (user.getLogin() >= MIN_LOGCOUNT_FOR_SILVER); 
		case SILVER: return (user.getRecommend() >= MIN_RECCOMEND_FOR_GOLD);
		case GOLD: return false;
		// 레벨별로 구분해서 조건을 판단합니다.
		default: throw new IllegalArgumentException("Unknown Level: " + currentLevel); 
		// 현재 로직에서 없는 레벨이 주어지면 예외를 발생시킵니다.
		}
	}

	private void upgradeLevel(User user) {
		if (user.getLevel() == Level>BASIC) user.setLevel(Level.SILVER);
		else if(골드조건) ...
		userDao.update(user);
	}
```
코드가 하는 구체적인 내용은 모르지만 직관적으로 어떤 작업을하는지 이해할 수 있습니다.  
하지만 upgradeLevel()가 마음에 들지 않습니다. 로직이 노골적으로 드러나있고, 예외 상황 처리도 없습니다. 이것도 더 분리해봅니다.  
먼저 레벨의 순서와, 다음 단계 레벨이 무엇인지를 결정하는 일은 enum인 Level클래스에 맡기도록 합니다.  

```java
public enum Level {
	GOLD(3, null), SILVER(2, GOLD), BASIC(1, SILVER);  
	// DB에 저장할 값과, 다음 단계의 레벨 정보를 추가합니다.
	
	private final int value;
	private final Level next; //다음 단계의 정보를 스스로 갖도록 필드를 추가합니다.
	
	Level(int value, Level next) {  
		this.value = value;
		this.next = next; 
	}
	
	public int intValue() {
		return value;
	}
	
	public Level nextLevel() { 
		return this.next;
		// 다음 레벨이 무엇인지 호출합니다.
	}
	
	public static Level valueOf(int value) {
		switch(value) {
		case 1: return BASIC;
		case 2: return SILVER;
		case 3: return GOLD;
		default: throw new AssertionError("Unknown value: " + value);
		}
	}
}
```
이렇게 Level이 업그레이드 순서를 담당하면서 일일이 if 조건식을 비즈니스 로직에 담아둘 필요가 없어졌습니다.  
이번에는 사용자 정보가 바뀌는 부분을 UserService 메소드에서 User로 옮깁니다. User의 내부 정보가 변경되는 것은 User가 스스로 다루는 게 적절합니다. User는 단순한 자바빈이지만 엄연히 자바 오브젝트이기에 내부 정보를 다루는 기능이 있을 수 있습니다. User에 아래 메소드를 추가합니다.

```java
public void upgradeLevel(){
	Level nextLevel = this.level.nextLevel();
	// Level타입의 필드 level에게 다음 레벨이 무엇인지 알려달라고 요청합니다.
	if(nextLevel == null){
		throw new IllegalStateException(this.level = "은 업그레이드가 불가능합니다.");
		// 업그레이드가 진행되지 않도록 예외를 던집니다.
	}
	else{
		this.level = nextLevel;
	}
}
```

이제 한결 간결해진 UserSerivce의 upgradeLevel()입니다. UserSerivce는 User오브젝트에게 알아서 업그레이드에 필요한 작업을 수행하라고 요청만 합니다.  

```java
public void upgradeLevel(User user){
	user.upgradeLevel();
	userDao.update(user);
}
```
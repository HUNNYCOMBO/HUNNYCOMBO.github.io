---
layout: single
title:  "토비의 스프링 vol.1 5장"
categories: spring
tags: [spring, 서비스 추상화]
toc: true
toc_sticky : true
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

#### 1-4. UserService.add()
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

이처럼 객체지향적인 코드는 데이터를 요구하는 것이 아닌 데이터를 갖고있는 다른 오브젝트에게 작업을 해달라고 요청해야합니다. 지금 코드는 UserService는 User에게 레벨 업그레이드 작업을 요청하고,  
User는 Level에게 다음 레벨이 무엇인지 알려달라 요청하고 있습니다.  

이제 User의 upgradeLevel()에 대한 테스트도 만들어봅니다.  

```java
public class UserTest {
	User user;
	
	@Before
	public void setUp() {
		user = new User();
		// User는 스프링 빈이 관리하는 객체가 아니므로 생성자를 호출합니다.
	}
	
	@Test()
	public void upgradeLevel() {
		Level[] levels = Level.values();
		// enum에 정의된 모든 level을 가져옵니다.
		for(Level level : levels) {
			if (level.nextLevel() == null) continue;
			// 다음 단계가 null인 경우 아래 코드를 실행하지 않습니다.
			user.setLevel(level);
			user.upgradeLevel();
			assertThat(user.getLevel(), is(level.nextLevel()));
		}
	}
	
	@Test(expected=IllegalStateException.class)
	public void cannotUpgradeLevel() {
		// 더 이상 업그레이드 할 레벨이 없는 경우 예외상황 테스트입니다.
		Level[] levels = Level.values();
		for(Level level : levels) {
			if (level.nextLevel() != null) continue;
			// null일 경우만 테스트 합니다.
			user.setLevel(level);
			user.upgradeLevel();
		}
	}
}
```

UserServiceTest도 아직 개선할 사항이 남아있습니다. 기존 테스트에서는 checkLevel()을 호출할 때 일일이 다음 단계의 레벨이 무엇인지 넣어주었습니다. Level이 갖고 있어야 할 다음 레벨이 무엇인지는 테스트에 직접 넣어둘 필요가 없습니다. 아래와 같이 upgradeLevels()를 수정합니다.

```java
@Test
	public void upgradeLevels() {
		userDao.deleteAll();
		for(User user : users) userDao.add(user);
		
		userService.upgradeLevels();
		
		checkLevelUpgraded(users.get(0), false);
		checkLevelUpgraded(users.get(1), true);
		checkLevelUpgraded(users.get(2), false);
		checkLevelUpgraded(users.get(3), true);
		checkLevelUpgraded(users.get(4), false);
	}

	private void checkLevelUpgraded(User user, boolean upgraded) {
		// 파라미터를 통해 어떤 레벨로 바뀔것인가가 아닌, 다음 레벨로 업그레이드가 될 여부를 지정합니다.
		User userUpdate = userDao.get(user.getId());
		if (upgraded) {
			assertThat(userUpdate.getLevel(), is(user.getLevel().nextLevel()));
			// 어떤 레벨로 바뀔 것인지는 Level에게 요청합니다.
		}
		else {
			assertThat(userUpdate.getLevel(), is(user.getLevel()));
			// 업그레이드가 일어나지 않은 부분입니다.
		}
	}
```

이렇게 수정하면, 로직이 들어나지 않으면서 각 사용자에 대해 업그레이드를 확인하려는 것인지 아닌지가 true,false로 쉽게 나타나 있어서 보기 좋습니다.  
다음은 UserService 클래스의 업그레이드 조건인 부분도 중복되어 나타나기에 수정합니다. 한 가지 변경 이유가 바생했을 때 여러 군데를 고치게 만든다면 중복입니다.  

```java
public class UserService {
	public static final int MIN_LOGCOUNT_FOR_SILVER = 50;
	public static final int MIN_RECCOMEND_FOR_GOLD = 30;
	// 로그인 조건으로 둘 상수를 선언합니다.

		private boolean canUpgradeLevel(User user) {
		Level currentLevel = user.getLevel(); 
		switch(currentLevel) {                                   
		case BASIC: return (user.getLogin() >= MIN_LOGCOUNT_FOR_SILVER); 
		case SILVER: return (user.getRecommend() >= MIN_RECCOMEND_FOR_GOLD);
		// 상수 도입
		case GOLD: return false;
		default: throw new IllegalArgumentException("Unknown Level: " + currentLevel); 
		}
	}

// 테스트에서도 해당 상수를 이용하게끔 바꿉니다.

public class UserServiceTest {
	@Autowired 	UserService userService;	
	@Autowired UserDao userDao;
	
	List<User> users;	// test fixture
	
	@Before
	public void setUp() {
		users = Arrays.asList(
				new User("bumjin", "name1", "p1", Level.BASIC, MIN_LOGCOUNT_FOR_SILVER-1, 0),
				// 테스트에선 가능한 경계값을 설정하는게 좋습니다.
				new User("joytouch", "name2", "p2", Level.BASIC, MIN_LOGCOUNT_FOR_SILVER, 0),
				new User("erwins", "name3", "p3", Level.SILVER, 60, MIN_RECCOMEND_FOR_GOLD-1),
				new User("madnite1", "name4", "p4", Level.SILVER, 60, MIN_RECCOMEND_FOR_GOLD),
				new User("green", "name5", "p5", Level.GOLD, 100, Integer.MAX_VALUE)
				);
	}
```

상수를 도입함으로서 무슨 의도로 어떤 값을 넣었는지 이해하기 쉬워졌습니다. 만약 레벨을 업그레이드하는 정책을 유연하게 변경하고 싶다면, UserService에서 그떄그떄 코드를 수정하기보단,  
UserService에서 분리하는 방법을 고려하면 됩니다. 분리된 업그레이드 정책을 담은 오브젝트는 DI를 통해 UserService에 주입합니다.  

### 2. 트랜잭션 서비스 추상화
#### 2-1. 모 아니면 도
만약 정기 사용자 레벨 관리 작업을 하는 도중 오류가 생겨서 작업을 완료할 수 없다면, 그떄까지 변경된 작업은 그대로 둘지 모두 초기 상태로 돌려놔야 하는지에 대한 질문이 나왔습니다. 그렇다면 지금까지 만든 코드는 어떻게 작동할까요? 테스트를 만들어 확인해봅니다. 5명의 사용자를 업그레이드 하다 중간에 예외를 일으키게 합니다.  
이를 위해 직접 UserService 코드를 건들이는 것은 좋지 않으므로, UserService를 상속받은 클래스를 만들어 사용합니다. 테스트에서만 사용할 클래스라면 테스트 클래스 내부에 스태틱 클래스로 만드는 것이 간편합니다.  
UserService의 메소드는 대부분 private로 선언되 있어 접근이 불가하므로, 이런 일은 피하는게 좋지만 어쩔 수 없이 upgradeLevel()의 접근 제한자를 protected로 수정합니다.  

```java
@RunWith(SpringJUnit4ClassRunner.class)
@ContextConfiguration(locations="/test-applicationContext.xml")
public class UserServiceTest {
	static class TestUserService extends UserService {
		// 내부 스태틱 클래스
		private String id;

		private TestUserService(String id){
			// 예외를 발생시킬 User 오브젝트의 id를 지정합니다.
			this.id = id;
		}

		@overide
		protected void upgradeLevel(User user) {
			if(user.getId().equals(this.id)) throw new TEstUserServiceException();
			// 지정된 User 오브젝트가 발견되면 예외를 던져 작업을 강제로 중단합니다.
			super.upgradeLevel(user);
		}
	}

	static class TestUserServiceException extends RuntimeException{
		// 다른 예외와 구분하기 위해 정의
	}

	@Test
	public void upgradeAllOrNothing(){
		UserService testUserService = new TestUserService(users.get(3).getId());  
		// 스프링 빈에 등록하지 않고 직접 만듭니다.
		testUserService.setUserDao(this.userDao); 
		// 수동 DI, UserService를 상속받아 사용할수 있는 메소드입니다. DAO는 스프링 빈입니다.
		// 컨테이너에 종속적이지 않은 스프링 DI 스타일의 장점입니다.
		testUserService.setDataSource(this.dataSource);
		 
		userDao.deleteAll();			  
		for(User user : users) userDao.add(user);
		
		try {
			testUserService.upgradeLevels();   
			fail("TestUserServiceException expected"); 
			// 혹시 코드를 잘못작성해서 예외 발생이없다면 fail()에 의해 테스트가 실패합니다.
		}
		catch(TestUserServiceException e) { 
			// 예외를 잡아서 계속 진행되도록 합니다.
		}
		
		checkLevelUpgraded(users.get(1), false);
		// 예외가 발생하기 전에 레벨 변경이 있었던 사용자의 레벨이 롤백되었는지 확인합니다.
	}
}
```

이렇게 테스트를 돌려보면 우리의 코드는 오류전 업그레이드 된 채로 유지되는 것을 알 수 있습니다. 이런 문제는 **트랜잭션** 문제입니다.  
모든 사용자의 레벨을 업그레이드하는 작업인 upgradeLevel()이 하나의 트랜잭션 안에서 동작하지 않았기 떄문입니다.

> 트랜잭션 : 더 이상 나눌 수 없는 단위 작업(원자성)

모든 사용자에 대한 업그레이드 작업은 전체가 다 성공하던지 다 실패해야 합니다.  


#### 2-2. 트랜잭션 경계설정
DB는 그 자체로 완벽한 트랜잭션을 지원합니다. SQL을 이용해 다중 로우를 수정할때 일부 로우만 수정하는 경우는 없습니다. 하지만 여러 개의 SQL이 사용되는 작업을 하나의 트랜잭션으로 취급해야 하는 경우도 있습니다.  
대표적으로 계좌이체같은 경우입니다. 이체를 할 때는 출금계좌의 잔고는 이체금액만큼 줄어들고, 입금계좌에는 이체금액만큼 증가해야 합니다. 첫번째 SQL을 성공적으로 실행했지만 두번쨰 SQL이 중단됐다면, 앞에서 처리한 SQL작업도 취소시켜야합니다. 이런 작업을 **트랜잭션 롤백**이라고 합니다.  
여러 개의 SQL을 하나의 트랜잭션으로 처리하는 경우에 모든 SQL 작업을 성공적으로 마무리했다고 DB에 알려줘서 작업을 화정시키는 것은 **트랜잭션 커밋**이라고 합니다.  

모든 트랜잭션은 시작하는 지점과 끝나는 지점이 있습니다. 끝나는 방법은 두가지 롤백과 커밋 두가지입니다. 애플리케이션 내에서 트랜잭션이 시작되고 끝나는 위치를 트랜잭션의 경계라고 합니다. 이 트랜잭션 경계를 설정하는 일은 매우 중요한 작업입니다.  

JDBC의 트랜잭션은 하나의 Connection을 가져와 사용하다가 닫는 사이에 일어납니다. 즉 트랜잭션의 시작과 종료는 Connection오브젝트를 통해 이루어집니다. 기본 설정은 작업마다 자동 커밋해 트랜잭션을 끝내버리므로 여러개의 DB작업을 모아서 트랜잭션을 만드는 기능이 꺼져있습니다. setAutoCommit(false)를 이용해 트랜잭션의 시작을 선언하고 commit()또는rollback()으로 종료합니다. 이런 작업을 트랜잭션의 경계설정 이라고 합니다. 하나의 DB커넥션 안에서 만들어지는 트랜잭션을 로컬 트랜잭션 이라고 합니다.  


```java
Connection c = dataSource.getConnection();

c.setAutoCommit(false); //트랜잭션 시작
try{
	excute1;
	...
	execute2;

	c.commit();
}
catch(){
	c.rooback();
}
c.close();
```

JdbcTemplate은 하나의 템플릿 메소드 안에서 Connection을 가져오고 작업을 마치면 닫아주고 템플릿메소드를 빠져나옵니다. 이렇게 보면 JdbcTemplate의 메소드를 사용하는 UserDao는 메소드마다 독립적인 트랜잭션으로 실행될 수 밖에없습니다. upgradeAllOrNothing() 에는 순차적으로 진행하다 2번째 사용자에서 레벨을 변경하고 트랜잭션을 종료시키기 떄문에 그 결과가 DB에 남아있는 것입니다.  
DAO 메소드에서 DB커낵션을 매번 만들기 떄문에 결국 DAO를 사용하면 UserService내에서 진행되는 여러가지 작업을 하나의 트랜잭션으로 묶는 일이 불가능해집니다.  

이를 해결하려면 UserSerivce에서 트랜잭션의 경계설정 작업을 하도록 해야합니다. 트랜잭션 경계를 upgradeLevel()안에 두려면 DB 커낵션도 이 메소드 안에서 만들고 종료시켜야 합니다.  
하지만 이 방법은 결국 지금까지 해왔던 SoC, 싱글톤(**트랜잭션을 위해 메소드마다 connection 객체를 계속 파라미터로 넘겨야 함**), 독립, DI, 테스트 코드 등의 장점들을 없애버리는 문제가 발생합니다.  

#### 2-3. 트랜잭션 동기화
스프링은 이 문제를 해결할 수 있는 멋진 방법을 제공합니다. 먼저 upgradeLevels()안에서 만들어진 connection객체를 필요할때마다 파라미터로 넘기는 문제는 트랜잭션 동기화 방식으로 해결합니다.  

> 트랜잭션 동기화 : DAO가 사용하는 JdbcTempalte이 트랜잭션을 시작하기 위해 만든 Conenction 오브젝트를 특별한 저장소에 보관하고, 이후 호출되는 메소드에서는 이를 사용하게 함.

작업 흐름은 다음과 같습니다.  

1. UserService는 Connection을 생성
2. 이를 트랜잭션 동기화 저장소에 저장해두고 setAutoCommit(false)를 호출해 트랜잭션 시작
3. 첫 번째 update()가 호출되고, update() 내부에서 사용하는 JdbcTemplate 메소드에서는
4. 트랜잭션 동기화 저장소에 현재 시작된 트랜잭션을 가진 Connection 오브잭트가 존재하는지 확인
5. 있다면 발견하고 가져온 connection을 이용해 preparedStatement를 만들어 SQL을 실행하고, 닫지는 않은채로 마침
6. connection은 열려있고 트래잭션은 진행중인 채로 저장소에 저장되어있음
7. 두번째 update() 호출 이후 4번부터 반복
8. 정상적으로 끝났으면 commit()을 호출해 완료, 예외시 rollback()
9. connection 닫음

트랜잭션 동기화 저장소는 작업 스레드마다 독립적으로 connection오브젝트를 저장하고 관리하기 떄문에 서버의 멀티스레드 환경에서도 충돌이 날 염려가 없습니다.  

```java
	private DataSource dataSource;  			
	// Db커넥션을 직접 다루므로 DI 설정을 해줍니다.

	public void setDataSource(DataSource dataSource) {
		this.dataSource = dataSource;
	}

		public void upgradeLevels() throws Exception {
		TransactionSynchronizationManager.initSynchronization();  
		// 트랜잭션 동기화 관련 클래스입니다. 트랜잭션 동기화 작업을 초기화합니다.
		Connection c = DataSourceUtils.getConnection(dataSource); 
		// DataSoruceUtils에서 제공하는 메소드를 통해 DB커넥션을 생성합니다.
		// dataSoruce에서 직접 가져오지 않는 이유는 트랜잭션 동기화에 사용하도록 저장소에 바인딩해주기 때문입니다.
		c.setAutoCommit(false);
		// 트랜잭션 시작
		
		try {									   
			List<User> users = userDao.getAll();
			for (User user : users) {
				if (canUpgradeLevel(user)) {
					upgradeLevel(user);
				}
			}
			c.commit();  
		} catch (Exception e) {    
			c.rollback();
			throw e;
		} finally {
			DataSourceUtils.releaseConnection(c, dataSource);	
			// 닫을때도 스프링 유틸리티 메소드를 이용합니다.
			TransactionSynchronizationManager.unbindResource(this.dataSource);  
			TransactionSynchronizationManager.clearSynchronization();  
			// 동기화 작업 종료도 해줘야 합니다.
		}
	}

	// UserServiceTest의 upgradeAllOrNothing()에 dataSource빈을 가져와 주입해주는 @autowired와 수정자메소드를 선언해줍니다.
	// 트랜잭션에 동기화에 필요한 datasource를 DI해줘야 하기 때문입니다.
	public class UserServiceTest {
	@Autowired UserService userService;	
	@Autowired UserDao userDao;
	@Autowired DataSource dataSource;

	@Test
	public void upgradeAllOrNothing() {
		UserService testUserService = new TestUserService(users.get(3).getId());  
		testUserService.setUserDao(this.userDao);
		testUserService.setDataSource(this.dataSource);
		...
	}
	
	@Test
	public void upgradeLevels() throws Exception {
		userDao.deleteAll();
		for(User user : users) userDao.add(user);
		
		userService.upgradeLevels();
		// 스프링 빈인 userService를 사용해야 합니다. userService의 필드 dataSource가 스프링 빈으로 등록되 DI받아야 합니다.
		// xml설정에 프로퍼티로 dataSource를 추가합니다.
		
		checkLevelUpgraded(users.get(0), false);
		checkLevelUpgraded(users.get(1), true);
		checkLevelUpgraded(users.get(2), false);
		checkLevelUpgraded(users.get(3), true);
		checkLevelUpgraded(users.get(4), false);
	}
	}

	<bean id="userService" ...>
		<property name="dataSoruce" ref="dataSource" />
```

JdbcTemplate은 영리하게 작동합니다. 미리 생성된 트랜잭션 동기화 저장소에 등록된 커넥션이 없는 경우 직접 DB커넥션을 만들고 트랜잭션을 시작하지만, 트랜잭션 동기화를 시작해놓았다면 직접 DB커넥션을 만드는 대신 트랜잭션 동기화 저장소에 들어있는 DB커낵션을 사용합니다. 따라서 트랜잭션 적용 여부에 맞춰 UserDao 코드를 수정할 필요가 없습니다.  
JDBC 코드의 try/catch 흐름 지원, SQL예외 지원과 함께 JdbcTemplate이 제공하는 세가지 유용한 기능 중 하나입니다.  

#### 2-4. 트랜잭션 서비스 추상화
문제가 하나 발생했습니다. 한 회사에서 이 사용자 관리 모듈을 사용하기로 했는데 이 회사는 여러개의 DB를 사용하고 있다고 가정합니다. 그래서 하나의 트랜잭션 안에서 여러 개의 DB에 데이터를 넣는 작업을 해야 할 필요가생겼습니다. 로컬 트랜잭션은 하나의 DB Connection에 종속되기 떄문에 한개 이상의 DB로의 작업을 하나의 트랜잭션으로 만드는건 불가능합니다.  

따라서 별도의 트랜잭션 관리자를 통해 트랜잭션을 관리하는 **글로벌 트랜잭션** 방식을 사용해야 합니다. 자바는 이런 글로벌 트랜잭션을 지원하는 트랜잭션 매니저를 지원하기 위한 API인 JTA(Java Transaction API)를 제공합니다.  
애플리케이션에서는 기존의 방법대로 DB는 JDBC, 메세징 서버라면 JMS 같은 API를 사용해서 필요한 작업을 수행합니다. 단, 트랜잭션은 JDBC나 JMS API를 직접 제어하지않고 JTA를 통해 트랜잭션 매니저가 관리하도록 위임합니다. 트랜잭션 매니저는 DB와 메세징 서버의 리소스 매니저와 XA 프로토콜을 통해 연결됩니다. 일단은 하나 이상의 DB가 참여하는 트랜잭션을 만들려면 JTA를 사용해야 한다는 사실만 기억해둡니다.  

[![](https://mermaid.ink/img/eyJjb2RlIjoiZ3JhcGhcbiAgICBBW-yVoO2UjOumrOy8gOydtOyFmF0gLS0-fEpEQkN8IEJb66as7IaM7IqkIOunpOuLiOyggCAvIERCIDFdXG4gICAgQSAtLT58SkRCQ3wgQ1vrpqzshozsiqQg66ek64uI7KCAIC8gREIgMl1cbiAgICBBIC0tPnxKVEF8IERb7Yq4656c7J6t7IWYIOunpOuLiOyggCAvIO2KuOuenOyereyFmCDshJzruYTsiqRdXG4gICAgRCAtLT58WEHtlITroZzthqDsvZx8IEJcbiAgICBEIC0tPnxYQe2UhOuhnO2GoOy9nHwgQ1xuICAgIEEgLS0-fEpNU3wgRVvrpqzshozsiqQg66ek64uI7KCAIC8gSk1TIOyEnOuyhF1cbiAgICBEIC0tPnxYQe2UhOuhnO2GoOy9nHwgRSIsIm1lcm1haWQiOnsidGhlbWUiOiJkYXJrIn0sInVwZGF0ZUVkaXRvciI6ZmFsc2UsImF1dG9TeW5jIjp0cnVlLCJ1cGRhdGVEaWFncmFtIjpmYWxzZX0)](https://mermaid.live/edit#eyJjb2RlIjoiZ3JhcGhcbiAgICBBW-yVoO2UjOumrOy8gOydtOyFmF0gLS0-fEpEQkN8IEJb66as7IaM7IqkIOunpOuLiOyggCAvIERCIDFdXG4gICAgQSAtLT58SkRCQ3wgQ1vrpqzshozsiqQg66ek64uI7KCAIC8gREIgMl1cbiAgICBBIC0tPnxKVEF8IERb7Yq4656c7J6t7IWYIOunpOuLiOyggCAvIO2KuOuenOyereyFmCDshJzruYTsiqRdXG4gICAgRCAtLT58WEHtlITroZzthqDsvZx8IEJcbiAgICBEIC0tPnxYQe2UhOuhnO2GoOy9nHwgQ1xuICAgIEEgLS0-fEpNU3wgRVvrpqzshozsiqQg66ek64uI7KCAIC8gSk1TIOyEnOuyhF1cbiAgICBEIC0tPnxYQe2UhOuhnO2GoOy9nHwgRSIsIm1lcm1haWQiOiJ7XG4gIFwidGhlbWVcIjogXCJkYXJrXCJcbn0iLCJ1cGRhdGVFZGl0b3IiOmZhbHNlLCJhdXRvU3luYyI6dHJ1ZSwidXBkYXRlRGlhZ3JhbSI6ZmFsc2V9)

아래는 JTA를 이요한 트랜잭션 코드 구조입니다.
```java
InitialContext ctx - new InitialContext();
UserTransaction tx = (UserTransaction)ctx.lookup(USER_TX_JNDI_NAME);
// JNDI를 이용해 서버의 UserTransaction 오브젝트를 가져옵니다.

tx.begin();
Connection c = dataSource.getConnect();
// JNDI로 가져온 dataSource를 이용합니다.
try{
	// DA 코드
	tx.commit();
}catch(){
	tx.rollback();
	throw e;
}finayll{
	c.close();
}
```

문제는 JDBC 로컬 트랜잭션을 JTA를 이용하는 글로벌 트랜잭션으로 바꾸려면 UserService의 코드를 수정해야 합니다. 로컬 트랜잭션을 사용하는 고객을 위해서는 JDBC를 이용한 트랜잭션 관리 코드를, 글로벌 트랜잭션을 필요로 하는 곳을 위해서는 JTA를 이용한 트랜잭션 관리 코드를 적용해야 한다는 문제가 생깁니다. UserService의 로직이 바뀌지 않았음에도 기술 환경에따라서 코드가 바뀌어버리게 돼버렸습니다.  
또, 하이버네이트를 이용하는 경우에도 트랜잭션 관리 코드가 JDBC나 JTA의 코드와 다르기 떄문에(Connection대신 Session과 독자적인 트랜잭션 관리 API를 사용) 코드를 변경해야 합니다.  

즉, **JDBC에 종속적인 Conection을 이용한 트랜잭션 코드**가 UserService에 등장하면서 부터 UserDao의 구현 클래스에 의존하는 코드가 돼버렸습니다.  
UserService의 메소드 안에서 트랜잭션 경계설정 코드를 제거할 수는 없지만, 특정 기술에 의존적인 Connection기능 오브젝트에 종속되지 않게 할 수 있는 방법이 있습니다.  
트랜잭션의 경계설정을 담당하는 코드는 유사한 구조를 갖습니다. 여러 기술의 사용법에 공통점이 있다면 추상화를 생각해볼 수 있습니다.  

> 추상화 : 하위 시스템의 공통점을 뽑아내서 분리시킵니다. 하위 시스템이 바뀌어도/무엇인지 알지 못해도 일관된 방법으로 접근가능 합니다. 예를들면 DB는 모두 SQL을 사용하는 공통점이 있기에, 이를 뽑아내 추상화한 JDBC가 있습니다. JDBC는 DB종류에 상관없이 일관된 방법으로 데이터 엑세스 코드를 제공합니다.

스프링은 트랜잭션 기술의 공통점을 담은 트랜잭션 추상화 기술을 제공하고 있습니다. PlatformTransactionManager 추상 인터페이스 입니다. 

```java
public void upgradeLevels(){
	PlatformTransactionManager transactionManager = new DataSourceTransactionManager(dataSource);
	// JDBC를 이용할 때는 해당 구현 클래스를 이용하여 dataSoruce를 파라미터로 넘깁니다.
	// 적용 기술에 따라 구현 클래스가 바뀝니다.
	// transactionManager = new JTATrasactionManager(); 로 바꾸어도 메소드는 바꾸지않아도 됩니다.

	TransactionStatus status = transactionManager.getTransaction(new DefaultTransactionDefinition());
	// getTransaction()으로 트랜잭션을 시작합니다. 기존 JDBC에서는 Connection을 생성하고 트랜잭션을 시작한것과 다릅니다.
	// 필요에 따라 트랜잭션 매니저가 DB 커낵션을 가져오는 역할을 합니다.
	// 파라미터 오브젝트는 트랜잭션에 대한 속성을 담고있습니다.
	// 시작된 트랜잭션은 status에 저장됩니다.

	try{
		List<User> users = userDao.getAll();
		for (User user : users){
			if (canUpgradeLevel(user)){
				upgradeLevel(user);
			}
		}
	transactionManager.commit(status);
	// 트랜잭션에 대한 조작이 필요할때 PlatformTransactionManager 메소드의 파라미터로 넘겨주면 됩니다.
	} catch(RuntimeException e){
		transactionManager.rollback(status);
		thorw e;
	}
}
```

어떤 트랜잭션 매니저 구현 클래스를 사용할지 UserService가 알고 있는 것은 DI 원칙에 위배되므로, 스프링의 DI방식으로 외부에서 주입받도록 수정합니다.  
DataSourceTransactionManager를 스프링 빈으로 등록해야하는데, 어떤 클래스든 빈으로 등록할 때 먼저 검토해야할 것은 싱글톤으로 만들어져 여러 스레드에서 동시에 사용해도 괜찮은가에 대한 것입니다. 무상태가아니고 멀티스레드환경에 safe하지 않다면 문제가 발생합니다. 스프링이 제공하는 PlatformTransactionManager 구현 클래스들은 싱글톤으로 사용이 가능합니다.  

```java
public class UserService {
	...
	private PlatformTransactionManager transactionManager;
	// DI 받도록 수정자메소드와 필드를 추가합니다.
	
		public void setTransactionManager(PlatformTransactionManager transactionManager) {
			// 관례예외적으로 PlatFormtransactionManager의 수정자 메소드와 변수명은 transactionManager로 합니다.
		this.transactionManager = transactionManager;
	}

// xml
<bean id="userService" ...>
	<property name="transactionManager" ref...>
	// 기존의 dataSource 프로퍼티를 없앱니다.

<bean id="transactionManager" ...>
	<property name="dataSource" ref...>
	// dataSoruce 빈으로부터 Connection을 가져와 처리하기 트랜잭션을 처리하기 때문에 dataSource 프로퍼티를 가져야 합니다.

// 테스트에서도 수동 DI를 하는 upgradeAllOrNothing()는 수정이 필요합니다.
public class UserSerivceTest{
	@Autowired
	PlatformTransacitonManager transactionManager;
	// 스프링 컨테이너로부터 transactionManager 빈을 주입받습니다.

	@Test
	public void upgradeAllOrNothing() thorws Exception{
		...
		testUserService.setTransactionManager(transactionManager);
		// 수동 DI
	}
}
```

UserSerivce는 트랜잭션 기술에서 완전히 독립적인 코드가 됐습니다. 사용 DB가 바뀌어도 UserSerivce의 코드는 조금도 수정할 필요가 없습니다.  

### 3. 서비스 추상화와 단일 책임 원칙
UserDao와 UserService는 각각 담당하는 로직에 따라 분리되고, 독자적으로 확장이 가능하도록 만들었습니다. 같은 애플리케이션 내, 즉 같은 계층에서 수평적인 분리라고 볼 수 있습니다.  
하지만 트랜잭션의 추상화는 이와는 다릅니다. 애플리케이션의 비지니스 로직과 그 하위에서 동작하는 로우레벨의 트랜잭션 기술이라는 다른 계층의 특성을 갖는 코드를 분리했습니다. 수직적인 분리 입니다.  

||||
|--|--|--|
|애플리케이션 계층|UserService|UserDao|
|서비스 추상화 계층 |TransactionManager |DataSource |
|기술 서비스 계층| JDBC, JTA, JNDI, WAS, ...|

수평적(애플리케이션 로직의 종류), 수직적(로직과 기술) 모두 결합도가 낮으며 서로 영향을 주지않고 자유롭게 확장될 수 있는 구조를 스프링 DI가 책임을 집니다.  
**DI가 없었다면 인터페이스를 도입해서 추상화를 했더라도, 적지않은 코드 사이의 결합이 남아있게 됩니다.  **
바로 위의 new DataSoruceTransactionManager()라는 구체적인 의존 클래스 정보가 드러나는 코드가 존재할 때를 보면 로우레벨의 변화가 있을 때마다 비즈니스 로직을 담은 코드의 수정이 발생합니다. 하나를 수정하면 여러곳을 수정해야 합니다.  

이런 적절한 분리가 가져오는 특징은 단일 책임 원칙(SRP)으로 설명할 수 있습니다.

> Single Responsibility Principle : 하나의 모듈은  한 가지 책임을 가져야 한다. 하나의 모듈이 바뀌는 이유는 한 가지여야 한다.

UserSerivce에 JDBC Connection 메소드를 직접 이용하는 트랜잭션 코드가 들어있을 때를 생각해보면, 두가지 책임을 갖고, 코드가 수정되는 이유가 두가지 이유라는 뜻입니다.

결국 객제치향 설계는 인터페이스를 도입하고 이를 DI로 연결하며 단일 책임 원칙과 개방 폐쇄 원칙을 잘 지키고, 낮은 결합도(서로 영향을 주지않음)와 높은 응집도(단일 책임 집중)가 나오는 코드 입니다. 이런 과정에서 수많은 디자인 패턴이 저굥되기도 합니다.  
지금까지 발전시켜온 코드를 보면 DI가 빠진 적이 없습니다. 이토록 스프링을 DI 프레임워크라고 부르는 이유는 DI를 활용해서 자바 엔터프라이즈 기술의 많은 문제를 해결하는 데 적극적으로 활용하고 있기 떄문입니다.  

### 4. 메일 서비스 추상화
고객으로부터 새로운 요청이 들어왔습니다. 레벨이 업그레이드 된 사용자에게는 안내 메일을 발송해달라는 것입니다. 먼저 User에 email 필드를 추가하고, UserService의 upgradeLevels()에 메일 발송 기능을 추가합니다.
#### 4-1. JavaMail을 이용한 메일 발송 기능
자바에서 메일을 발송할 떄는 표준 기수린 javaMail을 사용합니다. javax.mail 패키지에서 제공하는 이메일 클래스입니다. 전형적인 코드이므로 생략합니다.

#### 4-2. JavaMail이 포함된 코드의 테스트
엄밀히 말해서 메일 발송 테스트란 불가능합니다. 메일이 정말 잘 도착헀는지를 확인하지 못합니다. 기껏해야 메일 발송용 서버에 별문제 없이 전달됐음을 확인할 뿐입니다. 물론 메일 서버는 충분히 테스트된 시스템입니다.  
또, 테스트용으로 사용할 메일 서버는 서버에 부담을 줄 수 있으므로 테스트용으로 따로 준비된 메일 서버를 이용합니다.
따라서 메일 테스트를 한다고 매번 메일 수신 여부를 확인할 필요는 없고, 테스트용 메일 서버 까지만 잘 전송되는지 확인하면 됩니다.  

우리는 SMTP라는 검증된 프로토콜을 믿은 것처럼, JavaMail에서도 적용할 수 있습니다. JavaMail API를 통해 요청이 들어간다는 보장이 있다면 굳이 테스트 할 때 마다 JavaMail을 직접 구동할 필요가 없습니다. JavaMail이 동작하면 외부의 메일 서버와 네트워크로 연동하고 전송하는 부하가 큰 작업이 일어나기 떄문입니다. 마찬가지로 테스트용 JavaMail을 준비합니다.  

#### 4-3. 테스트를 위한 서비스 추상화
그런데 한 가지 심각한 문제가 있습니다. JavaMail은 확장이나 지원이 불가능하도록 만들어진 API입니다. JavaMail에서는 Session이라는 오브젝트로 메일 메시지를 생성 하고 전송할 수 있습니다. 이 클래스는 상속이 불가능한 final 클래스에 생성자가 모두 private로 되어 있습니다.  
스프링은 이 문제를 해결하기 위해서 JavaMail에 대한 추상화 기능을 제공합니다. MailSender 인터페이스 입니다.

```java
public interface MailSender{
	void send(SimpleMailMessage simpleMessage) throws MailException;
	// 이 인터페이스는 SimpleMailMessage 인터페이스를 구현한 클래스에 담긴 메일 메시지를 전송하는 메소드로만 이루어져 있습니다.
	// 기본적으로 JavaMailSenderImple 클래스를 이용하면 됩니다. 이 클래스는 JavaMail API를 이용합니다.
}

// MailSender를 이용한 코드
private void sendUpgradeEmail(User user){
	JavaMailSenderImpl ms = new JavaMailSenderImple();
	// 직접 JavaMailSenderImpl을 사용하고 있습니다.
	// MailSender 를 구현한 클래스
	ms.setHost("mail.naver.com");

	SimpleMailMessage mm = new SimpleMailMessage();
	mm.setTo();
	mm.setFrom();
	...

	ms.send(mm);
}
```

try/catch 블록은 MailException 런타임 예외로 포장하기에 만들지 않아도 됩니다.  
JavaMailSenerImpl은 내부적으로 JavaMail API를 이용해 메일을 전송합니다.  
JavaMail API를 사용하는 JavaMailSenderImpl 오브젝트를 코드에서 직접 사용하기 떄문에 JavaMail API를 사용하지 않는 테스트용 오브젝트로 대체할 수 없습니다. DI를 도입합니다.

```java
public class UserService{
	...
	private MailSender ms;
	// JavaMailSenderImpl 이 구현한 인터페이스 입니다.
	// DI를 통해 테스트를 수행할때는 JavaMail을 사용하지 않고, 운영시에는 JavaMail을 사용하게 합니다.

	public void setMailSender(...){...}

	public void sendUpgradeEmail(User user){
		// DI받을 것이므로 메일 발송 호스트를 설정하는 코드도 제거합니다.
		SimpleMailMessage mm = new ...
		mm.setTo();
		...
		this.mailSender.send(mm);
	}
}
// xml
<bean id="userSerivce">
	<property name="mailSender">

<bean id="mailSender">
	<property name="host">
```

이렇게 JavaMail을 직접 사용했을 떄와 동일하게 지정된 메일 서버로 메일 발송됩니다. 우리가 원하는건 JavaMail을 사용하지 않고, 테스트를 하는 것입니다.  
mailSender 구현 빈 클래스를 만듭니다.

```java
public class DummyMailSender implements MailSender {
	...
	// 아무기능 없는 클래스입니다.
}
// xml 의 mailSender 빈의 클래스를 이 클래스로 지정합니다.

public class UserServiceTest{
	...
	@Autowired
	MailSender mailSender;
	// 스프링 빈으로 등록됐으므로 자동으로 빈을 가져옵니다.

	@Test
	public void upgradeAllOrNothing()throws Exception{
		...
		testUserService.setMailSender(mailSender);
		// 수동 DI를 하기 때문에 필드에 mailSender를 추가해야 합니다.
	}
}
```

일반적으로 서비스 추상화라고 하면 트랜잭션 처럼, 기능은 유사하나 사용방법이 다른 기술에 대해 추상 인터페이스와 일관성 있는 접근방식을 제공해 주는 것입니다. 반면에 JavaMail처럼 테스트를 하기 어렵게 설계된 API를 사용할 때도 유용하게 쓸 수 있습니다. JavaMail이 아닌 다른 메시지 API를 이용해 메일을 보내야 해도, 해당 기술의 API를 이용하는 MailSender ㅜ현 클래스를 만들어서 DI해주면 됩니다.

|||
|--|--|
|애플리케이션 계층 |UserService |
|추상화 계층 |MailSender, 구현 클래스들 |
|메일 서비스 계층 |JavaMail |

아직 부족한것이 하나있습니다. 바로 메일 발송 작업에 트랜잭션 개념이 빠져있습니다. 이를 해결하기 위해서는 업그레이드할 사용자를 발견했을 때 마다 보내지 않고, 별도로 목록에 저장해 두었다가 commit()이 실행되면 한번에 메일을 전송하거나, 다른 방법으로 MailSender를 확장해서 메일 전송에 트랜잭션 개념을 적용한 클래스를 만드는 것입니다. 이 클래스는 업그레이드 작업 이전에 새로운 메일 전송 작업 시작을 알려주고, send()를 호출해도 메일을 발송하지 않고 저장해두었다가 업그레이드 작업이 Commit()되면 저장된 메일을 모두 발송합니다.  
두 가지 방법에 쓴 전략이 비슷하지만 전자는 비지니스 로직과 발송에 트랜잭션을 적용하는 부분이 섞이게 됩니다.  

#### 4-4. 테스트 대역
서비스 추상화란 이렇게 원활한 테스트만을 위해서도 충분한 가치가 있습니다. 테스트에서 JavaMail로 메일을 직접 발송했다면 테스트는 매우 불편해집니다. XML설정으로 DB를 테스트용과 운영용으로 분리시킨 것도 같은 맥락입니다.  
이처럼 테스트 대상이 되는 오브젝트가 또 다른 오브젝트에 의존하는 일은 매우 흔합니다. UserSerivce는 이미 DI를 통해 주입받는 오브젝트만 세가지 입니다. 이렇게 하나의 오브젝트가 사용하는 오브젝트들을 의존(협력) 오브젝트라고 부릅니다.  

테스트용으로 사용되는 의존 오브젝트들을 테스트 대역(Test Double)이라고 합니다. 대표적인 테스트 대역은 테스트 스텁(test stub)이 있습니다. 테스트 스텁의 간단한 예는 우리가 만든 DummyMailSender 입니다. 아무 일도 행하지 않는 DummyMailSender와 달리 스텁에 미리 테스트 중에 필요한 정보를 리턴해주도록 만들 수 있습니다. 혹은 스텁에서 강제로 예외를 발생시켜 대상 오브젝트가 어떻게 예외상황에 대처하는지 테스트에 적용할 수도 있습니다.  

이런 간접적인 도움을 주는 개념과 달리 어떤 테스트 대역은 테스트 과정에 적극적으로 참여합니다. 스텁을 이용하면 간접적인 입력 값을 지정할 수도있고, 간접적인 출력 값을 받게 할 수도 있습니다.  
테스트 대상 오브젝트의 메소드가 스텁으로 넘기는 값과 출력 값에 대한 검증할 하고싶다면 assertThat()으로 검증하는 것은 불가능합니다.  
이런 경우에는 테스트 대상 오브젝트와 의존 오브젝트 사이에서 일어나는 일을 검증할 수 있도록 설계된 목 오브젝트(mock object)를 사용해야 합니다.

> 목 오브젝트 : 스텁처럼 테스트 오브젝트가 정상적으로 실행되게 도와주면서, 테스트 오브젝트와 자신의 사이에서 일어나는 내용을 저장해뒀다가 테스트 결과를 검증하는 데 활용할 수 있게 해줍니다. 사실상 검증만 제외하면 스텁과 마찬가지입니다.

목 오브젝트를 UserServiceTest에 적용해봅니다. 트랜잭션 기능을 테스트하려 했던 upgradeAllOrNothing() 테스트는 메일이 전송 됐는지 여부는 관심의 대상이 아니기에, DummyMailSender가 어울립니다. 반면 사용자 레벨 업그레이드 결과를 확인하는 upgradeLevels() 테스는 메일 전송 자체에 대해 검증할 필요가 있습니다. 우리는 JavaMail 서비스 추상화를 적용해놨기 떄문에, 목 오브젝트를 만들어서 메일 발송 여부를 확인할 수 있습니다. 물론 목 오브젝트에 메일 발송 기능은 없습니다. 대신 테스트 대상이 넘겨주는 출력 값을 보관하는 기능을 추가합니다. 한정적으로 사용 될 것이기에 내부 클래스로 정의합니다.
```java
static class MockMailSender implements MailSender {
		private List<String> requests = new ArrayList<String>();	
		
		public List<String> getRequests() {
			return requests;
		}
		// UserService로 부터 전송 요청을 받은 메일 주소들을 저장해두고 이를 읽을 수 있게 메소드를 만듭니다.

		public void send(SimpleMailMessage mailMessage) throws MailException {
			requests.add(mailMessage.getTo()[0]);  
		}
		// 전송 요청을 받은 이메일 주소를 저장합니다. 간단한 테스트를 위해서 첫 번쨰 수신자 메일 주소만 저장합니다.
		// 메일을 보내는 기능은 없습니다.

		public void send(SimpleMailMessage[] mailMessage) throws MailException {
		}
	}

// 이제 이를 이용해 upgradeLevels() 테스트를 수정합니다.
	@Test 
	@DirtiesContext	// 컨텍스트의 DI 설정을 변경하는 테스트라는 것을 의미합니다.
	public void upgradeLevels() {
		userDao.deleteAll();
		for(User user : users) userDao.add(user);
		
		MockMailSender mockMailSender = new MockMailSender();  
		userService.setMailSender(mockMailSender);  
		// 목 오브젝트를 의존 오브젝트로 주입합니다.
		
		userService.upgradeLevels();
		// 메일을 보내게 되면
		
		checkLevelUpgraded(users.get(0), false);
		checkLevelUpgraded(users.get(1), true);
		checkLevelUpgraded(users.get(2), false);
		checkLevelUpgraded(users.get(3), true);
		checkLevelUpgraded(users.get(4), false);
		// MockMailSender의 리스트에 메일 발송 결과가 저장됩니다.
		// 업그레이드 결과에 대한 검증입니다.
		
		List<String> request = mockMailSender.getRequests();  
		assertThat(request.size(), is(2));  
		// 업그레이드 대상은 두번째와 네번재 사용자 두명입니다.
		assertThat(request.get(0), is(users.get(1).getEmail()));
		// 리스트의 첫 번째 메일 주소와 두 번째 사용자의 메일을 비교합니다.  
		assertThat(request.get(1), is(users.get(3).getEmail()));  
		// 목 오브젝트에 저장된 리스트를 getRequests()로 불러와 업그레이드 대상과 일치하는지 확인합니다.
	}
```

이렇게 레벨 업그레이드가 일어날 때 DB의 내용 변경과, 메일 발송 여부를 검증했습니다.

### 5. 정리
- 비지니스 로직을 담은 코드는 데이터 엑세스 로직을 담은 코드와 분리해야한다(수직적)
- 비지니스 로직 코드 또한 내부적으로 책임과 역할에 따라서 메소드로 정리돼야 한다.
- 이를 위해서는 DAO의 기술 변화에 서비스 계층의 코드가 영향을 받지 않도록 인터페이스와 DI를 활용해 결합도를 낮춘다.
- DAO를 사용하는 비즈니스 로직에는 트랜잭션이 필요하다.
- 트랜잭션의 시작과 종료를 지정하는 일을 트랜잭션 경계설정 이라 한다.
- 트랜잭션 경계 설정은 주로 비즈니스 로직 안에서 일어난다.
- 트랜잭션 정보를 직접 DAO에 전달하기 보단 스프링이 제공하는 트랜잭션 동기화 기법을 활용한다.
- 트랜잭션 경계설정 코드가 비즈니스 로직 코드에 영향을 주지 않게 하려면 스프링이 제공하는 트랜잭션 서비스 추상화 기술을 이용한다.
- 서비스 추상화는 로우레벨의 트랜잭션 기술과 API의 변화에 상관 없이 일관된 API를 가진 추상화 계층을 도입한다.
- 서비스 추상화는 JavaMail같은 테스트 하기 어려운 기술에도 적용할 수 있다.
- 테스트 대상이 사용하는 의존 오브젝트를 대채하는 오브젝트를 테스트 대역이라고 한다.
- 테스트 대역은 간접적인 정보를 제공하기도 한다.
- 테스트 대역 중에서 테스트 대상에게서 받은 정보를 검증할 수 있도록 설계된 것을 목 오브젝트라 한다.
---
layout: single
title:  "토비의 스프링 vol.1 2장"
categories: spring
tags: [spring, 테스트]
toc: true
author_profile: false
sidebar:
    nav: "docs"
search: true
---

## 테스트
### 1. UserDaoTest 다시 보기
스프링을 통한 개발이 제공하는 가장 중요한 가치는   
확장과 변화를 고려한 객체지향적 설계를 담는 IoC/DI와,  
변화에 유연하게 대처하고 확신하게 해주는 테스트 입니다.  

#### 1-1. UserDaoTest의 특징
```java
public class UserDaoTest {
	public static void main(String[] args) throws ClassNotFoundException, SQLException {
		ApplicationContext context = new AnnotationConfigApplicationContext(DaoFactory.class);
		UserDao dao = context.getBean("userDao", UserDao.class);
		
		User user = new User();
		user.setId("hunny");
		user.setName("hunny");
		user.setPassword("spring");

		dao.add(user);
			
		System.out.println(user.getId() + " 등록 성공 ");
		
		User user2 = dao.get(user.getId());
		System.out.println(user2.getName());
		System.out.println(user2.getPassword());
		System.out.println(user2.getId() + " 조회 성공");
	}
}
```

우리는 지금껏 많은 리팩토링을 거쳐가면서, 코드가 변경되도 테스트 클래스의 main()를 통해 결과가 동일한지 확인할 수 있었습니다.  
이 테스트 방법에서 돋보이는 것은 테스트할 대상인 UserDao를 직접 호출해서 사용한다는 점입니다.
> UserDao dao = context.getBean();

또한, 테스트에 사용할 입력 값(User 오브젝트)를 직접 코드에서 만들고 넣어줍니다.  
  
이러한 방법 외에, 웹을 통한 DAO테스트 방법도 있지만,  
많은 문제점이 있습니다.
- DAO뿐만 아니라 서비스 클래스, 컨트롤러, JSP 뷰 등 모든 레이어의 기능을 만들고 나서 테스트가 가능.
- 테스트를 수행하는데 많은 클래스가 참여해 원인을 찾기 힘듦.
- 테스트가 자동으로 수행되지 않고 일일이 값을 입력해야 함.

이처럼 웹을 통한 테스트는 위험합니다.  
  
테스트하고자 하는 대상이 명확하다면 그 대상에만 집중해서 테스트하는 것이 바람직합니다.  
가능하면 **작은 단위**로 쪼개서 집중 할 수 있어야 합니다.(SoC의 원리)  
이런 것을 단위 테스트(unit test)라고 합니다.  
또, 각 단위 기능은 잘 작동하는데 묶어놓으면 안 되는 경우가 종종 발생하기에,  
많은 단위들이 참여하는 테스트도 필요합니다.  

UserDaoTest는 UserDao라는 DAO(데이터 접근)기능 만을 테스트하기 위해 만들어졌기 떄문에,  
작은 단위의 개발자 테스트 라고 부를 수 있습니다.  

#### 1-2. UserDaoTest의 문제점
- 수동확인 작업의 번거로움
  - 테스트를 수행하는 과정은 자동으로 진행하지만 결과는 사람의 눈으로 확인해야 합니다. 이는 완전 자동이라고 할 수 없습니다.
- 실행작업의 번거로움
  - DAO가 수백 개가 되면 main()도 그만큼 만들어지게 되고, 이를 다시 눈으로 확인해야합니다.

우리는 좀 더 편리하고 체계적으로 테스트를 실행하고 그 결과를 확인할 수 있어야 합니다.  

### 2. UserDaoTest의 개선
#### 2-1. 테스트 검증의 자동화
테스트를 통해 확인하고 싶은 사항은,  
add()에 전달한 User 오브젝트에 담긴 정보와 get()을 통해 DB에서 가져온 User 오브젝트가 일치하는가 입니다.  
결과는 성공, 에러, 실패(결과값 다름)를 가질 수 있습니다.  
테스트 코드를 아래와 같이 수정합니다.  

```java
if(!user.getName().equals(user2.getName())){
    System.out.println("테스트 실패 (name)");
}
else if(!user.getPassword().equals(user2.getPassword())){
    System.out.println("테스트 실패 (password)");
}else{
    System.out.println("테스트 성공");
}
```

이렇게 수정한 후, 실패하는 것을 보고싶다면 get()안의 코드를 수정하고 테스트 해보면 됩니다.  

#### 2-2. 테스트의 효율적인 수행과 결과 처리
이제 테스트에 필요한 기능은 갖췃지만 여전히 편리하진 않습니다.  
main메소드가 제어권을 직접 갖고있기에 한계가 있습니다.  
자바에서는 실용적인 테스트를 위한 도구가 존재합니다.  
자바 테스팅 프레임워크라고 불리는 JUnit입니다.  

이제 테스트용 main메소드를 Junit으로 전환해봅니다.  
**JUint역시 제어의 권한을 담당하는 프레임워크입니다.**  

새로 만들 테스트 메소드는 JUnit 프레임워크가 요구하는 조건 두가지를 따라야 합니다.
- 메소드가 public으로 선언
- 메소드에 @Test 어노테이션을 붙임
- 리턴값이 void이고 파라미터가 없어야합니다.

그리고 if/else 문장을 JUnit이 제공하는 assertThat()이라는 스태틱 메소드를 이용해 전환합니다.  
> asserThat(user2.getName(), is(user.getName()));

assertThat 메소드의 첫 번째 파라미터의 값을 두번째 파라미터로 준 매처(조건)과 비교해서  
일치하면 다음으로 넘어가고, 아니면 테스트가 실패하도록 만듭니다.  
is() 매처는 equals()로 비교해주는 기능을 가졌습니다.  
  
그리고, JUnit 테스트를 실행하기 위해 main 메소드를 하나 추가하고,  
JUnitCore 클래스의 main메소드를 호출하는 코드를 넣어줍니다.  
파라미터에는 @Test 어노테이션을 가진 클래스 이름을 넣어줍니다.  
아래는 이렇게 수정한 코드입니다.  

```java
// 물론 JUnit 라이브러리를 추가해야 사용할 수 있습니다.
public class UserDaoTest {
	
	@Test 
	public void andAndGet() throws SQLException {
		ApplicationContext context = new GenericXmlApplicationContext("applicationContext.xml");
		UserDao dao = context.getBean("userDao", UserDao.class);
		
		User user = new User();
		user.setId("hunny");
		user.setName("hunny");
		user.setPassword("spring");

		dao.add(user);
			
		User user2 = dao.get(user.getId());
		
		assertThat(user2.getName(), is(user.getName()));
		assertThat(user2.getPassword(), is(user.getPassword()));
	}
	
	public static void main(String[] args) {
        // Junit을 실행해주는 main메소드
		JUnitCore.main("springbook.user.dao.UserDaoTest");
	}
}
```
실행하면, 걸린 시간과 결과, 몇 개의 테스트 메소드가 실행됐는지 알려줍니다.  
만약 asserTaht()의 조건을 만족하지 못하면 테스트는 중단되고 실패를 알려줍니다.  

### 3. 개발자를 위한 테스팅 프레임워크 JUnit
스프링 프레임워크 자체도 JUnit 프레임워크를 이용해 테스트를 만들어가며 제작되었고,  
스프링 테스트 모듈도 JUnit을 이용합니다.  

#### 3-1. JUnit 테스트 실행 방법
가장 좋은 JUnit 테스트 실행 방법은 자바 IDE에 내장된 JUnit 지원 도구를 사용하는 것입니다.  
이를 이용하면 JUnitCore를 이용할 때처럼 main메소드를 만들지 않아도 됩니다.  
대표적으로 이클립스 IDE의 Run As항목에 JUnit Test를 선택하면 테스트가 자동으로 실행됩니다.  
테스트가 시작되면 테스트 정보를 표시해주는 view가 나타나서 진행상황을 깔끔하게 보여줍니다.  
또한, 한 번에 여러 테스트 클래스를 동시에 실행할 수도 있습니다.  
  
개인별로는 IDE를 이용하면 편리하지만, 여러 개발자가 만든 코드를 통합해서 테스트를 수행해야할 경우에는,  
서버에서 모든 코드를 가져와 통합하고 빌드한 뒤에 테스트를 수행하는 것이 좋습니다.  
이떄는 Maven(메이븐)이나 ANT같은 빌드툴 혹은 스크립트를 이용해 결과를 메일 등으로 통보받는 방법을 사용합니다.  

#### 3-2. 테스트 결과의 일관성
지금까지 테스트를 실행하면서 가장 불편했던 점은, 매번 UserDaoTest 테스트를 실행하기 전에 DB의 User 테이블 데이터를 삭제해줘야 하는 것입니다.  
같은 코드를 반복해서 테스트가 성공하기도 실패하기도 한다면 좋은 테스트라고 할 수 없습니다.  
코드에 변경이없다면 테스트는 **동일한 결과를 보장**해야합니다.
이를 위해선 addAndGet()테스트를 마치면 테스트가 등록한 사용자 정보를 삭제하게 만드는 것입니다.  
이 기능을 하는 deleteAll()와 이를 검증하기 위한 getCount()를 UserDao에 만듭니다.  

```java
public void deleteAll() throws SQLException {
		Connection c = dataSource.getConnection();
	
		PreparedStatement ps = c.prepareStatement("delete from users");
		ps.executeUpdate();

		ps.close();
		c.close();
	}	

	public int getCount() throws SQLException  {
		Connection c = dataSource.getConnection();
	
		PreparedStatement ps = c.prepareStatement("select count(*) from users");

		ResultSet rs = ps.executeQuery();
		rs.next();
		int count = rs.getInt(1);

		rs.close();
		ps.close();
		c.close();
	
		return count;
	}
```

이 두 메소드에 대한 테스트 역시 만들어야 하지만, 둘다 독립적으로 테스트하기에는 무리가 있습니다.  
차라리 addAndGet()를 실행 한 뒤 getCount()로 테이블에 남아있는지 확인해 deleteAll()을 테스트하고,  
add()를 실행 한 뒤 getCount()의 값을 검증해 getCount()에 대한 테스트도 완료합니다.  

```java
@Test
public void andAndGet() throws SQLException {
		ApplicationContext context = new GenericXmlApplicationContext("applicationContext.xml");
		UserDao dao = context.getBean("userDao", UserDao.class);
		
		dao.deleteAll();
		assertThat(dao.getCount(), is(0));
		// User 테이블을 비움으로서 0이 리턴되야 합니다.
		//생략
		dao.add(user);
		assertThat(dao.getCount(), is(1));
		// User를 DB에 추가함으로 1이 리턴되야합니다.
		//생략
}
```

addAndGet()의 검증이 끝날 때 deleteAll()을 실행해주는 방법도 있지만,  
addAndGet() 테스트 실행 이전에 다른 이유로 USER테이블에 다른 데이터가 들어가있다면,  
실패하게 됩니다. 그러므로 테스트하기 전에 문제가 되지 않는 상태를 만들어주는게 좋습니다.  

#### 3-3. 포괄적인 테스트
getCount()에대한 테스트처럼 한 두가지 결과만 검증하고 마는것은 위험합니다.  
개선한 테스트 메소드의 제작이 필요합니다.  
편리한 테스트를 위해 User 클래스에 파라미터가 있는 생성자를 만들어 둡니다.

```java
pulbic User(String id, // 생략){
	this.id = id;
	// 생략
}
public User(){} // 기본 생성자도 물론 만들어줘야 합니다.
```

이후, 다음과 같이 테스트를 작성합니다.  

```java
@Test
public void count() throws SQLException {
	// 생략
		dao.deleteAll();
		assertThat(dao.getCount(), is(0));
				
		dao.add(user1);
		assertThat(dao.getCount(), is(1));
		
		dao.add(user2);
		assertThat(dao.getCount(), is(2));
		
		dao.add(user3);
		assertThat(dao.getCount(), is(3));
}
```

주의할 점은 addAndGet과 count 테스트가 어떤 순서로 실행될지 알 수 없습니다.  
**이는 테스트의 결과가 테스트의 실행 순서에 영향을 받지 않아야한다는 의미(독립)**입니다.  
예를 들어, addAndGet()에서 등록한 정보를 count()에서 활용한다면 안됩니다.  
  
get()에서도 파라미터로 주어진 id에 해당하는 사용자를 가져온것인지 검증하는 코드가 필요합니다.  
두 개의 User를 add()하고, 각각의 User의 id를 파라미터로 전달해서 get()을 실행하게 합니다.  

```java
@Test 
	public void andAndGet() throws SQLException {
		ApplicationContext context = new GenericXmlApplicationContext("applicationContext.xml");
		UserDao dao = context.getBean("userDao", UserDao.class);

		User user1 = new User("gyumee", "박상철", "springno1");
		User user2 = new User("leegw700", "이길원", "springno2");
		
		dao.deleteAll();
		assertThat(dao.getCount(), is(0));
	
		dao.add(user1);
		dao.add(user2);
		assertThat(dao.getCount(), is(2));
		
		User userget1 = dao.get(user1.getId());
		assertThat(userget1.getName(), is(user1.getName()));
		assertThat(userget1.getPassword(), is(user1.getPassword()));
		// 첫번째 User의 id로 get()을 실행하면 첫 번째 User의 값을 가진
		// 오브젝트를 돌려주는 지에 대한 테스트 코드입나다.

		User userget2 = dao.get(user2.getId());
		assertThat(userget2.getName(), is(user2.getName()));
		assertThat(userget2.getPassword(), is(user2.getPassword()));
	}
```

만약 get()에 전달된 id값에 해당하는 사용자 정보가 없다면 어떻게 해야할까요?  
이런 경우에 결과는 null같은 값을 리턴하게 하거나, 예외를 던지게 하는 방법이 있습니다.  
스프링이 정의한 데이터 억세스 예외 클래스 들이 있는데, 그 중  
EpmtyResultDataAccessException 예외를 사용합니다.  
  
일반적으로 테스트 중에 예외가 던져지면 테스트가 실패하지만,  
이번엔 반대로 예외가 발생해야 하는 경우입니다.  
더군다나 예외 발생 여부는 메소드를 실행해서 리턴 값을 비교하는 방법으로는 확인할 수 없습니다.(asserThat메소드로 불가능합니다.)  
JUnit은 예외 조건 테스트를 위한 방법을 제공해줍니다.  
@Test에 expected를 추가하는 것입니다.  

```java
@Test(expected=EmptyResultDataAccessException.class)
// 발생하리라 기대하는 예외 클래스를 넣어줍니다.
	public void getUserFailure() throws SQLException {
		dao.deleteAll();
		assertThat(dao.getCount(), is(0));
		
		dao.get("unknown_id");
		// 이 메소드 실행 중에 예외가 발생해야 합니다.
		// 예외가 발생하지 않으면 테스트 실패입니다.
	}
```

하지만, 아직 이 테스트는 실패합니다.  
쿼리 결과의 첫번째 로우를 가져오는 rs.next()를 실행할 수 없어서  
SQLException이 발생하기 때문입니다.  
이제부터 할 일은 이 테스트가 성공하도록 get() 코드를 수정하는 것입니다.

```java
	public User get(String id) throws SQLException {
		Connection c = this.dataSource.getConnection();
		PreparedStatement ps = c
				.prepareStatement("select * from users where id = ?");
		ps.setString(1, id);
		
		ResultSet rs = ps.executeQuery();

		User user = null;
		// null 상태로 추가해 둡니다.
		if (rs.next()) {
			user = new User();
			user.setId(rs.getString("id"));
			user.setName(rs.getString("name"));
			user.setPassword(rs.getString("password"));
		}
		// 쿼리의 결과가 있다면 User 객체를 만들고 값을 넣어줍니다.
		rs.close();
		ps.close();
		c.close();
		
		if (user == null) throw new EmptyResultDataAccessException(1);
		// 결과가 없으면 null상태 그대로입니다. 이를 확인해서 예외를 던져줍니다.

		return user;
	}
```

이제 세 개의 테스트가 모두 성공했습니다. 새로 추가한 기능도 정상적으로 작동하고  
기존의 기능에도 영향을 주지 않았다는 확신을 얻을 수 있습니다.  
개발자들이 가장 많이 하는 실수는 성공하는 테스트만 골라서 만드는 것입니다.  
항상 네거티브 테스트를 먼저 만들라는 조언을 잊지 말아야 합니다.  

#### 3-4. 테스트가 이끄는 개발
우리가 작업한 순서를 잘 생각해보면 테스트를 먼저 만들어 검증을 하고나서(getUserFailure 테스트)  
UserDao의 코드(get 메소드)에 수정을 했습니다.  
어떻게보면 테스트할 코드도 안 만들어놓고 테스트 코드부터 만드는 것은 좀 이상하게 보일 수도 있습니다.
하지만 많은 개발자가 이런 개발 방법을 적극적으로 사용합니다.  
이는 만들어진 코드를 보고 어떻게 테스트할까라고 생각하면서 테스트 코드를 만든것이 아닌,  
추가하고 싶은 기능을 코드로 표현하려고 했기 때문에 가능합니다.  

| |단계 |내용 | 코드 |
|--|--|--|--|
|조건 |어떤 조건을 가지고 |가져올 사용자 정보가 존재 안 할 경우 |dao.deleteAl(); assertThat(dao.getCount(),is(0));|
|행위 |무엇을 할 때 |존재하지 않는 id로 get()실행 |get("unknow_id"); |
|결과 |어떤 결과가 나온다 |특별한 예외가 던져진다 |@Test(expected=EmptyRe...) |

테스트 모드를 먼저 만들고, 테스트를 성공하게 해주는 코드를 작성하는 방식을  
**TDD(테스트 주도 개발)**이라고 합니다.  
실패한 테스트를 성공시키기 위한 목적이 아닌 코드는 만들지 않는 것이 원칙입니다.  
TDD에서는 테스트를 작성하고 이를 성공시키는 코드를 만드는 작업의 주기를 가능한 짧게 하도록 권장합니다.  

#### 3-5. 테스트 코드 개선
필요하다면 테스트 코드도 언제든지 리팩토링 해 볼 수 있습니다.  
UserDaoTest 코드를 잘 살펴보면 반복되는 부분이 눈에 띕니다.  

> ApplicationConext context = new GericXml....

물론 중복된 코드는 별도의 메소드로 추출하는 것이 쉬운 방법입니다.  
하지만 JUnit의 제공하는 기능을 활용해보겠습니다.  

먼저, 세 개의 테스트 메소드에 반복적으로 등장하는 위의 코드를 제거하고 이를 담을 setUp메소드를 만듭니다.  
아래의 코드를 보며 따라가겠습니다.  

```java
public class UserDaoTest {
	private UserDao dao; 
	// setUp 메소드에 dao 변수가 지역변수로 선언되 있으므로,
	// dao 변수를 인스턴스 변수로 추가합니다.
	private User user1;
	private User user2;
	private User user3;
	// 이는 테스트 수행에 필요한 오브젝트로 픽스처(fixture)라고 합니다.
	
	@Before
	// @Test 메소드가 실행되기 전에 먼저 실행되야 하는 메소드를 정의합니다.
	// 많은 테스트 메소드에 공통적으로 실행될 경우 지정하는게 좋습니다.
	// 만약 일부에서만 사용한다면 일반적인 메소드 추출 방식을 사용하는게 좋습니다.
	public void setUp() {
		ApplicationContext context = new GenericXmlApplicationContext("applicationContext.xml");
		this.dao = context.getBean("userDao", UserDao.class);
		
		this.user1 = new User("gyumee", "111", "springno1");
		this.user2 = new User("leegw700", "222", "springno2");
		this.user3 = new User("bumjin", "333", "springno3");
		// 생략
	}
	
```

JUnit이 하나의 테스트 클래스를 가져와 테스트를 수행하는 방식을 살펴봅니다.
- 테스트 클레스에서 @Test가 붙은 조건을 만족하는 테스트메소드를 모두 찾는다.
- 테스트 클래스의 오브젝트를 하나 만든다.
  - 각 테스트 메소드를 실행 할 때마다 테스트 클래스의 오브젝트를 새로 만듭니다. 테스트 클래스가 두개의 테스트 메소드를 갖고있다면 JUnit은 이 클래스의 오브젝트를 두 번 만듭니다. 이는 독립성을 보장하기 위함입니다.
- @Befor가 붙은 메소드가 있으면 실행한다.
- @Test가 붙은 메소드를 하나 호출하고 테스트 결과를 저장한다.
- @After가 붙은 메소드가 있으면 실행한다.
- 나머지 테스트 메소드에 대해 2~5번을 반복한다.
- 모든 테스트의 결과를 종합하여 돌려준다.

### 4. 스프링 테스트 적용
리팩토링을 마쳤지만 @Befor 메소드가 **테스트 메소드 수만큼 반복되기 때문에 자원낭비**가 됩니다.  
테스트는 가능한 독립적으로 매번 새로운 오브젝트를 만들어야하지만 반면, 애플리케이션 컨텍스트는  
초기화되고 나면 내부의 상태가 바뀌는 일이 거의없고, 빈은 싱글톤으로 만들었기 때문에 무상태입니다.  
따라서 애플리케이션 컨텍스트는 여러 테스트가 공유해서 사용해도 됩니다.  

#### 4-1. 테스트를 위한 애플리케이션 컨텍스트 관리
스프링은 JUnit을 사용하는 **테스트 컨텍스트 프레임워크**를 제공합니다.  
간단한 어노테이션 만으로 테스트에서 필요로 하는 애플리케이션 컨텍스트를 만들어서  
모든 테스트가 공유할 수 있게 합니다.  
먼저, @Before 메소드에서 애플리케이션 컨텍스트를 생성하는 코드를 제거합니다.  
그다음 ApplicationContet타입의 인스턴스 변수를 선언하고 @Autowired어노테이션을 붙입니다.  

```java
// 라이브러리도 추가해야합니다.
@RunWith(SpringJUnit4ClassRunner.class)
// 테스트 컨텍스트 프레임워크의 JUnit 확장기능 지정
@ContextConfiguration(locations="/applicationContext.xml")
// 테스트 컨텍스트가 자동으로 만들어줄 애플리케이션 컨텍스트의 위치 지정
public class UserDaoTest {
	@Autowired
	// 테스트 오브젝트가 만들어지고 나면 테스트 컨텍스트에 의해 자동으로 DI
	ApplicationContext context;
	// 초기화 해주는 코드없이 JUnit확장 기능이 사용합니다.
	
	private UserDao dao; 
	
	private User user1;
	private User user2;
	private User user3;
	
	@Before
	public void setUp() {
		this.dao = this.context.getBean("userDao", UserDao.class);
		
		this.user1 = new User("gyumee", "name1", "springno1");
		this.user2 = new User("leegw700", "name2", "springno2");
		this.user3 = new User("bumjin", "name3", "springno3");
	}
```

그 후 @Befor 메소드에서 context변수의 주소값과 UserDaoTest의 주소값을 비교해보면,  
context는 매 테스트마다 주소값이 같고 UserDaoTest의 오브젝트는 매번 다른 것을 알 수 있습니다.  
이렇게 해서 테스트의 수행시간이 짧아졌고(최초 수행시 application context의 생성시간 제외),  
**하나의 테스트 클래스 내의 테스트 메소드가 같은 애플리케이션 컨텍스트를 공유해서 사용함**을 확인했습니다.  

> 만약 다른 테스트 클래스가 같은 설정파일을 가진 애플리케이션 컨텍스트를 이용한다면, 스프링 테스트 컨텍스트 프레임워크는 하나의 애플리케이션 컨텍스트를 공유하게 합니다.


@Autowired가 붙은 인스턴스 변수가 있으면, 테스트 컨텍스트 프레임워크는 변수 타입과 일치하는 애플리케이션 컨텍스트 내 빈을 찾아서 자동으로 주입해줍니다.  
일반적으로 DI를 위해서는 생성자나 수정자 메소드같은 메소드가 필요하지만,  
이 경우에는 메소드나 DI 설정 없이 필드의 타입 정보를 이용해 주입이 가능합니다.  

테스트코드에서는 xml파일에 정의되지 않은 ApplicationContext라는 타입의 변수에 DI를 했는데,  
애플리케이션 컨텍스트는 초기화 할 때 자기자신도 빈으로 등록하기에 가능합니다.  

@Autowired는 지정하기만 하면 어떤 빈이든 가져올 수 있습니다.
```java
public calss UserDaoTest{
	@Autowired
	UserDao dao;
}
```

만약 같은 타입의 빈이 두 개 이상 있는경우에는 변수의 이름과 같은 이름의 빈을 찾아서 주입합니다.  
찾을 수 없는 경우에는 예외가 발생합니다.  

#### 4-2. DI와 테스트
1. 테스트 코드에 의한 DI

xml에 정의한 DataSource 빈이 운영용 DB 커넥션을 돌려준다고 가정한다면,  
테스트 할 때 이 빈을 이용하면 deleteAll()에 의해 운영용 DB 사용자가 전부 삭제되버릴 것입니다.  
그렇다고 xml설정을 테스트 할 때마다 수동으로 바꿔주기에는 위험합니다.  
이런 경우엔 **테스트코드에 의한 DI**를 이용해서 테스트 중에 DAO가 사용할 DataSource 오브젝트를 바꿔주는 방법을 이용할 수 있습니다.  
이 방법의 장점은 XML 설정파일을 수정하지 않고 오브젝트 관계를 재구성 할 수 있지만, 
**UserDao 빈의 의존관계를 강제로 변경합니다.**   
애플리케이션 컨텍스트의 구성을 테스트 내에서 변경하지 않는 원칙을 어겼습니다.  

그래서 @DiretiesContext라는 어노테이션을 추가하고 testdb 테이블을 생성하고 연결합니다.  
```java
@Before
public void setUp(){
	//생략
	DataSource dataSource = new SingleConenctionDataSoruce(......);
	// 테스트에서 UserDao가 사용할 DataSource 오브젝트를 직접 설정합니다.(수동)
	// 생략
}
```
이 어노테이션이 붙은 테스트 클래스에는 애플리케이션 컨텍스트의 상태가 변경될 것을 알려 어플리케이션 컨텍스트의 공유를 허용하지 않습니다.  
테스트 메소드를 수행하고 나면 **매번 새로운 애플리케이션 컨텍스트를 만들어서** 다음 테스트가 사용하게 합니다.  
이렇게 문제점은 피해갔지만 애플리케이션 컨텍스트를 매번 만드는 건 조금 찝찝합니다.  

2. 테스트를 위한 별도의 DI 설정
아예 테스트 전용 XML파일을 따로 만들어두는 방법을 이용해도 됩니다.  
기존의 applicationContext.xml을 복사한 test-applicationContext.xml을 만들고 propety의 값을  
testdb로 변경합니다.  
이후 테스트용 설정 파일을 적용합니다.  
```java
@RunWith(SpringJUnit4ClassRunner.class)
@ContextConfiguration(locations="/test-applicationContext.xml")
// 테스트용 설정파일을 사용합니다.
public class UserDaoTest{
}
```
3. 컨테이너 없는 DI테스트
스프링 컨테이너를 사용하지않고 테스트를 만드는 것입니다.  
처음의 DaoFactory를 만들던 방식과 같습니다.  
오브젝트 생성, 관계설정 등을 모두 직접합니다.  
스프링은 비침투적 기술이기 때문에 컨테이너 없는 DI 테스트가 가능합니다.  

> 침투적 기술 : 어떤 기술을 적용했을 때, 코드에 기술 관련 API가 등장하거나, 특성 클래스를 사용하도록 강제합니다.

> 비침투적 기술 : 어떤 기술이 코드에 영향을 주지 않고 적용이 가능합니다. 


4. 테스트 방법 선택
**항상 컨테이너 없이 테스트 할 수 있는 3번째 방법을 우선적으로 고려합니다.**  
복잡한 의존관계를 갖고있는 오브젝트를 테스트 할 때는, xml을 이용한 스프링의 도움을 받습니다.  
스프링의 도움을 받아도 예외적인 의존관계를 강제로 구성해야 할 경우에는 수동 DI해서 테스트하는 방법을 사용합니다.  

### 5. 학습 테스트로 배우는 스프링
때때로 자신이 사용할 API나 프레임워크의 기능을 테스트로 보면서 사용 방법을 익혀야 할 때 가 있습니다.  
이때는 물론 기능에 대한 검증이 목적이 아니라 사용방법을 얼마나 알고있는지에 대한 검증이 목적입니다.  
  
그리고 버그가 발생 했을 때 역시, 무턱대고 수정하기보다는 버그 테스트를 만들어서 해당 원인으로 실패하고 성공할수 있도록 수정해가며 만들어 보는 것이 좋습니다.

### 6.정리
2장에서 우리는 다음과 같이 테스트의 필요성과 작성 방법을 살펴 보았습니다.
- 테스트는 자동화, 빠르게 실행할 수 있어야 한다.
- JUnit 프레임 워크와 IDE를 이용한다.
- 테스트 결과는 일관성이 있어야 한다.(JUnit은 매 테스트 마다 새로운 오브젝트를 생성한다.)
  - 환경이나 테스트 실행 순서에따라 결과가 달라지면 안된다.
- 코드 작성과 테스트 수행 간격이 짧을수록 좋다.
- TDD개발 방법도 유용하다.
- 테스트 코드도 리팩토링이 필요하다.
- @Befor, @After, @Autowired 등의 어노테이션
- 스프링 테스트 컨텍스트 프레임워크를 이용하면 JUnit테스트 성능을 향상시킨다.
- 동일한 xml을 사용하는 테스트는 하나의 application context를 공유한다.
- 테스트 방법 3가지
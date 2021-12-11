---
layout: single
title:  "토비의 스프링 vol.1 1장"
categories: spring
tags: [spring, 오브젝트와 의존관계]
toc: true
author_profile: false
sidebar:
    nav: "docs"
search: true

---
## 오브젝트와 의존관계

### 1. 초난감 DAO

JDBC API를 통해 간단한 DAO를 하나 만들어 봅니다.

> DAO(Dat access abject) : DB를 사용해 데이터를 조회하거나 조작하는 기능을 전담하도록 만든 오브젝트 입니다.

#### 1-1. User

 사용자 정보를 저장할 때는 자바빈 규약을 따르는 오브젝트를 이용합니다.

> 자바빈 규약 : 파라미터가 없는 기본 생성자가 존재. 프레임워크에서 리플렉션을 이용해 오브젝트를 생성하기 때문입니다.



> 멤버변수의 접근제어자는 private로 선언하고 접근 가능한 getter/setter 메서드가 존재.

```java
public class User{
//   domain 클래스로 분류합니다.
    public String getId() {
    return id;
    }
    public void setId(String id) {
        this.id = id;
    }
    public String getName() {
        return name;
    }
    public void setName(String name) {
        this.name = name;
    }
    public String getPassword() {
        return password;
    }
    public void setPassword(String password) {
        this.password = password;
    }
    String id;
    String name;
    String password;
}
```

#### 1-2. User 테이블

 이제 User 오브젝트에 담긴 정보가 실제로 보관될 DB의 테이블을 만듭니다. (mysql 기준입니다.)

```sql
create table users(
    id varchar(10) primary key,
    name varchar(20) not null,
    password varchar(20) not null
)
```



#### 1-3. UserDAO

 우선 조회와 등록 기능이 있는 UserDAO클래스를 JDBC를 이용하여 작성합니다.  

일반적인 JDBC 작업 순서는 아래와 같습니다.

- DB연결을 위한 Connection을 가져온다.

- SQL문을 담은 Statement / PreparedStatement를 만든다.

- Statement를 실행한다.

- 조회의 경우 쿼리 실행 결과를 ResultSet으로 받아서 오브젝트(User 클래스)에 옮긴다.

- 리소스들은 반드시 예외처리를 해서 닫아준다.

```java
public class UserDao {
	// User를 등록하는 메소드 입니다.
	public void add(User user) throws ClassNotFoundException, SQLException {
		Class.forName("com.mysql.jdbc.Driver");
		Connection c = DriverManager.getConnection("jdbc:mysql://localhost/springbook?characterEncoding=UTF-8", "spring",
				"book");
	// DB커넥션
		PreparedStatement ps = c.prepareStatement(
			"insert into users(id, name, password) values(?,?,?)");
		ps.setString(1, user.getId());
		ps.setString(2, user.getName());
		ps.setString(3, user.getPassword());
	// 쿼리문 담기
		ps.executeUpdate();
	//실행
		ps.close();
		c.close();
	// 리소스 반납
	}

// 조회하는 메소드
	public User get(String id) throws ClassNotFoundException, SQLException {
		Class.forName("com.mysql.jdbc.Driver");
		Connection c = DriverManager.getConnection("jdbc:mysql://localhost/springbook?characterEncoding=UTF-8", "spring",
				"book");
		PreparedStatement ps = c
				.prepareStatement("select * from users where id = ?");
		ps.setString(1, id);

		ResultSet rs = ps.executeQuery();
		// 쿼리의 결과를 담습니다.
		rs.next();
		User user = new User();
		user.setId(rs.getString("id"));
		user.setName(rs.getString("name"));
		user.setPassword(rs.getString("password"));

		rs.close();
		ps.close();
		c.close();

		return user;
	}

}
```

이렇게 DAO를 간단하게 개발했지만 위 코드는 문제점이 많은 복잡한 코드입니다. 아래부터는 초난감 DAO코드를 객체지향기술의 원리에 맞춰 개선해보는 작업을 합니다.

### 2.DAO의 분리
#### 2-1. 관심사의 분리
어플리케이션에서 오브젝트에 대한 설께와 이를 구현한 코드는 변합니다.  
이러한 변경이 일어날 때 필요한 **작업을 최소화**하고 문제를 일으키지않게 하려면,  
**분리와 확장**을 고려하여 설계해야 합니다.  
> 관심사의 분리(Separation of Concerns) : 관심이 같은 것 끼리는 하나의 객체 안으로 모이게 하고, 관심이 다른 것은 분리하는 것.
  
#### 2-2. 커넥션 만들기 추출
위의 UserDAO클래스의 add()메소드 하나에서 세 가지 관심사항을 발견할 수 있습니다.
- DB와 연결을 위한 커넥션
- Statement를 만들고 실행하는 것
- 리소스를 반납하는 것
  
이렇듯, 현재 add()메소드에는 **다른 관심사**인 DB커넥션을 가져오는 코드가 섞여있습니다.  
또한, get()메소드에도 **동일한 코드가 중복**되어 있습니다.  
아래와 같이 커낵션 만들기 코드를 분리해 보겠습니다.
```java
public class UserDao {
	public void add(User user) throws ClassNotFoundException, SQLException {
		Connection c = getConnection();
	// 커낵션 만들기 분리
		PreparedStatement ps = c.prepareStatement(
			"insert into users(id, name, password) values(?,?,?)");
		// 생략
	}

		public User get(String id) throws ClassNotFoundException, SQLException {
		Connection c = getConnection();
		// 중복 제거
		PreparedStatement ps = c
				.prepareStatement("select * from users where id = ?");
		//생략
	}

	private Connection getConnection() throws ClassNotFoundException,
			SQLException {
		Class.forName("com.mysql.jdbc.Driver");
		Connection c = DriverManager.getConnection("jdbc:mysql://localhost/springbook?characterEncoding=UTF-8", "spring",
				"book");
		return c;
	}
}
```
위와 같이 수정한다면 DB연결과 관련된 부분에 변경이 일어났을 경우 **관련된 관심사를 담고있는** getConnection()의 코드만 수정하면 됩니다.  
이 과정을 내부 구조만 변경해서 재구성하는 리팩토링(refactoring)이라고 합니다. 중복된 코드를 뽑아내는 것을 리팩토링에서는 메소드 추출기법(extract method)이라고 부릅니다.

#### 2-3. DB 커넥션 만들기의 독립
지금까지 만든 UserDAO가 다른 종류의 DB를 쓴다고 가정할때, 코드를 공개하지 않으면서 원하는 DB 커넥션 생성 방식을 적용시킬 수 있을까요?  
DB커넥션 연결이라는 관심을 이번에는 상속을 통해 서브클래스로 분리합니다.

- 우선 UserDAO에서 메소드의 구현 코드를 제거하고 **getConnection()을 추상 메소드**로 만들어 놓습니다.
- UserDAO 클래스를 상속한 NUserDAO와 DUSERDAO라는 서브클래스를 만듭니다.
- 서브클래스에서 getConnection()메소드를 구현합니다.

코드로 보겠습니다.
```java
public abstract class UserDao {
	public void add(User user) throws ClassNotFoundException, SQLException {
		Connection c = getConnection();
		PreparedStatement ps = c.prepareStatement(
			"insert into users(id, name, password) values(?,?,?)");
		// 생략. getConnection의 내용은 없지만 메소드는 존재하기 때문에 선언 할 수 있습니다.
	}


	public User get(String id) throws ClassNotFoundException, SQLException {
		Connection c = getConnection();
		// 생략
	}

	abstract protected Connection getConnection() throws ClassNotFoundException, SQLException ;
	// 추상메소드가 된 getConnection()
}

// 아래는 서브 클래스 입니다.
public class DUserDao extends UserDao {
	protected Connection getConnection() throws ClassNotFoundException,
			SQLException {
		Class.forName("com.mysql.jdbc.Driver");
		Connection c = DriverManager.getConnection(
				"jdbc:mysql://localhost/springbook?characterEncoding=UTF-8",
				"spring", "book");
		return c;
		// 서브클래스 에서 getConnection()을 구현했습니다.
	}
}
```
위와 같은 방법을 디자인 패턴에서 템플릿 메소드 패턴이라고 합니다.
> 템플릿 메소드 패턴(template method pattern) : 변하지 않는 기능은 슈퍼클레스에서 만들어두고 자주 변경/확장 하는 기능은 서브클래스에서 만들도록 합니다.  
이때, 반드시가 아니라 선택적으로 오버라이드가 가능한 메소드를 hookMethod라 부릅니다.

그리고 UserDAO에서는 getConnection()에서 생성한 객체가 Connection 인터페이스 타입의 객체라는 것 외에는 관심을 두지 않습니다. 어떤 기능(메소드)을 사용하는 데에만 관심을 두고 있습니다.  
반면, 서브클래스에서는 어떤식으로 Counnection 기능을 구현할지에 관심을 두고 있습니다.
이는 팩토리 메소드패턴이라고 합니다.

> 팩토리 메소드 패턴 : 슈퍼클래스의 코드에서 서브클래스에서 구현할 메소드를 호출해서 필요한 객체를 사용하는 것.

이런 디자인 패턴은 클래스 상속과 오브젝트 합성이라는 두 가지 구조로 정리되기 때문에 비슷하게 느껴집니다.  

#### 2-4. 지금까지의 문제점
이 방법은 상속을 사용했다는 단점이 있습니다. 문제를 찾아내는 것은 중요합니다.
- 자바는 클래스의 다중상속을 허용하지 않기때문에 다른 목적이 필요 할 때 UserDAO에 상속을 적용하기 힘듦.
- 다른 DAO클래스에 적용할 수 없음.

### 3. DAO의 확장
#### 3-1. 클래스의 분리
이번에는 상속관계가 아닌 독립적인 클래스로 만들어 보겠습니다.  
SimpleConnectionMaker라는 새로운 클래스를 만들고 DB 생성 기능을 이 클래스로 옮기겠습니다.

```java
public abstract class UserDao {
	private SimpleConnectionMaker simpleConnectionMaker;
	
	public UserDao() {
		this.simpleConnectionMaker = new SimpleConnectionMaker();
		// 생성자에 오브젝트를 만들어 두었는데
		// 인스턴스 변수에 저장해두고 메소드에서 사용하게 하기 위함입니다.
	}

	public void add(User user) throws ClassNotFoundException, SQLException {
		Connection c = this.simpleConnectionMaker.getConnection();

		PreparedStatement ps = c.prepareStatement(
			// 생략
}

// 별도의 클래스로 독립시킨 DB 연결 기능
public class SimpleConnectionMaker {
	public Connection getConnection() throws ClassNotFoundException,
			SQLException {
		Class.forName("com.mysql.jdbc.Driver");
		Connection c = DriverManager.getConnection(
				"jdbc:mysql://localhost/springbook?characterEncoding=UTF-8", "spring", "book");
		return c;
	}
}
```

위와 같이 상속문제를 해결했지만 다시 자유로운 확장이 불가능한 문제로 재귀했습니다.  
가장 큰 문제는 UserDAO가 DB 커넥션을 제공하는 클래스가 어떤 것인지를 구체적으로 알고 있어야 한다는 점입니다.(어떤 기능을 구현했는지에 관심을 두게 됩니다.)  
즉, UserDAO는 DB 커넥션을 가져오는 구체적인 방법에 종속됩니다.  

#### 3-2. 인터페이스의 도입
두 개의 클래스(UserDAO,SimpleConnectionMaker)가 서로 긴밀한 관계를 맺지않도록 중간에 추상적인 연결고리를 만들어 줍니다.  
바로 인터페이스 입니다.  
인터페이스로 추상화해놓은 최소한의 통로를 통해 접근하는 쪽은 오브젝트를 만들 때 사용할 클래스(UserDAO)가 무엇인지 몰라도 됩니다.

``` java
public interface ConnectionMaker {
	public abstract Connection makeConnection() throws ClassNotFoundException,
			SQLException;
}

public class DConnectionMaker implements ConnectionMaker {
	public Connection makeConnection() throws ClassNotFoundException,
			SQLException {
		Class.forName("com.mysql.jdbc.Driver");
		Connection c = DriverManager.getConnection(
				"jdbc:mysql://localhost/springbook?characterEncoding=UTF-8", "spring", "book");
		return c;
	}
}

public class UserDao {
	private ConnectionMaker connectionMaker;
	
	public UserDao() {
		this.connectionMaker = new DConnectionMaker;
	}
```

UserDAO에서 DB 커넥션을 제공하는 클래스에 대한 구체적인 정보는 제거했지만, 초기에 한번 어떤 클래스의 오브젝트를 사용할지를 결정하는 생성자 코드는 남아있습니다.  

> this.connectionMaker = new DconnectionMaker;

#### 3-3. 관계설정 책임의 분리
이런 사항이 일어나는 이유는 또 다른 관심사항이 존재하고 있기 때문입니다.  
바로 UserDAO가 어떤 ConnectionMaker 인터페이스의 구현 오브젝트를 사용할지를 **결정**하는 것입니다.  
이 제 3의 관심사항인 결정권은 UserDAO의 클라이언트(서비스를 사용하는 오브젝트)에 두기 적절합니다.  
  
오브젝트 사이의 관계를 만들기위해선 외부에서 만들어 준 것을 가져오는 방법도 있습니다.  
메소드 파라미터나 생성자 파라미터를 이용하는 것입니다.  
파라미터로 제공받은 오브젝트는 그 오브젝트가 어떤 클래스로부터 만들어졌는지 신경 쓰지 않아도 됩니다.  
오브젝트(UserDAO)와 오브젝트(DconnectionMaker) 사이에 사용관계를 **의존관계**라고 합니다.  
이 **의존관계**를 맺어주는것이 UserDAO 클라이언트라고 칭한 오브젝트의 관심입니다.  

```java
public class UserDao {
	private ConnectionMaker connectionMaker;
	
	public UserDao(ConnectionMaker simpleConnectionMaker) {
		// 수정한 생성자
		this.connectionMaker = simpleConnectionMaker;
	}
}

public class UserDaoTest {
	public static void main(String[] args) throws ClassNotFoundException, SQLException {
		ConnectionMaker connectionMaker = new DConnectionMaker();
		// 의존관계 책임이 추가된 테스트용 메인 메소드
		UserDao dao = new UserDao(connectionMaker);
		//사용할 오브젝트를 선택합니다.
		User user = new User();
		//생략
	}
}
```

이렇게 UserDAO는 자신의 관심사인 데이터 접근에 집중 할 수 있게 되었고, DB생성 방법이나 커넥션을 가져오는 방법에 대해서는 영향을 받지 않는 코드가 됐습니다.  
또한, 상속을 사용했을 때 보다, 인터페이스를 사용했을 때 다른 DAO클래스에서도 ConnectionMaker 인터페이스의 구현 클래스들을 적용할 수 있게 됐습니다.  

#### 3-4. 원칙과 패턴
- 객체지향 설계원칙(SOLID)
	- 단일 책임 원칙(SRP, The Single Responsibility Principle)
	- 개방 폐쇄 원칙(OCP, Open-Closed Principle) : 클래스나 모듈은 확장에는 열려 있어야 하고 변경에는 닫혀 있어야 한다.
		- UserDAO를 예로 들면, DB 연결 방법에는 UserDAO를 건들이지 않고 확장하는데 열려 있습니다.
		- 동시에 UserDAO 자체의 핵심 기능(데이터 접근 기능)을 구현한 코드는 이런 변화(확장)에 영향을 받지 않으므로 변경에는 닫혀 있다고 볼 수 있습니다.
		- 높은 응집도 : 하나의 패키지, 컴포넌트, 모듈, 클래스가 하나의 책임 또는 관심사에 집중되어 있다는 뜻입니다. 변경이 일어날 때 모듈의 많은 부분이 함께 바뀐다면 응집도가 높다고 말할 수 있습니다.
		- 낮은 결합도 : 책임과 관심사가 다른 오브젝트와는 낮은 결합도. 즉, 느슨한 연결 관계를 유지하는 최소한의 방법만 간접적인 형태로 제공하고, 나머지는 서로 독립적이게 만들어 주는 것입니다. 하나의 변경이 발생할 때 다른 모듈과 객체로 변경에 대한 요구가 전파되지 않는 상태입니다. 앞서보았던 결정의 책임을 UserDAO의 클라이언트(UserDAOTest)로 분리한 덕에 ConnectionMaker의 구현 클래스가 바뀌어도, DAO 클래스의 코드를 수정할 필요가 없게 된 것이 낮은 결합도 입니다.
		- 전략 패턴(Strategy Pattern) : 자주 사용되는 패턴으로, 자신의 기능 맥락(context)에서, 필요에 따라 변경이 필요한 알고리즘을 인터페이스를 통해 외부로 분리시키고(ConnectionMaker), 이를 구현한 구체적인 알고리즘 클래스를 필요에 따라 바꿔서 사용할 수 있게(DconnectionMaker) 하는 디자인 패턴입니다.
	- 리스코프  치환 원칙(LSP, The Liskov Substitution Principle)
	- 인터페이스 분리 원칙(ISP, The Interface Segregation Principle)
	-  의존관계 역전 원칙(DIP, The Dependency Inversion Principle)
### 4. 제어의 역전(IoC, Inversion of Control)
IoC는 개발자가 코드로 제어권을 갖는 것이 아닌 다른 대상이 제어권을 갖는 것을 의미합니다. 스프링의 IoC를 살펴보기 전에, UserDAO 코드를 개선해서 IoC를 살펴보겠습니다.
UserDAOTest는 원래 목적인 테스트 기능과 어떤 ConnectionMaker 구현 클래스를 사용할지 결정하는 기능까지 갖고 있습니다. 먼저 이것을 분리시킵니다.
#### 4-1.  오브잭트 팩토리
분리시킬 기능을 담당할 클래스를 만듭니다. 이클래스의 역할은 **객체의 생성방법을 결정하고 생성된 객체를 돌려주는 것**입니다. 이런 오브젝트를 팩토리라고 부릅니다. 팩토리 역할을 맡을 클래스를 DaoFactory라고 하겠습니다.

```java
public class DaoFactory{
	public UserDao userDao(){
	ConnectionMaker cm = new DConnectionMaker();
	// 어떤 구현 클래스를 쓸지 결정합니다.
	UserDao userDao = new UserDao(cm);
	return userDao;
	}
}

public class UserDaoTest{
	public static void main(String[] args) throws ClassNotFoundException, SQLException{
	UserDao dao = new DaoFacory().userDao();
	// 생략
	}
}
```

DaoFactory를 적용한 구조를 그림을 보겠습니다.

[![](https://mermaid.ink/img/eyJjb2RlIjoiZ3JhcGggTFJcbkFbY2xpZW50XSAgLS0g7JqU7LKtIC0tPiBCW0Rhb0ZhY3RvcnldXG5CIC0tIOyDneyEsSAtLT4gQ1tVc2VyRGFvXVxuQSAtLeyCrOyaqS0tPiBDXG5DIC0t7IKs7JqpLS0-IERbQ29ubmVjdGlvbk1ha2VyIOq1rO2YhCDtgbTrnpjsiqRdXG5CIC0t7IOd7ISxLS0-IEQiLCJtZXJtYWlkIjp7InRoZW1lIjoiZGFyayJ9LCJ1cGRhdGVFZGl0b3IiOmZhbHNlLCJhdXRvU3luYyI6dHJ1ZSwidXBkYXRlRGlhZ3JhbSI6ZmFsc2V9)](https://mermaid-js.github.io/mermaid-live-editor/edit#eyJjb2RlIjoiZ3JhcGggTFJcbkFbY2xpZW50XSAgLS0g7JqU7LKtIC0tPiBCW0Rhb0ZhY3RvcnldXG5CIC0tIOyDneyEsSAtLT4gQ1tVc2VyRGFvXVxuQSAtLeyCrOyaqS0tPiBDXG5DIC0t7IKs7JqpLS0-IERbQ29ubmVjdGlvbk1ha2VyIOq1rO2YhCDtgbTrnpjsiqRdXG5CIC0t7IOd7ISxLS0-IEQiLCJtZXJtYWlkIjoie1xuICBcInRoZW1lXCI6IFwiZGFya1wiXG59IiwidXBkYXRlRWRpdG9yIjpmYWxzZSwiYXV0b1N5bmMiOnRydWUsInVwZGF0ZURpYWdyYW0iOmZhbHNlfQ)

#### 4-2. 오브젝트 팩토리의 활용
만약 다른 DAO의 생성 기능을 추가한다고 가정했을 때, C.M 구현 클래스의 객체를 생성하는 코드가 메소드마다 반복되게 됩니다.

```java
public class DaoFactory{
	public UserDao userDao(){
		return new UserDao(new DcounnectionMaker());
	}
	public AccountDao accountDao(){
		return new AccountDao(new DconnectionMaker());
	}
}
```

이런 중복 문제를 해결하려면 역시 분리하는게 가장 좋은 방법입니다.

```java
public class DaoFactory{
	public UserDao userDao(){
		return new UserDao(counnectionMaker());
	}
	public AccountDao accountDao(){
		return new AccountDao(connectionMaker());
	}
	public ConnectionMaker connectionMaker(){
		return new DConnectionMaker();
		// 분리해낸 코드
	}
}
```

#### 4-3. 제어권의 이전을 통한 제어관계 역전
제어의 역전 개념은 이미 폭넓게 적용되어 있습니다. 서블릿을 예로들면, 일반적인 자바 프로그램은 main메소드에서 시작해서 개발자가 쓴 코드에 따라 오브젝트가 생성되고 실행됩니다. 그런데 서블릿은 그 실행을 개발자가 직접 제어할 수 있는 방법은 없습니다. 대신 서블릿에 대한 제어 권한을 가진 컨테이너가 서블릿 클래스의 오브젝트를 만들고 메소드를 호출합니다.

앞서본, 템플릿 메소드 패턴에서도 제어의 역전이라는 개념이 활용됐습니다.
DaoFacotry는 가장 단순한 수준의 IoC컨테이너라고 불릴 수 있습니다.

> 라이브러리와 프레임워크가 어떻게 다른가?
> 라이브러리를 사용하는 코드는 애플리케이션이 흐름을 직접 제어합니다.
> 반면, 프레임워크는 코드가 프레임워크에 의해 사용됩니다.

### 5. 스프링의 IoC
스프링에는 여러가지 기술이 있지만 핵심을 담당하는 것은 바로 **빈 팩토리(애플리케이션 컨텍스트)**라고 불리는 것입니다.
이는 우리가 만든 DaoFactory의 역할을 좀 더  일반화 한것이라고 볼 수 있습니다.
이제, DaoFactory를 스프링에서 사용이 가능하도록 개선해봅니다.

#### 5-1. 오브젝트 팩토리를 이용한 스프링 IoC
> bean : 스프링이 직접 제어권을 가지고 관계를 부여하고 만드는 오브젝트를 빈 이라고 합니다.

> 빈 팩토리 : 빈의 생성과 제어를 담당하는 IoC 오브젝트를 빈 팩토리 혹은 **어플리케이션 컨텍스트(application context), 스프링 컨테이너**라 부릅니다.

애플리케이션 컨텍스트에는 DaoFactory처럼 코드로 정보가 담겨있진 않지만, 별도로 설정정보를 담고있는 무엇인가를 가져와 이를 활용합니다.
스프링이 빈 팩토리를 위한 오브젝트 설정을 담당하는 클래스라고 인식 할 수 있도록
@Configuration이라는 어노테이션을 추가합니다.
그리고 오브젝트를 만들어 주는 메소드 에는
@Bean 이라는 어노테이션을 붙여줍니다.
이 두가지 어노테이션 만으로 애플리케이션 컨텍스트가 사용할 설정정보가 된 것입니다.
```java
@Configuration	//애플리케이션 컨텍스트가 사용할 설정정보라는 표시
public class DaoFactory{
	@Bean	// 오브젝트 생성을 담당하는 IoC용 메소드라는 표시
	public UserDao userDao(){
		//생략
```

이제 DaoFactory를 설정정보로 사용하는 애플리케이션 컨텍스트를 만듭니다. 
```java
public class UserDaoTest{
	public static void main(String[] args) throws ClaaNotFoundException, SQLException{
	ApplicationContext context =
	// 애플리케이션 컨텍스트는 ApplicationContext타입 오브젝트 입니다.
	new AnnotationConfigApplicationContext(DaoFactory.class);
	// 생성자 파라미터로 설정정보로 사용할 DaoFactory클래스를 넣어줍니다.
	UserDao dao = context.getBean("userDao", UserDao.class);
	// 이제 ApplicationContet의 getBean(빈이름, 리턴타입) 메소드를 이용해 UserDao의 오브젝트를 가져올 수 있습니다.
	// userDao : @Bean 애노테이션이 붙은 메소드의 이름이 빈 이름이 됩니다.
	// 생략
```
이렇게 첫번째 스프링 애필리케이션을 만들었습니다.

#### 5-2. 애플리케이션 컨텍스트의 동작방식
기존 DaoFactory가 DAO 오브젝트를 생성하고 DB 생성 오브젝트와 관계를 맺어주는 제한적인 역할을 하는 데 반해,
애플리케이션 컨텍스트는 IOC를 적용해서 관리할 모든 오브젝트에 대한 생성과 관계설정을 담당합니다. 
그림으로 애플리케이션 컨텍스트가 사용되는 방식을 보겠습니다.

[![](https://mermaid.ink/img/eyJjb2RlIjoiZ3JhcGggTFJcbkFbY2xpZW50XSAtLXVzZXJEYW_smpTssq0tLT4gQltBcHBsaWNhdGlvbkNvbnRleHQuZ2V0QmVhbiDruYjrqqnroZ0g7KGw7ZqMXVxuQiAtLeyDneyEseyalOyyrS0tPiBDW0NvbmZpZ3VyYXRpb24sIEJlYW4g7Ja064W47YWM7J207IWYXVxuQyAtLeuTseuhnS0tPiBCXG5DIC0t7IOd7ISxLS0-IERbVXNlckRhb11cbkEgLS3sgqzsmqktLT4gRCIsIm1lcm1haWQiOnsidGhlbWUiOiJkYXJrIn0sInVwZGF0ZUVkaXRvciI6ZmFsc2UsImF1dG9TeW5jIjp0cnVlLCJ1cGRhdGVEaWFncmFtIjpmYWxzZX0)](https://mermaid-js.github.io/mermaid-live-editor/edit#eyJjb2RlIjoiZ3JhcGggTFJcbkFbY2xpZW50XSAtLXVzZXJEYW_smpTssq0tLT4gQltBcHBsaWNhdGlvbkNvbnRleHQuZ2V0QmVhbiDruYjrqqnroZ0g7KGw7ZqMXVxuQiAtLeyDneyEseyalOyyrS0tPiBDW0NvbmZpZ3VyYXRpb24sIEJlYW4g7Ja064W47YWM7J207IWYXVxuQyAtLeuTseuhnS0tPiBCXG5DIC0t7IOd7ISxLS0-IERbVXNlckRhb11cbkEgLS3sgqzsmqktLT4gRCIsIm1lcm1haWQiOiJ7XG4gIFwidGhlbWVcIjogXCJkYXJrXCJcbn0iLCJ1cGRhdGVFZGl0b3IiOmZhbHNlLCJhdXRvU3luYyI6dHJ1ZSwidXBkYXRlRGlhZ3JhbSI6ZmFsc2V9)

어플리케이션 컨텍스트를 사용했을 때 장점
- 클리언트는 구체적인 팩토리 클래스를 알 필요가 없다.
	- DaoFactory같은 IoC를 적용한 오브젝트가 계속 추가 될 것인데, 클라이언트가 필요한 오브젝트를 가져오려면 어떤 팩토리클래스를 사용해야 할지 알아야하고, 필요때 마다 팩토리오브젝트를 생성해야하는 번거로움이 있습니다. 애플리케이션 컨텍스트를 사용하면 직접 사용할 필요가 없어집니다.
-  애플리케이션 컨텍스튼 종합적인 IoC 서비스를 제공합니다. 
	- 오브젝트가 만들어지는 방식, 시점과 전략, 자동생성, 후처리 등 다양한 기능을 제공합니다.
- 애플리케이션 컨텍스트는 빈을 검색하는 다양한 방법을 제공한다.

#### 5-3. 스프링 IoC의 용어 정리
- 빈 : 스프링 방식으로 관리되는 오브젝트 입니다.
- 빈 팩토리 : 빈을 등록하고, 생성하고, 조회하고, 돌려주고 등 부가적인 빈을 관리하는 컨테이너입니다. 이 인터페이스에 getBean과 같은 메소드가 정의 되어있고, 보통 이를 확장한 애플리케이션 컨텍스트를 이용합니다.
- 애플리케이션 컨텍스트 : 빈의 지원 뿐 만아니라 애플리케이션 지원 기능을 모두 포함합니다.
- 설정정보/메타정보 : 애플리케이션 컨텍스트 또는 빈 팩토리가 IoC를 적용하기 위해 사용하는 메타정보입니다. 컨테이너에 어떤 기능을 설정하는 경우에도 사용하지만, 그보다는 빈을 생성하고 구성할 때 사용됩니다.
- 컨테이너 또는 IoC컨테이너 : 주로 애플리케이션 컨텍스트를 가리키는 것입니다.

### 6. 싱글톤 레지스트리와 오브젝트 스코프
지금까지 DaoFactory 클래스를 직접 사용하는 것과, Configuration을 사용하는 것의 결과는 같았습니다.
하지만 DaoFactory의 userDao()를 여러번 호출하면 new 연산자에 의해 매번 새로운 객체를 생성해냅니다.
> 오브젝트의 동일성과 동등성
> 동일성은 같은 객체인지(주소값) 비교하고, 동등성은 같은 내용을 담고 있는지 비교합니다. Object의 equals()와 ==연산자는 동일성을 비교합니다.

반면, getBean()을 이용해 불러온 UserDao는 여러번 호출해도 매번 동일한 오브젝트를 돌려줍니다.

#### 6-1. 싱글톤 레지스트리로서의 애플리케이션 컨텍스트
애필르케이션 컨텍스트는 싱글톤을 저장하고 관리하는 싱글톤 레즈스트리(Singleton registry) 입니다.
스프링은 별다른 설정을 하지 않으면 빈 오브젝트를 모두 싱글톤으로 만듭니다.
이와같이 싱글톤 패턴으로 관리하는 이유는 스프링이 주로 사용되는 대상이 자바 엔터프라이즈 기술(대표적으로 서블릿)을 사용하는 서버환경이기 때문입니다.
> 싱글톤 패턴

> 애플리케이션 내에서 주로 하나만 존재하도록 강제하는 패턴입니다. 여러 스레드에서 하나의 오브젝트를 공유해 동시에 사용합니다.

- 싱글톤 패턴 구현하는 방법
```java
public class UserDao{
	private static UserDao INSTANCE;
	// 생성된 싱글톤 객체를 저장할 자신과 같은 타입의 스태틱 필드를 정의합니다.
	private ConnectionMaker connectionMaker;
	
	private UserDao(ConnectionMaker cm){
		this.connectionMaker = cm;
		}
	// 클래스 외부에서 접근하지 못하도록 생성자를 private으로 만듭니다.
	private static sychronized UserDao getInstance(){
		if(INSTANCE == null) INSTANCE = new UserDao(???);
		// 최초로 호출됐다면 한번만 오브젝트를 생성해 스태틱  필드에 저장합니다. 또는 스태틱필드의 초기값으로 미리 만들어둡니다.
		retrun INSTANCE;
		// 이미 싱글톤 오브젝트가 만들어졌다면 저장해둔 오브젝트를 넘겨줍니다.
		}
```

- 싱글톤 패턴의 한계
	- private 생성자를 갖고 있기 떄문에 상속할 수 없습니다.
	- 만들어지는 방식이 제한적이기 때문에 생글톤은 테스트하기가 힘듭니다.
	- 서버환경에서는 싱글톤이 하나만 만들어지는 것이 보장되지 않습니다.
	- 싱글톤의 사용은 전역 상태를 만들 수 있기 때문에 바람직하지 않습니다.
		- 아무 객체나 자유롭게 접근 가능하고 수정할 수 있게 두는것은 객체지향에 바람직하지 않습니다.

이런 여러가지 단점이 있기 떄문에, 스프링은 직접 싱글톤 형태의 오브젝트를 관리합니다.
그것이 바로 **싱글톤 레지스트리** 입니다.

이 싱글톤 레지스트리는 스태틱메소드와 private 생성자가 강제되는 클래스가 아니라 **평범한 자바 클래스를 싱글톤으로 활용**하게 해줍니다.
따라서, 테스트를 위한 Moc 오브젝트로 대체하는 것도 간단하고, 객체지향적인 설계 방식원칙과 디자인패턴을 적용하는데 제약 없게 해줍니다.

#### 6-2. 싱글톤과 오브젝트의 상태
싱글톤은 스레드들이 동시에 싱글톤 오브젝트의 인스턴스 변수를 수정하는 것이 위험하기 때문에(상태 유지방식, stateful), 상태정보를 내부에 갖고 있지 않은 무상태(stateless)방식으로 만듭니다.
만약, 읽기전용 값이라면 초기화 시점에서 인스턴스 변수에 저장해두고 공유하는 것은 문제가 없습니다.

무상태방식으로 클래스를 만드는 경우에는 파라미터나 로컬변수, 리턴값을 이용하여 요청에 대한 정보를 다룹니다. 이와 같은 지역변수들은 매번 새로운 값을 저장할 독립적인 공간이 만들어지기 때문에 여러 스레드가 변수의 값을 덮어쓸 일이 없습니다.

> 인스턴스 변수 : 인스턴스마다 다른 값을 가지고 있어야할 때 사용합니다. 싱글톤 패턴에서는 인스턴스가 하나이기 때문에 주의해야 합니다.


> 클래스 변수 : 스태틱변수라고도하며 클래스가 메모리에 올라갈 때 동시에 생성되는 인스턴스들이 공유하는 변수입니다. 인스턴스 생성없이 사용가능 합니다.


> 지역 변수 : 메소드 영역에 존재하는 변수입니다. 해당 메소드 내에서만 사용 가능합니다.


> 전역 변수 : public이 붙으며 같은 클래스내 어디서든 사용가능합니다.

기존의 UserDao를 살펴보면, 인스턴스 변수로 선언 된 connectionMaker는 읽기 전용 값이기 때문에 인스턴스 필드에 두어도 좋습니다.

반면, 만약 기존에 로컬변수(지역변수)로 선언되 값을 리턴하는 User클래스와 Connection클래스를 **인스턴스 변수로 두게되면**, 이 두 클래스는 매번 새로운 값으로 바뀌는 정보를 담기 때문에 심각한 문제가 발생합니다.

#### 6-3. 빈의 스코프
빈이 관리되는 범위를 빈의 스코프라고 합니다. 스프링 빈의 기본 스코프는 싱글톤입니다.  
경우에 따라서 싱글톤 외의 스코프를 가질 수 있습니다.
- 프로토타입 스코프 : 컨테이너에 빈을 요청할 때 마다 매번 새로운 오브젝트를 돌려줍니다.
- 요청 스코프 : 웹을 통해 새로운 HTTP요청이 생길 때 마다 생성됩니다.
- 세션 스코프 : 웹의 세션과 유사합니다.

### 7. 의존관계 주입(DI)
#### 7-1. 제어의 역전과 의존관계 주입
스프링의 IoC 기능의 대표적인 동작원리를 의존관계 주입(Dependency Injection)이라고 합니다. 이는 스프링이 다른 프레임워크와 차별화돼서 제공해주는 기능입니다.

#### 7-2. 런타임 의존관계 설정
두 개의 클래스가 의존관계에 있다고 말할 때는 항상 방향성이 있습니다.

[![](https://mermaid.ink/img/eyJjb2RlIjoiZ3JhcGggTFJcbkFbQe2BtOuemOyKpF0gLS1B6rCAIELsl5Ag7J2Y7KG0LS0-IEJbQu2BtOuemOyKpF0iLCJtZXJtYWlkIjp7InRoZW1lIjoiZGFyayJ9LCJ1cGRhdGVFZGl0b3IiOmZhbHNlLCJhdXRvU3luYyI6dHJ1ZSwidXBkYXRlRGlhZ3JhbSI6ZmFsc2V9)](https://mermaid-js.github.io/mermaid-live-editor/edit#eyJjb2RlIjoiZ3JhcGggTFJcbkFbQe2BtOuemOyKpF0gLS1B6rCAIELsl5Ag7J2Y7KG0LS0-IEJbQu2BtOuemOyKpF0iLCJtZXJtYWlkIjoie1xuICBcInRoZW1lXCI6IFwiZGFya1wiXG59IiwidXBkYXRlRWRpdG9yIjpmYWxzZSwiYXV0b1N5bmMiOnRydWUsInVwZGF0ZURpYWdyYW0iOmZhbHNlfQ)

의존 한다는 것은 B(의존대상)이 변하면 A에 영향을 미친다는 것입니다.  
대표적으로 A가 B의 메소드를 호출해서 사용하는 경우입니다.

userDao의 의존관계를 보면, userDao가 ConnectionMaker를 사용함으로 의존하고 있지만, 그 구현 객체인 DConnectionMaker에는 userDao가 영향을 받지 않습니다.  
이렇게 인터페이스에 대해서만 의존관계를 만들어두면 구현 클래스와는 관계가 느슨해지게되며 **낮은 결합도** 상태가 됩니다.  
이런 모델링 시점의 코드에서 클래스와 인터페이스를 통해 드러나는 의존관계 말고,  
런타임 시에 오브젝트 사이에서 만들어지는 실체화 된 의존관계도 있습니다.  
이를 런타임 의존관계 또는 오브젝트 의존관계라고 합니다.  
실제 사용대상인 오브젝트를 의존 오브젝트(DConnectionMaker)라고 말합니다.  


정리하면 DI란 다음 조건을 충족하는 작업을 말합니다.
- 코드에는 런타임 시점의 의존관계가 드러나지 않는다.(인터페이스만 의존하고 있습니다.)
- 런타임 시점의 의존관계는 컨테이너 같은 제3의 존재가 결정합니다.
- 의존관계는 사용할 오브젝트에 대한 레퍼런스를 외부에서 제공해줌으로써 만들어집니다.
  

```java
public class UserDao{
	private ConnectionMaker cm;

	public UserDao(ConnectionMaker cm){
		this.cm = cm;
		// DI컨테이너인 DaoFactory는 자신이 결정한 의존관계를 맺어줄 클래스의 오브젝트(UserDao)를 만들고
		//이 오브젝트 생성자의 파라미터로 레퍼런스를 전달합니다.
	}
}
```


#### 7-3. 의존관계 주입
스프링에는 스스로 검색을 이용해 의존관계를 맺는 의존관계 검색(dependency lookup)이라고 불리는 것도 있습니다.  
물론 **이때 어떤 오브젝트를 이용할지는 결정하지 않습니다.**  
단지, 메소드나 생성자를 통한 주입 대신 스스로 컨테이너에게 요청하는 방법(getBean 메소드)입니다.  

이런 검색방식은 코드안에 오브젝트 팩토리 클래스나 스프링 API가 나타나므로 바람직하진 않지만,  
의존관계 검색방식을 사용해야 할 때가 있습니다. 바로 main메소드에서는 DI를 이용해 오브젝트를 주입받을 방법이 없기때문입니다.  

DI와 검색의 가장 중요한 차이점은 검색은 자신(UserDao)이 Bean일 필요가 없지만, **DI를 위해서는 자신도 Bean이어야 합니다.**  

#### 7-4. 의존관계 주입의 응용
- 기능 구현의 교환
  - 만약, 개발용 로컬DB를 사용하다 실제 운영을 위해 다른 DB로 바꿔야 한다면, DB에 연결된 클래스를 수백가지 DAO에서 모두 수정해야합니다.  하지만 DI를 통해 만들었다면 @Configuration이 붙은 DaoFactory에서 return값만 수정하면됩니다.
- 부가기능 추가
  - 새로운 관심사를 추가하려고하면, 새로운 클래스를 만들어 DI를 해주면 됩니다.


```java
public class CountingConnectMaker implements ConnectionMaker{
	// DB에 연결횟수를 세는 기능을 추가한다고 합시다.
	// 이 클레스는 직접 내부에서 DB커넥션을 만들지 않습니다.
	// reacm에 저장된 ConnectionMaker 타입의 오브젝트의 makeConnection()을 호출해서 DAO에게 돌려줍니다.
	int counter = 0;
	private CounnectionMaker realcm;

	public CountingConnectionMaker(ConnectionMaker realcm){
		// CountingConnectionMaker 역시 DI 주입을 받고 있습니다.
		this.realcm = realcm;
	}
	public Connection makeConnection(){
		this.counter++;
		return realcm.makeConnection();
		// DB커넥션을 돌려주게 됩니다.(아마도 DConnectionMaker)
	}

	public int getCounter(){
		return this.counter
	}
}
```

이를 토대로 설정정보를 담은 클래스도 만듭니다.

```java
@Coinfiguration
public class CountingDaoFactory{
	@Bean
	public UserDao userDao(){
		return new UserDao(cm);
		// 모든 DAO는 여전히 cm()을 통해 만들어지는 오브젝트를 DI받습니다.
	}
	@Bean
	public ConnectionMaker cm(){
		return new CountingConnectionMaker(realcm());
	}
	@Bean
	public ConnectionMaker realcm(){
		return new DConnectionMaker();
		// 실질적인 DI오브젝트 입니다.
	}
}
```

이후 이 기능을 위한 테스트를 위해 테스트용 클래스에서 cm이라는 빈 이름으로 의존관계 검색(DL)을 합니다.  
이로써 아래 그림과같은 런타임 의존관계가 만들어집니다.  

[![](https://mermaid.ink/img/eyJjb2RlIjoiZ3JhcGggTFJcbkFbVXNlckRhb10gLS0-IEJbQ291bnRpbmdDTV0gLS0-IENbRENvbm5lY3Rpb25NYWtlcl0iLCJtZXJtYWlkIjp7InRoZW1lIjoiZGFyayJ9LCJ1cGRhdGVFZGl0b3IiOmZhbHNlLCJhdXRvU3luYyI6dHJ1ZSwidXBkYXRlRGlhZ3JhbSI6ZmFsc2V9)](https://mermaid-js.github.io/mermaid-live-editor/edit#eyJjb2RlIjoiZ3JhcGggTFJcbkFbVXNlckRhb10gLS0-IEJbQ291bnRpbmdDTV0gLS0-IENbRENvbm5lY3Rpb25NYWtlcl0iLCJtZXJtYWlkIjoie1xuICBcInRoZW1lXCI6IFwiZGFya1wiXG59IiwidXBkYXRlRWRpdG9yIjpmYWxzZSwiYXV0b1N5bmMiOnRydWUsInVwZGF0ZURpYWdyYW0iOmZhbHNlfQ)

#### 7-5. 메소드를 이용한 의존관계 주입
지금까지 생성자를 통한 DI만 사용해왔지만 일반 메소드를 이요한 방법이 더 많이 사용됩니다.  
- setter를 이용한 주입
  - 파라미터로 전달된 값을 내부의 인스턴스 변수에 저장합니다. 외부에서 오브젝트내부의 애트리뷰트 값을 변경하는 용도로 주요 사용됩니다.
- 일반 메소드를 이용한 주입
  - setter와 다르게 여러개의 파라미터를 가질수 있습니다. 한번에 모든 파라미터를 받아야하는 생성자보다 낫습니다.

```java
@Bean
public UserDao userDao(){
	UserDao userDao = new UserDao();
	userDao.setConnectionMaker(cm());
	// 세터 메소드를 이용하여 바꾼 DaoFactory 클래스 입니다.
	return userDao;
}
```

### 8. XML을 이용한 설정
DI 컨테이너인 스프링을 도입하면서 DaoFactory는 참고정보로 사용되고 있습니다.  
오브젝트 사이의 의존정보를 일일이 자바코드로 작성하기에는 번거롭습니다.  
XML은 단순한 텍스트 파일이기 때문에 컴파일이 필요없으며 빠르게 변경사항을 반영할 수 있습니다.
애플리케이션 컨텍스트는 XML에 담긴 DI 정보를 \<beans>를 루트 엘리먼트로 사용해 활용할 수 있습니다.

#### 8-1. XML 설정
먼저 DaoFacotry의 connectionMaker()에 해당하는 빈을 XML로 정의해봅니다.  

|  |자바 코드  |XML |
|--|--|--|
|빈 설정파일  |@Configuration  | \<beans> |
|빈의 이름  |@Bean 메소드명  |<bean id="메소드명" |
|빈의 클래스  |return new 주입할 의존클래스명();  |class="패키지.주입할 의존클래스명"> |

이때, class 애트리뷰트에는 패키지 까지 모두 포함시켜서 작성해야합니다.  
  
이번에는 userDao()를 전환해봅니다. userDao메소드에는 수정자 메소드를 사용합니다.  
자바빈의 관례에 따라서 setter 메소드는 프로퍼티가 됩니다.  
\<property> 태그는 name과 ref라는 애트리뷰트를 갖습니다.  
ref는 주입해줄 오브젝트의 빈 이름이라는 것에 주의해야합니다.  
즉, DaoFactory에서 설정한 빈이름 메소드 cm을 의미하게 됩니다.

```java
// userDao.setConnectionMaker(cm());
// 위 코드가 아래 XML로 치환됩니다.
// userDao 빈의 cm프로퍼티를 이용해 의존관계를 주입한다는 뜻입니다.

<beans>
	<bean id="cm" class"springbook.user.dao.DconnectionMaker" />
	<bean id="userDao" class="springbook.user.dao.UserDao">
		<property name="connectionMaker" ref="cm" />
		// name은 setConnectionMaker(수정자 메소드)의 set을 제거한 이름입니다.
		// ref는 메소드를 통해 주입해줄 오브젝트의 "빈 이름" 입니다.(bean id = cm)
		// DI할 오브젝트 역시 빈으로 등록되있기 때문입니다.
	</bean>
</beans>
```

> 참고) xml문서의 구조를 정의하는 방법에 DTD와 스키마(schema)가 있습니다. 특별한 이유가없다면 스키마를 사용하는 것이 바람직합니다.


#### 8-2. XML을 이용하는 application context
XML에서 빈의 의존관계 정보를 이용하는 IoC/DI작업에는 GenericXmlApplicationContext를 사용합니다.  
생성자 파라미터로는 XML 파일의 경로를 지정해줍니다.  
XML설정 파일은 관례에 따라 applicationContext.xml으로 저장하고 클래스패스 최상단에 둡니다.  
이제, AnnotationConfigApplicationContext대신 XML을 사용하게 수정합니다.  
> Application context = new GenericXmlApplicationContext("applicationContext.xml");

생성자에 /가 없는 경우에 루트에서부터 시작하는 경로입니다.  
GenericXml...외에도 ClassPathXmlApplicationContext(xml, UserDao.class)가 있는데,  
생성자로 xml 파일명과, 특정 패키지의 위치로부터 찾도록 지정하는 패키지에 소속한 클래스를 적습니다.  

#### 8-3. DataSource 인터페이스로 전환
자바에서는 이미 DB커넥션을 가져오는 기능을 추상화해서 사용할수 있게 만든 DataSource 인터페이스가 존재합니다.  
DataSource 인터페이스와 다양한 구현 클래스를 사용할 수 있도록 UserDao를 리팩토링 합니다.  

```java
public class UserDao{
	private DataSource ds;

	public void setDataSource(DataSource ds){
		this.dataSource = ds;
	}
	pulbic void add(User user) thorws SQLException{
		Connection c = ds.getConnection();
		//생략
	}
}
```

다음으로는, DataSoruce 구현 클래스가 필요합니다.  
스프링이 제공해주는 구현 클래스 중, SimpleDriverDataSource라는 것이 있습니다.  
이 클래스를 사용도록 DI를 재구성합니다.  
DaoFactory클래스의 cm메소드를 제거하고 SimpleDriverDataSoruce를 리턴하도록 수정합니다.  

```java
@Bean
public DataSource dataSource(){
	SimpleDriverDataSource dataSource = new SimpleDriverDataSource();
	
	dataSource.setDriverClass(com.mysql.jdbc.Driver.class);
	dataSource.setUrl("jdbc:msyql://localhost/springbook");
	dataSource.setUsername("hunny");
	dataSource.setPassword(spring);
	// DB연결 정보를 수정자 메소드를 통해 제공합니다.
	return dataSource;
}

@Bean
public UserDao userDao(){
	//생략
	userDao.setDataSource(dataSource());
	return userDao;
}
```

이후 XML 설정 방식으로까지 수정을 하게되면, 문제가 하나 있습니다.  
dataSource메소드에 수정자 메소드로 넣어준 DB접속정보가 XML에는 나타나지않습니다.  
심지어 단순 값이거나 단순 텍스트거나 클래스 타입의 오브젝트입니다.  

#### 8-4. 프로퍼티 값의 주입
다른 빈의 레퍼런스(ref)가 아니라 단순 값을 주입해주는 것이기 때문에,  
ref 애트리뷰트 댇신 value 애트리뷰트를 사용합니다.  
빈으로 등록될 클래스에 수정자 메소드가 정의되어 있다면 정보를 지정할 수 있다는 점에서,  
공통점이 있습니다.

```java
<property name"driverClass" value="com.mysql.jdbc.Drvier" />
//생략
```

그런데 어떻게 "com.mssql.jdbc.Drvier"라는 스트링 값이 Class 타입의 파라미터를 갖는  
수정자 메소드에 사용 될 수 있는 것일까요?  
이는, 수정자 메소드의 파라미터타입을 참고해서 스프링이 적절한 형태로 변환해주기 때문입니다.  

### 9. 정리
우리는 1장에서 아래의 내용들을 공부했습니다.
- 관심사의 분리(SoC), 리팩토링
- 전략 패턴 / 싱글톤 레지스트리
- 개방폐쇄원칙(OCP)
- 낮은 결합도, 높은 응집도
- IoC (제어의 역전)
- DI(의존관계 주입) / 생성자 주입, 수정자 주입
- XML 설정


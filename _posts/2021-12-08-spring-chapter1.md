---
layout: single
title:  "토비의 스프링 vol.1 1장"
categories: 토비의 스프링
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

### 1-2. User 테이블

 이제 User 오브젝트에 담긴 정보가 실제로 보관될 DB의 테이블을 만듭니다. (mysql 기준입니다.)

```sql
create table users(
    id varchar(10) primary key,
    name varchar(20) not null,
    password varchar(20) not null
)
```



### 1-3. UserDAO

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

-- 계속



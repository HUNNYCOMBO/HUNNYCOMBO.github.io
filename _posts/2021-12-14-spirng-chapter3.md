---
layout: single
title:  "토비의 스프링 vol.1 3장"
categories: spring
tags: [spring, 템플릿]
toc: true
author_profile: false
sidebar:
    nav: "docs"
search: true
---

## 템플릿
템플릿이란 변화가 거의 일어나지않는 특성을 갖는 코드를,  
자유롭게 변경되는 성질을 가진 부분으로부터 독립시켜서  
효과적으로 활용할 수 있도록 하는 기법입니다.  

### 1. 다시 보는 초난감DAO
UserDao코드에는 아직 문제점이 있습니다. 바로 예외상황 처리입니다.  

#### 1-1. 예외 처리 기능을 갖춘 DAO
DB커넥션이라는 제한적인 리소스를 굥유해 사용한다면,  
중간에 어떤 이유로든 예외가 발생햇을 경우 사용한 리소스를 반드시 반환해야 합니다. 그런데 우리가 만든 UserDao의 deleteAll()을 살펴보면

```java
public void deleteAll() throws SQLException{
    Connection c = dataSource.getConnection();

    PreparedStatement ps = c.prepareStatement("delte from users");
    ps.excuteUpdate();

    ps.close();
    c.close();
    // 메소드가 성공적으로 실행됐다면 반납하게 되지만,
    // 만약 ps를 만들던 도중 오류가 나면 반납하지 않는다.
}
```

이런 JDBC 코드에서는 어떤 상황에서라도 가져온 리소스를 반환하도록  
**try/catch/finally** 구문 사용을 권장합니다.  
일반적으로 DB커넥션은 커넥션 풀을 이용하여 반환한 객체를 재사용하기 떄문에,  
반환되지 않는다면 오류가 생기게 됩니다.  

- try : 예외 발생 가능성이 있는 코드를 묶어둡니다.
- catch : 예외 발생시 부가적인 작업을 해주도록 합니다.
- finally : 반드시 수행합니다.

```java
public vodi delteAll() thorws SQLException{
    Conenction c = null;
    PreparedSatement ps = null;
    // 예외가 c를 생성하는 시점에서 발생할지 ps를 생성하는 시점에서 발생하지 모르고, null값으로 초기화를 해줬습니다.
    // 그로인해 null일 떄 close()를 호출하면 nullpointexception이 발생합니다.
    // 반드시 null이 아닌지 확인 후 close() 를 해줍니다.

    try{
        c = dataSoure.getConnection();
        ps = c.prepareStatement(....);
        ps.excuteUpdate();
    }catch (SQLException e){
        throw e;
        // 아직은 예외를 메소드 밖 SQLException으로 던지는 것 밖에 할 수 없습니다.
    }finally {
        if(ps != null){
            try{
                ps.close();
                // 최종적으로 close() 역시 SQLException이 발생할 수 있으므로,
                // try/catch 문으로 감싸줍니다.
            }catch(SQLException e){
                throw e;
                // 특별히 해줄일이 없어서 비워놔도 됩니다.
                // 로그를 남기는 등의 부가작업을 해줘도 좋습니다.
                // 이미 delteAll()에 SQLException이 선언돼있어서 불필요하다 생각들 수도있지만,
                // try/catch로 안감싸주면 아래 c.close()를 실행하지 못하고 메소드를 벗어납니다.
            }
        }
        if(c != null){
            try{
                c.close();
            }catch (SQLException e){
            }
        }
    }
}
```
close()는 만들어진 순서의 역순으로 하는게 원칙입니다.  
resultset을 사용하는 코드에서는 rs역시 close()로 반환해줍니다.  

### 2. 변하는 것과 변하지 않는 것
#### 2-1. JDBC try/catch/finally 코드의 문제점
UserDao를 살펴보면, 복잡한 try/catch 블록이 반복적으로 등장합니다.  
1장에서 살펴봤던 SoC와 같이 접근하면 되지만,  
관심사를 분리하는 것과는 성격이 다르기 때문에 해결 방법이 조금 다릅니다.  

#### 2-2. 분리와 재사용을 위한 디자인 패턴 적용
1. 메소드 추출  
만약 변하지 않는 부분을 나머지 부분에서 분리해서 따로 메소드로 두게 된다면, 해당 메소드가 다른 곳에서 재사용이 불가능하기 때문에 다른 방법이 필요합니다. 

```java
public void delteAll() throws SQLE...{
    ...
    try{
        c = dataSource.getConnection();
        ps = makeStatement(c);
    }....
}
private PreparedStatement makeStatement(Connection c) thorws ... {
    // 변하는 부분을 추출한 메소드
    PreparedStatment ps;
    ps = c.prepareStatement("delte form users");
    return ps;
    // 재사용성이 없습니다.
}
``` 

2. 템플릿 메소드 패턴(상속)  
상속을 통해 변하지 않는 부분은 슈퍼클래스에 두고, 변하는 부분은 추상 메소드로 정의해둬서  
서브클래스에서 오버라이딩하여 사용하는 방식입니다.  
이 방식은 접근에 제한이 많아 DAO로직마다 새로운 서브클래스를 만들어야하는 문제가 있습니다.  
또한, 이미 설계시점에서 확장구조가 고정되어 버립니다. 

```java
abstract protected PreparedStatement makeStatement(Connection c) thorws...{
    // makeStatement()를 추상 메소드로 변경했습니다.
}

// UserDao 추상 클래스를 구현한 UserDaoDeletlAll 클래스
publci class UserDaoDeleteAll extends UserDao{
    @override
    protected PreparedSta.....{
        ...
        return ps;
    }
}
``` 

3. 전략 패턴의 적용(인터페이스)  
오브젝트를 별개의 둘로 분리하고 클래스 레벨에서는 인터페이스를 통해서만 의존하도록 만드는 전략 패턴입니다.  
deleteAll()의 맥락을 살펴보면,
- DB 커넥션 가져오기
- PreparedStatement를 만들어줄 외부 기능 호출
- 전달받은 ps 실행
- 예외발생시 처리
- 리소스 반환하기

이 중에 두번째 작업인 ps를 만들어주는 외부기능이 바로 전략패턴 이라고 할 수 있습니다.  
따라서 이 기능을 인터페이스로 만들어두고, 메소드를 통해  
ps 생성 전략을 호출해 생성한 ps를 전달해주면 됩니다.  

하지만 전략패턴은 맥락(컨텍스트)은 유지되면서 필요에 따라 전략을 바꿔 쓸 수 있다는 것인데,  
코드 안에서 이미 전략 클래스를 사용하도록 **고정**되버립니다.  
이는 OCP에 들어맞다고 볼 수 없습니다.  

```java
public interface StatementStategy{
    PreparedStatement makePreparedStatement(Connection c) throws ...;
}
// 이 인터페이스를 상속해서 PreparedStatement를 생성하는 전략 클래스를 만듭니다.

public class DeleAllStatement implements StatementStrategy{
    public PreparedStatement makePreparedStatement.....{
        ...
        StatementStrategy st = new DeleteAllStatement();
        ps = st.makePreparedStatement(c);
        // 구현 클래스가 로직에 들어납니다.
        ...
    }
}
```

4. DI 적용을 위한 클라이언트/컨텍스트 분리  
결국 우리는 UserDao 때처럼,  
컨텍스트(UserDao)가 필요로 하는 전략(ConnectionMaker)의 특정 구현 클래스(DConnectionMaker)의 오브젝트를  
클라이언트(UserDaoTest)가 만들어서 제공해주는 방법을 똑같이 적용해야합니다.  
중요한 것은 deleteAll()의 컨텍스트에 해당하는 try/catch문을 클라이언트 코드인 StratementStrategy를 만드는 부분에서 분리시켜야 합니다.  

```java
pulbic void jdbcContextWithStatementStrategy(StatementStrategy stmt) thorws...{
    // 클라이언트가 호출할때 넘겨줄 메소드파라미터
    ...
    try{
        ...
        ps = stmt.makePreparedStatement(c);

        ps.executeUpdate();
    }...
}

public void delteAll() thorws SQLException{
    // 컨텍스트를 jdbcContext..메소드로 분리해내서 이 메소드가 클라이언트가 됩니다.
    StatementStrategy st = new DeleteAllStatement();
    // 사용할 전략 클래스를 생성하고
    jdbcContextWithStatementStrategy(st);
    // 컨텍스트를 호출하고 전략 오브트를 전달합니다.
}
```

deleteAll()은 이제 전략 오브젝트를 만들고 컨텍스트를 호출하는 책임을 지고 있습니다.

### 3. JDBC 전략 패턴의 최적화
우리는 이제 delteAll() 메소드에 변하지 않는 부분을 분리해내 DAAO 메소드들이 공유할 수 있게 만들었습니다.  
컨텍스트는 PreparedStatement를 실행하는 작업 흐름이고,  
전략은 PreparedStatement를 생성하는 것입니다.
#### 3-1. 전략 클래스의 추가 정보
이번엔 add()에도 적용해봅니다. add메소드는 user라는 부가적인 정보가 필요하기 떄문에  
클라이언트로부터 User 타입 오브젝트를 받을 수 있도록 생성자를 통해 제공받게 만듭니다.

```java
public class AddStatement implements StratementStrategy{
    User user;
    public AddStatement(User user){
        this.user= user;
    }

    public PrepaerdStatement makePreparedStatement(Connection c){
        ...
        ps.setString(1, user.getId());
        ...
    }
}

// UserDao 클래스의 add()를 user정보를 생성자를 통해 전달해주도록 수정합니다.
public void add(User user)...{
    StatementStrategy st = new AddStatement(user);
    jdbcContextState...(st);
}
```

이제 deleAll()과 add() 모두 ps를 실행하는 jdbcContextWithStatementStrategy(컨텍스트)를 공유해서 사용 할 수 있게 됐습니다.  
앞으로 비슷한 기능의 DAO 메소드가 필요할떄마다 이 Statement전략과 컨텍스트를 활용할 수 있습니다.  
그러나 상속과 마찬가지로 DAO 메소드마다 새로운 st 구현 클래스를 만들어야 하고,  
전달해야할 부가적인 정보가 필요한 경우 생성자와 이를 저장해둘 인스턴스 변수를 만들어야 합니다.  

#### 3-2. 전략과 클라이언트의 동거
위의 두가지 문제점을 해결하기 전에 중첩클래스에 대해 알아보고 갑니다.  

- 중첩클래스(nested class) : 다른 클래스 내부에 정의되는 클래스
  - 스태틱 클래스 : 독립적인 오브젝트로 만들어질 수 있습니다.
  - 내부 클래스(inner class) : 자신이 정의된 클래스의 오브젝트 안에서만 만들어집니다.
    - 멤버 내부 클래스 : 멤버 필드처럼 오브젝트 레벨에 정의됩니다.
    - 로컬 클래스 : 메소드레벨에 정의됩니다. 로컬(지역) 변수를 선언하듯이 선언합니다.
    - 익명 내부 클래스 : 클래스 선언과 오브젝트 생성이 합쳐져 이름을 갖지 않습니다. scope는 선언위치에 따라 다릅니다. 클래스를 재사용할 필요가 없을때 유용합니다. new 인터페이스이름() {클래스 본문}; 으로 사용합니다.

아래 코드는 add()메소드 내 로컬 클래스로 이동한 AddStatement 클래스 입니다.  
StatementStrategy를 구현한 클래스들은 UserDao 밖에서는 사용되지 않기 때문에,  
UserDao 메소드에 강하게 결합되어 있습니다.  
특정 메소드에서만 사용된다면 로컬클래스로 만들 수 있습니다.

```java
public void add(final User user) throws SQLE..{
    // 내부클래스에서 외부의 변수를상ㅇ할 때는 반드시 final로 선언해야 합니다.
    class AddSatement implements StatementStrategy{
        // add 메소드 내부에 선언된 로컬 클래스
        public PreparedStratement makePrepared.....{

        }
        ...
    }

    StatementStrategy st = new AddStatement();
    // 생성자 파라미터로 user를 전달하지 않아도 됩니다.
    ...
}
```
**로컬클래스는 자신이 선언된 곳의 정보에 접근할 수 있습니다. ** 
그렇기 때문에 add()에서 번거롭게 생성자를 통해 User오브젝트를 전달해줄 필요가 없습니다.

이번엔 AddStrategyment를 익명 내부 클래스로 만들어 봅니다.

```java
	public void add(final User user) throws SQLException {
		jdbcContextWithStatementStrategy(
				new StatementStrategy() {			
					public PreparedStatement makePreparedStatement(Connection c)
					throws SQLException {
						PreparedStatement ps = 
							c.prepareStatement("insert into users(id, name, password) values(?,?,?)");
						ps.setString(1, user.getId());
						ps.setString(2, user.getName());
						ps.setString(3, user.getPassword());
						
						return ps;
					}
				}
		);
	}
```

### 4. 컨텍스트와 DI
#### 4-1. jdbcContext의 분리
전략 패턴 구조를 정리해봅니다.  
- 클라이언트 : UserDao의 메소드
- 전략 : 익명 내부클래스로 만들어지는 것
- 컨텍스트 : jdbcContextWithStatementStrategy()
  - 이 컨텍스트는 다른 DAO에서도 사용이 가능하므로 UserDao 클래스 밖으로 독립시켜서 모든 DAO가 사용할 수 있게 해봅니다. 

컨텍스트 메소드를 분리시키면 DataSource가 필요한 것은 UserDao가 아니라 분리시킨 클래스(JdbcContext)가 됩니다.  
DB 커넥션을 필요로 하는 코드는 JdbcContext안에 있기 때문입니다.

```java
public class JdbcContext {
	DataSource dataSource;
	
	public void setDataSource(DataSource dataSource) {
		this.dataSource = dataSource;
	}
    // DataSource 타입 빈을 DI 받을 수 있게 준비합니다.
	
	public void workWithStatementStrategy(StatementStrategy stmt) throws SQLException {
		Connection c = null;
		PreparedStatement ps = null;

		try {
			c = dataSource.getConnection();

			ps = stmt.makePreparedStatement(c);
		
			ps.executeUpdate();
		} catch (SQLException e) {
			throw e;
		} finally {
			if (ps != null) { try { ps.close(); } catch (SQLException e) {} }
			if (c != null) { try {c.close(); } catch (SQLException e) {} }
		}
	}
}

```

그 다음 UserDao가 JdbcContext를 DI 받아서 사용할 수 있게 만듭니다.

```java
public class UserDao {
	private DataSource dataSource;
	private JdbcContext jdbcContext;
		
	public void setDataSource(DataSource dataSource) {
		this.jdbcContext = new JdbcContext();
		this.jdbcContext.setDataSource(dataSource);
        // jdbccontext를 DI 받도록 만듭니다.
		this.dataSource = dataSource;
	}
	
	
	public void add(final User user) throws SQLException {
		this.jdbcContext.workWithStatementStrategy(
			// jdbcContext의 메소드를 사용하도록 변경합니다.
            ...
	}
```

이제 xml파일도 수정합니다.
```java
<bean id="userDao" ...> 
    <property name="jdbcContext" ref="jdcbContext" />
</bean>
<bean id="jdbcContext" class=...>
    <property name="dataSource" ref="dataSource" />
```

스프링의 DI는 기본적으로 인터페이스를 사이에 두고 의존클래스를 바꿔사용하도록 하는게 목적이지만,  
JdbcContext는 인터페이스도 구현클래스도 아닌 클래스입니다. 하지만 이 구현 방법이 바뀔리 없으므로,  
UserDao와 JdbcContext는 인터페이스를 사이에 두지 않고 DI를 적용하는 특별한 구조가 됐습니다.(런타임시가 아닌 클래스 레벨에서 의존관계가 고정됩니다.)

[![](https://mermaid.ink/img/eyJjb2RlIjoiZ3JhcGggTFJcbiAgICBBW1VzZXJEYW9dIC0tPiBCW0pkYmNDb250ZXh0XVxuICAgIEIgLS0-IENbZGF0YVNvdXJjZSA6IHNpbXBsZURyaXZlckRTXSIsIm1lcm1haWQiOnsidGhlbWUiOiJkYXJrIn0sInVwZGF0ZUVkaXRvciI6ZmFsc2UsImF1dG9TeW5jIjp0cnVlLCJ1cGRhdGVEaWFncmFtIjpmYWxzZX0)](https://mermaid.live/edit#eyJjb2RlIjoiZ3JhcGggTFJcbiAgICBBW1VzZXJEYW9dIC0tPiBCW0pkYmNDb250ZXh0XVxuICAgIEIgLS0-IENbZGF0YVNvdXJjZSA6IHNpbXBsZURyaXZlckRTXSIsIm1lcm1haWQiOiJ7XG4gIFwidGhlbWVcIjogXCJkYXJrXCJcbn0iLCJ1cGRhdGVFZGl0b3IiOmZhbHNlLCJhdXRvU3luYyI6dHJ1ZSwidXBkYXRlRGlhZ3JhbSI6ZmFsc2V9)

#### 4-2. JdbcContext의 특별한 DI
스프링 DI의 기본의도에 맞게 JDbcContext의 메소드를 인터페이스로 뽑아내고,  
이를 UserDao에서 사용하게 해도 됩니다.  
인터페이스를 사용해서 클래스를 자유롭게 변경할 수 있게 하진 않았지만, JdbcContext를 UserDao와 DI구조로 만든 이유를 생각해 봅니다.

1. JdbcContext가 싱글톤 빈입니다.  

JdbcContext는 변경되는 상태정보가 없고, dataSource 인스턴스 변수 역시 읽기전용입니다.

2. JdbcConetxt가 DI를 통해 다른 빈(dataSoruce)에 의존하고 있습니다.  

DI를 위해서는 양쪽 모두 빈으로 등록되어야 합니다. 따라서 JdbcContext는 다른 빈을 DI 받기 위해서라도 빈으로 등록돼야 합니다.

3. UserDao와 JdbcContext가 매우 강한 응집도를 갖고있습니다.

만약 UserDao가 JPA같은 ORM을 사용한다면 JDbcContext도 통째로 바뀌어야합니다.

4. DataSource와 달리 테스트에서 마저 다른 구현 클래스로 사용할 이유가 없습니다.

다만 이렇게 클래스를 바로 사용하는 구성을 DI에 적용하는 것은 가장 마지막에 고려해볼 사항입니다.(구체적인 관계가 설정에 노출됩니다.)  

반면 수동DI방식으로 만들면, JdbcContext를 싱글톤으로 만들수 없고, 간접적인 DI를 위해 부가적인 코드가 필요하지만,  
관계를 외부에 들어내지 않고 만들 수 있습니다.  

```java
public class UserDao{
    private DataSource datasource;
    private JdbcContext jc;

    public void setDataSource(DataSource ds){
        // 수정자 메소드면서 jdbcContext에 대한 생성, DI를 동시에 합니다.
        this.jc = new JdbcContext();
        // IoC
        this. jc.setDatSource(ds);
        // DI
        this.dataSource = ds;
    }
}
// xml
<bean id "userDao" ...>
    <property name="dataSource" ...>
```

설정 파일만 보면 dataSource를 직접 주입받는 것 같지만, 내부적으로는 JdbcContext를 통해 간접적으롤 dataSource를 사용하고 있을 뿐입니다.  

### 5. 템플릿과 콜백
전략 패턴의 기본 구조에 익명 내부클래스를 활용한 것을 템플릿/콜백 패턴이라 합니다.  
전략 패턴의 컨텍스트를 템플릿이라 부르고, 익면 내부 클래스로 만들어지는 오브젝트를 콜백이라고 부릅니다.  

- 템플릿 : 고정된 작업 흐름을 가진 코드를 재사용
  - 템플릿 메소드패턴을 생각해보면 고정된 로직은 슈퍼클래스에 두고, 바뀌는 부분을 서브클래스의 메소드에 둡니다.
- 콜백 : 템플릿 안에서 호출되는 것을 목적으로 만들어진 오브젝트
  - 파라미터로 전달되지만 값을 참조하기 위한 것이 아닌 로직을 담은 메소드를 실행시키기 위해 사용됩니다.(functional object)
  - 보통 단일 메소드 인터페이스(추상형 인터페이스)를 사용합니다.

일반적인 DI라면 템플릿에 인스턴스 변수를 만들어두고 사용할 의존 오브젝트를 수정자 메소드를 통해 저장해 사용할 것입니다.  
반면 템플릿/콜백 방식에서는 매번 매소드 단위로 사용할 오브젝트를 새롭게 전달받는게 특징입니다.(메소드레벨에서 일어나는 DI)  
하나의 디자인 패턴으로 기억해두는게 좋습니다.  

#### 5-1. JdbcContext에 적용된 템플릿/콜백
템플릿과 클라이언트가 메소드 단위인 것이 특징입니다.  
[![](https://mermaid.ink/img/eyJjb2RlIjoiZ3JhcGggTFJcbiAgICBBW2NsaWVudCA6IFVzZXJEYW8uYWRkIOuplOyGjOuTnF0gLS0xLiDsnbXrqoUgQ2FsbGJhY2sg7Jik67iM7KCd7Yq4LS0-IEJb7YWc7ZSM66a_IDogSmRiY0NvbnRleHQud29ya1dpdGhTdGF0ZW1lbnRTdHJhdGVneSDrqZTshozrk5xdXG4gICAgQiAtLTIuIENvbm5lY3Rpb27snYQg7KO87J6FLS0-IEFcbiAgICBBIC0tMy4gIOy9nOuwsSDsnbXrqoXtgbTrnpjsiqQgU3RhdGVtZW50U3RyYXRlZ3nqsIAgVXNlckRhb-ydmCB1c2Vy7JmAIGNvbm5lY3Rpb27snYQg7IKs7Jqp7ZWY7JesIFByZXBhcmVkU3RhdGVtZW507J2EIOyjvOyehS0tPiBCXG4gICAgQiAtLTQuIOumrO2EtC0tPiBBIiwibWVybWFpZCI6eyJ0aGVtZSI6ImRhcmsifSwidXBkYXRlRWRpdG9yIjpmYWxzZSwiYXV0b1N5bmMiOnRydWUsInVwZGF0ZURpYWdyYW0iOmZhbHNlfQ)](https://mermaid.live/edit#eyJjb2RlIjoiZ3JhcGggTFJcbiAgICBBW2NsaWVudCA6IFVzZXJEYW8uYWRkIOuplOyGjOuTnF0gLS0xLiDsnbXrqoUgQ2FsbGJhY2sg7Jik67iM7KCd7Yq4LS0-IEJb7YWc7ZSM66a_IDogSmRiY0NvbnRleHQud29ya1dpdGhTdGF0ZW1lbnRTdHJhdGVneSDrqZTshozrk5xdXG4gICAgQiAtLTIuIENvbm5lY3Rpb27snYQg7KO87J6FLS0-IEFcbiAgICBBIC0tMy4gIOy9nOuwsSDsnbXrqoXtgbTrnpjsiqQgU3RhdGVtZW50U3RyYXRlZ3nqsIAgVXNlckRhb-ydmCB1c2Vy7JmAIGNvbm5lY3Rpb27snYQg7IKs7Jqp7ZWY7JesIFByZXBhcmVkU3RhdGVtZW507J2EIOyjvOyehS0tPiBCXG4gICAgQiAtLTQuIOumrO2EtC0tPiBBIiwibWVybWFpZCI6IntcbiAgXCJ0aGVtZVwiOiBcImRhcmtcIlxufSIsInVwZGF0ZUVkaXRvciI6ZmFsc2UsImF1dG9TeW5jIjp0cnVlLCJ1cGRhdGVEaWFncmFtIjpmYWxzZX0)

#### 5-2. 편리한 콜백의 재활용
템플릿/콜백 방식은 클라이언트인 DAO의 메소드가 최소한의 로직만 갖고 있게 되는 장점이 있습니다.  
다만, 익명 내부 클래스를 사용하기 떄문에 상대적으로 코드를 읽기 불편합니다.  

그래서 이번에는 익명 내부클래스의 사용을 최소화 할 수 있는 방법을 찾아봅니다.  

JDBC의 try/catch문에 적용했던 방법을 UserDao의 메소드에도 적용해보는 것입니다.  
콜백에서 변하는 부분은 SQL문장뿐입니다. 나머지는 변하지 않습니다.  

```java
public void deleteAll() ....{
    executeSql("delete from users");
}
// 분리
private void executeSql(final String query) throws...{
    // 변하는 쿼리문을 파라미터로 받아서 사용하게 만듭니다.
    this.jdbcContext.worWithStatementStrategy(
        new StatementStrategy(){
            ......
            return c.prepareStatement(query);
        }
    )
}
```

SQL을 담은 파라미터를 final로 선언해서 콜백안에서 사용 할 수있게 해주는것만 주의합니다.  

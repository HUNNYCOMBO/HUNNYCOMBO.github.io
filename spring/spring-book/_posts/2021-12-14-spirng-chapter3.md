---
title:  "토비의 스프링 vol.1 3장"
excerpt: "토비의 스프링3장 템플릿입니다."
tags: [템플릿]
header:
  teaser: /assets/images/spring/toby.png
  overlay_image: /assets/images/spring/toby.png
  overlay_filter: 0.4
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
  - 파라미터로 전달되지만 값을 참조하기 위한 것이 아닌 로직을 담은 메소드를 실행(작업 수행)시키기 위해 사용됩니다.(functional object)
  - 보통 단일 메소드 인터페이스(추상형 인터페이스)를 사용합니다.
  - 다른 오브젝트의 메소드에 전달되는 오브젝트를 말합니다.

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
// UserDao 클래스
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
한단계 더 나아가서, executeSql()은 UserDao만 사용하기는 아깝습니다.  
이렇게 재사용 가능한 콜백을 담고 있는 메소드라면, DAO가 공유할 수 있는 템플릿(workWithStatementStrategy메소드)의 클래스(JdbcContext) 안으로 옮겨도 좋습니다.  
메소드 접근자는 public으로 바꿔서 외부에서 바로 접근이 가능하게 합니다.

```java
public void deleteAll() thorws SQLException {
    this.jdbcContext.executeSql("delete from users");
    // 메소드를 템클릿 클래스로 옮김
    // excuteSQl메소드(클라이언트)가 파라미터로 템플릿을 호출하고,
    // 템플릿(workWith...)이 콜백을 호출하고 파라미터로 정보를 넘깁니다.
    // 콜백이 최종적으로 클라이언트에게 리턴합니다.
}
```

일반적으로 성격이 다른 코드들은 가능한 분리시키지만, 이 경우에는 응집력이 강한 코드들이기 떄문에 한 군데 모여있는게 유리합니다.  

#### 5-3. 템플릿/콜백의 응용 (이 문단은 흐름을 끊으므로 3장을 모두 읽은 후 보세요.)
스프링에는 다양한 자바 엔터프라이즈 기술에 사용할 수 있도록 미리 만들어 제공되는 수십가지 템플릿/콜백 클래스와 API가 있습니다.  
이 기능을 잘 사용하려면 직접 만들어서 사용할 줄도 알아야합니다. 원리도 모른채 기계적으로 사용하는 경우와 이해하고 사용하는 경우에는 큰 차이가 있습니다.  

고정된 작업 흐름을 갖고 있으면서 여기저기서 반복되는 코드가 있따면, 중복되는 코드를 분리할 방법을 생각해보는 습관을 기릅니다.
1. 중복된 코드를 먼저 메소드로 분리해봅니다.
2. 일부 작업을 필요에 따라 바꾸어 사용해야 한다면 인터페이스를 사이에 두고 분리해서 DI로 관리하도록 만듭니다.
3. 바뀌는 부분이 한 애플리케이션 안에서, 여러 종류가 동시에 만들어질 수 있다면, 템플릿/콜백 패턴을 적용하는 것을 고려합니다.


우리는 템플릿/콜백 패턴에 익숙해지도록 예제를 하나 만들어 보겠습니다.  
예제는 파일을 하나 열어서 모든 라인의 숫자를 더한 합을 돌려주는 코드입니다.  
다음과 같이 4개의 숫자를 담고 있는 numbers.txt파일을 하나 준비합니다.

```txt
1
2
3
4
```
모든 라인의 숫자 합은 10이고, numbers.txt 파일 경로를 주면 10을 돌려주도록 만들면 됩니다.  
그리고 연 파일은 잊지말고 try/catch 블록으로 닫아줍니다.
이를 아래와 같은 테스트로 만들 수 있습니다.

```java
public class CalcSumTest{
    @Test
    public void sumOfNumbers() thorws IOException{
        Calculator c = new Calculator();
        int sum = c.calcSum(getClass().getResource("numbers.txt").getPath());
        // 파라미터의 스트링으로 경로값을 받습니다.
        assertThat(sum,is(10));
        // 합이 10이면 통과
    }
}

//이하 Calculator 클래스 구현
public class Calculator{
    public Integer calcSum(String filepath) thorws IOException{
        BufferedReader br = null;

        try{
            br = new BufferdReader(new FileReader(filepath));
            // 한줄씩 읽기위해 bufferedreader로 파일을 가져옵니다.
            Integer sum = 0;
            String line = null
            while((line = br.readLine()) != null){
                // 한줄씩읽어들이며 읽을 값이 없을때 까지 반복합니다.
                sum += Integer.valueOf(line);
                // 스트링값을 integet타입으로 바꾸어 연산합니다.
            }

            br.close();
            //한 번 연 파일은 반드시 닫아줍니다.
            return sum;
        }catch(IOException e){
            throw e;
        }finally{
            if(br != null){ // 오브젝트 생성 전 예외가 발생할 수도 있으므로 체크해줍니다.
                try{br.close();}
                catch(IOException e){}
            }
        }
    }
}
```

만약 이번에는 모든 숫자의 곱을 계산하는 기능을 추가해야한다는 요구가 발생한다면,  
비슷한 기능이 새로 필요할 때마다 복사해서 사용할 수는 없습니다.  
템플릿/콜백 패턴을 적용해서 해결해봅시다. 먼저 템플릿에 담을 반복되는 작업(변하지 않는)이 어떤 것인지 살펴봅니다.  
**템플릿이 콜백에게 전달해줄 내분의 정보는 무엇이고, 콜백이 템플릿에게 돌려줄 내용은 무엇인지 생각해봅니다.**  

> 템플릿이 파일을 열고 각 라인을 읽는 br을 만들어서 콜백에게 전달하고, 콜백이 연산을 처리한 후 템플릿에게 돌려주게 합니다.

이것을 콜백 인터페이스의 메소드로 표현해봅시다.
```java
public interface BrCallback{
    Integer doMath(BufferedReader br) thorws IOException;
    // 콜백의 추상 메소드 입니다.
}
```

이제 템플릿 부분을 메소드로 분리해봅니다.  
콜백 인터페이스타입의 오브젝트를 받아서 실행하고 받은 결과를 클라이언트에게 돌려주게 합니다.  

```java
public class Calculator{
    public Integer fileReadTemplate(String filepath, BrCallback callback) thorws IOException{
        BufferedReader br = null;

        try{
            br = new BufferdReader(new FileReader(filepath));
            int ret = callback.doMath(br);
            // 콜백 오브젝트를 호출하는 부분입니다.
            // 템플릿에서 만든 컨텍스트 정보인 br을 전달해주고 콜백의 작업 결과를 받아둡니다.
            return ret;
        }catch(IOException e){
            throw e;
        }finally{
            if(br != null){ // 오브젝트 생성 전 예외가 발생할 수도 있으므로 체크해줍니다.
                try{br.close();}
                catch(IOException e){}
            }
        }
    }
}
```

이제 템플릿을 사용하도록 calcSum메소드를 수정해 보겠습니다. 템플릿으로 분리한 나머지 부분을 콜백 인터페이스 익명 내부 클래스에 담습니다.  

> 클라이언트가 calcsum()을 호출하면 반복되는 기능(br 생성, 닫기)을 분리한 템플릿을 호출하고, 템플릿에서 익명 내부 클래스로 만들어진 콜백에게 br을 전달해주고, 콜백이 작업을 처리하고 템플릿에게 건내며, 템플릿이 최종적으로 클라이언트에게 돌려줍니다.

```java
public class Calculator{
    public Integer calcSum(String filepath) thorws IOException{
        BrCallBack sumCallback = (br) -> {
            // 람다식을 이용하여 간략하게 표현했습니다.
            // sumcallback은 br을 이용하여 만들어진 콜백 익명 내부클래스(작업 처리 결과) 입니다.
            // !!! br은 템플릿이 호출했을 당시 콜백에게 넘겨주는 오브젝트입니다.
            Integer sum = 0;
            String line = null
            while((line = br.readLine()) != null){
                sum += Integer.valueOf(line);
                }
            return sum;
            };

        return fileReadTemplate(filepath, sumCallback);
        // 경로와 콜백을 템플릿에게 전달합니다.
        // 이 메소드의 return 값은 integer 입니다.
    }

    // 곱을 구하는 메소드
    public Integer calcMul(String filepath) thorws IOException{
        BrCallBack mulCallback = (br) -> {
            Integer mul = 1;
            String line = null
            while((line = br.readLine()) != null){
                mul *= Integer.valueOf(line);
                }
            return mul;
            };

        return fileReadTemplate(filepath, sumCallback);
    }
}
```

이제 테스트도 수정합니다. 테스트 메소드가 두개가 되고, 사용할 오브젝트와 파일 이름이 공유됩니다. @Befor를 이용하여 픽스처로 만들어둡니다.  

```java
public class CalcSumTest{
    Calculator c;
    String filepath;

    @Before
    public void setUp(){
        this.c = new Calculator();
        this.filepath = getClass().getResource("numbers.txt").getPath();
    }

    @Test
    public void sumOfNumbers() thorws IOException{
        assertThat(c.calcSum(this.filepath),is(10));
    }

    @Test
    public void mulOfNumbers() thorws IOException{
        assertThat(c.calcMul(this.filepath),is(24));
    }
```

이렇게 try/catch문이 로직에 없이 파일을 안전하기 처리하는 코드를 재사용 할 수 있게 됐습니다.  
그런데 우리는 calcSum()와 calcMul()에서 다시 반복되는 코드를 발견할 수 있습니다. 바로 while문 입니다.  
바뀌는 코드(콜백)는 반복문의 본문 입니다.(sum += , mul *=) 본문으로 전달한 정보는 처음에 선언한 변수 값이고, 리턴하는 것은 계산한 결과입니다.(변하지 않음, 템플릿)  
이를 새로운 콜백 인터페이스로 정의해봅니다.  

```java
public interface LineCallback{
    Integer doRead(String line, Integer value);
}

/// linecallback을 사용하는 템플릿
public class Calculator{
    public Integer lineReadTemplate(String filepath, LineCallback callback, int initVal) thorws IOException{
        // initval : 변수의 초기값
        BuffredRead br = null;
        try{
            br = new BuffereadReader(new FileReader(filepath));
            Integer res = initVal;
            String line = null;
            while((line = br.readLine()) != null){ //루프까지 템플릿이 맡습니다. 콜백을 여러번 호출합니다.
                res = callback.doRead(line,res);    //계산을 콜백이 맡습니다. 다음 라인에 사용하기위해 참조변수를 둡니다.
                }
            return res;
        }catch..... //br을 닫아주는 코드도 정의해 줍니다.
}
```

이제 fileReadTemplate()를 사용하는 메소드들을 lineReadTemplate()를 사용하도록 바꿔봅니다.  

```java
public class Calculator{
    public Integer calcSum(String filepath) thorws IOException{
        LineCallBack sumCallback = (line, value) -> {
            return value + Integer.valueOf(line);
            // value 는 템플릿에게 받은 누적된 계산 값입니다.
            };

        return lineReadTemplate(filepath, sumCallback, 0);
        // 템플릿을 호출하면 템플릿이 txt를 담은 br을 가져오고 한 줄씩 읽어들이며,
        // 계산된 값과 한 줄을 콜백에게 넘겨 끝날때 까지 작업을 수행하게 합니다.
    }

    // 곱을 구하는 메소드
    public Integer calcMul(String filepath) thorws IOException{
        LineCallBack mulCallback = (line, value) -> {
            return value * Integer.valueOf(line);
            // 연산이 달라졌습니다.
            };

        return fileReadTemplate(filepath, sumCallback, 1);
    }
}
```

이렇게 파일처리 코드가 템플릿으로 분리되고 순수한 계산 로직만남아 코드가 깔끔해졌습니다.  
Calculator 클래스와 메소드는 계산한다는 핵심 기능 코드만 갖고있습니다.  

여기서 더 강력한 템플릿/콜백 구조를 생각해봅시다. 만약 줄마다 있는 문자를 모두 연결해서 하나의 스트링으로 돌려주는 기능을 만든다면,  
템플릿이 리턴하는 타입이 스트링이어야 하고, 콜백의 결과도 스트링이어야하고, 호출하는 메소드도 스트링 타입이어야 합니다.  
하지만 지금은 Integer타입으로 고정되있습니다. 만약 결과 타입을 다양하게 가져가고싶다면 타입 파라미터라는 개념을 도입한  
**Generics(제네릭스)를 이용하면 됩니다. 제네릭스를 이용하면 다양한 오브젝트 타입을 지원하는 인터페이스나 메소드를 정의할 수 있습니다.**  

기존에 만들었던 Integer타입의 결과만 다루는 콜백과 템플릿을 확장해 보겠습니다.  
먼저, 콜백 메소드의 리턴 값과 파라미터 값의 타입을 제네릭 타입 파라미터 T로 선언합니다.  
그리고 템플릿 메소드에도 콜백의 타입 파라미터와 동일하게 결과 값 타입, initVal의 타입을 설정합니다.  

```java
public interface LineCallback<T>{
    // 타입 파라미터 T를 갖는 인터페이스
    T doRead(String line, T value);
    // T 타입 파라미터입니다.
}

// 템플릿
public class Calculator{
    public Integer lineReadTemplate(String filepath, LineCallback<T> callback, T initVal) thorws IOException{
        // initval : 변수의 초기값
        BuffredRead br = null;
        try{
            br = new BuffereadReader(new FileReader(filepath));
            T res = initVal;
            String line = null;
            while((line = br.readLine()) != null){
                res = callback.doRead(line,res);
                }
            return res;
        }catch.....
}
```

이제 콜백과 템플릿은 파일의 라인을 처리해서 T 타입의 결과를 만들어내는 범용적인 템플릿/콜백이 됐습니다.  
이제 파일의 모든 라인의 내용을 하나의 문자열로 연결하는 메소드를 추가해 봅니다. 추가적으로 테스트와 기존의 메소드도 변경합니다.  

```java
public Stirng concatenate(Stirng filepath) throws IOException{
    LineCallback<String> conCallback = (line, value) -> {
        return value + line;
    };

    return lineReadTemplate(filepath, conCallback, "");
    // conCallback템플릿 메소드의 T는 모두 스트링이 됩니다.
}

@Test
publci void conStrings() thorws IOException{
    asserThat(calculator.concatenate(this.filepath), is("1234"));
}

// calSum, Mul 메소드들은 다음과 같이 수정하면 그대로 사용가능 합니다.
LineCallback<Integer> sumCallback = () -> {};
```

이런 제네릭스 타입을 갖는 메소드나 콜백 인터페이스 등의 기법은 종종 사용되고 있습니다.  

### 6. 스프링의 JdbcTemplate
스프링이 제공하는 JDBC 코드용 기본 템플릿은 JdbcTemplate입니다. 우리가 만든 JdbcContext와 유사하지만 더 강한 기능을 갖고 있습니다.  
이제 코드를 JdbcTemplate으로 변경해봅니다. 생성자의 파라미터로 DataSource를 주입하면 됩니다.  

```java
public class UserDao{
    ...
    private JdbcTemplate jdbcTemplate;
    private DataSource dataSource;

    public void setDataSource(DataSource dataSource){
        this.jdbcTemplate = new JdbcTemplate(datasource);
        this.dataSource = dataSource;
        // 기존에는 jdbcContext 에 ds를 주입해 사용했었습니다.
    }
}
```

이제 템플릿을 사용할 준비가 됐습니다.  

#### 6-1. update()
deleteAll 메소드에 먼저 적용해봅니다. 
| | 인터페이스| 메소드| 콜백을 받아서 사용하는 템플릿 메소드|
|--|--|--|--|
|JdbcContext의 콜백 | StatementStrategy| makePreparedStatement()| executeSql()|
|JdbcTemplate의 콜백 | PreparedStatementCreator| createPreparedStatement()| update()|

다음과 같이 대응 합니다. 템플릿으로부터 Connection을 제공받아서 PreparedStatement를 만들어 돌려준다는 기능은 동일합니다.  

```java
public class UserDao {
	public void deleteAll() throws SQLException {
		this.jdbcTemplate.update("delete from users");
        // 이렇게 파라미터로 sql문장을 전달하면 미리 준비된 콜백을 만들어서 템플릿을 호출합니다.
        // 기존의 방식대로 update()의 파라미터로 PreparedStatementCreator의 추상 메소드를 이용하여 익명 내부 클래스를 사용하는 방법도 가능합니다.
    }
}
```

다음은 add() 입니다. 기존 add메소드는 SQL로 PreparedStatement를 만들고, 제공하는 파라미터를 순서대로 바인딩해서 사용했었습니다.  
JdbcTemlate에서 제공하는 메소드로 바꿔보면, 조금더 깔끔한 코드로 수정할 수 있습니다.
```java
// 기존의 add
PreparedStatement ps = c.prepareStatement("insert into users(id, name, password) values(?,?,?)");
ps.setString(1, user.getId());
ps.setString(2, user.getName());
ps.setString(3, user.getPassword());

// JdbcTemplate의 update 메소드
	this.jdbcTemplate.update("insert into users(id, name, password) values(?,?,?)",
						user.getId(), user.getName(), user.getPassword());
```

#### 6-2. queryForInt()
다음은 템플릿/콜백 방식을 적용하지 않았던 getCount()에 적용해 봅니다.  
getCount()는 쿼리를 실행하고 ResultSet을 통해 결과 값을 가져오는 코드입니다. 이때 사용할 콜백은 두가지 입니다.

- PreparedStatementCreator : 앞서 본 udate()의 용도와 같습니다. Connecton을 템플릿으로 부터 받아서 ps를 돌려줍니다.
- ResultSetExtractor : ps의 쿼리를 실행해서 얻은 ResultSet을 전달 받는 콜백입니다. ResultSet은 템플릿으로부터 받습니다. 추출 할 수 있는 타입은 다양하기에 제너릭스 타입 파라미터를 갖습니다.

템플릿은 이 두 콜백을 파라미터로 받는 query() 입니다.
```java
public int getCount() throws SQLException  {
		return this.jdbcTemplate.query(
            new PreparedStatementCreator(){ // 첫번째 파라미터
                public PreparedStatement createPreparedStatement(Connection con) thorws SQLException{
                    return con.preparedStatement("select count(*) from users");
                }
            }, new ResultSetExtractor<Integer>(){ // 두번쨰 파라미터, 제너릭으로 선언한 타입으로 query()의 리턴 타입도 바뀝니다.
                public Integer extractData(ResultSet rs) thorws SQLException, DataAccessException{
                    rs.next();
                    return rs.getInt(1);
                }
            }
        );
	}
```

익명 내부 클래스가 두번이나 등장해서 복잡해보입니다. JDbcTemplate은 **이런 기능을 가진 콜백을 내장**한 queryForInt()를 제공합니다.  
INteger 타입의 결과를 가져올 수 있는 SQL문장을 파라미터로 전달해주면 됩니다.

```java
public int getCount(){
    return this.jdbcTemplate.queryForInt("select count(*) from users");
}
```

#### 6-3. queryForObject()
이번에는 get()에 JdbcTemplate를 적용해 봅니다. get()은 getCount()처럼 단순한 값이 아니라  
복잡한 User 오브젝트를 ResultSet으로 만들어 프로퍼티에 넣어줘야 합니다.  
이를 위해, ResultSetExtractor 콜백 대신 RowMapper 콜백을 사용합니다.

> ResultSetExtractor vs RowMapper : 템플릿으로부터 ResultSet을 전달받고 결과를 리턴하는 것은 RSExtractor와 같으나, RSExtractor는 ResultSet을 한번만 전달받아 작업을 모두 진행하고 최종 결과만 리턴해주는데 반해, RomwMapper는 ResultSet의 로우 하나를 매핑하기 위해 사용돼 여러번 호출 될 수 있습니다.

get()의 SQL실행결과는 로우가 하나인 ResultSet입니다. ResultSet의 첫번째 로우에 RowMapper를 적용하도록 만듭니다.  
RomwMapper 콜백은 로우에 담긴 정보를 하나의 User 오브젝트에 매핑하게 합니다.  
사용할 템플릿은 queryForObject()입니다. 첫번째 파라미터는 ps를 만들기 위한 sql이고, 두번째는 바인딩할 값입니다.  

```java
public User get(String id){
    return this.jdbcTemplate.queryForObject("select * from users where id = ?", //첫번째 파라미터
        new Object[] {id},  // 두번째 파라미터. 바인딩 할 값입니다. 가변인자 대신 배열을 사용합니다.
        new RowMapper<User>() { // 세번째 파라미터. 로우를 User 오브젝트에 매핑합니다.
            public User mapRow(ResultSet rs, int rowNum) thorws SQLException{
                User user = new User();
                user.setId(rs.getString("id"));
                ...
                return user;
            }
        }
    );
}
```

> 가변인자 : 오버로딩(같은 메소드명으로 다른 파라미터를 갖는 것)으로 쓸 매개변수의 개수가 사용자의 쓰임에 따라 달라질 떄 오버로딩 대신 사용합니다. 대표적으로 printf()가 있습니다, 앞의 문자열을 뒤의 % 지시자로 값을 형식화 해주는 메소드인데, 뒤의 파라미터가 Object... args로 선언되어 있기에 뒤의 값의 수를 사용자가 마음대로 정할 수 있습니다. 파라미터를 컴파일러가 구분할 수 없으므로 오버로딩할 수 없습니다. 가변인자는 내부적으로 배열을 생성해서 사용합니다. 가변인자 외에 다른 매개변수가 더 있다면 가변인자는 마지막에만 선언할 수 있습니다.

두번째 파라미터는 뒤에 다른 파라미터가 있기 때문에 가변인자를 사용 할 수 없습니다. 대신 Object타입 배열을 사용합니다.  
이 배열 초기화 블록을 사용해서 첫번쨰 파라미터의 ?에 바인딩할 id값을 전달합니다.  
queryForObject()템플릿에서 이 두가지 파라미터를 사용하는 ps 콜백이 만들어집니다.  

기본적으로 queryForObeject()는 한 개의 로우를 얻을 것이라 기대하기 때문에, 내부적으로 rs.next()를 실행시켜서 첫 번째 로우로 이동시킨 후, rs를 전달해 RowMapper 콜백을 호출 합니다.  
그래서 rs.next를 호출할 필요가 없습니다. 그런데 기존의 예외처리 코드가 없습니다.  
queryForObject()는 받은 로우의 개수가 하나가 아니라면 예외를 던지도록 만들어 졌습니다.

#### 6-4. query()
현재 등록되어 있는 모든 사용자 정보를 가져오는 메소드를 만들어 봅니다.  
여러개의 User 오브젝트를 담기위해선 List<User>를 사용하면 됩니다.  
순서는 기본키인 id 순으로 정렬해서 가져오도록 합니다. 테스트를 먼저 만들어 봅니다.

```java
@RunWith(SpringJUnit4ClassRunner.class)
@ContextConfiguration(locations="/test-applicationContext.xml")
@DirtiesContext
public class UserDaoTest {
	@Autowired
	ApplicationContext context;
	
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
        // 테스트를 위한 픽스처
	}
    @Test
	public void getAll()  {
        // 테스트 메소드
		dao.deleteAll();
        // 테스트 전 비워두기
		
		dao.add(user1); // Id: gyumee
		List<User> users1 = dao.getAll();
        // List 타입으로 돌려받아야 합니다.
		assertThat(users1.size(), is(1));
        // 크기 확인
		checkSameUser(user1, users1.get(0));
        // 픽스처의 user1과 list에 첫번째로 담은 오브젝트를 비교합니다.
		
		dao.add(user2); // Id: leegw700
		List<User> users2 = dao.getAll();
		assertThat(users2.size(), is(2));
		checkSameUser(user1, users2.get(0));  
		checkSameUser(user2, users2.get(1));
		
		dao.add(user3); // Id: bumjin
		List<User> users3 = dao.getAll();
		assertThat(users3.size(), is(3));
        //id 순서대로 객체가 들어갔는지 확인하는 코드
        // id 순이므로 3, 1, 2 순이어야 합니다.
		checkSameUser(user3, users3.get(0));  
		checkSameUser(user1, users3.get(1));  
		checkSameUser(user2, users3.get(2));  
	}

	private void checkSameUser(User user1, User user2) {
        // 동일성이 아닌 동등성으로 비교합니다.
        // 반복되는 코드는 메스드로 분리합니다.
		assertThat(user1.getId(), is(user2.getId()));
		assertThat(user1.getName(), is(user2.getName()));
		assertThat(user1.getPassword(), is(user2.getPassword()));
	}
}
```

이제 테스트를 성공시키는 getAll()를 작성합니다. queryForObject()는 결과가 로우 하나일 때 사용하고, query()는 여러 개의 로우가 결과로 나오는 일반적인 경우에 사용합니다. 리턴 타입은 List<T> 입니다. 타입은 파라미터로 넘기는 RowMapper<T>로 결정됩니다.  

```java
public List<User> getAll(){
    return this.jdbcTemplate.query("select * from users order by id",
        new RowMapper<User>(){
            public User mapRow(ResultSet rs, int rowNum) throws SQLException{
                User user = new User();
                user.setId(rs.getString("id"));
                ...
                return user;
            }
        }
        );
}
```

queryForObject()와 마찬가지로 바인딩할 파라미터가 있다면, 두번째 파라미터에 추가할 수 있습니다. RowMapper는 여러번 호출 될 수 있으므로 여러 개의 로우를 가져옵니다.  

그런데 우리는 테스트에서 get()에서 id가 없을 때 어떻게 되는지처럼,
getAll()에서 네거티브 테스트를 진행하지 않았습니다. 바로, 결과가 하나도 없는 경우입니다.  
기본적으로 query()는 오류를 던지지않고 크기가 0인 List<>를 돌려줍니다.  
테스트 코드에서도 이를 그대로 반영하도록 합니다.

```java
dao.deleteAll();

List<User> user0 = dao.getAll();
assertThat(user0.size(), is(0))'
```

이미 0을 리턴하는데 검증 코드를 추가하는 이유는 UserDao를 사용하는 쪽의 입장에서 getAll()이 JdbcTempalte를 사용하는지 직접만든 코드를 사용하는지 모르기 떄문입니다.  
또 JdbcTemplate를 사용하더라도 getAll()가 다른 결과를 리턴하게 할 수도 있기 떄문입니다.  

#### 6-5. 재사용 가능한 콜백의 분리
이제 최종적으로 마무리 해봅니다.
1. DataSource 인스턴스 변수는 필요없어졌으므로 제거합니다. 모든 메소드가 JdbcTempalte를 생성하면서 DataSource를 DI를 받으니 직접 사용할 일이 없습니다.
2. RowMapper가 2번 중복되므로 분리합니다. 앞으로 다양한 조건으로 사용자를 조회하는 검색 기능이 추가될 것이므로 RomwMapper의 사용은 앞으로도 계속 될것입니다. 그러므로 분리해 재사용 가능하게 만듭니다. 먼저 매번 새로운 오브젝트를 만들어야 하는지 생각합니다. RowMapper 콜백 오브젝트에는 상태정보가 없으므로 하나만 만들어서 공유해도 됩니다.

```java
public class UserDao {
	public void setDataSource(DataSource dataSource) {
		this.jdbcTemplate = new JdbcTemplate(dataSource);
	}
	// datasource를 직접 사용하지 않으므로 지웁니다.
	private JdbcTemplate jdbcTemplate;
	
    // RowMapper 콜백 인터페이스를 분리, 재사용 코드로 만들었습니다.
	private RowMapper<User> userMapper = 
		new RowMapper<User>() {
				public User mapRow(ResultSet rs, int rowNum) throws SQLException {
				User user = new User();
				user.setId(rs.getString("id"));
				user.setName(rs.getString("name"));
				user.setPassword(rs.getString("password"));
				return user;
			}
		};

	
	public void add(final User user) {
		this.jdbcTemplate.update("insert into users(id, name, password) values(?,?,?)",
						user.getId(), user.getName(), user.getPassword());
	}

	public User get(String id) {
		return this.jdbcTemplate.queryForObject("select * from users where id = ?",
				new Object[] {id}, this.userMapper);
                // 인스턴스 변수를 사용하도록 변경합니다.
	} 

	public void deleteAll() {
		this.jdbcTemplate.update("delete from users");
	}

	public int getCount() {
		return this.jdbcTemplate.queryForInt("select count(*) from users");
	}

	public List<User> getAll() {
		return this.jdbcTemplate.query("select * from users order by id",this.userMapper);
	}

}
```

다음과 같이 UserDao가 정리되었습니다.
- UserDao에는 User정보를 DB와 상호작용하는 로직만 담겨있습니다. 높은 응집도
  - User 오브젝트와 User 테이블 사이에 어떻게 무엇을 주고받을지에 대한 정보
- JDBC API를 사용하는 방식, 예외철, 리소스의 반납, DB연결을 어떻게 가져올지는 JdbcTempalte에 달려있습니다. 변경이 일어나도 UserDao에 변경을 주지않습니다. 낮은 결합도
  - 하지만 특정 템플릿/콜백에서는 템플릿을 직접 이용하므로 강한 결합도를 갖습니다.
  - JdbcOperations 인터페이스를 통해 JdbcTemplate을 DI받아 사용하면 결합도를 낮춥니다.
  
조금 더 개선할 수 있는 부분을 생각해봅니다.
1. userMapper가 한 번 만들어지면 변경되지 않는 프로퍼티 성격을 띠고 있으니, 인스턴스 변수가 아니라 UserDao빈의 DI용 프로퍼티로 만들 수 있습니다. UserMapper를 독립된 빈으로 등록하고 XML설정에 User테이블의 필드명과 User오브젝트의 매핑정보를 담을 수 있습니다. 이렇게 분리하면 필드명이 변하거나 매핑 방식이 바뀌는 경우에 UserDao 코드를 수정하지 않아도 됩니다.
2. UserDao의 메소드에서 사용하는 SQL문장을 UserDao코드가 아니라 외부 리소스에서 읽어와 사용하게 하는 것입니다. 이렇게하면 SQL문을 UserDao코드와 분리할 수 있습니다.

### 7. 정리
3장에서는 아래와 같은 내용을 공부했습니다.
- 예외가 발생할 수 있는 공유 리소스의 반환 코드는 반드시 try/catch 블록 처리 합니다.
- 바뀌지 않는 부분은 context로, 바뀌는 부분은 전략으로 만들고 인터페이스를 통해 전략을 변경할 수 있도록 구성합니다.
- 같은 애플리케이션 안에서 여러 종류의 전략을 구성해서 사용해야 한다면 컨텍스트를 이용하는 클라이언트 메소드에서 직접 전략을 정의하고 제공합니다.
- 클라이언트 메소드안에 익명 내부 클래스를 사용해서 코드를 간결하게 합니다.
- 컨텍스트가 하나 이상의 클라이언트 오브젝트에서 사용된다면 클래스를 분리해서 공유하도록 합니다.
- 컨텍스트는 별도의 빈으로 등록해서 DI받거나 클라이언트 클래스에서 직접 생성해서 사용합니다.
- 단일 전략 메소드를 가지면서 익명 내부클래스로 매번 새로 만들어 사용하고, 컨텍스트 호출과 동시에 전략DI를 수행하는 방식을 템플릿/콜백 패턴이라고 합니다.
- 콜백의 코드에서도 코드가 반복된다면 콜백을 템플릿에 넣고 재활용 합니다.
- 타입이 다양하게 바뀔 수 있다면 제너릭스를 이용합니다.
- JdbcTemplate
- 템플릿은 한 번에 하나 이상의 콜백을 사용할 수도있고, 여러번 호출할 수도 있습니다.
- 템플릿과 콜백 사이에 주고받는 정보에 관심을 둬야합니다.
- 
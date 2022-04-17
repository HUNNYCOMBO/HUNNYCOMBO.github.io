---
layout: single
title:  "토비의 스프링 vol.1 4장"
categories: spring
tags: [spring, 예외]
toc: true
toc_sticky : true
author_profile: false
sidebar:
    nav: "docs"
search: true
---

## 예외

### 1. 사라진 SQLException
JdbcTemplate로 변경하면서 얼렁뚱땅 넘어간 것이 있습니다. 바로 dao메소드 옆에 예외처리하는 throws 코드가 사라진 것입니다. 왜 사라졌는지 알아보기 전에 초난감 예외처리들을 살펴봅니다.  

#### 1-1. 초난감 예외처리
1. catch(SQLException e){}

아무 조치를 하지 않고 넘어가는 것은 위험합니다. 오류의 원인이 무엇인지 찾아내기가 매우 힘들기 떄문입니다.

2. catch(e){System.out.println(e); 혹은 e.printStackTrace()};

예외를 화면에 출력해주지만 서버 운영시 콘솔 로그를 계속 모니터링 하지 않는 한 발견하기 쉽지 않습니다. 또한 출력하는게 조치를 취한 것은 아닙니다. 차라리 System.exit(1); 처럼 다음 코드로 넘어가지 않게 하는것이 낫습니다.(이렇게 쓰면 당연 안됩니다.)
**모든 예외처리는 복구되던지 작업을 중단시키고 개발자에게 통보되어야 합니다.**
조치를 취할 방법이 없다면 thorws를 이용해 호출한 곳으로 책임을 전가합니다.

4. 무의미하고 무책임한 thorws 처리

단순히 귀찮아서 throws로 던져버리는 경우에도, 조치를 취할 수 있음에도 그 기회를 박탈당하게 됩니다. 조치를 취할게 없는 경우에만 사용합니다.

#### 1-2. 예외의 종류와 특징
자바에서 throw를 통해 발생시킬 수 있는 예외는 크게 세가지가 있습니다.

1. Error

java.lang.Error 클래스의 서브클래스들 입니다. 주로 JVM이 발생시키는 것이고 코드에서 잡으려 하면 안됩니다. 애플리케이션에서는 이런 에러에 대한 처리는 신경쓰지 않아도 됩니다.

2. Exception과 체크 예외

java.lang.Exception 클래스와 그 서브클래스로 정의되는 예외들은 코드의 작업 중에 예외상황에서 사용됩니다. Exception 클래스는 다시 체크 예외와 언체크 예외(unchecked)로 구분됩니다.  
체크 예외는 RuntimeException을 상속 하지 않은 것들이고, 언체크 예외는 상속한 클래스들을 말합니다. 일반적으로 예외라고 하면 체크 예외라고 생각하면 됩니다.  
체크 예외는 반드시 catch문이나 throws를 이용해야 합니다.

3. RuntimeExceptio과 언체크 예외

java.lang.RuntimeException 클래스(Exception의 서브클래스 중 하나)를 상속한 예외들은 명시적인 예외처리를 하지 않습니다.  
주로 개발자 부주의로 인한 예외, NullPinter나 IllegalArumentException 등이 있습니다. 예상 가능한 예외이기 떄문에 별도로 catch나 throws를 하지 않아도 됩니다.

#### 1-3. 예외처리 방법
1. 예외복구

예외상황을 파악하고 해결해서 정상 상태로 돌려놓는 것입니다. 예를 들어 사용자가 요청한 파일을 읽으려고 시도했는데 파일이 없다거나 파일에 문제가 있다면 사용자에게 상황을 알려주고 다른 파일을 이용하도록 안내하는 것입니다.  
또 다른 예로, 네트워크가 불안해서 원격 DB 서버에 접속하다 실패해서 SQLException이 발생하는 경우 재시도를 해볼 수있습니다. 물론 정해진 횟수만큼 재시도해서 실패했다면 예외 복구는 포기해야 합니다. 아래의 예제를 참고합니다.  
예외처리를 강제하는 체크 예외는 이렇게 복구할 가능성이 있는 경우에 사용합니다.

```java
int maxretry = MAX_RETRY;
while(maxretry -- >0){
    try{
        // 예외가 발생할 가능성이 있는 시도
        return; //작업 성공
    }
    catch(){
        // 로그출력. 정해진 시간만큼 대기
    }
    finally{
        // 리소스 반납. 정리 작업
    }
}
throw new RetryFailedException();
// 최대 재시도 횟수를 넘기면 직접 예외 발생
```

2. 예외처리 회피(Throws)
예외처리를 자신이 담당하지 않고 자신을 호출한 쪽으로 던져버리는 것입니다.  
빈 catch블록으로 예외가 발생하지 않은 것처럼 만드는 경우는 회피한 것이 아닙니다. 콜백 오브젝트의 메소드는 모두 throws SQLException이 붙어있습니다.  
SQL예외를 처리하는 일은 콜백 오브젝트의 역할이 아니라고 보기 떄문입니다.(템플릿에게 처리하도록 던집니다.) 예외를 회피하는 것은 예외를 복구하는 것처럼 의도가 분명해야합니다.  
콜백/템플릿처럼 긴말한 관계가 있는 다른 오브젝트에게 던지거나, 자신을 사용하는 쪽에서 예외를 다루는게 최선이라는 분명한 확신이 있어야합니다.  

3. 예외 전환
   
예외 회피와 달리, 적절한 예외로 전환해서 던진다는 특징이 있습니다. 보통 두가지 목적으로 사용됩니다.
- API가 발생하는 기술적인 로우레벨을 상황에 적합한 의미를 가진 예외로 변경(의미없는 예외를 의미있는 예외로 변경)
  - 예를 들어, 아이디가 같은 사용자가 있어 등록하는데 DB에러가 발생하면 JDBC API는 SQL예외를 발생시킵니다. 이경우 add()가 SQLException을 그대로 밖으로 던져버리면, 서비스 계층에서는 왜 SQL예외가 발생했는지 알 수 없습니다. 이럴 땐 DAO에서 SQL예외를 해석해서 DuplicateUserIdException같은 예외로 바꿔 던져줍니다.

```java
public void add(User user)throws DuplicateUserIdException, SQLException {
    // 중첩 예외
    try{
        ...
    }
    catch{
        if(e.getErrorCode() == MysqlErrorNumbers.ER_DPU_ENTRY)
            throw DupliateUserIdException(e);
            // Mysql의 "Duplicate Entry(1062)"에러면 예외 전환
        else
            throw e;
    }
    }
}
```

- 예외처리를 강제하는 체크 예외를 언체크 예외로 바꾸는 경우
  - 어차피 **복구가능한 예외가 아닐경우** 런타임 예외로 포장해서 던지는 편이 낫습니다., 대표적으로 EJBException을 들 수 있습니다.

```java
try{
    OrderHome oh = EJBHomeFactory.getInstance().etOrderHome();
    Oder oder = oh.findByPrimaryKey(Integer id);
}
catch(NamingException ne){throw new EJBException(ne);}
```

물론 반대로 API가 던지는 예외가 아니라 코드에서 던지는 예외는 체크 예외를 사용해야 합니다.  

### 1-4. 예외처리 전략
자바의 환경이 서버로 이동하면서 표준 스펙에서는 API가 발생시키는 예외를 언체크 예외로 정의하는 것이 일반화되고 있습니다.  
독립형 애플리케이션돠 달리 서버의 특정 계층에서 예외가 발생했을 떄 작업을 중지하고 예외상황을 복구할 수 있는 방법이 없기 때문입니다.  
항상 복구할 수 있는 예외가 아니라면 일단 언체크 예외로 만듭니다.
우리가 만든 add()의 DuplicatedUserIdExc...는 굳이 체크 예외로 둘 필요가 없습니다. 어디에서든 Duplicated..를 잡아서 처리할 수 있다면, 런타임 예외로 만드는 게 낫습니다.  
Duplicated...처럼 의미있는 예외는 복구 가능한 예외이므로 필요하면 언제든 잡아서 처리할 수 있도록 별도의 예외로 정의하기는 하지만, 필요 없다면 신경 쓰지 않도록 런타임 예외로 만듭니다.  
반면 SQLException은 대부분 복구 불가능한 예외이므로 그냥 런타임 예외로 포장해 던집니다.

```java
public class DuplicatedUserIdException extends RuntimeException{
    public DuplicatedUserIdExeption(Throwable cause){
        // 생성자로 중첩 예외를 만들 수 있도록 해줍니다.
        super(cause);
    }
}

// add메소드 수정
public void add(User user)throws DuplicateUserIdException {
    // throws를 선언할 필요없지만 add()를 사용하는 쪽에서 예외를 처리하고 싶은 경우 활용할 수 있음을
    // 알려주도록 thorws 선언에 포함시킵니다.
    try{
        ...
    }
    catch{
        if(e.getErrorCode() == MysqlErrorNumbers.ER_DPU_ENTRY)
            throw new DupliateUserIdException(e);
            // Mysql의 "Duplicate Entry(1062)"에러면 예외 전환
        else
            throw new RuntimeException(e);
            // 예외 포장(기존 sql예외)
    }
    }
}
```

이렇게 런타임 예외를 일반화시키면 예외처리를 강제하지 않으므로 주의를 기울일 필요가 없습니다. 런타임 예외를 사용하는 경우에는 API문서를 통해  
메소드를 사용할 때 발생할 수 있는 예외의 종류와 원인, 활용 방법을 자세히 설명해둬야합니다.  

이런 예외들 외에 코드로 고의적으로 발생시키는 예외를 애플리케이션 예외라고 합니다. 예를 들면, 계좌에서 잔고보다 많은 돈을 출금하려 했을 떄 작업을 중단시키고 경고를 보내야합니다.  
이런 메소드를 설계하는 방법은 두가지 있습니다.

1. 성공했을 때와 한도를 초과한 경우 각각 다른 종류의 리턴 값을 돌려줍니다. 시스템 오류가 아니므로 두가지 경우 모두 정상흐름이지만 리턴값으로 고의적으로 오류를 발생시키는 것입니다. 하지만 if블록이 범벅된 코드가 이어질지 모르는 단점이 존재합니다.
2. 정상적인 흐름을 따르는 코드는 그대로 두고, 잔고 부족과 같은 예외상황에서 비지니스적 의미를 띈 예외를 던지도록 만듭니다. 정상적인 흐름을 따르지만 예외가 발생할 수 있는 코드를 try/catch 블록으로 처리 할 수 있어서 보기에도 편합니다. 이때 사용하는 예외는 예외상황에 대한 로직 구현을 강제하도록 의도적으로 체크 예외로 만듭니다.

```java
try{// 정상적인 처리 결과를 출력하도록 진행
}
catch(의도적예외클래스 e){// 예외에 담긴 잔고 정보를 가져오고 잔고부족시 안내 메세지를 출력
}
```

#### 1-5. SQLException은 어떻게 됐나?
대부분의 SQLException은 복구가 불가능하고 다룰 수 있는 가능성도 없습니다. 따라서 throws로 방치하지 말고 언체크 예외로 전환해 줘야 합니다.  
JdbcTemplate은 이 예외처리 전략을 따르고있습니다. 템플릿과 콜백 안에서 발생하는 SQL예외를 런타임 예외인 DataAccessException으로 포장해서 던져줍니다.  
그래서 DAO메소드에서 SQLException이 모두 사라진 것입니다. 필요한 경우에만 런타임 예외를 잡아서 처리하면 됩니다.  

### 2. 예외전환
DataAccessException은 SQL예외에서 다루기 힘든 예외정보를 의미있는 예외로 전환해서 추상화해주려는 용도로 쓰이기도 합니다.  

#### 2-1. JDBC의 한계
JDBC는 가장 많이 사용되는 API중 하나지만 DB를 자유롭게 변경해서 사용할 수 있는 유연한 코드를 보장해 주지는 못합니다.  
첫째 문제는 SQL입니다. 대용량 데이터를 처리하는 SQL의 경우 대부분 비표준 SQL문장이 만들어집니다. 이는 결국 특정 DB에 종속적인 코드가 됩니다. 
이를 위해서는 DB별로 별도의 DAO를 만들거나 SQL을 외부에 독립시켜서 DB에 따라 변경해 사용하게 합니다.  
두 번쨰 문제는 SQL예외 입니다. DB마다 에러의 종류와 원인이 다르기 떄문입니다. 그래서 SQLException의 getErrorCode()로 가져올 수 있는 에러코드도 DB별로 다릅니다.  
그래서 SQLException은 예외가 발생했을 떄의 DB상태를 담은 DB에 독립적인 SQL 상태정보를 부가적으로 제공합니다. 이 부가정보는 Open Group의 XOPEN SQL 스펙에 정의된 상태코드를 따릅니다.  
문제는 JDBC드라이버에서 SQLException을 담을 상태코드를 정확하게 만들어주지 않아 사용할 수 없습니다.  

#### 2-2. DB 에러 코드 매핑을 통한 전환
대신 스프링은 DB별 에러 코드의 종류를 분류해서 스프링이 정의한 예외 클래스와 매핑해놓은 에러 코드 매핑정보 테이블을 만들어두고 이용합니다.

```java
<bean id="Oracle" class="org.spring...">
    <property name="badSqlGrammarCodes">    //예외 클래스 종류
        <value>900,903,904,917,936,942,17006 </value>
        // 매핑되는 DB 에러코드
```

JdbcTempalate은 SQLException을 단지 런타임 예외로 포장하는 것이 아니라 DB의 에러 코드를 런타임 에러 계층 구조의 클래스 중 하나로 매핑해줍니다.  
JdbcTempalate에서 던지는 예외는 모두 DataAcceseeException의 서브클래스 타입입니다. 중복 키 에러를 분류해서 예외처리를 했던 add메소드를 JdbcTemplate을 이용하게 바꾸면,  
아래와 같이 간단해집니다.

```java
public void add() throws DuplicateKeyException{
    // DataAccessException의 계층구조(상속) 클래스로 포장하기 떄문에 예외 포장을 위한 코드가 따로 필요 없습니다.
    // add메소드를 호출하는 쪽에서 필요에따라 대응하도록 메소드 선언에 넣어줍니다.
    // JdbcTemplate안에서 DB별로 미리 준비된 에러 코드와 비교해서 적절한 예외를 던져줍니다.
}
```

이제 왜 이렇게 계층구조를 이용해 기술에 독립적인 예외를 사용하게 하는지 생각해봅니다.

#### 2-3. DAO 인터페이스와 DataAccessException의 계층 구조
DataAccessException은 SQLException을 전환하는 용도 뿐만 아니라 JDBC 외의 DA 기술(ORM, iBatis, JPA, JDO, 하이버네이트 등)에서 발생하는 예외에도 적용됩니다.  
DataAccessException은 의마가 같은 예외라면 데이터 억세스 기술의 종류와 상관없이 일관된 예외가 발생하도록 만들어줍니다.  

우리는 DAO의 코드를 DAO를 사용하는 클라이언트로 부터 감추어ㅆ지만, 메소드 선언에 나타나는 예외정보가 문제가 될 수 있습니다.

```java
public interface UserDao{
    public void add(User user);
    // 완전히 기술에 독립적인 인터페이스인 이 메소드 선언은 사용할 수 없습니다. JDBC가 예외를 던지기 떄문입니다.
    public void add(User user) throws SQLException;
    // 따라서 이렇게 선언하게 됩니다. 문제는 DA기술이 던지는 예외가 일치하지 않아 독자적인 예외를 던지게 됩니다.
}
```

다행히도 JDBC 이후에 등장한 DA 기술은 런타임 예외를 사용하고, SQLException을 던지는 JDBC API을 사용하는 DAO가 남았는데, 이 경우에는 앞의 내용과 같이 DAO 메소드 내에서 런타임 예외로 포장해서 던져주면 됩니다.  
이제 throws 없이 DAO에서 사용하는 기술에 완전히 독립적인 인터페이스 선언이 가능해졌습니다. 하지만 아직 불충분합니다. 중복 키 에러처럼 의미있게 처리할수 있는 예외도 있고,  
시스템 레벨에서 DA 예외를 의미 있게 분리할 필요도 있습니다. 문제는 DA 기술이 달라지면 같은 상황이어도 다른 종류의 예외가 던져진다는 것입니다.(JDBC면 SQLException이, JPA면 PERsistenceException이....)  
따라서 클라이언트 입장에서는 DA기술에 따라서 예외 처리방법이 달라지게 됩니다. 단지 인터페이스로 추상화하고, 런타임 예외로 전환하는것만으로는 의미가 없습니다.  

그렇기 때문에 스프링은 다양한 DA기술을 사용할 떄 발상하는 예외들을 추상화해서 DataAccessException 계층구조 안에 정리해 놓았습니다.  
각각의 DA기술이 보낸 에러 코드를 DB별로 매핑해서 그에 해당하는 의미 있는 DataAccessExcetion의 서브클래스 중 하나로 전환해서 던져줍니다.  
심지어 JDBC 예외가 아닌 템플릿 메소드나 DAO 메소드에서도 활용할 수 있는 예외가 정의되어 있습니다.  
직접 구현하고 싶다면 서브클래스를 상속해서 직접 정의해 사용할 수도 있습니다.  
결국 인터페이스, 런타임 예외, DataAccessException 예외 추상화를 적용하면 DA 기술과 구현 방법에 독립적인 이상적인 DAO를 만들 수가 있습니다.  

#### 2-4. 기술에 독립적인 UserDao 만들기
지금까지 만들어온 UserDao클래스를 인터페이스와 구현 클래스로 분리합니다.

```java
pulbic interface UserDao{
    void add(User user);
    User get(String id);
    List<User> getAll();
    ...

    // 수정자 메소드를 인터페이스에 추가하지 않습니다.
    // 구현 방법에 따라 변경될 수 있는 메소드이고, 클라이언트가 알고 있을 필요도 없기 때문입니다.
}

public class UserDaoJdbc implements UserDao{
    ....
    // xml 파일도 변경합니다. 클래스만 변경합니다. 보통 bean id는 구현 인터페이스 이름을 따르기 떄문입니다.
}
```

테스트에서는 DAO의 기능에 관심이있다면 그대로 사용하도록 하고, 특정 DA기술을 사용한 구현 내용에 관심이 있다면 DI받을때 구현 클래스를 사용합니다.  
이제 UserDaoTest에서 중복된 키를 가진 정보를 등록했을 떄 어떤 예외가 발생하는지를 확인하기 위한 테스트를 추가합니다.

```java
@Test(expected=DataAccessException.class)
// 중복 예외는 DataAccessException 예외 중 하나를 던져야 합니다. 예외가 발생하면 성공하는 expected를 이용합니다.
// expected없이 테스트하면 DuplicatedKeyException이 발생하는 것을 확인할 수 있습니다.
public void duplicatedKey(){
    dao.deleteAll();
    
    dao.add(user1);
    dao.add(user1);
}
```

우리는 DA기술에 상관없이 키중복 상황에서 동일한 예외가 발생하리라 기대하지만, 아쉽게도 DuplicatedKeyException은 아직까지 JDBC를 이용하는 경우에만 발생합니다.  
이처럼 DataAccessException의 기술이 완벽하다고 기대할 수는 없습니다. 이를 해결하려면 결국 직접 예의를 정의해두고 각각 메소드에서 좀 더 상세한 예외 전환을 해줘야합니다.  
대부분의 중첩된 예외로 SQLException이 전달되기 떄문에 이를 다시 스프링의 "JDBC 예외 전환 클래스"의 DataAccessException으로의 전환하는 도움을 받아서 처리할 수 있습니다.  
바로 SQLErrorCodeSQLExceptionTranslator 입니다. 에러 코드 변환에 필요한 DB종류를 알아내기 위해 현재 DataSource를 필요로 합니다.  

```java
public class UserDaoTest{
    @Autowired UserDao dao;
    @Autowired DataSource dataSource;
    ....

    // 픽스처 등
    
    @Test
    public void sqlExceptionTranslate(){
        dao.deleteAll();

        try{
            dao.add(user1);
            dao.add(user1);
        }
        catch(DuplicateKeyException ex){
            SQLException se = (SQLException)ex.getRootCause();
            // DuplicateKeyException은 JDBC API에서 처음 발생한 SQLException을 내부에 갖고 있습니다.
            //getRootCause()를 이용해 SQLException을 가져옵니다.
            SQLExceptionTranslator set = new SQLErrorCodeSQLExceptiontranslator(this.dataSource);
            // DI받은 datasource를 참고해 SQLException 변환

            assertThat(set.translate(null,null,se),is(DuplicateKeyException.class));
            // 변환기인 set에 추출한 sqlexception인 se를 파라미터로 넣고 translae()를 이용헤 DataAccessException의 타입으로 변환합니다.
            // 스프링 예외전환 API를 사용해서 DuplicateKeyException이 만들어 졌는가를 검증합니다.
            // equals() 비교 대신 is()로 비교하면 파라미터 클래스의 인스턴스 인지 검사합니다.
            // null 파라미터는 에러 메시지를 만들떄 사용하는 정보이므로 null로 넣어뒀습니다.
        }
    }
}
```

### 3. 정리
- 에외의 조취를 취하지 않거나 의미 없는 throws 는 위험합니다.
- 예외는 복구하거나 의도적으로 전달하거나 적절한 예외로 전환해야 합니다.
- 런타임 예외로 포장하거나 좀 더 의미 있는 예외로 변경시키는 예외 전환이있습니다.
- 복구할 수 없는 예외는 런타임 예외로 전환합니다.
- 로직을 담기 위한 예외는 체크 예외로 만듭니다.
- SQLExcpetion의 에러코드는 DB에 독립적인 예외로 전환될 필요가 있습니다.
- DataAccessException을 통해 추상한 런타임 예외 계층을 제공 받습니다.
- DAO를 데이터 억세스 기술에서 독립시키려면 인터페이스 도입, 런타임 예외 전환, 기술에 독립적인 추상화된 예외로 전환이 필요합니다.
---
layout: single
title:  "토비의 스프링 vol.1 4장"
categories: spring
tags: [spring, 예외]
toc: true
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
try{// 정상적인 처리 결과를 출력하도록 진행}
catch(의도적예외클래스 e){// 예외에 담긴 잔고 정보를 가져오고 잔고부족시 안내 메세지를 출력}
```

#### 1-5. SQLException은 어떻게 됐나?
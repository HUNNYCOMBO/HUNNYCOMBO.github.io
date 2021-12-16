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

2. 예외처리 회피


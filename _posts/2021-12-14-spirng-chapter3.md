

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

2. 템플릿 메소드 패턴(상속)  
상속을 통해 변하지 않는 부분은 슈퍼클래스에 두고, 변하는 부분은 추상 메소드로 정의해둬서  
서브클래스에서 오버라이딩하여 사용하는 방식입니다.  
이 방식은 접근에 제한이 많아 DAO로직마다 새로운 서브클래스를 만들어야하는 문제가 있습니다.  
또한, 이미 설계시점에서 확장구조가 고정되어 버립니다.  

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

4. DI 적용을 위한 클라이언트/컨텍스트 분리  
결국 우리는 UserDao 때처럼,  
컨텍스트(UserDao)
가 필요로 하는 전략(ConnectionMaker)의 특정 구현 클래스(DConnectionMaker)의 오브젝트를  
클라이언트(UserDaoTest)가 만들어서 제공해주는 방법을 똑같이 적용해야합니다.  

### 3. JDBC 전략 패턴의 최적화

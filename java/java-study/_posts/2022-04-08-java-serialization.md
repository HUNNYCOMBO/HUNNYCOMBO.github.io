---
title:  "자바의 직렬화 - serialization/deserialization"
tags: [직렬화]
excerpt: "객체를 데이터화 하는 직렬화에 대해 알아봅니다."
header:
  teaser: /assets/images/java/serialization.png
---

## 참고링크
+ [sa1341](https://velog.io/@sa1341/Java-%EC%A7%81%EB%A0%AC%ED%99%94%EB%A5%BC-%ED%95%98%EB%8A%94-%EC%9D%B4%EC%9C%A0%EA%B0%80-%EB%AC%B4%EC%97%87%EC%9D%BC%EA%B9%8C)

## 1. java 직렬화(Serialization)란?
직렬화는 자바 시스템 내부(JVM의 Heap, Stack영역)에서 사용되는 데이터(객체 등)들을 외부의 시스템에서도 사용할 수 있도록 byte형태의 데이터로 변환하는 기술입니다.  
변환된 데이터를 다시 객체로 변환하는 역직렬화를 포함합니다.  
역직렬화를 할 때는 예외가 생길 수 있다는 사실을 인지하고 반드시 예외 처리를 해야합니다.  
저장되는 특징이 있으므로 자주 변경되는 데이터를 직렬화 하지 않습니다.  


## 2. 직렬화를 어디에 적용할까?
JVM의 메모리에만 상주되어 있는 객체 데이터를 그대로 영속화(persist, 영구히 저장)할 때 사용됩니다. 시스템이 종료되더라도 없어지지 않는 장점을 가집니다.  
그리고 필요할 때 직렬화 된 데이터를 가져와 역직렬화 하여 객체를 바로 사용할 수 있게 됩니다.  

- session : 서블릿 세션들은 대부분 java직렬화를 지원하고 있습니다. 단순히 세션을 서블릿 메모리 위에서만 운용한다면 직렬화가 필요없지만, 파일로 저장하거나 DB를 저장하는 옵션 등을 선택하면 세션 자체가 직렬화 되어 저장되어 전달됩니다.
- cache : 캐시에서도 직렬화는 사용됩니다. 실시간으로 요구하는 데이터가 아니라면 메모리, 외부 저장소, 파일 등을 이용해서 데이터 객체를 저장한 후 동일한 요청이 오면 DB를 다시 요청하는 것이 아니라 직렬화 되어 저장된 객체를 찾아서 응답하는 형태를 캐시를 사용한다고 합니다. 캐시를 이용하면 DB리소스를 절약할 수 있기 때문에 많은 시스템에서 자주 활용됩니다. 
- 자바 RMI : 원격 시스템 간의 메시지 교환을 위해서 사용하는 자바에서 지원하는 기술입니다.

## 3. 직렬화의 종류
문자열 형태의 직렬화 방법으로 직접 데이터를 문자열 형태로 확인 가능한 직렬화 방법입니다. 범용적인 API나 데이터를 변환하여 추출할 때 많이 사용됩니다. 최근에는 SON을 많이 사용하고 있습니다.  

## 4. java 직렬화 예제
java.io.Serializable 인터페이스를 상속받아 직렬화 될 수 있는 조건을 갖춥니다.  

```java
import java.io.Serializable;

public class Member implements Serializable {

    private String name;
    private String email;
    private int age;

    public Member(String name, String email, int age) {
        this.name = name;
        this.email = email;
        this.age = age;
    }

    @Override
    public String toString() {
        return String.format("Member{name='%s', email='%s', age='%s',", name, email, age);
    }
}
```

직렬화를 위해 ObjectOutputStream 를 사용하여 진행합니다.  

```java
import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.util.Base64;

public class ObjectSerializableExam{

    public static void main(String[] args) throws Exception {
        Member member = new Member("hunny", "hunny@gmail.com", 93);
        byte[] serializedMember;
        // byte 버퍼역할

        /*
        직렬화
        */
        try(ByteArrayOutputStream baos = new ByteArrayOutputStream()) {
            try(ObjectOutputStream oos = new ObjectOutputStream(baos)) {
                oos.writeObject(member);
                // 직렬화된 member 객체
                serializedMember = baos.toByteArray();
            }
        }
        // base64로 인코딩한 문자열
        String base64Member = Base64.getEncoder().encodeToString(serializedMember);

```

역직렬화에는 조건이 필요합니다.  
- 직렬화 된 객체의 클래스가 class path에 존재하고 import 되어있어야 합니다.
- 직렬화와 역직렬화를 진행하는 시스템이 서로 다를 수 있습니다.
- java 직렬화 대상 객체는 동일한 serialVersionUID를 갖고 있어야 합니다.(후술)

```java
        /*
        역직렬화
        */
          // base64로 디코딩한 문자열
        byte[] deserializedMember = Base64.getDecoder().decode(base64Member);
        
        try(ByteArrayInputStream bais = new ByteArrayInputStream(deserializedMember)) {
            try(ObjectInputStream ois = new ObjectInputStream(bais)) {
                Object objectMember = ois.readObject();
                // member 객체로 역직렬화
                Member readMember = (Member) objectMember;
                System.out.println(member);
            }
        }
    }
}
```

## 5. serialVersionUID
serialVersionUID는 java 직렬화에 필요한 버전 정보입니다. 만약 객체를 직렬화하고 변경된다면(맴버변수 추가, 타입변경 등) 역직렬화 시에 InvalidClassException 예외가 발생합니다.  
변경에 취약한 클래스가 변견되면 역직렬화 시에 예외가 발생할 수 있으니 개발자가 각 시스템에서 사용하고 있는 serailVersionUID값을 직접 관리해주어 혼란을 줄일 수 있습니다.  
serailVersionUID가 선언되어 있지 않으면 클래스의 기본 해쉬값을 사용합니다.  

## 6. 직렬화는 왜 사용 하는가?
- 복잡한 데이터 구조의 객체라도 직렬화 기본 조건만 지키면 바로 직렬화가 가능합니다.
- 데이터 타입이 자동으로 맞춰지기 때문에 편리합니다.

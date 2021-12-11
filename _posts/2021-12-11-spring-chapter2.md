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
따라서 main메소드가 필요없습니다.  

새로 만들 테스트 메소드는 JUnit 프레임워크가 요구하는 조건 두가지를 따라야 합니다.
- 메소드가 public으로 선언
- 메소드에 @Test 어노테이션을 붙임

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
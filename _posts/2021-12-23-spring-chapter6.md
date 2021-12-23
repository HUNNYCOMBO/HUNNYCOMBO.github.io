---
layout: single
title:  "토비의 스프링 vol.1 5장"
categories: spring
tags: [spring, 서비스 추상화]
toc: true
author_profile: false
sidebar:
    nav: "docs"
search: true
---

## AOP
AOP는 IoC/DI와 서비스 추상화와 더불어 스프링의 3대 기반 기술입니다. AOP는 가장 이해하기 힘든 난해한 용어와 개념을 가져, 등장배경과 이것을 도입한 이유를 살펴봐야 합니다. AOP의 가장 인기있는 적용 대상은 바로 선언전 트랜잭션 기능입니다. 트랜잭션 경계설정 기능을 AOP를 이용해 더욱 세련되고 깔끔하게 바꿔봅니다.

### 1 트랜잭션 코드의 분리
UserSerivcㄷ를 트랜잭션 기술에 독립적이게 만들어 줬지만, 여전히 메소드 안에 트랜잭션 코드가 더 많은 자리를 차지하는 것이 찜찜합니다.  

#### 1-1. 메소드 분리
트랜잭션이 적용된 upgradeLevels() 코드를 자세히보면 비지니스 로직 전후로 트랜잭션 시작과 종료를 담당하는 코드가 있음을 알 수 있습니다.

```java
public void upgradeLevles() throws Exception{
    트랜잭션 시작
    try{비지니스 로직}
    트랜잭션 종료
}
```

또, 비즈니스 로직과 트랜잭션 코드 사이에 주고받는 정보도 없는 것을 알 수 있습니다. 그러면 우선 비지니스로직을 따로 메소드로 분리하는 리팩토링을 진행합니다.

#### 1-2. DI를 이용한 클래스의 분리
메소드로 분리는 했지만 트랙잭션의 코드가 여전히 UserService 안에 존재합니다.  
어차피 직접적으로 정보를 주고받는 것이 없으므로 트랜잭션 코드를 클래스 밖으로 뽑아낼 수 있습니다.  
그런데 이렇게하면 UserService를 사용하는 클라이언트에서는 트랜잭션 기능이 빠진 UserService를 사용하게 됩니다. 여태까지 해온 것 처럼 UserService를 인터페이스로 만들고 기존 코드는 UserService 인터페이스의 구현 클래스에 넣어 DI를 통해 간접적으로 접근하게 하면 해결할 수 있습니다. 그러면 클라이언트와 결합이 약해지고 직접 구현 클래스에 의존하지 않기 때문에 유연한 확장이 가능해 집니다.  

우리는 보통 한 번에 한 가지 클래스를 선택해서 DI를 적용시켜왔지만 꼭 그래야한다는 제약은 없습니다. 한 번에 두개의 구현 클래스를 이용할 수 도 있습니다.  
UserService를 구현한 클래스를 하나 더 만들고 트랜잭션 경계설정이라는 책임을 맡게합니다.  

[![](https://mermaid.ink/img/eyJjb2RlIjoiZ3JhcGggVERcbiAgICBBW1VzZXJTZXJ2aWNlSW1wbF0gLS0-IEJbVXNlclNlcnZpY2UgLyBpbnRlcmZhY2VdXG4gICAgQ1tVc2VyU2VydmljZVR4XSAtLT4gQlxuICAgIERbQ2xpZW50IC8gVXNlclNlcnZpY2VUZXN0XSAtLT4gQlxuICAgIFxuIiwibWVybWFpZCI6eyJ0aGVtZSI6ImRhcmsifSwidXBkYXRlRWRpdG9yIjpmYWxzZSwiYXV0b1N5bmMiOnRydWUsInVwZGF0ZURpYWdyYW0iOmZhbHNlfQ)](https://mermaid-js.github.io/mermaid-live-editor/edit#eyJjb2RlIjoiZ3JhcGggVERcbiAgICBBW1VzZXJTZXJ2aWNlSW1wbF0gLS0-IEJbVXNlclNlcnZpY2UgLyBpbnRlcmZhY2VdXG4gICAgQ1tVc2VyU2VydmljZVR4XSAtLT4gQlxuICAgIERbQ2xpZW50IC8gVXNlclNlcnZpY2VUZXN0XSAtLT4gQlxuICAgIFxuIiwibWVybWFpZCI6IntcbiAgXCJ0aGVtZVwiOiBcImRhcmtcIlxufSIsInVwZGF0ZUVkaXRvciI6ZmFsc2UsImF1dG9TeW5jIjp0cnVlLCJ1cGRhdGVEaWFncmFtIjpmYWxzZX0)

먼저 기존의 UserService는 UserServiceImpl로 이름을 변경합니다. 비즈니스 로직만 다루는 구현 클래스 이므로 트랜잭션과 관련된 코드는 모두 제거합니다. 그리고 UserService 인터페이스를 만듭니다.  
그리고 UserServiceTx 클래스는 비즈니스 로직에서 벗어나도록 UserServiceImpl에게 작업을 위임하게 합니다.  

```java
public class UserServiceTx implements UserService{
    UserService userService;
    PlatformTransactionManager transactionManager;

    public void setUserService(UserService userService){
        // UserServiceImpl 오브젝트를 DI 받습니다.
    }

    @Override
    public void add(User user){
        userService.add(user);
        // UserSerivceImpl 에게 비즈니스 로직을 위임합니다.
    }

    public void upgradeLevels(){
        트랜잭션 시작 코드
        try{
            userService.upgradeLevels();
            // 위임
        }
        ... 트랜잭션 종료 코드
    }
}
```

client가 UserServiceTx를 사용하고 UserServiceTx가 UserServiceImpl을 사용하는 의존관계를 띄고 있습니다. 이 의존관계에 맞춰 xml을 설정합니다.  

```java
<bean id="userService" class="...UserServiceTx">
    <property name="UserServiceImpl">

<bean id="userServiceImpl" class="...UserServiceImpl">
```

이렇게 xml설정을 추가하면 UserServiceTest에서 @Autowired받는 userService에 문제가 발생합니다. 인터페이스 타입이면 타입이 일치하는 빈을 찾아주지만 UserService 인터페이스 타입으로 등록된 빈이 UserServiceTx와 UserServiceImpl 두가지 입니다. 이런 경우 필드 이름을 이용해 빈을 찾습니다. 우리가 DI할 userService 구현 클래스는 userServiceTx 이므로 필드 변수 명을 userService로 둡니다.  
그런데 MailSender 목 오브젝트를 이용한 테스트에서는 수정자 메소드로 직접 mockMailSender를 DI 해 줄 필요가 있었습니다. MailSender를 DI 해줄 대상을 구체적으로 알고 있어야 하기에 UserServiceImpl 클래스의 오브젝트를 가져올 필요가 있습니다. userSeviceImpl 필드 변수 명으로 추가합니다. 그리고 테스트 메소드도 userService 변수를 사용하던 부분도 같이 수정해줍니다.  
또, 내부클래스로 정의한 TestUserService가 UserServiceImpl을 상속하도록 수정하고(예외 발생 코드가 이곳에 있기 떄문입니다.) 이 오브젝트가 UserServiceTx를 DI받도록 수정합니다.  

가장 복잡한 작업이었지만 이렇게 분리함으로서, 트랜잭션을 분리해내고 UserServiceTx 오브젝트가 먼저 실행되도록 만들기만 하면 트랜잭션을 그대로 사용할 수 있습니다.  

### 2. 고립된 단위 테스트
이렇게 비즈니스 로직에 집중되게 함으로써 테스트를 손쉽게 만드는 것도 가능합니다.  

#### 2-1. 복잡한 의존관계 속의 테스트
[![](https://mermaid.ink/img/eyJjb2RlIjoiZ3JhcGggTFJcbiAgICBVc2VyU2VydmljZVRlc3QgLS0-IFVzZXJTZXJ2aWNlXG4gICAgVXNlclNlcnZpY2UgLS0-IFVzZXJEYW9KZGJjXG4gICAgVXNlclNlcnZpY2UgLS0-IERTVHJhbnNhY3Rpb25NYW5hZ2VyXG4gICAgVXNlclNlcnZpY2UgLS0-IEphdmFNYWlsU2VuZGVySW1wbFxuIiwibWVybWFpZCI6eyJ0aGVtZSI6ImRhcmsifSwidXBkYXRlRWRpdG9yIjpmYWxzZSwiYXV0b1N5bmMiOnRydWUsInVwZGF0ZURpYWdyYW0iOmZhbHNlfQ)](https://mermaid-js.github.io/mermaid-live-editor/edit#eyJjb2RlIjoiZ3JhcGggTFJcbiAgICBVc2VyU2VydmljZVRlc3QgLS0-IFVzZXJTZXJ2aWNlXG4gICAgVXNlclNlcnZpY2UgLS0-IFVzZXJEYW9KZGJjXG4gICAgVXNlclNlcnZpY2UgLS0-IERTVHJhbnNhY3Rpb25NYW5hZ2VyXG4gICAgVXNlclNlcnZpY2UgLS0-IEphdmFNYWlsU2VuZGVySW1wbFxuIiwibWVybWFpZCI6IntcbiAgXCJ0aGVtZVwiOiBcImRhcmtcIlxufSIsInVwZGF0ZUVkaXRvciI6ZmFsc2UsImF1dG9TeW5jIjp0cnVlLCJ1cGRhdGVEaWFncmFtIjpmYWxzZX0)

단위 테스트 기준으로 보면 UserServiceTest의 단위는 UserService 클래스 여야 합니다. 하지만 UserSerivce는 세 가지 오브젝트와 의존관계를 맺고 있고 심지어 그 오브젝트들이 dataSoruce나 DB JavaMail 등의 기술에 의존하고 있습니다. 이 어느것이라도 바르게 셋업되어 있지 않다면 UserService에 대한 테스트는 실패해버리게 됩니다. 따라서 이런 경우의 테스트는 준비하기도 힘들고, 환경이 조금이라도 달라지면 동일한 결과를 내지 못할 수도 있습니다.  

#### 2-2. 테스트 대상 오브젝트 고립시키기
그러므로 테스트 대상이 다른 환경에 영향받지 않도록 고립시켜야할 필요가 있습니다. 바로 테스트를 위한 대역을 사용하는 것입니다.  
기존의 메소드를 살펴봅니다.  

```java
//UserServiceImpl의 메소드
	public void upgradeLevels() {
        // 리턴이 void이기 때문에 결과를 받아서 검증하는 것이 불가능합니다.
		List<User> users = userDao.getAll();
        // DAO를 통해 정보를 가져와 결과를 DAO를 통해 DB에 저장합니다.
        // 결과를 확인하려면 DB를 직접확인해야 합니다.
        // 그래서 DAO를 이용해 정보를 가져와 DB에 들어간 결과를 검증했습니다.
        // 그러나 UserServiceImpl을 독립시키면 DB로 부터 결과를 알 수 없습니다.
        // 이럴 땐 UserServiceImpl과 UserDao에게 어떤 요청을 했는지를 확인하면 됩니다.
        // UserDao의 update()가 호출 됐다면 그 결과가 반영될 것이라 결론을 낼 수 있기 떄문입니다.
        // UserDao와 같은역할을 하면서 UserServiceImpl과 주고받은 정보를 저장했다가, 검증에 사용하는 목 오브젝트를 추가합니다.
		for (User user : users) {
			if (canUpgradeLevel(user)) {
				upgradeLevel(user);
			}
		}
	}

    protected void upgradeLevel(User user) {
		user.upgradeLevel();
		userDao.update(user);
        // Dao가 사용되는 곳은 이 곳과 업그레이드 후보를 저장하는 List입니다.
		sendUpgradeEMail(user);
	}
```

목 오브젝트는 실제 UserDao가 해주는 기능을 지원해줘야 합니다. 업그레이드 후보 목록을 가져오는 것과 update()로 DB에 반영하는 것입니다. 전자는 스텁으로서 기능을, 후자는 목 오브젝트로서 동작하는 UserDao 타입의 테스트 대역이 필요합니다. 이 MockUserDao는 UserServiceTest 전용일 것이므로 스태틱 내부 클래스로 만들면 편리합니다.  


```java
    static class MockUserDao implements UserDao { 
        // UserDao를 구현합니다. UserDao를 대체해야 하니 당연합니다.
		private List<User> users;  // 업그레이드 후보를 담는 User 오브젝트 목록
		private List<User> updated = new ArrayList(); // 업그레이드 대상 오브젝트를 저장해둘 목록
        // 검증을 위해 사용됩니다.
		
		private MockUserDao(List<User> users) {
			this.users = users;
		}

		public List<User> getUpdated() {
			return this.updated;
		}

		public List<User> getAll() {  
			return this.users;
            // 스텁 기능(목록을 가져옵니다.)
		}

		public void update(User user) {  
			updated.add(user);
            // 목 오브젝트 기능()
		}
		
		public void add(User user) { throw new UnsupportedOperationException(); }
		public void deleteAll() { throw new UnsupportedOperationException(); }
		public User get(String id) { throw new UnsupportedOperationException(); }
		public int getCount() { throw new UnsupportedOperationException(); }
        // 테스트에 사용되지 않습니다.
	}

// 테스트 메소드를 이제 아래와 같이 수정합니다.
	@Test 
	public void upgradeLevels() throws Exception {
		UserServiceImpl userServiceImpl = new UserServiceImpl(); 
        // 고립된 테스트에서는 테스트 대상을 직접 생산합니다.
		
		MockUserDao mockUserDao = new MockUserDao(this.users);  
		userServiceImpl.setUserDao(mockUserDao);
        // 목 오브젝트 UserDao를 직접 DI해줍니다.

		MockMailSender mockMailSender = new MockMailSender();
		userServiceImpl.setMailSender(mockMailSender);
		
		userServiceImpl.upgradeLevels();

		List<User> updated = mockUserDao.getUpdated();  
        // mockUserDao로 부터 목록을 가져와 검증합니다.
        // 기존의 테스트는 DB에서 가져왔지만 독립시켜 목 오브젝트에 저장된 목록을 이용합니다.
		assertThat(updated.size(), is(2));  
		checkUserAndLevel(updated.get(0), "joytouch", Level.SILVER); 
		checkUserAndLevel(updated.get(1), "madnite1", Level.GOLD);
        // 업데이트 횟수와 정보를 확인합니다.
		
		List<String> request = mockMailSender.getRequests();
		assertThat(request.size(), is(2));
		assertThat(request.get(0), is(users.get(1).getEmail()));
		assertThat(request.get(1), is(users.get(3).getEmail()));
	}

	private void checkUserAndLevel(User updated, String expectedId, Level expectedLevel) {
		assertThat(updated.getId(), is(expectedId));
		assertThat(updated.getLevel(), is(expectedLevel));
	}
```

기존의 테스트는 @Autowired를 통해 가져온 UserService 타입의 빈 이었습니다. 이 빈은 많은 외부 환경에 의존하고 있었습니다. 이제는 완전히 고립대서 테스트만을 위해 독립적으로 동작하기떄문에 스프링 컨테이너에서 빈을 가져올 필요가 없습니다. 이제 UserServiceImpl 은 목 오브젝트 mailsender와 userdao만 이용하고 외부 클래스와 기술로부터 완전 독립되었습니다. 그로인해 테스트 성능이 좋아지는 것은 무시할 수 없는 강점입니다.  

#### 2-3. 단위 테스트와 통합 테스트
정해진 것은 아니지만 앞으로 위와 같이 완전히 고립시킨 테스트를 단위 테스트, DI를 포함해 두 개 이상의 단위가 결합해서 동작하면 통합 테스트라고 부르겠습니다.  
단위 테스트와 통합 테스트 중에서 어떤 방법을 쓸지는 아래 가이드 라인을 참고합니다.  

- 항상 단위 테스트를 먼저 고려한다.
- 외부 리소스를 사용해야만 가능한 테스트는 통합 테스트로 만든다.
- 단위 테스트로 만들기 어려운 대표적이 예는 DAO다. DAO는 DB까지 연동하는 테스트로 만들어야 하기 때문이다.
- 여러 개의 단위가 의존관계를 갖고 동작할 때는 통합 테스트가 필요하다.
- 하지만 미리 단위 테스트를 충분히 거쳤다면 통합 테스트의 부담은 줄어든다.
- 스프링 테스트 컨텍스트 프레임워크를 이용하는 테스트는 통합 테스트다.

#### 2-4. 목 프레임워크
단위 테스트는 많은 장점이 있지만, 목 오브젝트를 구현해야 하는 번거로움이 있습니다. 다행히도, 이런 목 오브젝트 작성을 도와주는 지원 프레임워크가 있습니다.  

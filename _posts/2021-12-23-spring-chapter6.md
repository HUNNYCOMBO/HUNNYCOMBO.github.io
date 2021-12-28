---
layout: single
title:  "토비의 스프링 vol.1 6장"
categories: spring
tags: [spring, AOP]
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
그중에서도 mockito 프레임 워크는 직관적이고 사용하기 편합니다. UserDao 인터페이스를 구현한 테스트용 목 오브젝트는 Mockito의 스태틱 메소드를 한 번 호출하면 만들어집니다.  

> UserDao mockUserDao = mock(UserDao.class);

이렇게 만들어진 목 오브젝트는 아무런 기능이 없으므로, 스텁 기능과 목 오브젝트 기능을 추가해 줘야합니다.  

```java
when(mockUserDao.getAll()).thenReturn(this.users);
// getAll()이 호출 됐을 때, users 리스트를 리턴해달라는 선언입니다.

verify(mockUserDao, time(2)).update(any(User.class));
// any는 파라미터를 무시하고 update()가 두 번 호출 되었는지 확인합니다.
```

특별한 기능을 가진 목 오브젝트를 만들어야 할 경우가 아니라면 대부분 단위 테스트에서는 Mockito를 이용하는 것으로 충분합니다.
Mockito 목 오브젝트는 다음의 네 단계를 거쳐 사용합니다.  

1. 인터페이스를 이용해 목 오브젝트를 생성
2. 목 오브젝트가 예외를 포함해 리턴할 값이 있다면 이를 지정해줍니다.
3. 테스트 대상 오브젝트에 DI해서 목 오브젝트가 테스트 중에 사용되도록 합니다.
4. 테스트 대상 오브젝트를 사용한 후에 목 오브젝트의 특정 메소드로 검증합니다.

다음은 Mockito를 이용해 만든 upgradeLevels() 테스트 입니다.

```java
@Test
	public void mockUpgradeLevels() throws Exception {
		UserServiceImpl userServiceImpl = new UserServiceImpl();

		UserDao mockUserDao = mock(UserDao.class);	    
		when(mockUserDao.getAll()).thenReturn(this.users);
		userServiceImpl.setUserDao(mockUserDao);
		// 복잡했던 목 오브젝트 생성과 리턴 값 설정과 DI가 세 줄로 해결됐습니다.

		MailSender mockMailSender = mock(MailSender.class);  
		userServiceImpl.setMailSender(mockMailSender);
		// 리턴값이 없는 목 오브젝트는 더 간단하게 만들어 집니다.

		userServiceImpl.upgradeLevels();

		verify(mockUserDao, times(2)).update(any(User.class));				  
		verify(mockUserDao, times(2)).update(any(User.class));
		verify(mockUserDao).update(users.get(1));
		// 넘겨준 파라미터가 users의 두번째 여야 합니다. 그리고 이 파라미터로 update()가 호출 된 적이 있는지 검증합니다.
		assertThat(users.get(1).getLevel(), is(Level.SILVER));
		verify(mockUserDao).update(users.get(3));
		assertThat(users.get(3).getLevel(), is(Level.GOLD));
		// 목 오브젝트가 제공하는 검증 기능을 통해서 몇 번 호출 됐는지, 파라미터는 무엇인지 확인합니다.

		ArgumentCaptor<SimpleMailMessage> mailMessageArg = ArgumentCaptor.forClass(SimpleMailMessage.class);  
		verify(mockMailSender, times(2)).send(mailMessageArg.capture());
		// ArgumentCaptor 를 사용해서 파라미터의 내부 정보를 확인합니다.
		List<SimpleMailMessage> mailMessages = mailMessageArg.getAllValues();
		assertThat(mailMessages.get(0).getTo()[0], is(users.get(1).getEmail()));
		assertThat(mailMessages.get(1).getTo()[0], is(users.get(3).getEmail()));
	}	

	private void checkLevelUpgraded(User user, boolean upgraded) {
		User userUpdate = userDao.get(user.getId());
		if (upgraded) {
			assertThat(userUpdate.getLevel(), is(user.getLevel().nextLevel()));
		}
		else {
			assertThat(userUpdate.getLevel(), is(user.getLevel()));
		}
	}
```

이상 Mockito의 사용 방법은 다루지 않습니다.  

### 3. 다이내믹 프록시와 팩토리 빈
#### 3-1. 프록시와 프록시 패턴, 데코레이터 패턴
목 오브젝트 전으로 돌아가서 생각해보면 우리는 트랜잭션 경계설정 코드를 비즈니스 로직 코드에서 분리했지만 위임을 통해 기능을 사용하는 코드가 비즈니스 로직 코드에 남아있었습니다.  
그래서 UserServiceTx와 UserServiceImpl로 나누어 트랜잭션 관련 코드를 모두 분리해냈습니다. 이렇게 트랜잭션이라는 부가기능을 담은 클래스는 부가기능 외의 나머지 모든 기능을 핵심기능을 가진 클래스로 위임해줘야 합니다. **따라서 부가기능이 핵심기능을 사용하는 구조가 됩니다.**  
클라이언트 입장에선 핵심 기능을 가진 클래스를 사용하는는것 같지만 실제로는 핵심기능클래스를 사용하는 부가기능 클래스를 사용하는 것입니다.  
이렇게 자신이 클라이언트가 사용하려고 하는 실제 대상인 것처럼 위장해서 요청을 받아주는 것을 대리자 역할을 한다해서 **프록시(proxy)**라고 부릅니다.  
프록시를 통해 요청을 위임받아 처리하는 실제 오브젝트를 타깃 또는 실체라고 부릅니다.  
프록시의 특징은 타깃과 같은 인터페이스를 구현했다는 것과 프록시가 타깃을 제어할 수 있는 위치에 있다는 것입니다.  
프록시의 사용 목적은 두 가지로, 클라이언트가 타깃에 접근하는 방법을 제어하기 위해서고, 다른 하나는 타깃에 부가적인 기능을 부여해주기 위해서 입니다. 목적에 따라서 디자인 패턴에서는 다른 패턴으로 구분합니다.  

- 데코레이터 패턴

데코레이터 패턴은 타깃에 부가적인 기능을 다이내믹하게 부여해주기 위해 프록시를 사용하는 패턴입니다. 다이내믹이라는 뜻은 컴파일시점(코드상)에서는 어떤 방법으로 프로깃와 타깃이 연결되어있는지 나타나지 않는다는 의미입니다. 데코레이터 패턴에서는 프록시가 한 개로 제한되지않고, 프록시가 타깃을 사용하지 않아도 됩니다. 그저 프록시가 여러 개인 만큼 순서를 정해서 위임하는 구조로 만들면 됩니다. 프록시에서 프록시로 위임하더라도 인터페이스로 접근하기 때문에 자신이 최종 타깃인지 다음 단계가 있는지 알지 못합니다.  
그래서 생성자나 수정자 메소드를 통해 위임 대상을 외부에서 런타임 시에 주입받을 수 있도록 만들어야 합니다.  

자바 IO 패키지의 InputStream과 OutputStream 구현 클래스가 데코레이터 패턴의 대표적인 예입니다.  

> InputStream is = new BufferedInputStream(new FilInputStream("a.txt")); : InputStream 인터페이스를 구현한 타깃 FileInputStream에 버퍼 읽기 부가기능을 추가한 Buffred.. 데코레이터를 적용했습니다.

이런 데코레이터 정의는 스프링 DI를 이용하면 아주 편리합니다. UserServiceTx와 UserServiceImpl을 설정한 xml파일을 보면 이 관계가 잘 나타나 있습니다.  
이처럼 데코레이터 패턴은 타깃의 코드를 수정하지 않고, 클라이언트는 인터페이스를 호출하므로 호출 방법도 변경 없이 새로운 기능을 추가할 떄 유용 합니다.  

- 프록시 패턴

프록시와 프록시 패턴은 구분해야 합니다. 전자는 대리인 역할을 하는 오브젝트라면, 후자는 프록시를 사용하는 방법 중에서 타깃에 대한 접근 방법을 제어하려는 목적을 가진 패턴입니다.  
프록시 패턴의 프록시는 타깃의 기능을 확정하거나 추가하지 않습니다. 만약 타깃 오브젝트를 생성하기가 복잡하다면 필요한 시점까지는 미리 오브젝트를 만들 필요가 없습니다. 다만, 타깃 오브젝트에 대한 래퍼런스(참조)가 미리 필요할 경우가 있는데, 이때 타깃 오브젝트를 만드는 대신 프록시를 넘겨주는 것입니다. 그리고 프록시의 메소드를 통해 타깃을 사용하려고 시도하면, 그떄 프록시가 타깃 오브젝트를 생성하고 요청을 위임합니다. 래퍼런스를 갖게 해주는 것고 생성을 지연시키는 것이 포인트 입니다.  

또는, 원격 오브젝트를 이용하는 경우에도 편리합니다. RMI나, EJB 등의 기술을 이용해 다른 서버에 존재하는 오브젝트를 사용해야 한다면, 원격 오브젝트를 대신할 프록시를 사용하게 하는 것입니다. 이 프록시는 클라이언트로부터 요청을 받으면 네트워크를 통해 원격 오브젝트를 실행하고 결과를 받아서 클라이언트에게 돌려줍니다.  

또는, 특별한 상황에서 타깃에 대한 접근권한을 제어하기 위해 사용하기도 합니다. 만약 수정 가능한 오브젝트가 있는데, 특정 레이어로 넘어가서는 읽기전용으로만 동작하게 강제해야 한다면, 이 오브젝트의 프록시를 만들어서 프록시의 특정 메소드를 사용하려고 하면 접근 불가능 예외를 발생시켜주며 됩니다. 이 예가 Collections의 unmodifiableCollection()입니다. 파라미터로 전달된 Collection 오브젝트의 객체를 만들어서, 정보를 수정하는 메소드를 호출할 경우 예외를 발생시킵니다.

이 모든 경우를 섞어서 쓸수도있습니다. 인터페이스를 통해 위임하기 떄문입니다.  

#### 3-2. 다이내믹 프록시
프록시는 유용하지만 이번에도 매번 새로운 클래스를 정의하고, 인터페이스의 구현해야 할 메소드가 많아지므로 번거롭습니다. 자바에서는 java.lang.reflect패키지 안에 프록시를 쉽게 만들 수 있도록 지원해주는 클래스들이 있습니다.  

부가기능 프록시인 UserServiceTx에서 프록시의 기능을 찾아봅니다.  

```java
public class UserServiceTx implements UserService{
	UserService userService; //타깃 오브젝트
	...

	public void add(User user){
		this.userService.add(user);
	}
	// 타깃과 같은 메소드를 구현하고 호출되면 타깃 오브젝트에게 위임합니다.

	public void upgradeLevels(){
		TransactionStatus status = this.transactionManager.getTransaction(new Default....);
		// 트랜잭션 시작이라는 부가기능 수행
		try{
			userService.upgradeLevels();
			// 위임
		}catch ...
		// 트랜잭션 종료라는 부가기능 수행
	}
}
```

위 코드를 보면 프록시를 만들기 번거로운 이유가 두 가지 있습니다.  

첫번째로 부가기능이 필요 없는 메소드도 구현해서 타깃으로 위임해야 하는 코드를 일일이 만들어야하기에 번거롭습니다.  
두번째는 부가기능 코드가 중복될 가능성이 많습니다. 다른 메소드에서 트랜잭션 부가기능이 필요하다면 부가기능 코드를 적어줘야 합니다.  

이런 문제를 해결하는데 유용한 것이 JDK의 다이내믹 프록시입니다. 다이내믹 프록시는 리플렉션 기능을 이용해서 프록시를 만들어줍니다.  

> 리플렉션 : 자바의 코드 자체를 추상화해서 접근합니다.

좀 더 쉽게 이해하기위해서 모든 클래스에는 그 클래스 자체의 정보를 담은 Class 타입의 오브젝트를 갖고 있다는걸 생각합니다. 흔히 클래스이름.class로 가져오는 정보입니다.  
리플랙션 API 중에서 메소드에 대한 정의를 담은 Method라는 인터페이스를 이용해 메소드를 호출 할 수 있습니다.  

> Method lenghtMethod = String.class.getMethod("length"); : 스트링 클래스의 length()를 가져옵니다.

Method인터페이스의 invoke()를 이용해 메소드를 사용할 수도 있습니다. 파라미터로 실행시킬 대상 오브젝트와, 파라미터 목록을 넣어 대상 메소드를 호출한 뒤 결과를 Object타입으로 돌려줍니다.  

> int length = lengthMethod.invoke(name); == int length = name.length();

이처럼 Stirng 클래스에서 메소드를 이용해 직접 호출하는 방식과 달리, Method를 이용해 호출하는 방법을 리플렉션이라고 합니다.  

다이내믹 프록시는 프록시 팩토리에 의해 만들어지는 오브젝트 입니다. 클라이언트는 **타깃 인터페이스**를 통해 다이내믹 오브젝트를 사용할 수 있습니다. 이 덕분에 프록시를 만들 때 인터페이스를 모두 구현해가면서 클래스를 정의할 필요가 없습니다. 프록시 팩토리가 인터페이스 정보만 알면 해당 인터페이스를 구현한 클래스의 오브젝트를 자동으로 만들어 주기 떄문입니다. 하지만 필요한 부가기능 코드는 직접 작성해야 합니다.  

이때 부가기능 코드는 프록시 오브젝트와 분리해 InvocationHandler를 구현한 오브젝트에 담습니다. InvocationHandler는 invoke() 하나만 갖는 인터페이스 입니다.  

> public Object invoke(Object proxy, Method method, Object[] args)

파라미터로 프록시 오브젝트와 리플렉션의 Method 인터페이스, 해당 메소드의 파라미터들을 받습니다. 다이내믹 프록시 오브젝트는 클라이언트의 모든 요청을 리플랙션 정보로 변환해서 invoke()로 넘깁니다. 타깃 인터페이스의 모든 메소드 요청이 하나의 메소드로 집중되기 때문에 중복되는 기능을 효과적으로 제공합니다.  

남은 것은 각 메소드 요청을 어떻게 처리할 지 결정하는 것입니다. 우리는 앞에서 Method와 파라미터 정보가 있으면 특정 오브젝트의 메소드를 실행할 수 있음을 확인했습니다. InvocationHandler 구현 오브젝트가 타깃의 래퍼런스를 갖고 있다면 리플렉션을 이용해 간단히 위임 코드를 만들어 냅니다.  

단순히 정리하자면, 다이내믹 프록시가 받은 모든 요청을 InvocationHandler의 invoke()로 모두 모은 뒤, 리플렉션 API를 이용해 타깃 오브젝트의 메소드를 호출합니다.  

지금까지의 내용을 코드로 한번 살펴봅니다.

```java
// 프록시를 적용할 간단한 인터페이스와 이를 구현한 클래스를 정의합니다.

interface Hello{
	String sayHello(String name);
	String sayHi(String name);
	String sayThankYou(String name);
}

// Hello를 구현한 타깃 클래스
public class HelloTarget implements Hello{
	@Override
	public Stirng sayHello(Stirng name){
		return "Hello" + name;
	}

	public String sayHi(Stirng name){
		return "Hi" + name;
	}
	...
}

// Hello 인터페이스를 구현한 프록시 입니다.
// 데코레이터 패턴을 적용해서 부가적인 기능을 추가합니다.
// 부가적인 기능은 모두 대문자로 바꿔주는 것입니다.

public class HelloUppercase implements Hello{
	Hello hello;
	// 위임할 타깃 오브젝트, 그러나 다른 프록시를 추가할 수도 있으므로 인터페이스로 접근합니다.

	public HeeloUppercase(Heelo hello){
		this.hello = hello;
	}

	public Stirng sayHello(Stirng name){
		return heelo.sayHello(name).toUpperCase();
		// 주입받은 타깃 hello 에게 sayHello()를 위임하고. toUppercase()를 적용합니다.
		// hello.sayHello의 리턴값이 String 이므로 String의 메소드를 사용합니다.
	}

	...
}

// 타깃 오브젝트를 사용하는 클라이언트 입니다.
@Test
public void simpleProxy(){
	Hello hello = new HelloTarget(); //타깃은 인터페이스를 통해 접근하도록합니다.
	assertThat(hello.sayHello("Hunny"), is("Hello Hunny"));
	assertThat(hello.sayHi()....);

	// 프록시 테스트 입니다.

	Hello proxiedHello = new HelloUppercase(new HelloTarget());
	// 프로시를 통해 타깃 오브젝트에 접근합니다.
	assertThat(proxciedHello.sayHello("Hunny"),is("HELLO HUNNY"));
	...
}

// 이렇게 프록시를 적용하면 두가지 문제점을 갖습니다.
// 프록시가 인터페이스의 모든 메소드를 구현해 위임하도록 해야하며,
// 부가적인 기능을 하는 코드가 모든 메소드에 중복돼서 나타납니다.

// 프록시 HelloUppercase를 InvocationHandler를 이용하는 다이내믹 프록시로 만들어봅니다.
// 먼저 InvocationHandler 구현 클래스를 만듭니다.
// 이 클래스는 다이내믹 프록시로부터 메소드 호출 정보를 받아 처리합니다.
// 기존의 HelloUppercase 프록시와 기능이 동일합니다.
public class UppercaseHandler implements InvocationHandler{
	Hello target;

	public UpeprcaseHandler(Hello target){
		this.target = target;
		// 다이내믹 프록시로부터 받은 요청을 다시 타깃에게 위임합니다.
	}

	@Override
	public Object invoke(Object proxy, Method method, Object[] args) throws Throwable{
		String ret = (Stirng)method.invoke(target, args);
		// 타겟에게 위임합니다.
		// Hello 인터페이스의 메소드 호출에 모두 적용됩니다.
		// Hello 의 모든 메소드는 리턴값이 String이므로 형변환 해도 안전합니다.
		return ret.toUppercase();
		// 기존 부가기능입니다.
	}
}

// 이제 클라이언트에 이 InvocationHanler를 사용하고 Hello 인터페이스를 구현하는
// 다이내믹 프록시를 만듭니다. Proxy클래스의 newProxyInstance()를 이용합니다.

Hello proxiedHello = (Hello)Proxy.newProxyInstance(
	// Hello 타입으로 캐스팅해도 안전합니다. 다이내믹 프록시가 Hello 오브젝트를 구현하고 있기 때문입니다.
	getClass().getClassLoader(),
	new Class[] {Hello.class},
	new UppercaseHandler(new HelloTarget())
);
assertThat(proxiedHello.sayHello("Hunny"),is("HELLO HUNNY"));
assertThat(proxiedHello.sayHi("Hunny"),is("HI HUNNY"));
...

// 파라미터가 많으니 주의합니다.
// 순서대로 동적으로 생성되는 다이내믹 프록시 클래스의 로딩에 사용할 클래스 로더
// 구현할 인터페이스(배열로 여러개 지정이 가능합니다. 하나 이상의 인터페이스를 구현가능)
// 부가기능과 위임 코드를 담은 InvocationHandler 구현 클래스 입니다.
```

newProxyInstance()에 의해 만들어진 다이내믹 프록시는 파라미터로 제공한 Hello 인터페이스를 구현한 클래스의 오브젝트입니다. 그리고 UppercaseHandler를 사용하게 됩니다. 아래 그림은 다이내믹프록시의 구조를 보여줍니다.  

[![](https://mermaid.ink/img/eyJjb2RlIjoiZ3JhcGggTFJcbiAgICDtgbTrnbzsnbTslrjtirggLS0-fO2UhOuhneyLnCDsmpTssq18IO2UhOuhneyLnO2Mqe2GoOumrFxuICAgIO2BtOudvOydtOyWuO2KuCAtLT5866mU7IaM65OcIO2YuOy2nHwg64uk7J2064K066-57ZSE66Gd7IucXG4gICAg7ZSE66Gd7Iuc7Yyp7Yag66asIC0tPnztlITroZ3si5wg7IOd7ISxfCDri6TsnbTrgrTrr7ntlITroZ3si5xcbiAgICDri6TsnbTrgrTrr7ntlITroZ3si5wgLS0-fOuplOyGjOuTnCDsspjrpqwg7JqU7LKtfCBJbnZvY2F0aW9uSGFuZGxlcuq1rO2YhO2BtOuemOyKpFxuICAgIEludm9jYXRpb25IYW5kbGVy6rWs7ZiE7YG0656Y7IqkIC0tPiB86rKw6rO8IOumrO2EtHwg64uk7J2064K066-57ZSE66Gd7IucXG4gICAgSW52b2NhdGlvbkhhbmRsZXLqtaztmITtgbTrnpjsiqQgLS0-fOychOyehHwg7YOA6rmD7Jik67iM7KCd7Yq4XG4iLCJtZXJtYWlkIjp7InRoZW1lIjoiZGFyayJ9LCJ1cGRhdGVFZGl0b3IiOmZhbHNlLCJhdXRvU3luYyI6dHJ1ZSwidXBkYXRlRGlhZ3JhbSI6ZmFsc2V9)](https://mermaid-js.github.io/mermaid-live-editor/edit#eyJjb2RlIjoiZ3JhcGggTFJcbiAgICDtgbTrnbzsnbTslrjtirggLS0-fO2UhOuhneyLnCDsmpTssq18IO2UhOuhneyLnO2Mqe2GoOumrFxuICAgIO2BtOudvOydtOyWuO2KuCAtLT5866mU7IaM65OcIO2YuOy2nHwg64uk7J2064K066-57ZSE66Gd7IucXG4gICAg7ZSE66Gd7Iuc7Yyp7Yag66asIC0tPnztlITroZ3si5wg7IOd7ISxfCDri6TsnbTrgrTrr7ntlITroZ3si5xcbiAgICDri6TsnbTrgrTrr7ntlITroZ3si5wgLS0-fOuplOyGjOuTnCDsspjrpqwg7JqU7LKtfCBJbnZvY2F0aW9uSGFuZGxlcuq1rO2YhO2BtOuemOyKpFxuICAgIEludm9jYXRpb25IYW5kbGVy6rWs7ZiE7YG0656Y7IqkIC0tPiB86rKw6rO8IOumrO2EtHwg64uk7J2064K066-57ZSE66Gd7IucXG4gICAgSW52b2NhdGlvbkhhbmRsZXLqtaztmITtgbTrnpjsiqQgLS0-fOychOyehHwg7YOA6rmD7Jik67iM7KCd7Yq4XG4iLCJtZXJtYWlkIjoie1xuICBcInRoZW1lXCI6IFwiZGFya1wiXG59IiwidXBkYXRlRWRpdG9yIjpmYWxzZSwiYXV0b1N5bmMiOnRydWUsInVwZGF0ZURpYWdyYW0iOmZhbHNlfQ)

[![](https://mermaid.ink/img/eyJjb2RlIjoiZ3JhcGggTFJcbiAgICDri6TsnbTrgrTrr7ntlITroZ3si5xzYXlIZWxsbyAtLT4gaW52b2tlXG4gICAg64uk7J2064K066-57ZSE66Gd7Iucc2F5SGkgLS0-IGludm9rZVxuICAgIOuLpOydtOuCtOuvue2UhOuhneyLnHNheVRoYW5rWW91IC0tPiBpbnZva2VcbiAgICBpbnZva2UgLS0-IO2DgOq5g3NheUhlbGxvXG4gICAgaW52b2tlIC0tPiDtg4DquYNzYXlIaVxuICAgIGludm9rZSAtLT4g7YOA6rmDc2F5VGhhbmtZb3UiLCJtZXJtYWlkIjp7InRoZW1lIjoiZGFyayJ9LCJ1cGRhdGVFZGl0b3IiOmZhbHNlLCJhdXRvU3luYyI6dHJ1ZSwidXBkYXRlRGlhZ3JhbSI6ZmFsc2V9)](https://mermaid-js.github.io/mermaid-live-editor/edit#eyJjb2RlIjoiZ3JhcGggTFJcbiAgICDri6TsnbTrgrTrr7ntlITroZ3si5xzYXlIZWxsbyAtLT4gaW52b2tlXG4gICAg64uk7J2064K066-57ZSE66Gd7Iucc2F5SGkgLS0-IGludm9rZVxuICAgIOuLpOydtOuCtOuvue2UhOuhneyLnHNheVRoYW5rWW91IC0tPiBpbnZva2VcbiAgICBpbnZva2UgLS0-IO2DgOq5g3NheUhlbGxvXG4gICAgaW52b2tlIC0tPiDtg4DquYNzYXlIaVxuICAgIGludm9rZSAtLT4g7YOA6rmDc2F5VGhhbmtZb3UiLCJtZXJtYWlkIjoie1xuICBcInRoZW1lXCI6IFwiZGFya1wiXG59IiwidXBkYXRlRWRpdG9yIjpmYWxzZSwiYXV0b1N5bmMiOnRydWUsInVwZGF0ZURpYWdyYW0iOmZhbHNlfQ)


메소드가 3개가 아니라 100개라면 HelloUppercase처럼 클래스로 직접 구현한 경우는 일일이 코드르 추가해야하지만, 다이내믹 프록시로 생성한 코드는 손댈 것이 없습니다. 

만약, 리턴 타입이 String이 아닌 메소드가 추가되면 지금의 코드는 모두 String으로 형변환 시켰기 때문에 캐스팅 오류가 발생할 것입니다. 따라서 타깃 오브젝트의 메소드의 리턴 타입이 Stirng인 경우에만 대문자로 바꿔주기로 하고 그 외에는 그대로 넘겨주도록 수정합니다.  

InvocationHandler의 방식의 장점은 타깃의 종류에 상관없이 적용이 가능하다는 것입니다.  
리플랙션의 Method인터페이스를 이용해 타깃의 메소드를 호출하는 것이니 Hello타입으로 제한할 필요가 없이 재사용이 가능합니다.  

```java
public class UppercaseHandler implements InvocationHandler{
	Object target;
	private UppercaseHandler(Object target){
		this target = target;
	}
	// 어떤 종류의 인터페이스를 구현한 타깃이든 적용이 가능합니다.

	public Object invoke(..){
		Object ret = method.invoke(target. args);
		if(ret instaceof Stirng){
			// 호출한 메소드의 리턴타입이 String인 경우만 uppercase를 적용합니다.
			return ((Stirng)ret).toUpperCase();
		}else{
			return ret;
		}
	}
}
```

invoke()는 단일 메소드에서 모든 요청을 처리하기 떄문에 어떤 요청에 어떤 기능을 적용할지를 선택하는 과정이 필요합니다. 이때 필요한 것이 메소드의 이름, 파라미터의 개수와 타입, 리턴 타입 등 입니다. 만약 메소드(요청)의 이름이 say로 시작하는 조건으로 제한해서 부가기능을 제공하려면 다음과 같이 수정할 수 있습니다.

> if (ret instaceof String && method.getName().startsWith("say"))

#### 3-3. 다이내믹 프록시를 이용한 트랜잭션 부가기능
이제 메소드마다 트랜잭션 처리코드가 중복되는 비효율적인 UserServiceTx를 다이내믹 프록시 방식으로 변경해봅니다.  

```java
public class TransactionHandler implements InvocationHandler {
	Object target;
	PlatformTransactionManager transactionManager;
	String pattern;	// 트랜잭션을 적용할 메소드 이름 패턴

	public void setTarget(Object target) {
		this.target = target;
	}

	public void setTransactionManager(
			PlatformTransactionManager transactionManager) {
		this.transactionManager = transactionManager;
	}

	public void setPattern(String pattern) {
		this.pattern = pattern;
	}

	public Object invoke(Object proxy, Method method, Object[] args)
			throws Throwable {
		if (method.getName().startsWith(pattern)) {
			// 트랜잭션 적용 대상 메소드를 pattern으로 선별합니다.
			return invokeInTransaction(method, args);
		} else {
			return method.invoke(target, args);
		}
	}

	// 부가기능인 트랜잭션 입니다.
	private Object invokeInTransaction(Method method, Object[] args)
			throws Throwable {
		TransactionStatus status = this.transactionManager
				.getTransaction(new DefaultTransactionDefinition());
		try {
			Object ret = method.invoke(target, args);
			this.transactionManager.commit(status);
			return ret;
		} catch (InvocationTargetException e) {
			// 예외를 RuntimeException이 아닌 다른 예외로 변경했습니다.
			// 리플렉션 메소드인 Method.invoke()를 이용할 때는
			// 타깃 오브젝트에서 발생하는 예외가 InvocationTargetException으로 포장되서 전달됩니다.
			this.transactionManager.rollback(status);
			throw e.getTargetException();
			// 중첩되어 있는 예외를 가져와야 합니다.
		}
	}
}

// 이제 클라이언트인 UserServiceTest의 upgradeAllOrNothing()에 적용해봅니다.

	@Test
	public void upgradeAllOrNothing() throws Exception {
		TransactionHandler txHandler = new TrasactionHandler();
		txHandler.setTarget(testUserService);
		txHandler.setTrasactionManager(transactionManager);
		txHandler.setPattern("upgradeLevles");
		// 트랜잭션 핸들러가 필요한 정보와 오브젝트를 DI 합니다.

		UserService txUserService = (UserService)Proxy.newProxyInstace(
			getClass().getClassLoader(),
			new Class[] {UserService.class},
			txHandler
		);
		// UserService인터페이스 타입의 다이내믹 프록시 생성
		...
	}
```

#### 3-4. 다이내믹 프록시를 위한 팩토리 빈
이제 TransactionHandler와 다이내믹 프록시를 스프링의 DI를 통해 사용할 수 있도록 만들어봅니다. 그런데 문제는 다이내믹 프록시 오브젝트는 빈으로 등록할 방법이 없습니다.  
스프링 빈은 기본적으로 **클래스의 이름**을 가지고 리플랙션API를 이용해서(newInstace 메소드) 해당 클래스의 오브젝트를 만들기 때문입니다. 새로 정의해서 사용하기 전에 다이내믹 프록시의 클래스가 어떤 것인지 알 수가 없습니다.  

그러나 스프링은 클래스 정보를 가지고 오브젝트를 만드는 방법 외에도 빈을 만드는 여러가지 방법을 제공합니다. 그 중 하나는 팩토리 빈을 이용한 생성 방법입니다. 팩토리 빈이란 스프링을 대신해서 오브젝트의 생성을 담당하도록 만들어진 특별한 빈입니다. 가장 간단한 방법은 FactoryBean이라는 인터페이스를 구현하는 것입니다.

FactoryBean 인터페이스는 세가지 메소드를 갖고 있습니다.
1. 빈 오브젝트를 생성해서 돌려줍니다. : T getObject()
2. 생성되는 오브젝트의 타입을 알려줍니다. : Class<? extends T> getObjectType()
3. getObject()로 돌려주는 오브젝트가 싱글톤 오브젝트인지 알려줍니다. : boolean isSingleton()

Message 클래스로 예를 들어봅니다. Message 클래스는 pirvate으로 생성자가 선언되어 생성자를 통해 오브젝트를 만들 수 없습니다. 오브젝트를 만들려면 반드시 Message 오브젝트를 리턴하는 스태틱 메소드인 newMessage(String text)를 사용해야 합니다. 사실 private 생성자를 가진 클래스도 스프링 빈으로 등록가능 하지만, 이는 접근 규약을 위반하는 특수한 경우로 위험하며 권장되지 않습니다.  

```java
public class MessageFactoryBean implements FactoryBean<Message> {
	Strin text;

	public void setText(String text){
		this.text = text;
		// 오브젝트를 생성할 때 필요한 정보는 필드(프로퍼티)로 선언해서 DI받을 수 있게합니다.
		// newMessage()에 필요합니다.
	}

	public Message getObject() throws Exception{
		return Message.newMessage(this.text);
		// 실제 빈으로 사용될 오브젝트를 생성합니다.
		// 코드로 정의하기에 복잡한 방식의 생성도 가능합니다.
	}

	public Class<? extends Message> getObejctType(){
		return Message.class;
	}

	public boolean isSingleton(){
		return false;
		// 팩토리 빈은 매번 요청마다 새로운 오브젝트를 만드므로 false로 설정합니다.
		// 다만 이것은 팩토리빈 설정이고 만들어진 빈 오브젝트는 싱글톤으로 스프링이 관리할 수 있습니다.
	}
}

// 팩토리빈 xml 설정
<bean id="message" class="MessageFactoryBean 경로">
	<property name="text" value="Factory Bean" />
		//String text의 값을 Factory Bean으로 설정합니다.
// class애트리뷰트의 값으로 MessageFactoryBean을 입력했지만 message 빈의 오브젝트 타입은
// Message 타입입니다.
```

message 빈의 타입이 Message인 이유는 getObjectType()이 돌려주는 타입으로 결정되기 때문입니다. 만약 팩토리 빈 자체를 가져오고 싶다면 getBean("&message"); 를 사용해서 가져옵니다.  

이제 팩토리 빈이 UserService를 구현한 다이내믹 프록시와 TransactionHandler를 생성해서 타깃 오브젝트를 주입하도록 변경해 봅니다. 스프링 빈에는 팩토리 빈과 UserServiceImpl만 등록합니다.  

```java
public class TxProxyFactoryBean implements FactoryBean<Object> {
	// 범용성을 위해 Object로 타입 파라미터를 정의합니다.
	Object target;
	PlatformTransactionManager transactionManager;
	String pattern;
	Class<?> serviceInterface; // 다이내믹 프록시를 생성할 때 필요합니다.
	// UserService가 아닌 인터페이스를 가진 타깃에도 적용 가능합니다.(재사용, 범용성)
	
	public void setTarget(Object target) {
		this.target = target;
	}

	public void setTransactionManager(PlatformTransactionManager transactionManager) {
		this.transactionManager = transactionManager;
	}

	public void setPattern(String pattern) {
		this.pattern = pattern;
	}

	public void setServiceInterface(Class<?> serviceInterface) {
		this.serviceInterface = serviceInterface;
	}

	// FactoryBean 인터페이스 구현 메소드
	@Override
	public Object getObject() throws Exception {
		TransactionHandler txHandler = new TransactionHandler();
		txHandler.setTarget(target);
		txHandler.setTransactionManager(transactionManager);
		txHandler.setPattern(pattern);
		return Proxy.newProxyInstance(
			getClass().getClassLoader(),new Class[] { serviceInterface }, txHandler);
		
		// DI 받은 정보를 이용해서 다이내믹 프록시를 생성합니다.
	}

	public Class<?> getObjectType() {
		return serviceInterface;
	}

	public boolean isSingleton() {
		return false;
	}
}
// xml 설정
<bean id="userService" class="txProxyFactoryBean 경로">
	프로퍼티 target : ref=userServiceImpl
		...
	프로퍼티 pattern : value=upgradeLevels
	프로퍼티 serviceInterface : value=UserService 인터페이스 경로
	// 빈 참조가 아닌 단순 값은 value를 사용하는데 클래스 경로도 value로 넣어줍니다.
```

이제 스프링 빈에서 생성되는 프록시 오브젝트에 대해 테스트 해야 하기 때문에 테스트가 간단하지 않습니다.  

- UserServiceTest에서 상관 없는 경우
  - add() : 트랜잭션이 적용되지 않으므로 다이내믹 프록시에서 걸러져 단순 위임 방식으로 작동
  - upgradeLevels(), mockUpgradeLevles() : 목 오브젝트를 이용한 테스트로 만들어져 트랜잭션과 무관합니다.

- 문제가 되는 경우
  - upgradeAllOrNothing() : 롤백을 확인하려면 테스트 메소드에서만 비즈니스 로직 코드를 수정한 TestUserService(내부 클래스)를 타깃 오브젝트로 사용해야 합니다.

가장 큰 문제는 타깃인 UserServiceImpl에 대한 래퍼런스를 TransactionHandler가 갖고있고, TransactionHandler는 팩토리 빈 내부에서 만들어져서 사용될 뿐 참조할 방법이 없다는 것입니다.  


[![](https://mermaid.ink/img/eyJjb2RlIjoiZ3JhcGggTFJcbiAgICDtjKnthqDrpqzruYggLS0-fOyDneyEsXwg64uk7J2064K066-57ZSE66Gd7IucXG4gICAg7YG065287J207Ja47Yq4Ou2FjOyKpO2KuCAtLT587Zi47LacfCDri6TsnbTrgrTrr7ntlITroZ3si5xcbiAgICDri6TsnbTrgrTrr7ntlITroZ3si5wgLS0-VHJhbnNhY3Rpb25IYW5kbGVyXG4gICAg7Yyp7Yag66as67mIIC0tPnzsg53shLF8IFRyYW5zYWN0aW9uSGFuZGxlclxuICAgIO2Mqe2GoOumrOu5iCAtLT587ZSE66Gc7Y287YuwfCBVc2VyU2VydmljZUltcGw67YOA6rmDXG4gICAgVHJhbnNhY3Rpb25IYW5kbGVyIC0tPnzsnITsnoR8IFVzZXJTZXJ2aWNlSW1wbDrtg4DquYMiLCJtZXJtYWlkIjp7InRoZW1lIjoiZGFyayJ9LCJ1cGRhdGVFZGl0b3IiOmZhbHNlLCJhdXRvU3luYyI6dHJ1ZSwidXBkYXRlRGlhZ3JhbSI6ZmFsc2V9)](https://mermaid-js.github.io/mermaid-live-editor/edit#eyJjb2RlIjoiZ3JhcGggTFJcbiAgICDtjKnthqDrpqzruYggLS0-fOyDneyEsXwg64uk7J2064K066-57ZSE66Gd7IucXG4gICAg7YG065287J207Ja47Yq4Ou2FjOyKpO2KuCAtLT587Zi47LacfCDri6TsnbTrgrTrr7ntlITroZ3si5xcbiAgICDri6TsnbTrgrTrr7ntlITroZ3si5wgLS0-VHJhbnNhY3Rpb25IYW5kbGVyXG4gICAg7Yyp7Yag66as67mIIC0tPnzsg53shLF8IFRyYW5zYWN0aW9uSGFuZGxlclxuICAgIO2Mqe2GoOumrOu5iCAtLT587ZSE66Gc7Y287YuwfCBVc2VyU2VydmljZUltcGw67YOA6rmDXG4gICAgVHJhbnNhY3Rpb25IYW5kbGVyIC0tPnzsnITsnoR8IFVzZXJTZXJ2aWNlSW1wbDrtg4DquYMiLCJtZXJtYWlkIjoie1xuICBcInRoZW1lXCI6IFwiZGFya1wiXG59IiwidXBkYXRlRWRpdG9yIjpmYWxzZSwiYXV0b1N5bmMiOnRydWUsInVwZGF0ZURpYWdyYW0iOmZhbHNlfQ)

이런 경우 팩토리 빈 자체를 가져올 수 있음을 확인했으므로, TxProxyFactoryBean을 가져와 target 필드를 재구성 해준 뒤에 프록시 오브젝트를 생성하도록 요청합니다. 애초에 트랜잭션을 지원하는 프록시를 바르게 만들어주는지가 목적이므로 가장 간단한 방법입니다.  

```java
public class UserServiceTest {
	...
	@Autowired ApplicationContext context;
	// 팩토리 빈을 가져오기 위해 getBean()을 사용하는 애플리케이션 컨택스트가 필요합니다.
	...

	@Test
	@DirtiesContext	// 컨텍스트 무효화 어노테이션
	public void upgradeAllOrNothing() throws Exception {
		TestUserService testUserService = new TestUserService(users.get(3).getId());
		testUserService.setUserDao(userDao);
		testUserService.setMailSender(mailSender);
		
		TxProxyFactoryBean txProxyFactoryBean = 
			context.getBean("&userService", TxProxyFactoryBean.class);
			// 팩토리 빈 자체를 가져옵니다.
		txProxyFactoryBean.setTarget(testUserService);
		// UserSerViceTest 를 주입합니다.
		UserService txUserService = (UserService) txProxyFactoryBean.getObject();
		// 변경된 DI로 다시 프록시를 생성합니다.
				 
		userDao.deleteAll();			  
		for(User user : users) userDao.add(user);
		
		try {
			txUserService.upgradeLevels();   
			fail("TestUserServiceException expected"); 
		}
		catch(TestUserServiceException e) { 
		}
		
		checkLevelUpgraded(users.get(1), false);
	}	
}
```

TxProxyFactoryBean은 여러 개를 동시에 빈으로 등록해도 상관 없습니다. 각 빈의 타입은 타깃 인터페이스로 정해지기 때문입니다. 만약 UserService외에 트랜잭션 경계설정 기능을 부여해줘야 한다면 다음과 같이 추가해주면 됩니다.

```java
<bean id="coreService" class="TxProxyFactoryBean 경로">
	프러퍼티 target : ref="coreServiceTarget" (CoreServiceImpl 빈)
	...
```

이렇게 만들어본 다이내믹 프록시는 기존의 프록시의 두 가지 문제점을 해결해 줍니다.  
1. 타깃 클래스가 적용한 인터페이스를 구현하는 프록시 클래스를 일일이 만들어야 함
2. 부가적 기능 코드가 중복 됌

반면, 프록시 팩토리 빈의 한계도 있습니다. 하나의 클래스 안에 여러 개의 메소드에 부가기능을 한번에 제공했지만, 한번에 여러 개의 클래스에 공통적인 부가기능을 제공하는 것은 불가능 합니다. 즉, 비슷한 프록시 팩토리 빈의 설정이 중복되는 것을 막을 수 없습니다.  
또, 하나의 타깃에 여러 개의 부가기능을 적용하려 할때도 빈설정이 무수히 늘어나는 문제가 발생합니다.  
코드의 수정은 없지만 설정파일이 급격히 복잡해지게 됩니다.  
또 한 가지 문제점은, TransactionHandler가 타깃 오브젝트가 달라지면 매번 새로운 오브젝트를 만들어야 한다는 것입니다.  

### 4. 스프링의 프록시 팩토링 빈
지금까지의 문제를 스프링이 어떻게 해결책을 제시하는지 살펴볼 차례입니다.  
#### 4-1. ProxyFactoryBean
스프링은 서비스 추상화를 프록시 기술에도 동일하게 적용하고 있습니다. 즉, 스프링은 일괄된 방법으로 프록시를 만들 수 있게 도와주는 추상 레이어를 제공합니다. ProxyFactroyBean 입니다.  
ProxyFactoryBean은 순수하게 프록시를 생성하는 작업만을 담당하고 빈 오브젝트로 등록합니다.  
부가적인 기능은 별도의 빈에 둘 수 있습니다. ProxyFactoryBean에서 생성하는 프록시에서 사용할 부가기능은 MethodIntefceptor 인터페이스를 구현해서 만듭니다.  

MethodInterceptor와 InovcationHandler 는 비슷하지만 한 가지 다른점이 있습니다.  
**기존의 Handler의 invoke()는 타깃 오브젝트에 대한 정보가 없어서, 타깃이 Handler 구현 클래스를 알고 있어야 했습니다.(이렇게 고정되는 것이 한계의 원인이었습니다.)**  
MethodInterceptor의 invoke()는 프록시로부터 타깃 오브젝트에 대한 정보까지 함께 제공 받으므로, 독립적으로 만들어 질 수 있습니다. 따라서 MethodInterceptor오브젝트는 타깃이 여러 프록시에 함께 사용할수 있고, 싱글톤 빈으로 등록이 가능합니다.  

UserService를 보기전 Hello 예제로 돌아가서 살펴봅니다.

```java
public class DynamicProxyTest {
	...
	@Test
	public void proxyFactoryBean() {
		ProxyFactoryBean pfBean = new ProxyFactoryBean();
		pfBean.setTarget(new HelloTarget());
		pfBean.addAdvice(new UppercaseAdvice());
		// 타깃과 부가기능을 추가합니다.

		Hello proxiedHello = (Hello) pfBean.getObject();
		// 팩토리 빈이므로 생성된 프록시를 가져옵니다.
		
		assertThat(proxiedHello.sayHello("Toby"), is("HELLO TOBY"));
		assertThat(proxiedHello.sayHi("Toby"), is("HI TOBY"));
		assertThat(proxiedHello.sayThankYou("Toby"), is("THANK YOU TOBY"));
	}
	
	static class UppercaseAdvice implements MethodInterceptor {
		public Object invoke(MethodInvocation invocation) throws Throwable {
			String ret = (String)invocation.proceed();
			// 기존의 방식과 달리 타깃 오브젝트를 전달할 필요가 없습니다.
			// MethodInterceptor가 타깃 오브젝트의 정보를 알기 때문입니다.
			// Object ret = method.invoke(target, args); 기존의 방식입니다.
			return ret.toUpperCase();
			// 부가기능 적용
		}
	}
}
```
MethodInterceptor는 일종의 콜백 오브젝트로 proceed()로 타깃 오브젝트의 메소드를 내부적으로 실행합니다. MethodInterceptor의 구현 클래스는 공유 가능한 템플릿 처럼 동작합니다.  
그래서 싱글톤으로 두고 공유할 수 있습니다.  

> 다시보는 탬플릿/콜백 : 템플릿은 고정된 작업 흐름을 가진 코드를 재사용하는 부분입니다, 콜백은 바뀌는 부분으로 템플릿 안에서 호출되는 것을 목적으로 만들어진 오브젝트입니다. 단순히 작업 수행을 위해 사용됩니다.

특이한 점으로 ProxyFactoryBean에 MethodInterceptor를 설정할 경우, 수정자 메소드를 사용하는 것이 아닌 addAdvice()를 사용합니다. add라는 이름에서 알수 있듯이, 여러 개의 MethodInterceptor를 추가할 수 있습니다.  
InvocationHandler의 한계인 하나만으로 여러 개의 부가기능을 제공해줄 수 없는 프록시와, 새로운 부가기능을 추가할 때마다 늘어나는 프록시와 프록시 팩토리 빈의 문제를 해결했습니다.  
타깃 오브젝트에 적용하는 부가기능을 담은 오브젝트를 스프링에서는 adivce라고 부릅니다. 꼭 기억해 두도록 합니다.  
또, 기존에 프록시를 만들 때 반드시 제공해야 했던 정보가 Hello 인터페이스였습니다. 그래야만 다이내믹 프록시 오브젝트의 타입을 결정할 수 있었습니다. 하지만 ProxyFactoryBean을 사용하니 프록시가 구현해야 하는 Hello 인터페이스 코드가 사라졌습니다.  
이는, setInterfaces()를 이용해 지정해 줄 수도 있지만, ProxyFactoryBean은 자동검출 기능을 이용해 타깃 오브젝트가 구현하고 있는 인터페이스 정보를 알아낼 수 있습니다.  

MethodInterceptor는 여러 부가기능이 있지만, InvocationHandler에서 사용했던 pattern이라는 래퍼런스로 메소드를 선별하는 기능은 불가능합니다. 그 이유는 여러 프록시가 공유하게 만들어져 타깃 정보를 갖고 있지 않기 때문입니다. 판별 기준이 프록시마다 다를 수 있기에 특정 프록시에만 적용되는 패턴을 넣으면 문제가 됩니다.  

이 문제를 해결하려면 우리가 해왔던 분리를 이용하면 됩니다. MethodInterceptor에는 재사용 가능한 순수한 부가기능 제공 코드만 남겨두고 분리하는 것입니다. 대신 부가기능 적용 메소드를 선택하는 기능은 프록시에 넣습니다. 물론 프로시는 대리인역할을 하는것이 존재 이유므로, 선별 기능은 프록시에서 다시 분리하는 것이 낫습니다.  

기존의 방식에서 메소드를 판별하던 방식을 살펴봅니다.  

[![](https://mermaid.ink/img/eyJjb2RlIjoiZ3JhcGggTFJcbiAgICBBW-2UhOuhneyLnCDtjKnthqDrpqwg67mIXSAtLT587IOd7ISxfCBCW-uLpOydtOuCtOuvuSDtlITroZ3si5xdXG4gICAgQiAtLT5866qo65OgIOuplOyGjOuTnCDsmpTssq18IENbSW52b2NhdGlvbkhhbmRsZXIv67aA6rCA6riw64qlK-uplOyGjOuTnOyEoOuzhF1cbiAgICBDIC0tPnzsnITsnoR8IO2DgOq5gyIsIm1lcm1haWQiOnsidGhlbWUiOiJkYXJrIn0sInVwZGF0ZUVkaXRvciI6ZmFsc2UsImF1dG9TeW5jIjp0cnVlLCJ1cGRhdGVEaWFncmFtIjpmYWxzZX0)](https://mermaid.live/edit#eyJjb2RlIjoiZ3JhcGggTFJcbiAgICBBW-2UhOuhneyLnCDtjKnthqDrpqwg67mIXSAtLT587IOd7ISxfCBCW-uLpOydtOuCtOuvuSDtlITroZ3si5xdXG4gICAgQiAtLT5866qo65OgIOuplOyGjOuTnCDsmpTssq18IENbSW52b2NhdGlvbkhhbmRsZXIv67aA6rCA6riw64qlK-uplOyGjOuTnOyEoOuzhF1cbiAgICBDIC0tPnzsnITsnoR8IO2DgOq5gyIsIm1lcm1haWQiOiJ7XG4gIFwidGhlbWVcIjogXCJkYXJrXCJcbn0iLCJ1cGRhdGVFZGl0b3IiOmZhbHNlLCJhdXRvU3luYyI6dHJ1ZSwidXBkYXRlRGlhZ3JhbSI6ZmFsc2V9)

그림을 보면 부가기능을 가진 InvocationHandler가 타깃과 메소드 선정 알고리즘 코드에 의도하고 있는 것을 알 수 있습니다. 만약 타깃이 달라지거나 메소드 선정 방식이 다르면 InvocationHandler를 여러 프록시가 공유할 수 없습니다. DI를 통해 타깃과 선별기능을 분리한다 해도, 한번 빈으로 등록된 InvocationHandler **오브젝트**는, 오브젝트로서 특정 타깃을 위한 프록시에만 제한됩니다. 그래서 빈으로 등록하는 대신 팩토리빈 내부에서 매번 생성하도록(콜백처럼) 만들었습니다. 따라서 변경이나 확장이 필요하면 팩토리 빈 내의 프록시 생성 코드를 직접 변경해야 합니다. 결국 확장에 열려있지 못한 OCP의 원칙에 어긋났습니다.  
이제 스프링의 ProxyFactoryBean 구조를 봅니다.  

[![](https://mermaid.ink/img/eyJjb2RlIjoiZ3JhcGggTFJcbiAgICBBW1Byb3h5RmFjdG9yeUJlYW5dIC0tPnzsg53shLF8IEJb64uk7J2064K066-5IO2UhOuhneyLnF1cbiAgICBCIC0tPnwxLuq4sOuKpeu2gOyXrCDrjIDsg4Eg7ZmV7J24fCBDW-2PrOyduO2KuOy7ty_rqZTshozrk5wg7ISg7KCVIOyVjOqzoOumrOymmF1cbiAgICBCIC0tPnwyLuyEoOygleuQnCDrqZTshozrk5zrp4wg7JqU7LKtfCBEW-yWtOuTnOuwlOydtOyKpC9NZXRob2RJbnRlcmNlcHRvci_rtoDqsIDquLDriqVdXG4gICAgRCAtLT58My58IEVbSW52b2NhdGlvbuy9nOuwsV0gLS0-fDQu7JyE7J6EfCBGW-2DgOq5g10iLCJtZXJtYWlkIjp7InRoZW1lIjoiZGFyayJ9LCJ1cGRhdGVFZGl0b3IiOmZhbHNlLCJhdXRvU3luYyI6dHJ1ZSwidXBkYXRlRGlhZ3JhbSI6ZmFsc2V9)](https://mermaid.live/edit#eyJjb2RlIjoiZ3JhcGggTFJcbiAgICBBW1Byb3h5RmFjdG9yeUJlYW5dIC0tPnzsg53shLF8IEJb64uk7J2064K066-5IO2UhOuhneyLnF1cbiAgICBCIC0tPnwxLuq4sOuKpeu2gOyXrCDrjIDsg4Eg7ZmV7J24fCBDW-2PrOyduO2KuOy7ty_rqZTshozrk5wg7ISg7KCVIOyVjOqzoOumrOymmF1cbiAgICBCIC0tPnwyLuyEoOygleuQnCDrqZTshozrk5zrp4wg7JqU7LKtfCBEW-yWtOuTnOuwlOydtOyKpC9NZXRob2RJbnRlcmNlcHRvci_rtoDqsIDquLDriqVdXG4gICAgRCAtLT58My58IEVbSW52b2NhdGlvbuy9nOuwsV0gLS0-fDQu7JyE7J6EfCBGW-2DgOq5g10iLCJtZXJtYWlkIjoie1xuICBcInRoZW1lXCI6IFwiZGFya1wiXG59IiwidXBkYXRlRWRpdG9yIjpmYWxzZSwiYXV0b1N5bmMiOnRydWUsInVwZGF0ZURpYWdyYW0iOmZhbHNlfQ)

스프링은 부가기능을 제공하는 오브젝트를 advice라 칭하고, 메소드 선정 알고리즘을 담은 오브젝트를 포인트컷이라고 부릅니다. 어드바이스와 포인트컷 모두 프록시에 DI로 주입해 공유 가능한 싱글톤 빈으로사용됩니다.  
포인트컷은 Pointcut인터페이스를 구현해서 만듭니다. 어드바이스는 기존의 MethodInterceptor에서 부가기능만 분리한 오브젝트로 타깃에 의존하지 않는 일종의 템플릿으로 구성돼있습니다.  
어드바이스가 부가기능을 부여하는 중에 타깃 메소드의 호출이 필요하면 프록시로부터 전달받은 콜백 오브젝트(MethodInterceptor 타입)의 proceed()를 호출하면 됩니다.  

**타깃 오브젝트에 대한 래퍼런스를 갖고 직접 타깃을 호출하는 것은 Invocation 콜백의 역할입니다.** 재사용 가능한 기능을 만들어 두고(어드바이스), 바뀌는 부분(콜백 오브잭트와 메소드 호출 정보)만 외부에서 주입해서 작업 흐름(부가기능 부여, 어드바이스)중에 사용하도록 하는 템플릿/콜백 구조입니다.  

어드바이스와 포인트 컷을 프록시로부터 독립시켜 DI를 사용하게 함으로, 프록시와 ProxyFactoryBean의 변경 없이 부가기능이나 메소드 선정 알고리즘만 바꿔 사용 할 수 있게 됩니다.

지금까지의 내용을 코드로 학습해봅니다.

```java
// 전에 만든 UppercaseAdvice를 사용하는 테스트 코드입니다.
// 스프링이 제공하는 NameMatchMethodPointcut을 이용합니다.
@Test
public void pointcutAdvisor(){
	ProxyFactoryBean pfBean = new ProxyFactoryBean();
	pfBean.setTarget(new HelloTarget);

	NameMatchMethodPointcut pointcut = new NameMatchMethodPointcut();
	// 메소드이름을 비교하는 선정 알고리즘/ 포인트컷
	pointcut.setMappedName("sayH*");	// sayH로 시작하는 모든 메소드를 선택

	pfBean.addAdvisor(new DefaultPointcutAdviser(pointcut, new UppercaseAdvice()));
	// 포인트컷과 어드바이스를 Advisor로 묶어서 추가합니다.

	Hello proxiedHello = (Hello)pfBean.getObject();

	assertThat(proxiedHello.sayHello("Hunny"), is("HELLO HUNNY"));
	assertThat(proxiedHello.sayHi("Hunny"), is("HI HUNNY"));
	assertThat(proxiedHello.sayThanYou("Hunny"), is("Thank You HUNNY"));
	// 포인트 컷 기준에 맞지 않으므로 대문자 변경이 되지 않아야 합니다.
}
```

포인트 컷이 없을 때는 addAdvice()로 어드바이스만 등록했지만, 이번에는 포인트컷을 어드바이스와 묶어서 addAdvisor()로 추가했습니다. ProxyFactoryBean에는 여러 개의 어드바이스와 여러 개의 포인트컷이 추가될 수 있기 떄문입니다. 포인트컷과 어드바이스를 따로 등록하면 어떤 부가기능에 대해 어떤 선정을 적용할지 모르게 됩니다. 이렇게 묶은 오브젝트를 어드바이저 라고 부릅니다.  

> 어드바이저 = 포인트컷(메소드 선정 알고리즘) + 어드바이스(부가기능)	반드시 외워두도록 합니다.

#### 4-2. ProxyFactoryBean 적용
우리가 구현했던 다이내믹 프록시인 TxProxFactoryBean을 ProxyFactoryBean으로 바꿔봅니다. transactionHandler의 코드에서 타깃과 메소드 선정 부분을 제거하고, MethodInterceptor를 구현한 adivce를 구현합니다.

```java
...
public class TransactionAdvice implements MethodInterceptor{
	PlatFormTransactionManager transactionManager;

	public void setTransactionManager(...){
		...
	}

	public Object invoke(MethodInvocation invocation) throws Throwable{
		// 콜백 오브젝트를 담당하는 invocatin입니다. 타깃의 정보를 알고 있습니다.
		TransactionStatus status = this.transactionManager.getTransaction(new DefalutTransactionDefinition());
		try{
			Object ret = invocation.proceed();
			// 콜백을 호출해서 타깃의 메소드를 실행합니다.
			// 타깃 메소드 호출 전후로 부가기능을 넣을 수 있습니다.
			this.transactionManager.commit(status);
			return ret;
		}catch(RuntimeException e){
			// Method와 달리 MethodInvocation은 예외가 포장되지 않습니다.
			롤백
		}

	}
}

//xml
<bean id="transactionAdvice">
	<property ...>
<bean id="transactionPointcut" class="org.springframework.aop.support.NameMatchMethodPointcut">
	<property name="mappedName" value="upgrade*" />
	// 포인트 컷은 스프링이 제공하는 클래스를 사용할 것이므로 별도의 클래스 없이 빈설정으로 사용합니다.
<bean id="transactionAdvisor" class="org.springframework.aop.support.DefalutPointcutAdvisor">
	<property name="advice" ref="transactionAdvice" />
	<property name="pointcut" ref="transactionPointcut" />
	// 어드바이저 역시 빈설정으로 사용합니다.

<bean id="userService" class="org.springframework.aop.famework.ProxyFactoryBean">
// userService 빈을 ProxyFactoryBean으로 설정합니다.
	...
	<property name="interceptorNames"> //어드바이스와 어드바이저가 list로 동시에 등록 가능한 프로퍼티명입니다.
		<list>	//list를 사용하므로, ref애트리뷰트이지만 value값을 사용합니다.
			<value>transactionAdvisor</value>
			// 한개 이상의 value 태그가 가능합니다.
```

마지막으로 테스트 검증도 해야합니다. UserService가 제공하는 기능의 테스트는 프록시 구현이나 설정방식에 영향을 받지 않지만,(메소드 선정도 upgrade로 시작하는 것으로 제한했습니다.)  
upgradeAllOrNothing()만큼은 프록시의 부가기능인 트랜잭션 적용을 테스트 해야하므로 테스트코드를 수정합니다.

```java
@Test
@DirtiesContext	//컨텍스트 설정을 여전히 변경하게 됩니다.
public void upgradeAllOrNothing(){
	TestUserService testUserService = new TestUserService(users.get(3).getId());
	testUserService.setUserDao(userDao);
	testUserService.setMailSender(mailSender);

	ProxyFactoryBean txProxyFactoryBean = context.getBean("$userService", ProxyFactoryBean.class);
	// 이곳이 컨텍스트 설정을 변경합니다. userService 빈이 xml설정과 다르게 스프링의 ProxyFactoryBean 그자체로 변경 했습니다.
	// &를 안붙이면 프록시팩토리빈으로 만들어진 userService타입의 오브젝트가 리턴됩니다.
	// 선언된 타입을 기존에 만들었던 TxProxyFactoryBean에서 스프링의 ProxyFactoryBean으로 변경했습니다.
	txProxyFactoryBean.setTarget(testUserService);
	UserService txUserService = (UserService)txProxyFactoryBean.getObject();
	// getObject()로 프록시를 가져옵니다.
}
```

ProxyFactoryBean은 스프링의 DI, 템플릿/콜백, 서비스 추상화 등의 기법이 적용된 것입니다. 그덕에 여러 프록시가 공유할 수 있고 확장할수 있는 독립성을 가졌습니다. UserService외에 새로운 비즈니스 로직 클래스에서도 TransactionAdvice를 그대로 사용할 수 있습니다. 부가기능 변경이나 메소드 선정 방식의 변경, 확장이 필요하다면, xml설정만 변경하면 됩니다.  

하나의 어드바이스(부가기능)을 이용해 2가지 방식으로 구현하는 경우를 그림으로 표현합니다.  

[![](https://mermaid.ink/img/eyJjb2RlIjoiZ3JhcGggTFJcbiAgICBBW1Byb3h5RmFjdG9yeUJlYW5dIC0tPnzri7Tqs6DsnojsnYx8IEJbQSBBZHZpc29yXVxuICAgIEIgLS0-fOuLtOqzoOyeiOydjHwgQ1tBIHBvaW50Y3V0IC8g66mU7IaM65OcIOyEoOuzhF1cbiAgICBCIC0tPnzri7Tqs6DsnojsnYx8IERbTWV0aG9kSW50ZXJjZXB0b3Ig6rWs7ZiEIC8gQWR2aWNlIC8g67aA6rCA6riw64qlIC_thZztlIzrpr9dXG4gICAgQSAtLT58QSBBZHZpc29y66W8IERJ7ZW07IScIOq1rO2YhO2VmOuKlCDtgbTrnpjsiqR8IEVbVXNlclNlcnZpY2UgLyDri6TsnbTrgrTrr7kg7ZSE66Gd7IucIC8g7YOA6rmDIOyduO2EsO2OmOydtOyKpOydmCDtg4DsnoXsnLzroZwg7J6Q64-ZIOyDneyEsV1cbiAgICBBIC0tPnztg4DquYMg7KCV67O0IOyghOuLrHwgR1xuICAgIEQgLS0-fOy9nOuwsXwgR1tNZXRob2RJbnZvY2F0aW9uIC8gaW52b2tl66mU7IaM65Oc7J2YIO2MjOudvOuvuO2EsCAvIOy9nOuwsV1cbiAgICBHIC0tPnzsnITsnoR8IEZb7YOA6rmDIOyYpOu4jOygne2KuF1cbiAgICBIW1Byb3h5RmFjdG9yeUJlYW5dIC0tPnxCIEFkaXZvc3LrpbwgREntlbTshJwg6rWs7ZiE7ZWY64qUIO2BtOuemOyKpHwgSVtCIFNlcnZpY2VdXG4gICAgSCAtLT5864u06rOgIOyeiOydjHwgSltCIEFkdmlzb3JdXG4gICAgSiAtLT5864u06rOgIOyeiOydjHwgRFxuICAgIEogLS0-fOuLtOqzoCDsnojsnYx8IEtbQiBwb2ludGN1dF1cbiAgICBIIC0tPnztg4DquYMg7KCV67O0IOyghOuLrHwgR1xuICAgIEEgLS0-fOuLtOqzoCDsnojsnYx8IEZcbiAgICBIIC0tPnzri7Tqs6Ag7J6I7J2MfCBGIiwibWVybWFpZCI6eyJ0aGVtZSI6ImRhcmsifSwidXBkYXRlRWRpdG9yIjpmYWxzZSwiYXV0b1N5bmMiOnRydWUsInVwZGF0ZURpYWdyYW0iOmZhbHNlfQ)](https://mermaid.live/edit#eyJjb2RlIjoiZ3JhcGggTFJcbiAgICBBW1Byb3h5RmFjdG9yeUJlYW5dIC0tPnzri7Tqs6DsnojsnYx8IEJbQSBBZHZpc29yXVxuICAgIEIgLS0-fOuLtOqzoOyeiOydjHwgQ1tBIHBvaW50Y3V0IC8g66mU7IaM65OcIOyEoOuzhF1cbiAgICBCIC0tPnzri7Tqs6DsnojsnYx8IERbTWV0aG9kSW50ZXJjZXB0b3Ig6rWs7ZiEIC8gQWR2aWNlIC8g67aA6rCA6riw64qlIC_thZztlIzrpr9dXG4gICAgQSAtLT58QSBBZHZpc29y66W8IERJ7ZW07IScIOq1rO2YhO2VmOuKlCDtgbTrnpjsiqR8IEVbVXNlclNlcnZpY2UgLyDri6TsnbTrgrTrr7kg7ZSE66Gd7IucIC8g7YOA6rmDIOyduO2EsO2OmOydtOyKpOydmCDtg4DsnoXsnLzroZwg7J6Q64-ZIOyDneyEsV1cbiAgICBBIC0tPnztg4DquYMg7KCV67O0IOyghOuLrHwgR1xuICAgIEQgLS0-fOy9nOuwsXwgR1tNZXRob2RJbnZvY2F0aW9uIC8gaW52b2tl66mU7IaM65Oc7J2YIO2MjOudvOuvuO2EsCAvIOy9nOuwsV1cbiAgICBHIC0tPnzsnITsnoR8IEZb7YOA6rmDIOyYpOu4jOygne2KuF1cbiAgICBIW1Byb3h5RmFjdG9yeUJlYW5dIC0tPnxCIEFkaXZvc3LrpbwgREntlbTshJwg6rWs7ZiE7ZWY64qUIO2BtOuemOyKpHwgSVtCIFNlcnZpY2VdXG4gICAgSCAtLT5864u06rOgIOyeiOydjHwgSltCIEFkdmlzb3JdXG4gICAgSiAtLT5864u06rOgIOyeiOydjHwgRFxuICAgIEogLS0-fOuLtOqzoCDsnojsnYx8IEtbQiBwb2ludGN1dF1cbiAgICBIIC0tPnztg4DquYMg7KCV67O0IOyghOuLrHwgR1xuICAgIEEgLS0-fOuLtOqzoCDsnojsnYx8IEZcbiAgICBIIC0tPnzri7Tqs6Ag7J6I7J2MfCBGIiwibWVybWFpZCI6IntcbiAgXCJ0aGVtZVwiOiBcImRhcmtcIlxufSIsInVwZGF0ZUVkaXRvciI6ZmFsc2UsImF1dG9TeW5jIjp0cnVlLCJ1cGRhdGVEaWFncmFtIjpmYWxzZX0)

그림을 보면 알 수 있듯이, ProxyFactoryBean(스프링 설정의 빈)이 구현한 Service 프록시(실제 빈 오브젝트)들은 독립적입니다. 타깃 오브젝트들은 ProxyFactoryBean의 xml 설정에 따라 결정됩니다. 타깃 오브젝트(userServiceImpl / 변하지 않는 기능)의 모든 메소드를 구현하는 userService타입의 프록시 클래스를 ProxyFactoryBean이 만들어 줍니다.

### 5. 스프링 AOP
#### 5-1. 자동 프록시 생성
타깃 코드는 깔끔한 채로 남아있고, 부가기능은 싱글톤으로 모든 타깃과 메소드에 재사용 되고(원래는 타깃 오브젝트마다 새로 만들어야 했습니다.), 타깃의 메소드 선별 방식도 분리했습니다.  
하지만 아직 한 가지 문제가 있습니다. 바로 부가기능 적용이 필요한 타깃 오브젝트마다 비슷한 내용의 ProxyFactoryBena 설정을 추가해야 하는 것입니다.  

우리는 변하지 않는 재사용 가능한 부분과 바뀌는 부분을 분리한 템플릿/콜백 전략 패턴으로 중복을 제거했었고, 다이내믹  프록시라는 런타임 코드 자동생성 기법을 사용해 프록시 클래스를 만들어서 위임과 부가기능 코드를 중복되지 않게하는 두가지 중복 제거 방법을 보았습니다.  
타깃으로의 위임과 부가기능 적용 대상 선별은 다이내믹 프록시에게 맡기고, 변하는 부가기능 코드(어드바이스)는 별도로 만들어서 프록시 팩토리에 DI로 제공하는 방법을 사용한 것입니다.  
만약 타깃 빈의 목록을 제공하면 자동으로 각 타깃의 빈에 대한 프록시를 만들어준다면 xml설정 파일을 이용해 ProxyFactoryBean 프로퍼티 설정을 매번 추가할 필요가 없을테지만, 아쉽게도 불가능합니다.  

OCP의 가장 중요한 요소는 유연한 확장입니다. 그래서 스프링은 스스로도 OCP의 가치를 따릅니다. 스프링이 제공하는 기능 중에서 변하지 않는 핵심적인 부분 외에는 대부분 **확장**할 수 있도록 확장 포인트를 제공합니다. 우리가 관심가질만한 확장 포인트는 BeanPostProcessor 인터페이스를 구현해서 만드는 빈 후처리기 입니다.  
빈 후처리기란 스프링 빈 오브젝트로 만들어지고 난 후에, 빈 오브젝트를 다시 가공할 수 있게 합니다.  

사용 방법은 간단합니다. 빈 후처리기 자체를 빈으로 등록합니다. 스프링은 빈 후처리기가 빈으로 등록되어 있으면 빈 오브젝트가 생성될 때마다 빈 후처리기에게 후처리 작업을 요청합니다.  
이를 잘 이용하면 스프링이 생성하는 빈 오브젝트의 일부를 프록시로 포장해서 빈으로 대신 등록할 수도 있습니다.  

DefaultAdvisorAutoProxyCreator는 스프링이 제공하는 빈 후처리기 입니다. 이름에서 알 수 있듯이 어드바이저를 이용한 자동 프록시 생성기입니다.  
이 빈 후처리기는 빈으로 등록된 모든 어드바이저 안의 포인트컷을 이용해 스프링으로부터 전달받은 빈이 프록시 적용 대상인지 확인합니다.  
적용 대상일 경우 내장된 프록시 생성기에게 전달받은 빈에 대한 프록시를 만들게 하고, 만들어진 프록시에 어드바이저를 연결해줍니다.  
빈 후처리기는 원래 빈 오브젝트 대신 만들어진 어드바이저를 컨테이너에게 돌려줍니다. 컨테이너는 빈 후처리기가 돌려준 오브젝트를 빈으로 등록하고 사용합니다.  

포인트 컷은 사실 메소드만 선별할 뿐 아니라 ClassFilter를 이용해 클래스 선별 기능도 갖고 있습니다. 두 기능을 모두 사용하면 먼저 클래스를 선별하고 메소드를 선별합니다.  
ProxyFactoryBean에서 포인트컷은 타깃에 대한 정보가 있으므로 클래스를 선별할 필요가 없었지만, DefalutAdvisorAutoProxyCreator는 클래스와 메소드 선정 알고리즘을 모두 갖고있는 포인트컷과 어드바이스가 결합되어 있는 어드바이저가 등록되어있어야 합니다.  

클래스를 선별하는 예시를 코드로 보겠습니다.
```java
@Test
public void classNamePointcutAdvisor(){
	NameMatchMethodPointcut classMethodPointcut = new NameMatchMethodPointcut(){
		// 내부 익명 클래스 방식으로 클래스를 선별합니다.
		public ClassFilter getClassFilter(){
			return new ClassFilter(){
				// 다시 내부 익명 클래스입니다.
				@Override
				public boolean matches(Class<?> clazz){
					return clazz.getSimpleName().startsWith("HelloT");
					// HelloT로 시작하는 클래스만 선정합니다.
					// 걸러 지므로 부가기능이 제공 되지 않게됩니다.
				}
			};
		}
	};

	classMethodPointcut.setMappedName("SayH*");	// 메소드 선별
}
```

#### 5-2. DefaultAdvisorAutoProxyCreator의 적용
이제 실제로 적용해봅니다. 새로운 클래스를 하나 만듭니다. NamedMatchMethodPoincut을 상속하고 classfilter를 정의합니다.

```java
public class NameMatchClassMethodPointcut extends NameMatchMethodPointcut {
	public void setMappedClassName(String mappedClassName) {
		this.setClassFilter(new SimpleClassFilter(mappedClassName));
		// 프로퍼티로 받은 클래스 이름을 이용해 필터를 적용합니다.
	}
	
	static class SimpleClassFilter implements ClassFilter {
		String mappedName;
		
		private SimpleClassFilter(String mappedName) {
			this.mappedName = mappedName;
		}

		public boolean matches(Class<?> clazz) {
			return PatternMatchUtils.simpleMatch(mappedName, clazz.getSimpleName());
			// 와일드 카드가 들어간 문자열 비교를 지원하는 스프링의 유틸리티 메소드 입니다.
		}
	}
}
//빈 후처리기를 빈으로 등록합니다.
<bean class="org.springframework.aop.framework.autoproxy.DefalutAdvisorAutoProxyCreator" />
// 다른 빈에서 참조될 필요가 없는 빈이라 id를 설정하지 않아도 됩니다.
```

이후 기존의 포인트컷 설정을 제거하고 새로 작성합니다.

```java
<bean id="transactionPointcut" class=NameMatchClassMethodPointcut 경로>
	<property name="mappedClassName" value="*ServiceImpl" /> //클래스 이름 패턴
	<property name="mappedName" value="*upgrade*">
```

어드바이스와 어드바이저는 변경 할 필요가 없습니다. 다만 어드바이저의 방식이 빈 후처리기가 돌려주는 포인트컷을 DI하도록 바뀌었습니다.  
프록시를 도입하고 부터, 프록시에 DI돼 간접적으로 타깃으로 사용되야 했던 userServiceImpl 빈의 아이디를 userService로 돌려 놓을 수 있게 됐습니다.  
더 이상 명시적인 프록시 팩토리 빈을 등록하지 않기 떄문입니다. 기존의 ProxyFactoryBean 빈 은 제거하고, userServiceImpl빈의 이름을 변경합니다.  

이제 테스트를 변경합니다. **@Autowired를 이용해 컨텍스트에서 가져오는 userService빈은 UserServiceImpl이 아니라, 트랜잭션이 적용된 프록시여야 합니다.**  
이를 검증하는 upgradeAllOrNothing() 테스트는 타깃을 코드에서 바꿔치기 했지만, 자동 프록시 생성기를 이용한 방법에서는 바꿔치기가 불가능합니다.  
자동 프록시 생성기는 스프링 컨테이너에 종속적인 기법이라 예외상황을 위한 테스트 대상도 빈으로 등록해야 합니다. 또한, 자동 프록시 생성기의 선별로 걸러진 대상이기에 적용이 됐는지도 빈을 통해 확인해야 합니다. 내부 스태틱 클래스인 TestUserService를 빈으로 등록합니다.  

문제는 내부 클래스라는 점과 클래스 이름 패턴이 *ServiceImpl로 되어있어서 TestUserService가 빈으로 등록되도 프록시 적용 대상에서 벗어납니다.  
우선 이름을 TestUserServiceImpl로 변경하고, xml 설정에서는 UserServiceTest의 경로에 $TestUserServiceImpl을 붙여주면 됩니다.  

```java
static class TestUserServiceImpl extends UserServiceImpl{
	private String id = "madnite1";	// 프록시 생성기에 의해 만들어진 빈이기 떄문에 픽스처를 사용할 수 없습니다.
	// users(3)의 id값을 고정시킵니다.

	protected void upgradeLevel(User user){
		if(user.getId().equals(this.id)) throw new TestUserServiceException();
		super.upgradeLevel(user);
		// 트랜잭션이 적용되어 롤백되어야 합니다.
		// 트랜잭션 코드가 없지만 어드바이스에 의해 부가기능이 부여된 프록시이므로 트랜잭션 기능이 있게됩니다.
	}
}

<bean id="testUserService" class="UserServiceTest경로.$TestUserServiceImpl" parent="userService" />
// parent 애트리뷰트는 상속받은 클래스의 xml 설정 내용을 받아올 수 있습니다.
// 별도의 userDao나 mailSender를 지정해주지 않아도 됩니다.

// 이제 프록시 생성 메소드 대상인 upgradeAllOrNothing()을 수정합니다.
public class UserServiceTest{
	@Autowired
	UserService userService;	// Impl
	@Autowired
	UserService testUserService;	// TestUserImpl
	...

	@Test	// 이제는 컨텍스트 빈 설정을 변경하지 않습니다.
	public void upgradeAllOrNothing(){
		userDao.deleteAll();
		for(User user : users) userDao.add(user);

		try{
			this.testUserService.upgradeLevles();
			fail("TestUserServiceException expeted");
		}
		...
		// xml을 사용하면서 기존에 testUserService에 DI하는 코드가 사라졌고,
		// ProxyFactoryBean자체를 가져와 타깃을 바꿔 주던 코드가 사라졌습니다.
	}
}
```

다시 한번 정리해 봅니다.  
1. 자동 프록시 생성기인 DefalutAdvisorAutoProxyCreator는 xml에 등록된 빈 중에서 Advisor 인터페이스(포인트컷과 어드바이스를 담음)를 구현한 것을 모두 찾습니다.
2. 모든 빈에 대해 빈이 생성 될 때 어드바이저 안에 포인트컷으로 프록시 적용 대상을 선정합니다.
3. 해당 빈 클래스가 선정 대상이라면 프록시를 만들어 생성된 빈 대신 프록시 오브젝트를 돌려줍니다.
4. 원래의 빈 오브젝트는 돌려준 프록시와 연결되어 프록시를 통해서만 접근 가능해집니다.
5. 즉, 타깃 빈에 의존한다고 정의한(프로퍼티로 등록한) 다른 빈들은 프록시 오브젝트를 대신 DI 받게 됩니다.
6. 원래 빈은 트랜잭션이 없는 클래스지만, 프록시는 자동 프록시 생성기로 선택돼 어드바이스 부가 기능을 부여받습니다.
7. 프록시는 invoke()를 통해 타깃의 모든 메소드를 일관된 방식으로 부가기능을 사용하게 합니다.(invoke메소드의 파라미터 MethodInvocation이 타깃의 정보를 담고 있습니다.)

위의 테스트를 통해 testUserService 빈을 자동으로 트랜잭션 부가기능을 제공해주는 프록시로 대체했는지 upgradeAllOrNothing()으로 확인합니다.  
한 가지 더 확인할 것은 아무 빈에나 트랜잭션 부가기능이 적용되는 것은 아닌지 확인합니다. 설정파일의 클래스 이름 패턴을 변경하면 테스트를 실패하게 되므로 검증합니다.  
혹은 getBean("testUserService")로 가져온 오브젝트는 TestUserServiceImpl 타입이 아니라 JDK의 Proxy타입이므로, 다음과 같이 검증할 수 도 있습니다.

```java
@Test
public void advisorAutoProxyCreator(){
	assertThat(testUserService, is(java.lang.reflect.Proxy.class));
}
```

#### 5-3. 포인트컷 표현식을 이용한 포인트컷
조금 더 복잡한 패턴을 줄 수도 있습니다. 리플랙션 API는 클래스와 메소드의 이름, 패키지, 파라미터, 리턴값, 애노테이션 등등 모든 정보를 알아낼 수 있기 떄문입니다. 하지만 이를 구현하기는 번거롭습니다. 스프링은 정규식이나 EL과 비슷한 일조의 표현식 언어를 사용해 포인트컷을 작성하게 해줍니다. 바로 포인트컷 표현식(pointcut expression)입니다.  
포인트컷 표현식을 지원하는 포인트컷을 적용하려면 AspectExpressionPointCut 클래스를 사용합니다. 포인트컷 표현식은 RegEx클래스의 정규식처럼 간단한 문자열로 복잡한 선정조건을 만들어 냅니다. 이름을 보면 알 수 있듯이 AspectJ 프레임워크에서 제공하는 것을 가져와 확장해 사용합니다.  

AspectJ 포인트컷 표현식은 포인트컷 지시자인 execution()을 이용해 작성합니다.

> excution( [접근제한자 패턴] 리턴타입패턴 [패키지.클래스타입 패턴] 메소드이름패턴 (파라미터 타입패턴 | "..",...) );

[]은 생략 가능하고, |은 OR의 의미입니다. 복잡하다면 리플랙션을 이용해 Target클래스의 minus()를 가져와서 풀 시그니처를 가져와 풀이해봅니다.  

```java
System.out.println(Target.class.getMethod("minus", int.class, .int.class));

// 출력 결과
public int springbook.learningtest.spring.pointcut.Target.minus(int,int) throws java.lang.RuntimeException
```

하나씩 살펴봅니다.
- public : 접근제한자입니다. 생략가능합니다.(조건 부여하지 않음)
- int : 리턴값의 타입을 나타냅니다. *을 써서 모든 타입을 선택할 수 있습니다.
- springbook.learningtest.spring.pointcut.Target : 패키지와 타입이름을 포함하는 클래스의 타입 패턴입니다. 생략가능합니다. 바로 뒤의 메소드 이름패턴과 .으로 연결되기에 잘 구분해야합니다. *을 사용할 수있고, ..을 사용하면 한번에 여러개의 패키지를 선택할 수 있습니다.
- minus : 메소드 이름 패턴입니다. *을 사용할 수 있습니다.
- (int, int) : 메소드 파라미터의 타입 패턴입니다. 파라미터의 타입들을 ,로 구분하여 적습니다. 없다면 ()만 적습니다. 개수와 타입 상관없이 허용하려면 ..을 넣습니다. ...을 이용하면 뒷부분의 파라미터 조건을 생략합니다.
- throws java.lang.RuntimeException : 예외 이름에 대한 패턴 타입입니다. 생략 가능합니다.

AspectJExpressionPointcut 클래스의 오브젝트를 만들어서 표현식을 이 오브젝트의 expression() 프로퍼티로 넣어주면 됩니다.  
테스트 코드로 살펴봅니다.

```java
// 테스트를 도와줄 메소드입니다.
public void pointcutMatches(String expression, Boolean expected, Class<?> clazz, String methodName, class<?>... args) throws Exception{
	// 순서데로 표현식, 결과, 클래스 이름 패턴, 메소드 이름 패턴, 파라미터 타입 패턴(... 으로 개수 제한을 두지않습니다.)
	AspectJExpressionPointcut pointcut = new AspectJExpressionPointcut();
	pointcut.setExpression(expression);
	// 주입받은 expression 으로 포인트컷 표현식을 생성합니다.

	assertThat(pointcut.getClassFilter().matches(clazz) && pointcut.getMethodMatcher().matches(clazz.getMethod(methodName, args), null),
	is(expected));
	// 클래스 필터와 메소드 매처를 각각 비교합니다. matches 메소드는 정규 표현식과 일치하는지 비교합니다.
	// boolean matches(Method method, Class<?> targetClass)으로, 타겟클래스는 null로 설정합니다.
}

@Test
public void pointcut() throws Excepion{
	tagetClassPointcutMatches("execution(* *(..))", true, true, true, true, true, true);
}

public void targetClassPointcutMatches(Stirng expression, boolean... expected) throws Exception{
	pointcutMatches(expression, expected[0], Target.class, "hello");
	...
	pointcutMatches(expression, expected[3], Target.class, "minus", int.class, int.class);
	...
}
```
이외에도 AspectJ 표현식은 빈의 이름으로 비교하는 bean()에도 쓰일 수 있고, 특정 애노테이션이 적용된 메소드를 선별할 수 도있습니다.  

- bean(*Service) : Service로 끝나는 빈을 가져옵니다.
- @annotaion(org.springframework.transacion.annotation.Trasactional) : @Trasactinal  이 적용된 메소드를 가져옵니다.

이제 사용법을 살펴보았으니 앞에서 만든 transactionPointcut 빈을 스프링이 제공하는 클래스로 변경합니다.

```java
<bean id="transacionPointcut" class="org.springframework.aop.aspectj.AspectJexpressionPointcut">
	<property name="expression" value="execution(* *..*ServiceImpl.upgrade*(..))" />
```

중요한 것은 기존에 단순히 mappeClassName 프로퍼티로 impl을 선별한 것과 포인트컷 표현식으로 impl을 선별한 것은 차이점이 있습니다.  
TestUserServiceImpl을 다시 TestUserService로 돌려 놓으면 선정대상으로 되지 않아야 하지만, 테스트는 멀쩡히 성공합니다.  
그 이유는 표현식의 클래스 이름 패턴이 아니라 클래스 **타입** 패턴 이기 때문입니다. 타입을 따져보자면 TestUserService의 슈퍼클래스인 UserServiceImpl이기도 하고, 구현 인터페이스인 UserService타입이기도 하고, 본인 자체로 TestUserService타입 이기도 합니다. 그렇기에 Impl로 끝나는 타입 패턴 조건에 충족합니다.  

#### 5-4. AOP란 무엇인가?
지금까지의 작업을 다시 복습해 봅니다.
1. 트래잭션 서비스 추상화

트랜잭션 경계설정 코드를 비즈니스 로직을 담은 코드에 넣으면서 특정 트랜잭션 코드에 종속되어 버렸습니다. JDBC를 이용한 트랜잭션 코드를, 다른 DB로 바꾸려면 모든 트랜잭션 코드를 수정해야했습니다. 그래서 서비스 추상화 기법을 이용해 트랜잭션 적용을 분리했습니다. 구현 방법을 담을 인터페이스를 선언해 연결관계를 느슨하게 하고, 구체적인 구현 내용을 담은 의존 오브젝트는 런타임 시에 다이내믹하게 DI해줍니다.

2. 프록시와 데코레이터 패턴

여전히 비즈니스 코드에 트랜잭션 코드가 나타납니다. 더 이상 단순한 추상화와 메소드 추출로는 분리해낼 수 없었습니다. 그래서 데코레이터 패턴을 적용했습니다. 트랜잭션의 코드는 데코레이터에 담겨서, 클라이언트와 비즈니스 로직을 담은 클래스 사이에 존재하고, 클라이언트 -> 프록시 -> 비즈니스 로직 을 통해 접근하는 구조로 만들었습니다.

3. 다이내믹 프록시와 프록시 팩토리 빈

비즈니스 로직 인터페이스의 모든 메소드마다 일일이 프록시 클래스를 만들어 줘야 했습니다. 프록시 오브젝트를 런타임 시에 만들어주는 ProxyFactoryBean을 사용하여 해결했습니다. 또 어드바이스와 포인트컷을 프록시에서 분리해 여러 프록시에서 공유해서 사용할 수 있게 됐습니다.

4. 자동 프록시 생성 방법과 포인트컷

xml 설정에서 빈마다 트랜잭션을 적용해야한다는 부담이 남았습니다. 빈 후처리기를 이용해 만들어진 빈을 프록시로 대체해주는 방법을 사용했습니다. 결국 어드바이스와 포인트컷을 완전 분리해냈습니다.

5. 부가기능의 모듈화
   
이처럼 부가기능은 스스로 독립적인 방식으로 존재하기 어렵습니다. 트랜잭션 부가기능이란 트랜잭션 기능을 추가해줄 다른 대상에게 의존해야 의미가 있기 때문입니다. 전통적인 방법으론 분리시킬 수 없습니다. 그래서 DI, 데코레이터 패턴, 다이내믹 프록시, 후 처리기, 자동 프록시 생성, 포인트컷 같은 기술을 사용해 TransactionAdvice라는 부가기능으로 독립적인 모듈화를 시킨 것입니다.

이런 트랜잭션 경계설정과 같은 부가기능의 모듈화는 기존의 객체지향 설계 패러다임과는 구분되는 특성이있어서, 오브젝트와는 다르게 특별한 이름으로 부릅니다. **애스펙트(aspect)**입니다.  

> 애스펙트 : 애플리케이션의 핵심기능은 아니지만, 구성하는 중요한 한 가지 요소이고, 핵심 기능에 부여되어 의미를 갖는 모듈. 어드바이저라고 봐도 됩니다.

기존에 핵심 기능(비즈니스 로직)에 부가기능들이 포함되어 복잡했다면, 핵심기능과 분리되고, 성격이 다른 부가기능들 끼리도 분리되어, 깔끔해지게 됩니다. 이렇게 핵심기능과 부가기능을 애스팩트로 분리해 설계하는 것을 **AOP(Aspect Oriented Programming, 애스펙트 지향 프로그래밍)**이라고 합니다. AOP는 OOP(객체지향)을 돕는 보조적인 기술이지, 대체하는 개념이 아닙니다.  
**이제 우리는 비즈니스 로직을 다룰 때는 비즈니스 로직 관점에서만 집중하고, 부가기능을 다룰 때는 부가기능에만 집중할 수 있게 됩니다. 이런 관점지향 프로그래밍이 AOP의 의미입니다.**  

#### 5-5. AOP 적용 기술
스프링 AOP의 핵심은 프록시를 사용했다는 것입니다. 따라서 JDK와 스프링 컨테이너 외에는 필요로하는 것이 없습니다. 이 프록시가 타깃 오브젝트의 메소드에 다이내믹하게 적용해주는 역할을 합니다.  
프록시를 사용하지 않는 AspectJ라는 AOP프레임워크도 있습니다. AspectJ는 프록시 처럼 간접적인 접근을 하지않고, 자동으로 타깃 오브젝트를 수정하는 직접적인 방법을 사용합니다.  
바이트 코드를 조작하므로 스프링보다 강력한 AOP 기능이 제공됩니다. 예를들면 타깃 오브젝트가 생성되는 순간 부가기능을 부여해주고 싶다면 프록시 방식에서는 불가능하지만 AspectJ는 가능합니다.  
타깃 오브젝트의 생성은 프록시 패턴을 적용할 수 있는 대상이 아니기 떄문입니다. 물론 대부분의 부가기능은 프록시 방식인 메소드의 호출 시점에 부여하는 것으로 충분합니다.  

#### 5-6. AOP의 용어
- 타깃 : 타깃은 부가기능을 부여할 대상입니다. 다른 부가기능을 제공하는 프록시가 될 수도 있습니다.
- 어드바이스 : 부가기능을 담은 모듈입니다. 오브젝트로 정의할 수 도있고 메소드레벨 에서 정의할 수도 있습니다.
- 조인 포인트 : 어드바이스가 적용될 수 있는 위치입니다. 스프링 AOP에서는 메소드의 실행 단계 뿐입니다. 타깃 오브젝트가 구현한 인터페이스의 모든 메소드는 조인 포인트가 됩니다.
- 포인트컷 : 어드바이스 적용 대상을 선별합니다. 스프링 AOP는 메소드를 선정합니다. execution을 이용해 표현식을 사용합니다.
- 프록시 : 클라이언트와 타깃 사이에 존재해 부가기능을 제공하는 오브젝트 입니다. DI를 통해 클라이언트에게 주입되고, 클라이언트의 메소드 호출을 타깃 대신 받아서 부가기능을 부여하고 타깃에게 위임합니다.
- 어드바이저 : 포인트컷 + 어드바이저 입니다. 스프링은 자동 프록시 생성기가 AOP 작업의 정보로 활용합니다.
- 애스팩트 : AOP의 기본 모듈입니다. 한 개 이상의 포인트컷과 어드바이스 조합으로 만들어지며 보통 싱글톤 형태 오브젝트 입니다. 따로 클래스 정의와 실체(오브젝트)의 구분이 없습니다. 어드바이저가 곧 애스팩트 입니다.

#### 5-7. AOP 네임 스페이스
스프링 AOP를 위해 추가한 어드바이저, 포인트컷, 자동 프록시 생성기 같은 빈들은 컨테이너에 의해 자동으로 인식돼서 특별한 작업을 위해 사용됩니다. DAO나 userService같은 빈과는 다릅니다.  
스프링 프록시 AOP를 적용하려면 4가지 빈이 필요합니다.

- 자동 프록시 생성기 : DefalutAdvisorAutoProxyCreator 클래스를 빈으로 등록합니다. 빈 후처리고서 동작합니다.
- 어드바이스 : 부가기능을 구현한 클래스를 빈으로 등록합니다. 유일하게 직접 구현하는 클래스입니다.
- 포인트컷 : AspectJExpressionPointcut을 빈으로 등록합니다.
- 어드바이저 : DefaultPointcutAdvisor 클래스를 빈으로 등록합니다.

굉장히 기계적인 방법이므로 AOP와 관련된 태그를 정의한 aop 스키마를 제공합니다. 네임스페이스로 aop를 접두어로 사용합니다.
```java
<aop:cofing>
	<aop:advisor>	// adivce를 ref 프로퍼티로 둡니다. pointcut애트리뷰트는 excution(표현식)을 사용합니다.
```

### 6. 트랜잭션 속성
트랜잭션 추상화를 적용할 때 그냥 넘어간것이 하나있습니다.

```java
TransactionStatus status = this.transactionManager.getTransaction(new DefaultTransactionDefinition());
```

바로 트랜잭션 메니저에서 트랜잭션을 getTransaction 해올 때 사용한 오브젝트 입니다. 이 DefaultTransactionDefinition이 무엇인지 알아봅니다.

#### 6-1. 트랜잭션 정의
트랜잭션 경계 안에서 진행된 작업은 반드시 모두 성공하거나 모두 롤백되야 합니다. 그런데 이 밖에도 트랜잭션의 동작 방식을 제어할 수 있는 몇가지 조건이 있습니다. 이 제어에 사용하는 것이 TransactionDefinition 인터페이스고 이를 구현한 클래스가 DefaultTransactionDefinition입니다.  

1. 트랜잭션 전파

트랜잭션 전파란 트랜잭션의 경계에서 이미 진행 중인 트랜잭션이 있을 때/없을 때 어떻게 동작할 것인가를 결정합니다.(A트랜잭션이 진행 중인데 B트랜잭션이 끼어드는 경우)

- PROPAGATION_REQUIRED : 가장 많이 사용됩니다. 진행 중인 트랜잭션이 없으면 새로 시작하고, 있으면 이에 참여합니다. 다양한 방식으로 결합해서 하나의 트랜잭션으로 구성합니다. Default...의 전파 속성은 이것입니다. 참여하게 되면 최초 트랜잭션이 경계까지 진행 되야 커밋됩니다.
- PROPAGATION_REQUIRES_NEW : 항상 새로운 트랜잭션을 시작합니다. 즉 항상 독자적입니다.
- PROPAGATION_NOT_SUPPORTED : 트랜잭션 없이 동작합니다. 진행 중인 트랜잭션이 있어도 무시합니다. 특별한 메소드만 제외하려고 할 때 포인트컷 작성이 복잡해질 경우 대신 사용할 수 있습니다.

트랜잭션 시작을 getTransaction()으로 사용하는 이유가 트랜잭션 전파 속성 떄문입니다. 항상 트랜잭션을 새로 시작하는 것이 아니라, 전파 속성과 현재 진행중인 트랜잭션의 존재 여부에 따라서 달라지기 때문입니다.  

2. 격리 수준

모든 DB 트랜잭션은 격리수준(isolation level)을 갖고 있습니다. 트랜잭션은 여러 개가 동시에 진행 될 수 있기 떄문입니다. 순차적으로 진행하면 필요 없겠지만 이럴 경우 성능에 많은 문제가 있게됩니다. 기본적으로 ISOLATION_DEFAULT 값을 따릅니다.

3. 제한시간

트랜잭션을 수행하는 제한시간을 설정할 수 있습니다. 기본 설정은 제한시간이 없습니다.

4. 읽기전용

lead only로 설정해두면 트랜잭션 내에서 데이터를 조작하는 시도를 막아줍니다. 또 성능이 향상 될 수도 있습니다. 트랜잭셩 정의를 바꾸고 싶다면 Defalut... 대신 TrasactionDefinition 오브젝트를 구현해서 DI 하면 됩니다. 하지만 이 방법으로 트랜잭션 속성을 변경하면 해당 어드바이스를 사용하는 모든 메소드의 트랜잭션 정의가 한번에 바뀝니다.  

#### 6-2. 트랜잭션 인터셉터와 트랜잭션 속성
패턴을 이용해 선별한것과 같이 적용하면 됩니다. TransactionAdvice를 다시 설계할 필요는 없습니다. 스프링이 트랜잭션 경계설정 어드바이스로 사용하도록 만든 TransactionInterceptor가 존재하기 떄문입니다. 이제부터 이 클래스를 이용합니다.  
TransactionInterceptor는 PlatformTransactionManger와 Properties 타입의 두 가지 프로퍼티(필드)를 갖습니다. Properties는 일종의 맵(컬랙션) 오브젝트 입니다.  
Properties 타입인 property name 은 transactionAttributes로, 트랜잭션 속성을 정의한 프로퍼티 입니다. 트랜잭션 속성은 TransactionDefinition 인터페이스의 네가지 속성 항목에 rollbackOn()이라는 메소드를 갖고 있는 TransactionAttribute 인터페이스로 정의됩니다. rollbackOn()은 어떤 예외가 발생하면 롤백할 것인가를 결정합니다.

기존의 TransactionAdvisor 코드를 보면 catch(RuntimeException e)가 롤백 대상인 예외 종류이고, new DefaultTransactionDefinition()이 네 가지 속성입니다.  
런타임 예외에만 롤백 시키게 설계한 이유는, 타깃 메소드가 체크 예외를 던지는 경우에는 이것을 의미 있는 리턴의 한 가지로 인식해서 트랜잭션을 커밋하기 때문입니다.  
기본적인 예외처리 원칙은 복구 불가능한 예외의 경우 런타임 예외로 포장해서 전달하는 방식을 따른다고 가정하기 떄문입니다.  
그런데 TransactonAttribute는 roobackOn()이라는 속성을 둬서 기본 원칙과 다른 예외처리가 가능하게 해줍니다. TransactionInterceptor가 TransactionAttribute를 Properties라는 맵 타입 오브잭트로 받는 이유는 메소드 패턴에 따라서 각기 다른 트랜잭션 속성을 부여하기 위함입니다.  

transactionAttributes 프로퍼티는 메소드 패턴과 트랜잭션 속성을 key와 value로 갖는 컬랙션입니다. 트랜잭션 속성으 문자열로 정의할 수 있습니다.  

```java
PROPAGATION_NAME, ISOLATION_NAME, readOnly, timeout_NNNN, -Ecxeption1, +Exception2
// 전파 방식, 격리수준, 읽기전용, 제한시간, 체크예외중에서 롤백대상으로 추가 여러개 지정 가능, 런타임예외중 롤백시키 않을 대상, 여러개 지정 가능
```

트랜잭션 전파 속성만 필수입니다. 순서는 상관 없습니다. 
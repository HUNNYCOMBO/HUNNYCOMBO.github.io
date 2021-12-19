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

## 서비스 추상화
5장에서는 지금까지 만든 DAO에 트랜잭션을 적용해보면서 스프링이 어떻게 성격이 비슷한 여러 종류의 기술을 추상화하고 이를 일관된 방법으로 사용하게 하는지 살펴봅니다.  

### 1. 사용자 레벨 관리 추가
우리는 단순히 UserDao를 이용한 CRUD기능을 만들었습니다. 이번에는 정기적으로 사용자의 활동내용윽 참고해서 레벨을 조정해주는 기능을 추가해봅니다.  
구현해야할 비지니스 로직은 다음과 같습니다.  

- 사용자 레벨은 BASIC, SILVER, GOLD 입니다.
- 가입 후 50회 이상 로그인하면 BASIC 에서 SILVER 레벨이 됩니다.
- SILVER 레벨 이면서 30번 이상 추천을 받으면 GOLD 레벨이 됩니다.
- 사용자 레벨의 변경 작업은 일정한 주기를 가지고 일괄적으로 진행됩니다.

#### 1-1. 필드 추가
DB는 varchar타입으로 선언하는 방법도있지만 각 레벨을 숫자화 해서 넣는 것이 더 편합니다. 이에 맞춰 User에 추가할 프로퍼티 역시 int 값이 되어야 하지만, 다른 종류의 정보를 넣는 실수를 해도 컴파일러가 체크하지 못하는 단점이 있습니다.  
그래서 자바 5 이상에서 제공하는 enum을 이용하는게 안전하고 편리합니다.  

```java
package springbook.user.domain;

public enum Level {
	BASIC(1), SILVER(2), GOLD(3);
    // 3개의 이넘 오브젝트. 들어갈 수 있는 값이 고정됐습니다.

	private final int value;
		
	Level(int value) {
		this.value = value;
        // DB에 저장할 값을 넣어줄 생성자 입니다.
	}

	public int intValue() {
		return value;
        // 값을 가져옵니다.
	}
	
	public static Level valueOf(int value) {
        // 값으로부터 Level 타입 오브젝트를 가져옵니다.
		switch(value) {
		case 1: return BASIC;
		case 2: return SILVER;
		case 3: return GOLD;
		default: throw new AssertionError("Unknown value: " + value);
		}
	}
}

```

다음은 User 클래스에 필드를 추가합니다. 로그인 횟수와, 추천수도 추가합니다.  

```java
public class User {
	String id;
	String name;
	String password;
	Level level;
	int login;
	int recommend;
	
	public User() {
	}
	
	public User(String id, String name, String password, Level level,
			int login, int recommend) { //생성자도 수정합니다.
		this.id = id;
		this.name = name;
		this.password = password;
		this.level = level;
		this.login = login;
		this.recommend = recommend;
	}


	public String getId() {
        ...
```

UserDaoJdbc와 테스트에도 필드를 추가해야합니다.

```java
// 픽스처 역시 수정합니다.

private void checkSameUser(User user1, User user2) {
		assertThat(user1.getId(), is(user2.getId()));
		assertThat(user1.getName(), is(user2.getName()));
		assertThat(user1.getPassword(), is(user2.getPassword()));
        // 아래부터 새로운 필드가 제대로 반영되었는지 비교하는 점검합니다.
		assertThat(user1.getLevel(), is(user2.getLevel()));
		assertThat(user1.getLogin(), is(user2.getLogin()));
		assertThat(user1.getRecommend(), is(user2.getRecommend()));

        // addAndGet() 에서 이 메소드를 사용하도록 합니다.
	}

// 클라이언트에서 테스트가성공하도록 변경합니다.
// enum을 이용한 set만 주의합니다.

// user를 get()
user.setLevel(Level.valueOf(rs.getInt("level")));

// update()
user.getLvel().intValue();
```

눈여겨볼 것은 Level 타입의 필드를 사용하는 부분입니다. enum 은 오브젝트이므로 DB에 저장될 수 있는 타입이 아닙니다. 따라서 정수형으로 변환해줘야 합니다.  
반대로 조회했을 떄는 valueOf()를 이용해 int의 값을 Level 타입 오브젝트로 만들어서 setLevl()에 넣어줍니다.

#### 1-2. 사용자 수정 기능 추가
사용자의 기본키인 id를 제외한 나머지 필드는 수정될 가능성이 많습니다. 이를 수정하는 테스트 메소드 먼저 만듭니다.  
User를 수정했을 때 원하는 로우가 수정됐는지 확인하기 위해, 변경한 로우 1개와 변경하지 않은 로우만 두고, checkSameUser()를 실행합니다.  
아래는 이를 성공시킬 udpate() 입니다.

```java
// 테스트
	@Test
	public void update() {
		dao.deleteAll();
		
		dao.add(user1);		// 수정할 사용자
		dao.add(user2);		// 수정하지 않을 사용자
		
		user1.setName("수정");
		user1.setPassword("springno6");
		user1.setLevel(Level.GOLD);
		user1.setLogin(1000);
		user1.setRecommend(999);
		
		dao.update(user1);
		
		User user1update = dao.get(user1.getId());
		checkSameUser(user1, user1update);
		User user2same = dao.get(user2.getId());
		checkSameUser(user2, user2same);
	}

// 메소드
public void update(User user) {
		this.jdbcTemplate.update(
				"update users set name = ?, password = ?, level = ?, login = ?, " +
				"recommend = ? where id = ? ", user.getName(), user.getPassword(), 
		user.getLevel().intValue(), user.getLogin(), user.getRecommend(),
		user.getId());
		
	}
```

#### 1-3. UserService.upgradeLevels()

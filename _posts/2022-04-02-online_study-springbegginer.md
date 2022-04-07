---
layout: single
title:  "인프런 강의 - 코드로 배우는 스프링 부트, 웹 MVC, DB 접근 기술(김영한)"
categories: spring
tags: [spring, ]
toc: true
toc_sticky : true
author_profile: false
sidebar:
    nav: "docs"
search: true
---

## 링크
+ [김영한 - 스프링 입문](https://www.inflearn.com/course/%EC%8A%A4%ED%94%84%EB%A7%81-%EC%9E%85%EB%AC%B8-%EC%8A%A4%ED%94%84%EB%A7%81%EB%B6%80%ED%8A%B8/dashboard)
+ [깃허브 바로가기](https://github.com/hunnycombo/springmvc)

## 자료
[스프링 입문 - 코드로 배우는 스프링 부트, 웹 MVC, DB 접근 기술 v2021-12-01_2.pdf](https://github.com/hunnycombo/hunnycombo.github.io/files/8402673/-.MVC.DB.v2021-12-01_2.pdf)


## 1. 프로젝트 환경설정

### 1.1. 프로젝트 생성
[스프링부트 프로젝트 생성](https://start.spring.io/)  

빌드관리툴은 gradle을 사용합니다. 스프링부트 버전은 (현시점) 2.6.6을 사용했습니다.  

+ Project Metadata
- Group : 보통 기업의 이름을 적습니다.
- Artifact : build의 결과물

+ Dependencies : 라이브러리 선택
- spirng web
- tymeleaf(템플릿 엔진)

를 선택한 후 generate하여 IDE(필자 vscode)에서 오픈합니다.  

vscode의 경우 마켓에서 spring dashboard, java, lombok 등 관련 확장 플러그인의 설치가 필요합니다.  

builld.gradle의 deepndecies를 보면 gradle을 통해 라이브러리가 관리되고 있는것을 확인할 수 있습니다.

```java
repositories {  // 라이브러리들을 다운로드 하는 repository
	mavenCentral()
}

dependencies {  // 선택한 라이브러리
	implementation 'org.springframework.boot:spring-boot-starter-thymeleaf'
	implementation 'org.springframework.boot:spring-boot-starter-web'
	testImplementation 'org.springframework.boot:spring-boot-starter-test'
}
```

스프링부트는 톰캣을 내장하고, 기본적으로 포트 8080을 사용합니다. localhost:8080의 주소로 웹어플리케이션 접속이 가능합니다.  

### 1.2. 라이브러리 살펴보기
빌드툴은 기본적으로 한 라이브러리에 관련된 모든 의존라이브러리를 가져옵니다. 


**spirng boot starter**
- spring-boot-srater-web의 tomcat : 내장된 was(web application server). 기존에는 따로 설치된 was에 java코드를 넣어서 사용했지만, 라이브러리가 자체적으로 was를 갖도록 발전했습니다.
- spring-boot-starter : core, logging, spring boot 등 필요한 모든 의존관계를 가져옵니다.
- logging의 slf4j : 로깅을 위한 인터페이스. 구현체로 log4j, logback을 갖고있습니다.
- test : JUnit, mockito, assertj 등 테스트코드를 위한 라이브러리
  
**테스트 라이브러리**
- junit : 테스트 **프레임워크**
- mockito : 목 라이브러리
- assertj : 테스트코드 작성을 돕는 라이브러리
- spirng-test : 스프링 통합 테스트 지원

### 1.3. view 환경설정
#### src - resources - static
정적페이지. 스프링 부트가 제공하는 기능으로 해당 경로에 index.html 파일을 작성하면 welcome page로 사용됩니다.  

> index.html


```html
<!DOCTYPE HTML>
<html>
<head>
 <title>Hello</title>
 <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
</head>
<body>
Hello
<a href="/hello">hello</a>
</body>
</html>
```

> [스프링부트 docs](https://docs.spring.io/spring-boot/docs/2.3.1.RELEASE/reference/html/spring-boot-features.html#boot-features-spring-mvc-welcome-page)


**thymeleaf 템플릿 엔진**
정적인 html에 동적인 기능을 부여합니다.  

**controller**
웹 진입의 첫번째. 요청의 주소값에 따라 연결된 메소드를 실행시킵니다.  

**main-java-group-project-SpringController.java**

```java
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;

@Controller //컨트롤러 역할을 부여하는 어노테이션
public class SpringController {
    
    @GetMapping("hello")    // "../hello"의 경로로 Get방식으로 들어오는 경우 해당 메소드를 실행
    public String hello(Model model){   // mvc의 model을 뜻합니다.
        model.addAttribute("data", "hello!!");
        // 첫번째 파라미터는 attribute의 이름, 두번째는 attribute의 값입니다.
        // 템플릿엔진 문법에 의해 data라는 attribute는 값으로 치환됩니다.
        return "hello";
        // 템플릿엔진의 hello.html을 보여줍니다.
    }
}


```
**resources/templates/hello.html**

```html
<!DOCTYPE HTML>
<html xmlns:th="http://www.thymeleaf.org">
    <!-- 타임리프 엔진 선언 부분. th태그를 사용합니다. -->
<head>
 <title>Hello</title>
 <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
</head>
<body>
<p th:text="'안녕하세요. ' + ${data}" >안녕하세요. 손님</p>
<!-- 타임리프 엔진을 선언해서 타임리프 문법을 사용할 수 있습니다.
컨트롤러를 통해 받은 attribute이름인 data를 자동으로 attributevalue로 치환해서 나타냅니다. -->
</body>
</html>
```

**localhost:8080/hello**
해당 주소로 템플릿엔진 페이지를 확인해봅니다.  

![공부자료1](https://user-images.githubusercontent.com/78904413/161382032-a20a7c93-3243-49c5-9747-31a44b651c69.png)  

위의 사진과 같이 동적인 기능을 부여하는 템플릿 엔진의 기능을 확인할 수 있습니다.  
일반 텍스트인 "안녕하세오. 손님"은 렌더링 되지 않았습니다.  

![공부자료2](https://user-images.githubusercontent.com/78904413/161382119-f5e8b5e7-1830-409f-a1a9-42a1e130a905.png)  

스프링부트는 기본적으로 templates폴더의 파일을 조회해서 렌더링 합니다.  
컨트롤러에서 리턴 값으로 문자를 반환하면 뷰 리졸버가 화면을 찾아서 처리합니다.  
resource:templates/{VieName}.html

**spring devtools 라이브러리**
[mavenrepository](https://mvnrepository.com/artifact/org.springframework.boot/spring-boot-devtools)  

해당 주소로 방문하여, gardle 의존설정에 devtools를 추가하면 코드변경시 재시작 없이 변경된 페이지를 확인할 수 있습니다.  

### 1.4. 빌드하고 실행하기
1. 어플리케이션 종료 후 콘솔(cmd)로 이동합니다.(IDE의 콘솔을 이용하는게 경로를 맞춰주므로 편리, javaHOME 오류시 IDE내의 jdk경로 확인할 것) 
2. ./gradle build 입력
3. build 경로의 libs에 springmvc-0.0.1-SNAPSHOT.jar 파일이 생성됩니다.(jar가 배포용 파일입니다.)


![공부자료2](https://user-images.githubusercontent.com/78904413/161383561-e72c45cd-cb14-4acc-b1a0-ce7c477c6155.png)  

**실행확인**
1. cd build/libs
2. java -jar springmvc-0.0.1-SNAPSHOT.jar

IDE의 run없이 웹어플리케이션이 동작하게됩니다.  

**./gradlew clean**
빌드를 삭제합니다.  

## 2. 스프링 웹 개발 기초
### 2.1. 정적 컨텐츠
스프링부트는 기본적으로 정적 컨텐츠를 지원합니다.  

> [스프링부트 docs](https://docs.spring.io/spring-boot/docs/2.3.1.RELEASE/reference/html/spring-boot-features.html#boot-features-spring-mvc-static-content)

어떤 프로그래밍(렌더링 등) 없이 파일 그대로 반영합니다.  
templates폴더에서 매핑된 컨트롤러가 없는 경우 static폴더에서 찾아서 있는 경우 리턴합니다.

![공부자료4](https://user-images.githubusercontent.com/78904413/161384270-ccdd76ab-6b1f-4af7-bd2e-f94646985dab.png)


### 2.2. mvc와 템플릿 엔진
model, view, controller로 분리된 방식입니다. 예전 model 1 방식의 경우 view와 controller가 분리되있지 않았습니다.  
view는 화면을 그리는데 집중하기위해 분리하게 되었습니다. 예제를 통해 다시 한번 동적html을 보겠습니다.  

**controller**
```java
 @GetMapping("hello-mvc")
    public String helloMvc(@RequestParam("name") String name, Model model){
        // @requestparam = 파라미터로 값을 넘길 때 사용합니다.        
        // 파라미터값으로 ?name=ddd 로 넘겼다면 메소드의 name 파라미터가 ddd로 값이 정해집니다.
        // string 값 name의 값은 ddd가 됩니다.
        model.addAttribute("name", name);
        // 모델의 name attribute의 값을 ddd로 설정합니다.
        return "hello-template";
    }
```

**hello-template.html**
```html
<html xmlns:th="http://www.thymeleaf.org">
<body>
<p th:text="'hello ' + ${name}">hello! empty</p>
<!-- 컨트롤러에서 받은 attribute의 값으로 치환합니다. -->
</body>
```

![제목 없음](https://user-images.githubusercontent.com/78904413/161384291-40aace7f-974b-4ae2-b463-45bc17ecaefb.png)  


### 2.3. API
Responsbody 어노테이션을 사용하면 뷰 리졸버가 작동하지 않습니다.(==페이지를 리턴하지 않습니다.)

**ResponsBody어노테이션을 사용**
- HTTP의 body에 문자 내용을 직접 반환합니다.
- viewResolver 대신에 HttpMessageConverter가 동작합니다.
- 문자처리는 StringHttpMessageConverter가 동작합니다.
- 객체처리는 MappingJackson2HttpMessageConverter가 동작합니다.(JSON)
- byte 처리 등 여러가지 HttpMessageConver가 기본으로 등록되어 있습니다.
- 클라이언트의 HTTP Accept헤더와 서버의 컨트롤러 반환 타입 정보를 조합해서 HttpMessageConver가 선택됩니다.

![5](https://user-images.githubusercontent.com/78904413/161385076-8b832ec2-9ac7-4508-b8c1-c2d83b6f4952.png)

코드로 살펴보겠습니다.  


```java
    @GetMapping("hello-string")
    @ResponseBody
    // reponsbody : http의 body에 직접 return 값을 넣는다는 의미입니다.
    public String helloString(@RequestParam(value = "name", required = false) String name){
        // required : 파라미터 입력이 필수인지 설정합니다.
        return "hello" + name;
        // 해당하는 페이지를 리턴하는 것이 아닌 데이터 그자체를 리턴합니다.
    }

    @GetMapping("hello-api")
    @ResponseBody
    public Hello helloApi(@RequestParam("name") String name){
        Hello hello = new Hello();
        hello.setName(name);
        return hello;
        // 객체를 JSON 방식으로 리턴하게 합니다.
    }

    static class Hello{
        // 내부클래스
        private String name;

        public String getName() {
            return name;
        }

        public void setName(String name) {
            this.name = name;
        }
        
    }
}

```

![6](https://user-images.githubusercontent.com/78904413/161385148-bafb62c8-a99a-4a12-ac7c-af6f3b24bdf4.png)  

JSON타입으로 객체가 전달된것을 확인할 수 있습니다.  



## 3. 회원 관리 예제 - 백엔드 개발
### 3.1. 비즈니스 요구사항 정리
- 데이터 : 회원id, 이름
- 기능 : 회원 등록, 조회
- 가상의 시나리오 : DB가 선정되지 안ㅇ흠

**일반적인 웹 어플리케이션 계층 구조**
![7](https://user-images.githubusercontent.com/78904413/161385299-021aa08a-0f33-4fa6-b78a-65cf6375ebeb.png)
- 컨트롤러 : 웹 MVC의 컨트롤러 역할
- 도메인객체 : 회원, 주문, 쿠폰 등 주로 데이터베이스에 저장되고 관리되는 **비즈니스 도메인 객체**
- 서비스 : 도메인 객체를 이용하여 핵심 비즈니스 로직을 구현
- 리포지토리 : 데이터베이스에 접근, 도메인 객체를 DB에 저장하고 관리

**클래스 의존 관계**
![8](https://user-images.githubusercontent.com/78904413/161385429-04307290-3b0a-4f32-a404-86de2481faca.png)
- MemberRepository : DB가 선정되지 않아서 인터페이스로 구현 클래스를 변경할 수 있도록 설계합니다.
- 초기 개발단계에는 가벼운 메모리기반의 DB를 사용합니다.

**src/main/domain/Member.java**
```java
public class Member {
    // 비즈니스 domain 객체로 관련 행위(메소드)를 가질 수 있습니다. 
    private Long id;
    // 시스템이 저장하는 id(db의 pk에 대응한다 봐도 무방)
    private String name;
    
    public Long getId() {
        return id;
    }
    public void setId(Long id) {
        this.id = id;
    }
    public String getName() {
        return name;
    }
    public void setName(String name) {
        this.name = name;
    }
}
```

**/repository/Memberrepository.java**
```java
public interface MemberRepository {

    // 구체적인 클래스 명시를 피하기 위해 인터페이스로 선언합니다.
    Member save(Member member); //회원 저장기능
    Optional<Member> findById(Long id); // id를 이용하여 조회
    Optional<Member> findByName(String name);   // name을 이용하여 조회
    // Optional : java8에서 추가된 기능으로 null값을 감싸서 return합니다.
    List<Member> findAll(); //모두 조회
    
}
```

**/repository/MemoryMemberRepository.java**
+ [동시성 문제](https://applepick.tistory.com/124)  


```java
public class MemoryMemberRepository implements MeberRepository {

    private static Map<Long, Member> store = new HashMap<>();
    // 공유되는 변수 이므로 ConcurrentHashMap을 사용해야하지만 예제이므로 사용합니다.
    private static long sequence = 0L;
    // 역시나 동시성 문제가 있지만 단순하게 넘어가겠습니다.

    @Override
    public Member save(Member member) {
        // TODO Auto-generated method stub
        return null;
    }

    @Override
    public Optional<Member> findById(Long id) {
        // TODO Auto-generated method stub
        return null;
    }

    @Override
    public Optional<Member> findByName(String name) {
        // TODO Auto-generated method stub
        return null;
    }

    @Override
    public List<Member> findAll() {
        // TODO Auto-generated method stub
        return null;
    }
    
}

```

**repository/MemroyMemberRepository.java**
```java
public class MemoryMemberRepository implements MeberRepository {

    private static Map<Long, Member> store = new HashMap<>();
    // 공유되는 변수 이므로 ConcurrentHashMap을 사용해야하지만 예제이므로 사용합니다.
    private static long sequence = 0L;
    // 역시나 동시성 문제가 있지만 단순하게 넘어가겠습니다.

    @Override
    public Member save(Member member) {
        member.setId(++sequence);
        store.put(member.getId(), member);
        // memory 저장개념이기 때문에 정보를 map형태로 저장합니다.
        return member;
    }

    @Override
    public Optional<Member> findById(Long id) {
        return Optional.ofNullable(store.get(id));
        // null 값을 자동으로 감싸서 반환합니다.
    }

    @Override
    public Optional<Member> findByName(String name) {
        return store.values().stream() //람다식 루프
                .filter(member -> member.getName().equals(name))    // 필터링
                .findAny(); // name과 일치하는 값을 "하나라도" 찾으면 반환
                // null일 경우 optional로 감싸져서 반환합니다.
    }

    @Override
    public List<Member> findAll() {
        return new ArrayList<>(store.values());
        // loop를 돌리기 쉬워 list를 많이 사용합니다.
    }
```

### 3.2. 회원 리포지토리 테스트 케이스 작성
JUnit 프레임워크로 테스트를 작성합니다.  
관례적으로 테스트하려는 클래스이름 뒤에 Test를 붙입니다.  

**test/java/practice/springmvc/repository/MemoryMemberRepositoryTest.java**
```java
public class MemoryMemberRepositoryTest {
 
    MemoryMemberRepository repository = new MemoryMemberRepository();
    // JUnit도 프레임워크이기 때문에 bean으로 관리됩니다.

    @Test   // test 메소드를 위한 JUnit 어노테이션
    public void save() {
        // 테스트코드를 작성하는 것은 실제 코드와 비슷합니다.
        Member member= new Member();
        member.setName("spring");
        // 객체를 직접 생성해서 프로퍼티를 설정합니다.

        repository.save(member);
        Member result = repository.findById(member.getId()).get();
        // 실제 로직이 동작하듯이 저장하고 id값으로 객체를 불러옵니다.
        // Optional에서 가져오므로 마지막 .get메소드를 붙여 가져옵니다.

        //Assertions.assertEquals(member, result);
        // 검증을 위한 메소드로 jupiter에서 제공하는 assert입니다.
        // 기대하는 member가 result와 같은지 비교하는 메소드입니다.
        // 테스트를 실행해 참이면 녹색불이 나타납니다.

        assertThat(member).isEqualTo(result);
        // Assertions.assertThat(member).isEqualTo(null);
        // 실패하는 테스트 케이스. 실패하는 모든 경우도 테스트 해야합니다.
        // assertj에서 제공하는 좀더 편리한 메소드입니다.
        // static으로 import해서 바로 메소드를 사용가능합니다.
    }

    @Test
    public void findByName(){
        Member member1= new Member();
        member1.setName("spring1");
        repository.save(member1);
        
        Member member2= new Member();
        member2.setName("spring2");
        repository.save(member2);

        Member result = repository.findByName("spring1").get();

        assertThat(result).isEqualTo(member1);
        // "spring1"이라는 이름으로 result를 조회했으므로 member1과 같아야 합니다.
        // assertThat(result).isEqualTo(member2);
        // 실패하는 테스트
    }
```
여기까지 테스트는 성공하게 됩니다. 하지만 아래 테스트를 추가하는 순간, findByName()의 테스트가 실패하게됩니다.  
그 이유는** 테스트는 순서를 보장하지 않기 때문입니다.**

```java

    @Test
    public void findAll(){

        Member member1= new Member();
        member1.setName("spring1");
        repository.save(member1);
        
        Member member2= new Member();
        member2.setName("spring2");
        repository.save(member2);

        List<Member> result = repository.findAll();

        assertThat(result.size()).isEqualTo(2);
        // list의 크기를 비교합니다.
        // assertThat(result.size()).isEqualTo(1);
        // 실패하는 테스트
    }
}
```

순서를 보장하지 않으므로 spring2가 저장되어 다른객체로 비교하게 되어 findByName()테스트에서 실패했습니다.(이 역시 순서는 보장되지 않으므로 다를 수 있습니다.)  

**테스트 순서 의존을 해결하는 방법**
테스트가 끝나면 후처리를 이용해 테스트 하나가 끝나면 공용데이터를 초기화해줘야 합니다.  

```java
    // test의 MemorymemberRepositoryTest.java
    @AfterEach  // 일종의 콜백메소드로, 메소드가 끝난 뒤 실행됩니다.
    public void afterEach(){
        repository.clearStore();
    }
    
    // java의 MemoryMemberRepository.java
    public void clearStore(){
        store.clear();
    }
```

위의 후처리르 추가하면 테스트가 성공적으로 끝납니다.  
예제는 구현을 먼저하고 테스트를 만들었지만 반대로 하는것을 TDD(Test Driven Development)라고 합니다.  

### 3.3 회원 서비스 개발
비즈니스 로직을 구현하는 service입니다.  

**java/practice/springmvc/service/MemberService.java**
```java
public class MemberService {
    
    private final MeberRepository memberRepository = new MemoryMemberRepository();

    // 회원 가입 로직
    public Long join(Member member){
        validateSameName(member);   // 중복 검사. 중복값이 잇는 경우 예외를 던져 나갑니다.
        memberRepository.save(member);
        // 중복값이 없는 경우 저장합니다.
        return member.getId();
    }

    private void validateSameName(Member member) {
        //같은 이름 중복 x
        memberRepository.findByName(member.getName())
         .ifPresent(m -> { // 람다식. 값이 null이 아니면(ifPresent) 동작합니다. optional이여서 가능합니다.
                throw new IllegalStateException("이미 존재하는 회원입니다.");
        });
    }

    // 전체 회원 조회
    public List<Member> findAllMembers(){
        return memberRepository.findAll();
    }

    // 회원 조회
    public Optional<Member> findOne(Long memberId){
        return memberRepository.findById(memberId);
    }
}
```

**서비스 테스트 코드**
테스트 코드를 작성할 때는 given, when, then으로 구분해서 작성합니다. 주어지고(값), 실행했을 때(검증 하려는 것), 결과 (기대)라고 생각하면 됩니다.  
서비스 테스트 코드를 작성하는데 이미 MemberService에서 필드로 있던 memberRepository를 후처리를 위해 다시 가져오게 됩니다.  
다른 인스턴스를 사용하게 되는 것은 위험하므로, MemberService의 필드인 memberRepository에 생성자를 추가해 주입받아 사용하도록 변경합니다.  

```java
public class MemberService {
    
    private final MemberRepository memberRepository;

    // DI받도록 변경합니다.
    public MemberService(MemberRepository memberRepository) {
        this.memberRepository = memberRepository;
    }
    ...
   }
```
이후 테스트 코드에서 BeforEach 어노테이션을 사용해 각각의 테스트 전에 주입받도록 설정합니다.(memberrepository 인터페이스에서 추상메소드 추가 필요)  
```java
public class MemberServiceTest {

    MemberService memberService;

    // MemoryMemberRepository memberRepository = new MemoryMemberRepository();
    // 후처리를 위해 가져온 객체이지만 이미 memberService의 프로퍼티로 같은 객체가 다른 인스턴스로 존재합니다.
    // 물론 repository에서 static으로 선언되어 서로 다른 객체가 값을 간섭하진 않지만 거슬리게 됩니다.
    
    MemberRepository memberRepository;

    @BeforeEach
    public void BeforeEach(){
        // DI
        memberRepository = new MemoryMemberRepository();
        memberService = new MemberService(memberRepository);
    }

    @AfterEach
    public void afterEach(){
        memberRepository.clearStore();
    }

    @Test
    void testFindAllMembers() {

    }

    @Test
    void testFindOne() {

    }

    @Test
    void 회원가입() {
        // given
        Member member = new Member();
        member.setName("spring");

        // when
        Long saveId = memberService.join(member);

        // then
        Member findMember = memberService.findOne(saveId).get();
        assertThat(member.getName()).isEqualTo(findMember.getName());
        // 중요한 로직인 중복회원 검사가 빠졌으므로 반쪽자리 테스트입니다.
        
    }

    @Test
    void 중복회원예외(){
        // given
        Member member1 = new Member();
        member1.setName("spring");

        Member member2 = new Member();
        member2.setName("spring");

        // when

        memberService.join(member1);

    /*
        try {
            memberService.join(member2);
            fail(); // 테스트 실패
        } catch (IllegalAccessException e) {
            assertThat(e.getMessage()).isEqualTo("이미 존재하는 회원입니다.");
            // 테스트 성공
        }
    */

        // 위의 try/catch를 좀 더 간결하게 제공하는 assertThrows 메소드.
        // 해당하는 클래스가 발생해야하고, 
        assertThrows(IllegalStateException.class, () -> memberService.join(member2));
        // 메세지 검증
        IllegalStateException e =  assertThrows(IllegalStateException.class, () -> memberService.join(member2));
        assertThat(e.getMessage()).isEqualTo("이미 존재하는 회원입니다.");
    }
}
```

### 4. 스프링 빈과 의존관계
**스프링 빈을 등록하는 2가지 방법**
- @Component 어노테이션(controller, service, repository)와 생상자에 @Autowired
- 자바 코드로 직접 스프링 빈으로 등록

직접 new로 생성한 객체는 스프링 빈으로 관리되는 객체가 아닙니다.


#### 4.1. 컴포넌트 스캔과 자동 의존관계 설정
memberController가 memberService를 의존하도록 설정합니다.  
MemberService를 주입받아 사용하면 스프링 컨테이너가 싱글톤 객체처럼 관리하기 때문에 불필요한 객체 생성을 하지 않게 됩니다.  

```java
@Controller // 스프링 컨테이너에 의해 bean으로 관리됩니다.
public class MemberController {

    @Autowired
    public MemberController(MemberService memberService) {
        this.memberService = memberService;
    }

    // private final MemberService = new MemberService();
    // bean으로 관리되도록 합니다.Mem
    private final MemberService memberService;
    // 생성자가 필요합니다.

}

@Service    // Controller어노테이션 처럼 bean으로 등록합니다.
public class MemberService {
    
    private final MemberRepository memberRepository;

    // DI받도록 변경합니다.
    @Autowired
    public MemberService(MemberRepository memberRepository) {
        this.memberRepository = memberRepository;
    }

@Repository
public class MemoryMemberRepository{

```

#### 4.2. 자바 코드로 직접 스프링 빈 등록하기
Configuration 어노테이션으로 직접 빈으로 등록합니다.  
상황에 따라 구현 클래스를 변경해야 하면 이 방법을 사용합니다.  

```java
@Configuration
public class SpringConfig {

    @Bean
    public MemberService memberService(){
        return new MemberService(memberRepository());
    }

    @Bean
    public MemberRepository memberRepository(){
        return new MemoryMemberRepository();
    }
}

```

#### 4.3. 3가지 DI방법(Autowired)
1. 생성자 : 생성자에 autowired. 권장되는 방법. 생성되는 시점에서 주입하고 그 후론 닫혀있습니다.
2. setter : 필드의 setter메소드에 autowired. public으로 열려있어야 하므로, 다른 호출에서 바뀔 가능성(런타임 에러)이 있어서 권장하지 않음.
3. 필드 : 필드맴버에 autowired.

### 5. 화면 웹기능
생략합니다.

### 6. 스프링 DB 접근 기술
#### 6.1. h2 데이터베이스 설치
+ [h2설치](https://www.h2database.com/html/main.html)
+ /h2.bat 파일 실행
+ 최초 한번 그대로 연결
+ 이후 URL jdbc:h2:tcp://localhost/~/test 주소로 사용(다른 db와 복합적으로 사용하기 위해)

프로젝트 루트에 sql/ddl.sql 을 생성하여 테이블 관리를합니다.

```sql
drop table if exists member CASCADE;
create table member
(
 id bigint generated by default as identity,
 name varchar(255),
 primary key (id)
);
```

#### 6.2. 순수 JDBC
생략합니다.(JdbcMemberRepository 참조)

build에 h2를 추가하고 applicationproperties에 다음 정보를 추가합니다.
```xml
implementation 'org.springframework.boot:spring-boot-starter-jdbc'
	runtimeOnly 'com.h2database:h2'

spring.datasource.url=jdbc:h2:tcp://localhost/~/test
spring.datasource.driver-class-name=org.h2.Driver
spring.datasource.username=sa

```

#### 6.3. 스프링 통합 테스트
기존에 MemberServiceTest에서 @Transactional 어노테이션과 @SpringBootTest어노테이션을 붙이고 BeforEach와 AfterEach를 제거합니다.  DI방법으로 필드주입을 사용합니다.  
SpringBootTest 어노테이션은 실제로 스프링 컨테이너을 띄워 모든 bean찾아 DI해줍니다.  
**Transactional 어노테이션을 테스트 케이스에 있으면** DB에 커밋하지않고 롤백해줍니다. 그러므로 DB에 데이터가 남지 않아 다음 테스트에 영향을 주지 않습니다.  

```java
@SpringBootTest
@Transactional
public class MemberServiceIntergrationTest {

    @Autowired MemberService memberService;
    @Autowired MemberRepository memberRepository;
```

#### 6.4. 스프링 JdbcTemplate
스프링 JdbcTemplate와 MyBatis같은 라이브러리는 JDBC API에서 본 반복 코드를 제거해줍니다. SQL문은 직접 작성해야 합니다.  

```java

```

---
title: "개인 기록용 포스팅"
excerpt: "추후 분리될 포스팅들을 두서없이 정리"
---

## intelij plugins
- atom materal icons
- atom onedark theme
- code glance3 : minimap 기능
- git toolbox : git 이력 추적
- grep console : 콘솔 로그 보기 쉽게 정리
- jpa buddy : jpa 관련
- key promoter X : 단축키 보여줌
- rainbow brackets : 블락 쉽게 파악

## intelij community version tomcat
무료버전 인텔리제이에서는 톰캣을 지원하지 않으므로 smart tomcat plugin을 설치하여 사용
- [smart tomcat 플러그인 설치](https://velog.io/@youjung/Intellij-IDEA-Community-Edition%EC%97%90%EC%84%9C-Tomcat-%EC%82%AC%EC%9A%A9%ED%95%98%EA%B8%B0)

## jar 파일
- java archive
- claa와 같은 java 리소스와 속성 파일, 라이브러리 및 악세사리 파일이 포함
- java 애플리케이션이 동작할 수 있도록 자바 프로젝트를 압축한 파일로 zip과 호환
- JDK에 포함하고 있는 JRE(java runtime environment)만 가지고 실행이 가능

## war 파일
- web application archive
- 웹 애플리케이션 압축 파일 포맷
- jsp, servlet, jar, class, xml, html, javascript 등 Servlet Context 관련 파일들로 패키징
- tomcat 등의 WAS(웹 컨테이너)가 필요

## sprig legacy vs boot
- 스프링 부트는 내장 서버를 포함
- 스프리 레거시는 서버 따로 띄워놓고 애플리케이션을 실행해야 함
- 스프링 부트의 경우 application.properties 나 yml을 사용
- 스프링 레거시의 경우 root-context.xml 혹은 servlet-context.xml 사용
- jsp 파일이 web-inf(일반 사용자 접근 불가)에서 작동하여 보안 취약점을 해결

![image](https://user-images.githubusercontent.com/78904413/173358936-f50a7b50-a465-45dd-abb8-e3559253471e.png)

## 1. mybatis란?
자바 object와 SQL문 사이의 자동 Mapping 기능을 지원하는 Sql Mapper 입니다. SQL을 별도의 파일로 분리해서 관리하게 해줍니다.  
Hibernate나 JPA(java persistence api)처럼 새로운 DB 프로그래밍을 익혀야 하는 부담이 없어, 익숙한 SQL을 그대로 이용하면서 JDBC 코드 작성에 불편함을 제거해 줍니다.  

### 1.1. 특징
- 쉬운 접근성과 코드의 간결함
  - XML형태로 서술된 JDBC코드라고 생각해도 될 만큼 JDBC의 기능 대부분을 mybatis가 제공
  - 복잡한 jdbc코드를 걷어내어 깔끔한 소스코드 유지(재사용 가능)
  - 수동적인 파라미터 설정과 커리 결과에 대한 mapping 구문을 제거
- SQL문과 프로그래밍 코드의 분리
  - SQL에 변경이 있을 때마다 자바 코드를 수정하거나 컴파일 불필요
- 다양한 프로그래밍 언어로 구현 가능

## 2. mybatis3의 주요 컴포넌트
- sqlmapconfig.xml : db 접속 정보나 mapping 파일의 경로 등 고정된 환경정보를 설정
- SqlSessionFactoryBuilder : build()를 통해 SqlMapConfig.xml을 바탕으로 SqlSessionFactory를 생성
- SQlSessionFactory : openSession()을 통해 SqlSession을 생성
- SqlSession : 핵심적인 역할을 하는 클래스. SQL 실행과 트랜잭션 관리. Thread-safe하지 않으므로 thread마다 필요에 따라 생성
  - public Object selectOne(String stmt, Object param) : 하나의 데이터를 검색, 두개 이상 리턴되면 예외 발생
  - public List selectList(String stmt, Object param) : 여러 개의 데이터를 검색
  - public int insert(String stmt, Object param) : 몇 건 삽입했는지 리턴
  - public int update(String stmt, Object param) : 몇 건 갱신했는지 리턴
  - public int delete(String stmt, Object param) : 몇 건 삭제했는지 리턴

- Mapping파일 : SQL문과 O/R Mapping을 설정

![image](https://user-images.githubusercontent.com/78904413/173473751-07329c0d-73ce-4ea4-a0fa-c0bd1fcfb0ca.png)
![image](https://user-images.githubusercontent.com/78904413/173473800-6814c063-a5bb-4425-9f73-4142d935938b.png)

## 3. mybatis-spring의 주요 컴포넌트
- SqlmapConfig.xml : VO객체의 정보를 설정
- SqlSessionFactory : SpringBean으로 등록해야 함. SqlSessionFactory를 생성
- SqlSessionTemplate : SpirngBean으로 등록해야 함. Thread-safe함.
- mybatisBeans.xml : SqlSessionFactoryBean을 등록할 때 DataSource정보와 SqlmapConfig정보, Mapping파일 정보를 함께 설정.

![image](https://user-images.githubusercontent.com/78904413/173474045-288fa251-bdd3-4674-a5cf-e792aff953a8.png)

## service와 dao
dao에는 단일 데이터 접근/갱신을 처리하고 service에서는 여러 DAO를 호출하여 여러번의 데이터 접근/갱신을 하며 이 데이터에 대한 비즈니스 로직을 수행하고 하나의 트랜잭션으로 묶습니다.  
하지만 비즈니스 로직이 단일 DB접근으로 끝난다면 DAO와 Service가 동일해지는 경우도 발생합니다. 만일 DAO의 메소드 하나에 다중 DB접근 로직이 들어가있다면 DAO의 모듈화가 제대로 안된 접근 방식일 가능성이 높습니다.  
- [참고댓글](https://okky.kr/article/179628)

## session을 이용하여 로그인 하기
- [참고자료](https://beomi.github.io/gb-crawling/posts/2017-01-20-HowToMakeWebCrawler-With-Login.html)
http가 구현된 방식에서 웹클라리언트와 서버는 **지속적으로** 연결을 유지한 상태가 아니라 요청 응답의 반복일 뿐입니다.
이전 요청과 새로운 요청이 같은 사용자에서 이루어졌는지 확인하는 방법이 필요합니다.
이 때 등장하는 것이 cookie와 session입니다.  

cookie는 웹사이트를 방문할 때 client(사용자)의 브라우저에 저장되는 작은 파일로, key-value 쌍의 형식으로 저장됩니다. 그러나 로컬에 저장된다는 문제로 악의적 사용자가 쿠키를 변조하거나 탈취해 비정상적인 쿠키로 서버에 request할 수 있습니다. 쿠키 변조를 통해 마치 관리자나 다른 유저처럼 ㅎ맹동할 수 있는 것입니다.  

이로 인해 서버측에서 사용자를 식별하는 session을 주로 이용하게 됩니다. 세션은 세션 정보를 파일이나 db에 저장하고 client의 브라우저에 session-id라는 임의의 긴 문자열(쿠키)를 줍니다. 이 쿠키는 서버와 클라이언트의 연결의 끊어진 경우 삭제되는 메모리 쿠키입니다.  

request모듈에는 session이라는 도구가 있습니다.
```python
# python
import requests

# Session 생성
s = requets.Session()

# With 구문을 사용하여 session 생성, with 구문 안에서 유지 됌
With request.Session()as s:

  # HTTP GET Request
  req = s.get('https://www.clen.net/service/')

  # HTML 소스 가져오기
  html = req.text

  # HTTP Header 가져오기
  headr = req.headres

  # HTTP Status 가져오기
  status = req.status_code

  # HTTP가 정상적으로 되었는지 확인하기
  is_ok = req.ok
```

예시를 위해 클리앙 사이트를 크롤링(웹사이트 데이터 추출) 해 봅니다.  

![image](https://user-images.githubusercontent.com/78904413/173969201-c5c2ec0d-1d75-41cb-9335-333b614bf705.png)
![image](https://user-images.githubusercontent.com/78904413/173969351-dadc8933-f025-4f88-aec9-de4bf9e65eed.png)

`input`필드들의 `name`이 `\_csrf`, `userId`, `userPassword`, `로그인하기` 등이 있는 것을 확인할 수 있습니다. 로그인 버튼을 누르면 `auth.login()`함수가 실행되는 것을 확인할 수 있습니다.  

### html form
html form field에서는 `name:입력값` 라는 `key:value` 식으로 데이터를 전달합니다. 클리앙 로그인 form field의 경우 `userId:id`, `userPassword:pw` 라는 세트로 입력을 받는 것을 볼 수 있습니다.  
`\_csrf`라는 특이한 것도 있습니다. CSRF는 클라이언트의 request가 악의적이거나 해킹된 요청인지 확인해주는 보안 도구 입니다. session과 연결되어 form을 전달할 때 form의 안정성을 높여줍니다. 새로고침하면 CSRF값이 매번 달라집니다. 주의할 점은 CSRF를 사용하는 경우 CSRF 값이 없는 form 전송은 위험한 요청으로 생각하고 form을 받아들이지 않아서 로그인이 되지 않습니다. 따라서 \_csrf라는 것도 함께 전송해 줘야 합니다. 메인화면을 먼저 가져와 `\_csrf`필드를 가져오고 로그인을 해야 합니다.  

### auth.login()
다음으로는 auth.login()이라는 함수를 살펴봅니다. `input`, `select`, `textarea` 등의 form elements에서 값을 구하는 val()를 이용합니다.

```javascript
function Auth() {
  var_this = this;  // _this변수에 Auth라는 함수를 넣았다는 의미
  _this.env = {}; // object
  _this.env.form = $('#loginForm'); // 로그인 폼. id, pw, _csrf 등을 받는 form
  _this.env.iptUserId = _this.env.form.find('*[name=userId]');  // 사용자가 form name userId에 입력한 값입니다.
  _this.env.iptUserPassword = _this.env.form.find('*[name=userPassword]');
  
  _this.loginValidate = function() {  //함수
    var isValid = ture; // 입력값 검증. 아무 문제가 없다면 true를 반환. 
    if (_this.env.iptUserId.val().trim() == '') { // 아이디가 빈칸이라면 false를 반환
      alert('아이디를 입력하세요');
      _this.env.iptUserId.focus();  // 입력칸이 userId에 가도록 포커스
      isValid = false;
      return isValid;
    }
    if (_this.env.inptUserPassword.val().trim() == '')
      alert('비밀번호를 입력하세요');
      _this.env.iptUserPassword.focus();
      isValid = false;
      return idsValid;
    }
  };

  _this.login = function() {
    var isValid = _this.loginValidate();  // 검증 함수
    if (isValid) {
      _this.env.form.attr({ // form 속성을 정의, 파라미터 안은 attribute로 속성을 key-value 쌍으로 지정해서 넘김
        method: 'POST',
        action: BASE_URL + '/login' //폼 전송하는 주소는 https://www.clien.net/service/login
      });
      _this.env.form.submit();  // form 전송
    }
  };
}
```
Auth.login()은 아이디와 비밀번호 `form`에 빈 칸이 없다면 `POST` 방식으로 `https://www.clien.net/service/login`에 폼을 전송해 로그인하는 기능을 정의한 함수입니다.  

## 컬럼, 필드, 로우 햇갈리는 표현 정리
![image](https://user-images.githubusercontent.com/78904413/173975451-271a68e0-2085-4e0d-b7db-575432bc7add.png)

## sessionAttribute와 modelAttribute의 차이점
- [참고자료](https://okky.kr/article/894648)
- [](https://kim-jong-hyun.tistory.com/45)

MVC컨트롤러는 DB에서 가져온 데이터를 model에 담습니다. view는 model에 있는 데이터를 추력합니다.  
세션은 WAS에서 관리합니다. 전역변수처럼 사용되어 모든 페이지에서 그 정보를 참조할 수 있습니다. 인증정보 같은 것을 session에 넣어두어, 모든 페이지에서 참조하도록 합니다.  

spring에서는 RequestAttributes 인터페이스를 제공합니다. request와 session의 scope 우선순위 값을 관리하는데, request의 scope상태가 더 높습니다. 만약 `member`라는 `key`를 session에 저장해 두었다면 화면에서 출력할 때 `request scope`에서 먼저 탐색 후 없으면 `session scope`에서 존재하기 때문에 데이터가 view에 뿌려져야 합니다.  

여기서 주의할 점은 사실 `member`는 페이지가 렌더링 되기 전 `request scope`에 저장된다는 것입니다. 그 이유는 ModelAttributeMethodProcessor 클래스를 보면 알 수 있습니다.  

![image](https://user-images.githubusercontent.com/78904413/173990223-21cbaadd-a314-40af-8097-37483cab45cd.png)

request가 들어오면 ModelAttributeMethodProcessor가 동작합니다. 메서드 매개변수에 `@ModelAttribute`가 선언되었다면 해당 기본생성자를 호출하여 인스턴스를 생성하고 request 매개변수에 데이터를 바인딩해주며 model에 추가되지만, `@ModelAttribute`어노테이션은 생략 가능합니다. 생략시 파라미터 타입 클래스이름의 맨 앞글자만 소문자로 바꾼 값이 key가 됩니다. jsp에서 session에 저장된 데이터를 가져올 때는 `session.memeber.name`처럼 key값 앞에 session을 붙여주면 됩니다.  

Model은 내부적으로 Map.Entry형태로 이루어져있습니다.  

> Entry란? 각 키가 고유해야하는 기본 Map과 달리 중복 키를 가질 수 있습니다. 보통 List로 구현한 SimpleEntry객체를 사용하기 때문입니다. 이는 모든 객체가 서로 독립적임을 의미합니다.

> 튜플이란? List처럼 여러 객체를 모아서 담는 자료구조입니다. 하지만 수와 순서가 고정되어 값의 수정, 추가, 삭제가 불가능하여 read-only로 사용합니다.


![image](https://user-images.githubusercontent.com/78904413/173989482-8ad2f7f2-0405-4dec-b2b5-27efc37ad2ed.png)

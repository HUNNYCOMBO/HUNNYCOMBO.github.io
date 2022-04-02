---
layout: single
title:  "인프런 강의 - 코드로 배우는 스프링 부트, 웹 MVC, DB 접근 기술(김영한)"
categories: spring
tags: [spring, 인강]
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


#### spirng boot starter
- spring-boot-srater-web의 tomcat : 내장된 was(web application server). 기존에는 따로 설치된 was에 java코드를 넣어서 사용했지만, 라이브러리가 자체적으로 was를 갖도록 발전했습니다.
- spring-boot-starter : core, logging, spring boot 등 필요한 모든 의존관계를 가져옵니다.
- logging의 slf4j : 로깅을 위한 인터페이스. 구현체로 log4j, logback을 갖고있습니다.
- test : JUnit, mockito, assertj 등 테스트코드를 위한 라이브러리
  
#### 테스트 라이브러리
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


#### thymeleaf 템플릿 엔진
정적인 html에 동적인 기능을 부여합니다.  

#### controller
웹 진입의 첫번째. 요청의 주소값에 따라 연결된 메소드를 실행시킵니다.  

> main-java-group-project-SpringController.java

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
#### resources/templates/hello.html

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


#### localhost:8080/hello
해당 주소로 템플릿엔진 페이지를 확인해봅니다.  

![공부자료1](https://user-images.githubusercontent.com/78904413/161382032-a20a7c93-3243-49c5-9747-31a44b651c69.png)  

위의 사진과 같이 동적인 기능을 부여하는 템플릿 엔진의 기능을 확인할 수 있습니다.  
일반 텍스트인 "안녕하세오. 손님"은 렌더링 되지 않았습니다.  

#### 그림으로 정리하기
![공부자료2](https://user-images.githubusercontent.com/78904413/161382119-f5e8b5e7-1830-409f-a1a9-42a1e130a905.png)  

스프링부트는 기본적으로 templates폴더의 파일을 조회해서 렌더링 합니다.  
컨트롤러에서 리턴 값으로 문자를 반환하면 뷰 리졸버가 화면을 찾아서 처리합니다.  
resource:templates/{VieName}.html

#### spring devtools 라이브러리
[mavenrepository](https://mvnrepository.com/artifact/org.springframework.boot/spring-boot-devtools)  

해당 주소로 방문하여, gardle 의존설정에 devtools를 추가하면 코드변경시 재시작 없이 변경된 페이지를 확인할 수 있습니다.  

### 1.4. 빌드하고 실행하기
1. 어플리케이션 종료 후 콘솔(cmd)로 이동합니다.(IDE의 콘솔을 이용하는게 경로를 맞춰주므로 편리, javaHOME 오류시 IDE내의 jdk경로 확인할 것) 
2. ./gradle build 입력
3. build 경로의 libs에 springmvc-0.0.1-SNAPSHOT.jar 파일이 생성됩니다.(jar가 배포용 파일입니다.)


![공부자료2](https://user-images.githubusercontent.com/78904413/161383561-e72c45cd-cb14-4acc-b1a0-ce7c477c6155.png)  

#### 실행확인
1. cd build/libs
2. java -jar springmvc-0.0.1-SNAPSHOT.jar

IDE의 run없이 웹어플리케이션이 동작하게됩니다.  

#### ./gradlew clean
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

#### controller
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

#### hello-template.html
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

#### ResponsBody어노테이션을 사용
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

#### 일반적인 웹 어플리케이션 계층 구조
![7](https://user-images.githubusercontent.com/78904413/161385299-021aa08a-0f33-4fa6-b78a-65cf6375ebeb.png)
- 컨트롤러 : 웹 MVC의 컨트롤러 역할
- 도메인객체 : 회원, 주문, 쿠폰 등 주로 데이터베이스에 저장되고 관리되는 **비즈니스 도메인 객체**
- 서비스 : 도메인 객체를 이용하여 핵심 비즈니스 로직을 구현
- 리포지토리 : 데이터베이스에 접근, 도메인 객체를 DB에 저장하고 관리

#### 클래스 의존 관계
![8](https://user-images.githubusercontent.com/78904413/161385429-04307290-3b0a-4f32-a404-86de2481faca.png)
- MemberRepository : DB가 선정되지 않아서 인터페이스로 구현 클래스를 변경할 수 있도록 설계합니다.
- 초기 개발단계에는 가벼운 메모리기반의 DB를 사용합니다.







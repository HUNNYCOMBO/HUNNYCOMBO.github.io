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


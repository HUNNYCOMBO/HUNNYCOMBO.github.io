---
title: "About Lala"
excerpt: "수정 예정."
layout: "single"
permalink: /about/
author_profile: false
toc: true
toc_sticky: true
sidebar:
  nav: "portfolio"
header:
  teaser: /assets/images/lala/lala-flower.jpg
  overlay_image: /assets/images/lala/lala-flower.jpg
  overlay_filter: 0.4
  caption: "Lala"
---
<!-- @todo about.md를 lala-ogu 레파지토리로 옮길 고민 중-->

## :hatching_chick: About Lala
### :blush: 간략한 소개
- code review 기업 문화에 관심이 많습니다.
- 기능에 중점적으로 개발하기보단 **clean code**와 **객체지향 원칙**을 잘 지키며 개발하고 싶습니다.
- 꾸준히 공부를 하려 노력하고 있으며, 공부한 내용은 정리하여 블로그에 작성하고 있습니다.

### :mortar_board: 학력
- 서경대학교 경영학부 중퇴 (2013 ~ 2014)

###  :briefcase: 경력
- 채워나갈 예정입니다!

### :grey_question: 자주받는 질문
- 비전공자인데 개발직을 선택하게 된 계기
  - 아무나 할 수 있는 사무직 보다는 꾸준히 성장할 수 있는 전문직을 하고 싶었고 (관련은 없지만)컴퓨터 다루는 것에 자신이 있었던지라 코딩을 알아봤습니다. 코딩의 시작은 유튜브 생활코딩님의 java 강의를 보고 따라해보며 할 수 있다와 해보고 싶다라는 생각이 들어서 개발 공부를 시작하게 되었습니다.
- 국비학원을 끝까지 수료하지 않은 이유
  - 마지막 달 전 까지 학원(미래능력개발교육원)에 출석했지만, 학원의 특성상 취업률을 올리기 위해 소위 말하는 경력 뻥튀기 업체와 연계가 되어있어서, 수료까지 2주정도 남은 상태에서 수료는 하지않고 개인적으로 더 준비해서 양심적으로 회사에 취직하고 싶었습니다. 

### :phone: 연락
- email: gnsrudfk@naver.com
     
### :link: 링크
- [깃허브](https://github.com/lala-ogu)
- [블로그](https://lala-ogu.github.io/)
- [TIL](https://github.com/lala-ogu/TIL)
- [프로젝트 모음](https://lala-ogu.github.io/portfolio)

### :computer: stack
#### <img src="https://img.shields.io/badge/JAVA-007396?style=for-the-badge&logo=java&logoColor=white" alt="java">
- JVM 메모리 구조에 대해 간략히 알고 있습니다.
- 객체지향원칙(SOLID) 대해서 공부했습니다.

#### <img src="https://img.shields.io/badge/SpringBoot-6DB33F?style=for-the-badge&logo=Spring&logoColor=white" alt="spring boot">
- MVC패턴으로 간단한 CRUD 애플리케이션을 제작 할 수 있습니다.
- RESTAPI로 응답하는 경험을 해봤습니다.
- layered architecture에 대해 이해하고 있습니다.
- DI로 관심사를 분리하는 과정을 이해하고 있습니다.
- pointcut과 advice를 이용한 AOP에 대해 공부했습니다.

#### <img src="https://img.shields.io/badge/mysql-4479A1?style=for-the-badge&logo=mysql&logoColor=white" alt="MySQL">
- dml문과 ddl문에 대해 알고 있습니다.
- index에 대해 알고 있습니다.

## :open_file_folder: 프로젝트 요약
### Gather Up - 모임 관리 웹사이트
---
- 링크
  - [github에서 보기](https://github.com/lala-ogu/gatherup)
  - [리팩토링 (미완)](https://lala-ogu.github.io/portfolio/refactoring-gatherup)

{% capture gu1 %}
- 개요
  - Gather Up은 **온라인 강의**를 참고하여 만든 1인 제작 프로젝트 입니다.  
  - 게임에서 파티를 맺는 것 처럼, 웹 상에서 한 '모임'에 가입하고 탈퇴하는 기능을 구현하고 싶어서 데이터를 collection처럼 다룰 수 있는 ORM을 선택하게 됐습니다. 
  - 프로젝트를 처음 개발 할 때는 DTO와 Entity를 나누는 이유도 모르고 architecture도 모른채로 온라인 강의의 코드, 설계와 많이 다르게 제작하여 간단한 리팩토링을 거쳤습니다.

- 기간
  - 2021.10 ~ 2021.11
  - 2022.04(리팩토링)

- 구현사항
  - OAuth2.0을 사용하여 google 로그인 구현
  - 게시물 및 댓글 CRUD
  - javamailsender를 이용한 이메일 인증 token 전송

- 사용한 기술
  - Languague: java 11
  - Framework: spring boot, spring data JPA, spring security
  - Database: H2, MySQL
  - BuildTool: maven

{% endcapture %}

<details>
  <summary>개요(클릭)</summary>
{{ gu1 | markdownify }}
</details>

{% capture gu2 %}
- 회원가입 검증과 가입 후 자동로그인, 메일 보내기
![gather-signupvalidate](https://user-images.githubusercontent.com/78904413/164649157-2bd03dea-7302-49cc-8eaa-71273922fae8.gif)
  - 회원가입시 랜덤한 토큰값을 저장해서, javamailsender를 이용해 메일을 보냅니다.
  - InitBinder 어노테이션을 통해 form객체의 요청이 오면, validator 객체를 통해 중복값을 체크하거나, 같은 주소로 이메일을 많이 보내지 않게 방지합니다.
- 이메일 인증과 프로필 수정
![gather-levelup](https://user-images.githubusercontent.com/78904413/164650170-99f55038-f970-4a2d-86a2-c0dc9ad02bfa.gif)
  - 파라미터의 token값을 통해 이메일 인증을 완료하면 정회원으로 등록되어 팀만들기와 게시판글쓰기 등의 활동이 가능해집니다.
  - password는 인코딩되어 저장됩니다.
    - 이메일 인증 전 db정보
    ![gather-signupdatabase](https://user-images.githubusercontent.com/78904413/164651634-cfbe5358-f6d0-4ff2-8813-fa1ce1454db4.jpg)
    - 이메일 인증 후 db정보(Role의 변화)
    ![gather-levelupafter](https://user-images.githubusercontent.com/78904413/164651690-4427f1c5-eec1-49e7-8be3-d041ff5bfbde.jpg)
- 로그인
  - 일반 로그인
  ![gather-login](https://user-images.githubusercontent.com/78904413/164650791-b71ff1c7-b5e2-467e-a849-7d8efa66ebb9.gif)
    - 앞서 만든 계정으로 로그인 합니다.
  - 외부 로그인
  ![gather-oauthlogin](https://user-images.githubusercontent.com/78904413/164650877-2e4b1061-faaf-4f47-9a94-17fc494e2f68.gif)  - google 계정을 통해 로그인합니다. 로그인과 동시에 회원가입 처리가 되며 자동으로 정회원으로 등록됩니다.
- 팀
  - 팀 생성
  ![gather-maketeam](https://user-images.githubusercontent.com/78904413/164650475-a32f52bf-9e95-4bab-bc15-85ccf3d4e53d.gif)
    - 팀을 만들기 위한 간단한 정보를 입력하고 생성하면 해당 계정은 팀의 관리자로 등록됩니다.
    - 관리자는 모집 신청을 수락하거나 거절하는 등 팀의 설정이 가능합니다.
  - 팀 가입하기
  ![gather-jointeam](https://user-images.githubusercontent.com/78904413/164651226-605ba71d-9d27-410c-af03-20a80adfae7c.gif)
    - 공개 중이며 모집 중인 팀은 가입신청이 활성화 되어 가입신청이 가능합니다.
    - 관리자 계정이 수락을 해야 팀원으로 등록되고 팀의 인원이 늘어나는 것을 확인 할 수 있습니다.
  - 팀 상태수정
  ![gather-updateteam](https://user-images.githubusercontent.com/78904413/164651897-c861dce9-7e00-4f06-8214-551628c391dd.gif)
    - 관리자는 팀을 비공개로 하거나 모집을 중단하는 등의 상태를 변경 할 수 있습니다.
- 게시판
![gather-crud](https://user-images.githubusercontent.com/78904413/164675115-8b3a054a-42e8-43e3-b668-1d9b2bc9e3fa.gif)
  - 간단한 게시판과 댓글 CRUD 입니다.

{% endcapture %}

<details>
  <summary>움짤로 보는 동작(클릭)</summary>
{{ gu2 | markdownify }}
</details>

{% capture gu3 %}

- Spring Boot, Thymeleaf
> 템플릿 엔진(thymeleaf)를 이용해 객체를 담아 응답합니다. (JSON리턴 방식 X)
>> 이후 REST API와 layered architecture를 알게되어 리팩토링 중에 있습니다.

- 패키지구조(리펙토링 전)
  - config: security와 project configuration을 관리합니다.
  - controller: controller들을 관리합니다.
  - domain: entity이자 domain model을 관리합니다. (dto와 domain의 차이를 알기 전이라 dto처럼 사용하였습니다.)
  - form: controller를 통해 thymeleaf에 보내지는 form객체들을 관리합니다.
  - service: domain별로 비즈니스 로직을 정리한 service객체들을 관리합니다.
  - validator: @initbinder를 이용하여 controller에서 form요청이 들어올 때 검증하도록 하는 객체들을 관리합니다.

- Spring Security
  - csrf: disable
  - hasAuthority("ROLE_REGULAR")를 이용하여 이메일 인증이 된 사용자만 접근가능 하도록 제한합니다.
  - remember-me: JdbcTokenRepositoryImpl을 이용하여 persistlogin테이블의 토큰 값으로 로그인 유지 기능을 활성화합니다.
  - form login: use
    - DetailService, OAuth2Service : 로그인에 필요한 UserDtails와 외부 로그인에 필요한 OAuth2User를 상속받은 PrincipalDetail 클래스로 로그인을 구현했습니다.

- ORM
  - JPA: 반복적인 CRUD작업을 처리합니다. collection개념으로 entity들의 관계를 다룰 수 있어서 선택했습니다.
  - QueryDSL: JPA로 해결할 수 없는 복잡한 쿼리를 작성합니다.
    - TeamReposityroExtension: QueryDSL Interface
    - TeamRepositoryExtensionImpl.findByKeyword: QueryDSL Implements Class. 팀검색을 위한 용도로 작성됐습니다.

{% endcapture %}

<details>
  <summary>프로젝트 구조(클릭)</summary>
{{ gu3 | markdownify }}
</details>

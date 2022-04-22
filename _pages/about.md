---
title: "About Lala"
excerpt: "꾸준히 성장하여 시니어 개발자가 되고싶은 취준생, 라경훈입니다."
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

## :hatching_chick: About Lala
### :blush: 간략한 소개
- java에 관심이 많고 back-end 개발자(가 되고싶은) 라경훈입니다.
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
  - [블로그에서 보기](https://lala-ogu.github.io/portfolio/refactoring-gatherup)

- 개요
  - lazir는 JPA에 관심이 있어 **온라인 강의**를 참고하여 만든 1인 제작 프로젝트 입니다.  
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


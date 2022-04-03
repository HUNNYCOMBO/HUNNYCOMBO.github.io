---
layout: single
title:  "프로젝트 리팩토링 - lazir"
categories: spring
tags: [spring, project, 온라인강의]
toc: true
toc_sticky : true
author_profile: false
sidebar:
    nav: "docs"
search: true
---

## 링크
+ [참조한 백기선님 온라인강의](https://www.inflearn.com/course/%EC%8A%A4%ED%94%84%EB%A7%81-JPA-%EC%9B%B9%EC%95%B1/dashboard)
+ [프로젝트 github](https://github.com/hunnycombo/lazir)


<details>
   <summary>미완</summary>
-
usecase - 구매
product domain 으로 상품을 조회하고, 없으면 예외처리를하고, 재고관련 domain, member, payment domain등을 활용하여 하나의 usecase로 묶어서 어플리케이션 레이어에서 처리.
? 하나의 domain을 사용하는 경우? -> domain을 직접 호출하는 경우도, 어플리케이션을 거치는 경우도 있음.(team by team)
모든 참조는 단방향으로 이루어져야한다는 규칙.
-

? querydsl
responsebody json 로 리턴하도록 
시리얼라이즈

--
1. 4개의 영역으로 나누기

컨트롤러 - 뷰 리턴할 때 restAPI  - JSON으로 리턴하게 해서 -> controller 어노테이션을 restcontroller로 반환
호출됐을때 넘어온 객체들을 validator로 검증하게끔 수정.

request - 시리얼라이즈 / response - 디시리얼라이즈

? account 도메인 객체를 그대로 리턴하지않는 이유 - > doamin 객체와 response, request객체와 분리해서 사용- >  domain에 어울리지않는 필드를 추가해야하는 경우가 생김
accountservice가 form을 참조하게되면 역방향 참조가일어나게 되므로,  프레젠테이션이나 어플리케이션에서 변환을해서 넘겨주 게된다.

변경한 부분 1.
public Account duplicatedEmail(Account account) { 이름변경

2. checkEmail(account.getEmail());  account가 아닌 email만 넘겨줘도된다.

--
? 트렌젝션 read only mysql의 트랜잭션 속성이나 rdbms 트랜잭션의 특징 ? <- 따로 공부. 트랜잭션 acid

? 트랜잭션 isolation 레벨

? mysql 스토리지엔진 이노db엔진. isolatioin 정책 레벨

db의 index를 왜쓰는지? . mysql의 index는 hash가 tree구조. 왜? 범위의 데이터를 찾는 경우 때문에. tree

모든 컬럼에 대해 index를 생성해야 하는지? index의 장단점.

? 커버링 index

? mysql 실행계획 explain

? 스프링 transation 주의할점 어떻게 동작하는지 - AOP 프록시
                                                      
                                                      ## 도와주신분
                                                      ben
                                                      
                                                      </details>

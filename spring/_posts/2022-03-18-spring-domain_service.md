---
layout: single
title:  "domain service와 application(비즈니스) service"
excerpt: "도메인 계층의 로직과 애플리케이션 계층의 로직의 차이점을 알아봅니다."
categories: spring
tags: [spring, domain serviced, application service]
toc: true
toc_sticky : true
author_profile: false
search: true
---

+ 참조한 블로그 [복세편살](https://americanopeople.tistory.com/372)

## domain service와 application service의 차이점
+ 도메인 서비스는 domain(entity) / DTO(VO)에 속할 수 없는 도메인 로직을 다룰 때 사용합니다.
+ 그러나 애플리케이션 서비스는 도메인 로직을 갖지 않습니다.
+ 도메인 서비스, 애플리케이션 서비스 모두 domain / DTO를 상위에서 다루는 stateless(무상태)한 **클래스**를 의미합니다.

## doamin service의 특징
+ 비즈니스 의사결정(아래 추가 설명)과 관련된 코드를 담당합니다.

## domain service 추출하기
1. 비즈니스 로직을 실행할 때 DB, 외부 API등을 통해 필요한 정보를 준비합니다.
2. 비즈니스 로직을 실행합니다. 1개 이상의 도메인 객체(모델)을 활용하여 비즈니스 의사결정을 합니다. 모델의 상태가 변경되거나 필요한 정보가 생성됩니다.
3. 비즈니스 로직의 실행 결과를 DB나 외부 서비스 등 실제 세계에 반영합니다.

## domain service를 분리함으로서 생기는 이점
+ 외부의존성이 적어 unit test를 작성하기 편합니다.
+ 도메인 지식이 도메인 모델과 근접한 곳에 모여서 유지보수하기 편합니다.

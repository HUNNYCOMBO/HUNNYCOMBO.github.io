---
layout: single
title:  "domain, DTO, entity"
excerpt: "개념이 비슷한 도메인, DTO의 차이를 알아봅니다."
categories: spring
tags: [spring, domain]
toc: true
toc_sticky : true
author_profile: false
search: true
---

+ 참조한 블로그 [heejeong Kwon](https://gmlwjd9405.github.io/2018/12/25/difference-dao-dto-entity.html)
+ 참조한 블로그 [doing7](https://doing7.tistory.com/79)

## VO
+ Value Object
+ 특정한 비즈니스 값을 담는 객체
+ read-only
+ equals()와 hashcode()를 오버라이딩 하여, 객체의 주소값이 같으면 같은 객체라고 판단하게 하는것이 핵심입니다.
+ 식별자가 없으므로 하나의 데이터(값)이라도 바뀌면 다른 객체로 판단합니다.
+ 그렇기에 불변타입으로 구현하는 것이좋습니다. setter는 구현하지 않습니다.
+ 식별자가 없으므로 db테이블과 대응될 수 없습니다.
+ 기존 객체의 데이터를 변경하고 싶다면 변경한 데이터로 새로운 객체를 만듭니다.

## DTO
+ Data Transfer Object
+ DB에서 데이터를 얻어 service, controller 등으로 보낼 때 사용하는 객체.
+ 로직을 갖지 않고 순수한 게터세터 메소드를 갖습니다.(db에서 꺼낸 데이터를 변경할 필요가 없으므로 세터 대신 생성자로 값을 할당합니다.)
+ doamin 객체가 doamin layer를 벗어나지 못하도록 합니다.(레이어간의 통신 용도로 오고가는 객체)

## entity
+ JPA에서 실제 DB테이블과 매칭될 클래스(DB테이블의 컬럼만을 필드로 갖는 클래스)
+ presetation 로직(화면 노출에 필요한 계산)을 갖고 있어서는 안됩니다.
+ @Entity, @Column, @Id 등을 이용
+ 식별자(id)를 가져서 식별자가 변경되면 다른 객체로 판단합니다.
+ db의 테이블은 실존하는 물리모델이지만, 엔티티는 개념적인 논리모델입니다.

## domain
+ 최대한 entity 클래스의 getter를 사용하지 않도록 필요한 로직을 구현합니다.
+ 구현한 로직은 주로 application layer(service layer)에서 사용합니다.(도메인 스스로 사용 가능)
+ presentation 로직은 담지 않습니다.
+ 필드 입력에 대한 유효성 검증 등 항상 완전한 상태로 모델이 만들어지도록 합니다.


![domain](https://user-images.githubusercontent.com/78904413/158943259-27d58aba-d0b1-4c95-9be3-b6c279464ff5.jpg)

## DTO와 domain(entity)을 분리하는 이유
+ presentaion 로직과 doamin 로직을 분리할 수 있습니다.(domain 로직은 presentation 로직을 담지 않습니다.)
+ DB테이블과 매핑되는 entity 클래스가 변경되면 여러 클래스에 영향을 끼쳐 완전한 상태여야 하지만, view와 통신하는 DTO클래스는 자주 변경되므로 분리해야 합니다.
+ 통계나 지표 등의 여러 테이블의 컬럼 값을 조합한 데이터가 필요할 경우 DTO를 통해 단순히 값만 담은 형태로 제공합니다.
+ 화면 노출 혹은 외부 API에 domain 객체가 사용된다면 scope오염부터 시작해서 많은 부분에 domain 로직이 오염됩니다.
+ 즉, DTO는 domain을 복사한 형태로, 다양한 presentation 로직을 추가한 정도로 사용하며, **domain 객체는 persistent(영속성**)만을 위해서 사용합니다.

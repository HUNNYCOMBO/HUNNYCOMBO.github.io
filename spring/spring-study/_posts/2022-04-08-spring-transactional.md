---
title:  "스프링의 @Transactional"
excerpt: "스프링의 Trasactional 어노테이션의 속성에 대해 알아봅니다."
tags: [어노테이션, 트랜잭션]
header:
  teaser: /assets/images/spring/transaction.jpg
  overlay_image: /assets/images/spring/transaction.jpg
  overlay_filter: 0.4
---

## 참고링크
+ [kdhyo](https://velog.io/@kdhyo/JavaTransactional-Annotation-%EC%95%8C%EA%B3%A0-%EC%93%B0%EC%9E%90-26her30h)

## 1. 트랜잭션이 하는 일
begin, commit, rollback를 자동으로 수행합니다.  

## 2. 스프링의 트랜잭션 처리 방법
스프링에서는 간단한 선언적 트랜잭션으로 @Transactional을 메소드, 클래스, 인터페이스 위에 추가하여 사용합니다.  
적용된 범위에서는 트랜잭션 기능이 포함된 **프록시 객체**가 생성되어 자동으로 commit 혹은 rollback을 진행합니다.  

## 3. @Transactional의 attribute
- isolation : 트랜잭션의 격리 수준을 설정합니다.
- propagation : 해당 트랜잭션이 동작 중에 다른 트랜잭션을 호출 할 때 어떻게 처리할지 지정합니다.
- noRollbackFor : 특정 예외 발생시 rooback하지않습니다.
- rollbackFor : 특정 예외 발생시 rollback합니다.
- timeout : 지정한 시간 내에 메소드 수행이 완료되지 않으면 rollback합니다.(default = -1)
- readOnly : 트랜잭션을 읽기 전용으로 설정합니다.(insert, update, delete 시 예외, default = false)

### 3.1. isolation
- Idsolation.DEFAULT : 기본 격리 수준이며 DB의 isolation Level을 따릅니다.
- Isolation.READ_UNCOMMITED (level 0) : 커밋되지 않은 데이터에 대한 읽기를 허용합니다.
- Isolation.READ_COMMITED (level 1) : 커밋된 데이터에 대해 읽기 허용
- Isolation.REPEATEDABLE_READ (level 2) : 동일한 필드에 다중 접근시 모두 동일한 결과를 보장. 트랜잭션이 완료될 때 까지 SELECT 문장이 사용하는 모든 데이터에 shared lock이 걸리므로 다른 사용자는 그 영역의 데이터에 대한 수정이 불가능합니다. 일관성 있는 결과를 리턴합니다.
- Isolation.SERIALIZABLE (level 3) : 데이터의 일관성 및 동시성을 위해 MVCC(Multi Version Concurrency Control)을 사용하지 않습니다. 성능 저하의 우려가 있습니다.

> MVCC : 다중 사용자 DB성능을 위한 기술, 데이터 조회시 LCOK을 사용하지 않고 데이터의 버전을 관리해 데이터 일관성과 동시성을 높이는 기술입니다.

#### 3.1.1. 격리수준에 따른 문제
- Dirty Read : A트랜잭션이 commit하지 않은 데이터를 다른 트랜잭션이 읽을 수 있습니다. 다른 트랜잭션의 데이터는 정합성에 어긋나게됩니다.
- Non-Repetable Read : A트랜잭션이 회원 A를 조회중에 다른 트랜션이 회원 A의 정보를 수정하고 커밋한다면, A 트랜잭션이 다시 조회 했을 때 수정된 데이터가 조회됩니다. 이처럼 반복해서 같은 데이터를 읽을 수 없는 문제입니다.
- Phantom Read : 반복 조회시 결과집합이 달라지는 경우입니다. A트랜잭션이 김씨 성을 가진 회원들을 조회했는데, 다른 트랜잭션에서 새로운 기씨성을 가진 회원을 추가하고 커밋하면, 트랜잭션 A가 다시 조회했을 떄 회원 한명이 추가된 상태로 조회됩니다.


|Level|Dirty Read|Non-Repetable Read|Phantom Read|
|--|--|--|--|
|Read Uncommited|O|O|O|
|Read Commited|-|O|O|
|Repetable Read|-|-|O|
|Serializable|-|-|-|

#### 3.1.2. 트랜잭션 격리 수준의 필요성
레벨이 높아질 수록 데이터 무결성을 유지할 수 있지만 DB의 성능은 떨어지고 비용은 높아집니다. 최대한 효율적인 방안을 찾아 상황에 맞게 사용하는 것이 중요합니다.


### 3.2. propagation(전파속성)
- REQUIRED : 기본값으로, 이미 진행중인 트랜잭션이 있다면 해당 트랜잭션 속성을 따르고, 진행중이 아니라면 새로운 트랜잭션을 생성합니다.
- REQUIRES_NEW : 항상 새로운 트랜잭션을 생성합니다. 이미 진행중인 트랜잭션은 잠깐 보류하고 해당 트랜잭션을 먼저 진행합니다.
- SUPPORT : 이미 진행 중인 트랜잭션이 있다면 해당 트랜잭션 속성을 따르고, 없다면 트랜잭션을 설정하지 않습니다.
- NOT_SUPPORT : 이미 진행중인 트랜잭션이 있다면 보류하고, 트랜잭션을 설정하지 않고 작업을 수행합니다.
- MANDATORY : 이미 진행중인 트랜잭션이 있어야만 작업을 수행합니다. 없다면 예외가 발생합니다.
- NEVER : 트랜잭션이 진행중이지 않을 떄만 작업을 수행합니다. 진행중인 트랜잭션이 있다면 예외를 발생시킵니다.
- NESTED : 진행중인 트랜잭션이 있다면 중첩된 트랜잭션이 실행됩니다. 트랜잭션이 없다면 새로운 트랜잭션을 생성합니다.

### 3.3. rollbackFor = Exception.class
@Transactional 은 기본적으로 Unchecked Exception,Error(예외처리 x, RuntimeException) 만을 rollback하고 있습니다. 그렇기 때문에 CheckedException에 대해서 rollback을 진행하고 싶을 경우 해당 어노테이션 옵션을 설정해야 합니다.  
스프링이 런타임 에러만 rollback이 되도록 설정한 이유는, CheckedException은 반드시 throw를 하는데, 이는 호출하는 코드에서 처리를 해줘야 한다는 것을 명시한 것입니다.  
즉, 반드시 처리되는 예외이므로 해당 트랜잭션 안에서 예외처리가 되었을 경우에는 이를 롤백 시킬 이유가 없기 떄문입니다.  

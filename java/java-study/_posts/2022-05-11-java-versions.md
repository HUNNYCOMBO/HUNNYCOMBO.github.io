---
title: "자바의 버전별 추가 기능"
excerpt: "자버 버전별로 추가 된 기능을 살펴봅니다."
tags: [java, version]
header:
  teaser: ![img](https://user-images.githubusercontent.com/78904413/167848741-c8dd2660-008c-467b-8db1-5b931da43ce6.png)
---

### 참고
- [juho0920.log](https://velog.io/@ljo_0920/java-%EB%B2%84%EC%A0%84%EB%B3%84-%EC%B0%A8%EC%9D%B4-%ED%8A%B9%EC%A7%95)

### 1. java 8
- Lambda : 익명 클래스를 람다를 이용하여 간결하게 표현 가능
- Stream : Stream API를 통해서 collection을 처리할 때 발생하는 반복적인 코드와 멀티코어 활용 어려움 문제를 해결
- Default method
- Optional : null 값을 감싸서 return하는 등 부가적인 활용이 가능
- new DataandTime API(LocalDataTime, ...)
- type annotation

### 2. java 9
- Jigsaw기반 런타임 모듈화 : AWT나 Swing같은 불필요한 라이브러리를 끌어쓸 필요가 없어짐
- JShell : java를 인터프리터 언어 셸처럼 사용할 수 있는 기능
- HTML5 Javadoc 지원

### 3. java 10
- var : 로컬 변수 유형 추론인 var 예약어가 도입
- 병렬 처리 가비지 컬렉션 도입
- JVM의 heap 영역을 시스템 메모리가 아닌 다른 종류의 메모리에도 할당 가능

### 4. java 11
- 람다 파라미터에 대한 지역 변수 문법 변경
- 라이선스 변경

### 5. java 12
- switch문 람다 표현

### 6. java 13
- switch문 yield 예약어 추가

### 7. java 14
- instanceof패턴 매칭 : if(obj instaceof String s)
- record 타입 지원

### 8. java 15
- 클래스 봉인 : 상속 가능한 클래스를 지정할 수 있는 봉인 클래스가 제공
- 외부 메모리 접근 API(인큐베이팅)
- ZGC : 스케일링 가능한 낮은 지연의 가비지 컬렉터 추가
- EdDSA암호화 알고리즘 추가
- 다중 텍스트 블록

### 9. java 16
- Vector API : 자동 병렬 프로세싱을 지원하는 자도 벡터 API
- OpenJDK소스를 github에서 관리


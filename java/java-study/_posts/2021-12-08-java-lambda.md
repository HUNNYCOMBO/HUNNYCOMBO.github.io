---
title:  "람다와 스트림"
tags: [람다, Stream, 함수형 인터페이스]
excerpt: "자바8에 추가된 람다와 스트림에 대해 알아봅니다."
header:
  teaser: /assets/images/java/lambda.png
---

## 람다
### 1. 람다식이란?
 람다식이란 하나의 함수(메소드)를 보다 단순하게 표현하는 방법입니다.  
 __메소드를 값처럼 선언 할 수 있고 파라미터로 전달 및 변수에 대입하기 같은 연산이 가능해집니다.(일급객체)__
   
 ``` java
 // 1. 람다는 매개변수(파라미터) -> 함수본문 로 사용 할 수있습니다.
 () -> {}
 // 2. 함수본문이 단일 실행문이면 {}를 생략 가능 합니다.
 () -> 1

// 기존 익명클래스 자바문법
new Thread(new Runnable(){
    @Override
    public void run() {
        System.out.println("Hello World");
    }
}).start();

// 람다식 문법
new Thread(()->{
    System.out.println("Hello Worlkd");
}).start();
 ```
  
람다식을 사용하면 위와 같이 코드가 훨씬 간결해지고 가독성이 좋아집니다.  
  
### 2. 람다의 특징
- 익명함수(Anonymous functions) : 람다함수는 이름을 가질 필요가 없습니다.
- 커링(Curring) : 두 개 이상의 입력이 있는 함수는 최종적으로 1개의 입력만 받는 람다식으로 단순화 될 수 있습니다.
- 일급객체(First Class Citizen) : 다른 객체들에 적용 가능한 연산을 모두 지원하는 개체입니다.
  
#### 2-1. 람다의 장점
- 코드의 간결성
- 지연연산 수행 : 람다는 지연 연산을 수행 함으로써 불필요한 연산을 최소화 할 수 있습니다.
- 병렬처리 용이 -멀티 쓰레드를 활용하여 병렬처리를 할 수 있습니다.

#### 2-2. 람다의 단점
- 재사용이 불가능 합니다.
- 재귀에 부적합합니다.
- 람다 stream 사용 시 단순 반복문(for, while)의 성능이 떨어집니다.
  
### 3. 함수형 인터페이스(@FunctionalInterface)
함수형 인터페이스란 **단 하나의 추상 메소드**를 갖는 인터페이스 입니다.  
  
```java
@FunctionalInterface // 함수를 일급객체처럼 다룰 수 있게 하는 어노테이션.
interface Math{
    public int Calc(int first, int second);
}
// 위에서 함수형 인터페이스를 선언 했습니다.

public static void main(String[] args){
    Math plusLambda = (a, b) -> a + b;
    System.out.println(plusLambda.Calc(4,2));

    Math minusLambda = (a, b) -> a - b;
    System.out.println(plusLambda.Calc(4,2));
}
// 위에서는 추상 메소드를 구현하여 함수형 인터페이스를 사용했습니다.
```
  
### 4. Stream API
 Steam이란 java8부터 추가된 다양한 데이터를 표준화된 방법으로 다루기 위한 함수를 정의한 **라이브러리** 입니다.  
 **데이터의 종류와 상관 없이 같은 방법**으로 데이터를 처리 할 수 있습니다.  
  
Stream API는 아래와 같이 구성됩니다.
```java
example.stream().filter(x -> {x < 2}).count
// stream() : 스트림 생성
// filter() : 중간 연산(스트림 변환), 연속적으로 수행 가능합니다.
// count : 최종 연산(스트림 사용)
```

#### 4-1. stream의 특징
- 원본의 데이터를 변경하지 않습니다.
- 일회용(재사용 불가, 디버그 힘듦)
- 병렬 처리가 쉽습니다.
- 지연 연산(내부 반복자)

#### 4-2. stream API 간단 예제
```java
IntStream.range(1, 11).filter(i -> {i % 2 == 0})
    .forEach(System.out::println);
    // 1~10 사이의 수 짝수판별
    // 실행결과 
    // 2
    // 4
    // 6
    // 8
    // 10

System.out.println(IntStream.range(0,1001)
    .skip(500)  // 500으로 넘어감
    .filter(i -> i % 2 == 0)    // 짝수 걸러냄
    .filter(i -> i % 5 == 0)    // 5의 배수 걸러냄
    .sum()  //합
    );
    // 0~ 1000 사이의 수 중 500이상이면서 짝수이면서 5의 배수인 수들의 합을 구하라.
    // 결과 38250
```

[람다식과 Stream에 더 알아보기](https://khj93.tistory.com/entry/JAVA-%EB%9E%8C%EB%8B%A4%EC%8B%9DRambda%EB%9E%80-%EB%AC%B4%EC%97%87%EC%9D%B4%EA%B3%A0-%EC%82%AC%EC%9A%A9%EB%B2%95)
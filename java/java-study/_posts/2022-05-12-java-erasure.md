---
title : "제네릭 type의 erasure란 무엇인가?"
excerpt: "erasure에 대해서 알아봅니다."
tags: [java, generic, erasure]
---

## 참고
- [Gyun's 개발일지](https://devlog-wjdrbs96.tistory.com/263)

## 1. 다시보는 제네릭
제네릭은 5버전에 처음 도입되었습니다. 따라서 하위 버전과의 호환성 유지를 위한 작업의 필요에 따라 erasure(소거)방식을 사용하게 됐습니다.  
제네릭과 배열의 차이를 먼저 되돌아 봅니다.  

### 1.1. 제네릭은 불공변이고 배열은 공변입니다.
공변이란 자신과 자식 객체로 타입변환을 허용해주는 것입니다.  
```java
Object[] array = new Long[1];
```
따라서 위와 같은 문법이 허용됩니다.  

반면 불공변이란, 자신과 같은 타입만 같다고 인식하는 특징입니다. 이러한 특징으로 컴파일 타임에 타입 안정성을 가지는 장접이 있습니다.  
예를 들어 List<String>과 List<Object>같은 부모관계에서 두 타입은 전혀 관련이 없게 바라봅니다.  
  
```java  
public class Test {
   public static void test(List<Object> list) {}  // 타입 파라미터로 Object가 선언
   public static void main(String[] args) {
       List<String> list = new ArrayList<>();
       list.add("Gyunny");
       test(list); // 타입 파라미터가 달라 컴파일 에러가 납니다.
   }
}  
```
  
### 1.2. 제네릭은 비구체화되고 배열은 구체화(reify)됩니다.
구체화 타입이란 자신의 타입 정보를 **런타임 시점**에도 알고 있는 것입니다.  
반면 비 구체화 타입은 런타임 시점에서는 소거(erasure)되기 떄문에 컴파일 시점보다 정보를 적게 가지게 됩니다.  
즉, 제네릭은 컴파일 시점에서 타입 체크를 한 후에 런타임 시점에서는 타입을 지우는 방법을 사용합니다.  
  
## 2. Generic Type erasure
erasure란 결국 런타임 시점에는 해당 타입 정보를 알 수 없는 것입니다.  

### 2.1. java 컴파일러의 타입 erasure 방법
- <T>,<?>같은 unbounded Type은 Object로 변환합니다.
- <E extends Comparable>같은 bound type은 Comprable로 변환합니다.
- 타입 안정성 보존을 위해 필요하다면 tyep casting을 넣습니다.
- 확장된 제네릭 타입에서는 다형성을 보존하기 위해 bridge(연결) method를 생성합니다.

```java
// bridge method의 예
public class MyComparator implements Comparator<Integer> {
   public int compare(Integer a, Integer b) {
      ...
   }
}
// 위와 같은 컴파일시의 코드는 런타임 시에 아래 코드처럼 소거되어 변할 것입니다.
public class MyComparator implements Comparator {
   public int compare(Integer a, Integer b) {
      ...
   }
}
// 이때 문제는, compare 메소드의 매개변수 타입이 Object로 바뀌는 것입니다.
// 이러한 불일치를 해결하기 위해서 컴파일러는 런타임 시점에 bridge method를 만들어줍니다.

public int compare(Object a, Object b) {
   return compare((Integer)a, (Integer)b);
  }
// bridge method를 통해 Integer타입의 매개변수인 compare 메소드를 사용할 수 있게 됩니다.
```

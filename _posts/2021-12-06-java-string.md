---
layout: single
title:  "String 클래스"
categories: java
tags: [java, string]
toc: true
author_profile: false
sidebar:
    nav: "docs"
search: false
---

## String 클래스
### 1. 불변객체(Immutable Object)
string 클래스는 **불변객체**입니다.\
불변객체란, 객체가 생성된 후 그 객체의 **상태**를 변경 할 수 없는 객체입니다. (read-only, 수정불가능)\
string은 불변 객체이기 때문에 + 연산으로 계속 더할 때 마다 새로운 객체를 생성하기 때문에 메모리를 많이 사용하는 단점이 있습니다.\

### 2. 방어적복사(defensive-copy)
일반적으로 **참조변수**를 통해 값을 수정한다면 의도대로 **값(상태, value)**이 변합니다.\
```java
int a = 1;
a = 5;
```
위의 참조변수 a는 값이 바뀌어도 같은 객체입니다.\
\
반면, string 클래스는 변수의 값(value)을 변경하면 새객체를 생성합니다.\

```java
String str = "원래 값";
str = "수정 값";
```
이때 참조변수 str이 참조하는 객체는 **서로 다른 객체**입니다.\
\
위와같이, 불변객체는 내부 상태를 제공하거나 수정하는 메소드가 없거나 **방어적 복사**를 통해 제공합니다.\
string 클래스의 방어적 복사는 toCharArray메소드가 있습니다.\

```java
public char[] toCharArray(){
    // Cannot use Arrays.copyOf because of class initialization order issues
    char result[] = new char[value.length];
    System.arraycopy(value, 0, result, 0, value.length);
    return result;
}
```

### 3. new 생성자

```java
int a = 1;
int b = 1;
```
위의 경우 a와 b는 **서로 다른 객체**를 참조합니다.\
\
반면 string클래스의 경우,\
```java
String str1 = "Hello World";
String str2 = "Hello World";
String str3 = new String("Hello World");
```
서로 같은 값을 가졌다면 str1과 str2는 **같은 객체를 참조**합니다.\
하지만 new를 통해 객체를 생성하게 되면 **무조건 새로운 객체**를 생성합니다.(다른 객체)\


### 4. equals()와 == 비교연산자
두 객체가 같은가를 비교하기 위해서는 == 비교연산자를 이용하여 boolean값을 받아내지만\
앞서본,

```java
String str1 = "Hello World";
String str2 = "Hello World";
String str3 = new String("Hello World");
System.out.println(str1 == str2);
System.out.println(str1 == str3);
```
위와 같은 경우, 일반적인 생각으로는 **값**이 같기 때문에 세 변수 모두 같다고 보는게 우리가 의도한 생각입니다.\
하지만, 실제로는\
>true

>false

위와 같이 의도한 생각과 다른 결과가 나오게 됩니다.\
\
== 비교연산자는 주소값(hashcode)을 비교하는 **Call by Reference**이기 때문입니다.\
== 비교연산자는 primitive type(기본형 타입)일 때는 값을 비교하고, reference type(참조형 타입)일 때는 객체의 주소가 같은지 비교합니다.\
2번 소목차에서 보았듯이 str1과 str2은 같은 객체를 참조하고있어서, 주소값이 같습니다.\
str1과 str3는 다른 객체를 참조하고있어서, 주소값이 다르기 때문에 false값이 나옵니다.\
\
string 같은 참조형 타입은 같은 객체인가를 비교하기 위해선 주소값을 비교하는 것이 아닌,\
실제 값을 비교하는 __Call by Value__ 방식이 적합합니다.\
string 클래스에서 값을 비교하기 위해서 메소드 재정의(overriding) 된 eqauls()를 제공합니다.\

```java
System.out.println(str1.eqauls(str2));
System.out.println(str1.eqauls(str3));
```
>true

>true

위와 같이 equals메소드를 이용하면 의도한 결과가 나오게 됩니다.\

eqauls()는 Object클래스의 메소드이므로 모든 객체에서 사용할 수 있습니다.\
재정의 하여 사용하는것이 권장되는데, 이때 hashcode()를 함께 재정의 해야합니다.\

> equals로 true라면 반드시 hashcode도 같아야 함.

>반대로 hashcode가 같은 값이어도 equals는 false일 수 있음.
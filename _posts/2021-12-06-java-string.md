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
1. 불변객체(Immutable Object)
string 클래스는 **불변객체**입니다.
불변객체란, 객체가 생성된 후 그 객체의 **상태**를 변경 할 수 없는 객체입니다. (read-only, 수정불가능)

2. 방어적복사(defensive-copy)
일반적으로 **참조변수**를 통해 값을 수정한다면 의도대로 **값(상태, value)**이 변합니다.
> int a = 1;
> a = 5;
위의 참조변수 a는 값이 바뀌어도 같은 객체입니다.

반면, string 클래스는 변수의 값(value)을 변경하면 새객체를 생성합니다.

> String str = "원래 값";
> str = "수정 값";
이떄 str이 참조하는 객체는 **서로 다른 객체**입니다.

이런 경우도 있습니다.
>int a = 1;
>int b = 1;
당연하게도 위의 경우 a와 b는 서로 다른 객체를 참조합니다.

하지만 string클래스의 경우,
>String str1 = "Hello World";
>String str2 = "Hello World";
>String str3 = new String("Hello World");
서로 같은 값을 가졌다면 str1과 str2는 **같은 객체를 참조**합니다.
하지만 new를 통해 객체를 생성하게 되면 **무조건 새로운 객체**를 생성합니다.

위와같이, 불변객체는 내부 상태를 제공하거나 수정하는 메소드가 없거나 **방어적 복사**를 통해 제공합니다.
string 클래스의 방어적 복사는 toCharArray메소드가 있습니다.

```java
public char[] toCharArray(){
    // Cannot use Arrays.copyOf because of class initialization order issues
    char result[] = new char[value.length];
    System.arraycopy(value, 0, result, 0, value.length);
    return result;
}
```

3. equals()와 == 비교연산자
일반적으로 두 객체가 같은가를 비교하기 위해서는 == 비교연산자를 이용하여 boolean값을 받아내지만,
string 클래스에서 값을 비교하기 위해서는 메소드 재정의(overriding)를 한 eqauls()를 제공합니다.

앞서본,
>String str1 = "Hello World";
>String str2 = "Hello World";
>String str3 = new String("Hello World");
>System.out.println(str1 == str2);
>System.out.println(str1 == str3);
위의 경우에서 str1과 str3는 다른 객체이지만 값이 같으므로 == 비교연산자를 이용한 비교시,
true가 나오는 것이 일반적인 생각이지만, 실제로는
>true
>false
와 같이 결과가 나오게 됩니다.
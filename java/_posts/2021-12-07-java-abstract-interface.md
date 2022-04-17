---
layout: single
title:  "추상클래스"
categories: java
tags: [java, abstract, interface]
toc: true
toc_sticky : true
author_profile: false
sidebar:
    nav: "docs"
search: true
---

## abstract와 interface

| abstract                   | interface                                      |
| -------------------------- | ---------------------------------------------- |
| 단일 상속(부모.자식 관계)            | 다중 상속                                          |
| 하나라도 구현된 메소드가 있다면 abstract | 모든 메소드가 추상 메소드                                 |
| 상속을 받아 기능 __확장__이 목적       | 구현하는 객체가 같은 동작을 보장하는 것이 목적                     |
| 특정 메소드들은 자손에서 구현해야 할 경우    | 구현하는 모든 클래스가 __특정한 메소드들이 반드시 존재__하도록 강제해야 할 경우 |

> 참고) final 클래스 : 더 이상 확장이 불가능한 클래스.(String같은...)
> 
> default 메소드 : 인터페이스에서 메소드의 내용을 포함하여 선언할 수 있게 함.(java8에 추가됌)



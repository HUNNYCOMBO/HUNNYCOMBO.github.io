---
layout: single
title:  "객채지향의 원리 - SOLID"
categories: java
tags: [java, solid, oop]
toc: true
toc_sticky : true
author_profile: false
sidebar:
    nav: "docs"
search: true
---

## 참조
+ [nextree블로그](https://www.nextree.co.kr/p6960/)
+ [wjdrbs96블로그](https://devlog-wjdrbs96.tistory.com/380)

## 객체지향(obejct-oriented programing)을 왜 사용할까?
객체지향은 실제 무언가를 설계할 때, 우리가 추상적으로 생각하는 설계도라는 개념을 도와줍니다.  
즉, 설계적인 측면이 강화된 언어입니다. 절차지향언어보다 (메모리같은)세부적인 설정은 할 수 없지만, **유지보수가 쉽고, 유연하며 확장이 쉬운** 애플리케이션을 만들 수 있습니다.  

## 객체지향의 원리
객체지향의 장점을 지키기 위해 따라야하는 5가지 원칙을 SOLID라고 합니다.  
5가지 원칙은 서로 조금씩 겹치는 개념이 존재할 수 있습니다.  

- Spr(single Responsibility Principle)
- Ocp(Open colse Principle)
- Lsp(The Liskov Substitution Principle)
- Isp(interface Segregation Principle)
- Dip(Dependency Inversion Principle)

### 1. SPR / 단일 책임의 원칙

> 어떤 클래스를 변경해야 하는 이유는 오직 하나뿐이어야 한다.

#### 1.1 정의
SPR원리를 적용하면 책임 영역이 확실해지기 때문에, 한 책임이 변경 될 때 다른 책임들이 변경되야하는 연쇄 작용을 피할 수 있게됩니다.  
뿐만 아니라 가독성 향상이라는 이점 까지 누릴 수 있습니다.  

#### 1.2 적용방법

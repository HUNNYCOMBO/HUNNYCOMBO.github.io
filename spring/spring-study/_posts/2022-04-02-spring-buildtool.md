---
title:  "spring의 빌드관리도구 - maven, gradle"
excerpt: "스프링의 빌드관리도구에 대해 알아봅니다."
tags: [maven, gradle]
header:
  teaser: /assets/images/spring/maven.png
---

## 1. 빌드
빌드란 소스코드 파일들을 컴퓨터에서 실행가능한 소프트웨어로 변환하는 일련의 정형화 된 과정으로  
컴파일, 테스팅, 배포 등 모든 과정의 집합입니다.  
빌드 툴(도구)는 이러한 빌드 과정을 자동으로 수행해주는 툴을 의미합니다.  
자바 빌드 도구에는 ant, maven, gradle 등이 있습니다.  

### 1.1. 빌드툴을 사용하는 이유
자바 빌드 도구가 없을 때는 웹 프로젝트를 생성한 후 직접 필요한 라이브러리를 다운로드하여 사용했습니다.  
하지만 스프링 버전이 자주 업데이트 됨에 따라 관련 라이브러리를 일일이 수정해야하는 불편함이 따랐습니다.  
이에따라 빌드 관리와 자동 라이브러리 관리기능을 해주는 maven이 등장하게 되었습니다.  

## 2. maven
### 2.1. 메이븐이란?
프로젝트를 진행하면서 사용하는 수많은 라이브러리들을 관리해주는 도구입니다.  
여기에 그치지않고 그 라이브러리들과 연관된 라이브러리르들까지 모두 관리가 된다는 점입니다.  

### 2.2. POM - Project Object Model
maven의 기능을 이용하기 위해 POM정보를 담고있는 pom.xml이 사용됩니다.  
pom.xml에서 주요하게 다루는 기능은 아래와 같습니다.  

- 프로젝트 정보 : 프로젝트명, 라이센스 등
- 빌드 설정 : 소스, 리소스, 라이프사이클 별 실행한 플러그인 등 빌드와 관련된 설정
- 빌드 환경 : 사용자 환경 별로 달라질 수 있는 프로파일 정보
- pom 연관 정보 : 의존 프로젝트(모듈), 상위 프로젝트, 포함하고 있는 하위 모듈 등

### 2.3. 라이프사이클
객체의 생명주기처럼 maven에는 라이플 사이클이 존재합니다.  

![다운로드](https://user-images.githubusercontent.com/78904413/161376730-e20bf0bc-f9d9-4840-b269-bf6491bf2150.png)

위의 그림처럼 크게 default, clean, site 라이플 사이클로 나누고 세부적으로 설정하는 phase가 있습니다.  

### 2.4. 플러그인
메이븐의 모든 기능은 플러그인을 기반으로 동작합니다. 플러그인에서 실행할 수 있는 각각의 작업을 goal이라고 하고, 
1개의 phase는 1개이상의 goal과 연결되어 있습니다.  


## 3. gradle
### 3.1.그레들이란?
자바뿐만아니라 c언어, 파이선등을 지원하며, 이론상 빌드 속도가 maven에비해 최대 100배 빠릅니다.  
안드로이드 앱의 공식 빌드 툴입니다. xml으로 라이브러리를 정의하고 활용하던 maven과 달리,  
gradle은 별도의 groovy 스크립트를 통하여 빌드 관리를 할 수 있습니다.  
스크립트 언어로 되어있어 if, else 등의 로직이 구현가능합니다.

### 3.2. groovy
groovy는 JVM에서 실행되는 스크립트 언어입니다. java와 달리 소스코드를 컴파일 할 필요가 없습니다.  
또한 java와 호환되며 클래스 파일 그대로 groov클래스로 사용할 수 있습니다.

## 참고링크
+ https://jeong-pro.tistory.com/168
+ https://dev-coco.tistory.com/65
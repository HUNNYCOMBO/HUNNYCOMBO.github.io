---
title: '클라우드 컴퓨팅 서비스 모델'
excerpt: 'laaS, PaaS, SaaS에 대해 알아보기'
tags: []
header:
  overlay: ![image](https://user-images.githubusercontent.com/78904413/234437723-ad612026-114f-48ad-a188-d8add234ce1b.png)

---

## 참고가 된 블로그
[zoohoney](https://zooteacher.tistory.com/entry/laaS-PaaS-SaaS-%EA%B0%9C%EB%85%90-%EB%B9%84%EA%B5%90-%EC%A0%95%EB%A6%AC)

LaaS, PaaS, SaaS는 클라우드 컴퓨팅의 서비스 모델 중 하나입니다.
각 서비스 모델은 제공되는 서비스 범위와 관리 책임에 따라 사용 용도가 다르며, 상황에 맞게 선택해야 합니다.
![image](https://user-images.githubusercontent.com/78904413/234437689-87c1c6e4-7628-4653-84e1-7e871765a9c6.png)

## 1. LaaS(Infrastructure as a Service)
![image](https://user-images.githubusercontent.com/78904413/234437760-862a31db-a7ef-47ce-b17c-cb0f22564d3a.png)

서버, 스토리지, 네트워크 등의 인프라를 제공하는 서비스 모델입니다.
infra란 일종의 준비된 시설로 이해할 수 있는 단어입니다.
사용자는 이러한 인프라를 대여하여 **자신이 필요한 OS, 미들웨어, 애플리케이션 등을 설치하고 구성**할수 있습니다.
대표적으로는 AWS, Azure, Google Cloud Platform 등이 있습니다.

장점
- 개발 및 테스트 환경을 필요에 따라 유연하게 확장 및 축소 가능

단점
- 일정한 사용량이 발생하는 경우 비용적인 측면에서 효용성이 감소
- 제공업체의 보안 문제 가능성
- 여러 클라이언트와 인프라 리소스를 공유해야 하는 멀티 테넌트 시스템 및 서비스 신뢰성 문제

## 2. PaaS(Platform as a Service)
![image](https://user-images.githubusercontent.com/78904413/234470423-66b71ed2-d25f-4a3f-9656-c68d89fa5a21.png)

애플리케이션을 개발, 배포, 운영하기 위한 플랫폼을 제공하는 서비스 모델입니다.
이러한 플랫폼은 인프라 및 미들웨어를 자동으로 관리하며,
애플리케이션 실행 환경이나 데이터베이스 등이 미리 마련되어 있어서
**사용자는 개발에만 집중**할수 있습니다.
대표적으로는 Heroku, Google App Engine, Azure App Service 등이 있습니다.

장점
- 개발 및 배포 프로세르를 빠르게 확보하며 유지관리 용이
- 수많은 사용자가 동일한 개발 응용 프로그램에 엑세스 가능
- 기본 소프트웨어 구성 요소를 활용하여 자체 애플리케이션을 개발할 수 있으므로 자체적으로 작성해야 하는 코드의 양을 줄일 수 있음


단점
- 기본적으로 애플리케이션과 플랫폼이 함께 제공되기 때문에 애플리케이션이 플랫폼에 종속되어 다른 플랫폼으로의 이동이 어려움

## 3. SaaS(Software as a Service)
![image](https://user-images.githubusercontent.com/78904413/234471598-0107c887-0f30-484d-b1f8-a4b45277ba9c.png)


클라우드 기반으로 제공되는 소프트웨어 서비스를 말합니다.
제공 업체에서 소프트웨어와 데이터, 버그 수정 및 기타 유지관리를 제공합니다.
사용자는 비용만 내고 대시보드 또는 API를 통해 서비스를 사용하게 됩니다.
이러한 소프트웨어는 사용자가 로컬 컴퓨터에 설치할 필요 없이 **인터넷을 통해 웹 브라우저나 모바일 앱 등을 통해 접근**할 수 있습니다.
대표적인 예시로는 Google Drive, Dropbox, Office 365등이 있습니다.


장점
- 소프트웨어 설치, 관리 및 업그레이드와 같은 작업에 소요되는 시간과 비용을 줄임
- 웹만 접속하면 되기 때문에 접근성이 좋고 최신 SW업데이트를 빠르게 제공 받음

단점
- 외부망을 사용하기 때문에 외부의 데이터 노출에 대한 보안상 이슈 발생 가능성

---
title:  "초창기 웹 서비스 구조 - 유튜브 강의(널널한 개발자 TV)"
tags: [web]
excerpt: "web의 작동방식에 대해 고전부터 현재까지 알아봅니다."
---

+ [1부](https://www.youtube.com/watch?v=4Sfned8HLzk)
+ [2부](https://www.youtube.com/watch?v=byR3BcrChT8)
+ [3부](https://www.youtube.com/watch?v=poKkQHUBt9A)

## Web
팀 버너스 리가 고안한 HTML + HTTP의 형태. TCP/IP연결로 web client(browser) -  internet - web server 간의 http(request, response)통신을 합니다.  
이떄 통신이란 각각 고유한 ip주소를 가지고 URL요청을 해 리소스를 상호작용 합니다.

## HTTP
1.0부터 계속 버전이 업그레이드 되어 발전해왔다. TCP/IP연결을 전재하에 둡니다.  
HTTP의 가장 중요한 속성은 **stateless(무상태)**이지만 "연결"은 상태를 포함하는 개념이므로 작은 문제들이 발생했습니다.

## URL(uniform Resource Location)
자원의 주소를 나타냅니다. 정확한 경로는 표시하지 않습니다. URL 입력시 DNS를 통해 ip주소를 가져옵니다.  

## request method
URL을 통해 리소스를 가져오는 방식으로 대표적으로 GET(read), POST가 있습니다.

## 리소스를 가져와서 하는 순서(HTTP 1.1 / 초창기 웹)
1. 구문 분석(자료구조/BOM)
2. 렌더링(렌더링 엔진을 이용하여 내용을 표시)

이렇듯 초창기 웹은 단순히 연결해서 **정적인 문서**를 주고 받는 단방향(request, response) 구조였으나, 웹이 발전을 하며 양방향 상호작용을 필요로 하게 됐습니다.  
예를들면, id와 pw로 로그인을 할 때 클라이언트에서 POST방식으로 id와 pw **값**을 서버에게 넘겨줘야 하는 경우 입니다.  
양방향 통신이 적용되며 값을 처리해야 할 연산(WAS)이 생기게 되고 상태->전이를 기록(DB)해야 할 필요가 생기게 됐습니다.  
즉, id를 server로 보냈을 때, 기록되 있는 id가 존재할 수도, 않을 수도 있는 경우가 생기고 경우에 따라 동적으로 다른 response를 해줘야 합니다.  

## 정적인 HTML에서 동적인 HTML으로(웹 클라이언트/브라우저의 구조)
결국 웹은 복잡하고 거대해지면서 유지보수 편의성을 위해 역할을 분리합니다.

1. HTML 정보를 읽어들이는 파싱(자료구조)
2. 화면을 표현하는 CSS
3. 연산을 수행하고 동적인 결과를 내는 java script
4. 클라이언트에서 기록 역할을 하는 Cookie

## WAS(middleware) - MVC패턴
web server(Front-end) - WAS(처리주체) - DB(Back-end) 식의 3 tier 구조를 보면,  
WAS는 비즈니스 로직으로 연산을 처리(Service)하며,  
web으로 view를 보내고 db에서 자료구조 (model)을 가져오고, URI를 통해 제어(Control)하는 MVC achitecture/model이 생겨났습니다.

## Middleware
S/W와 H/W(정확히는 OS에서 cpu가 s/w적으로 실행되는 JVM)의 중간에서 원할한 실행을 돕는 각종 구성요소를 갖는(jJVM에서 작동하는 모듈 / db, I/O..)M/W는 framework를 사용하도록 강제하여 시스템이 효율적으로 운영되도록 돕습니다.  

## APM(application performance Monitoring)
성능을 좌지우지하는 DB의 응답속도와 JVM의 응답속도를 모티너링 하는 도구입니다. DB의 응답속도 개선을 튜닝이라고 합니다. WAS의 처리속도나 네트워크 성능은 모니터링 하지 않습니다.  

## JSON
JSON은 response로 응답 할 때, 데이터만 보내는 것입니다. 그 이유는 ios/android/window등의 환경이 다양해지며 환경에 따라 UI가 변경될 필요가 있었습니다. 그렇기에 기존 HTML을 응답하는 것이 아닌, JSON이라 하는 데이터 자체를 응답하게 했습니다. 클라이언트단에서는 JSON으로 자신의 환경에 맞는 HTML을 java script로 스스로 생성하도록 (이때, react.js나 vue.js같은 프레임워크의 도움을 받습니다.) 합니다.  
결국 web은 request CRUD 함수를 호출(Call)하고 JSON으로 응답하는 형태(RESTful API)로 발전했습니다.  

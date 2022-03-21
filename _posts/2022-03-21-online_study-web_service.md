---
layout: single
title:  "초창기 웹 서비스 구조 - 유튜브 강의(널널한 개발자 TV)"
categories: web
tags: [web, 온라인강의]
toc: true
toc_sticky : true
author_profile: false
sidebar:
    nav: "docs"
search: true
---

## Web
팀 버너스 리가 고안한 HTML + HTTP의 형태. TCP/IP연결로 web client(browser) -  internet - web server 간의 http(request, response)통신을 합니다.  
이떄 통신이란 각각 고유한 ip주소를 가지고 URL요청을 해 리소스를 상호작용 합니다.

## HTTP
1.0부터 계속 버전이 업그레이드 되어 발전해왔다. TCP/IP연결을 전재하에 둡니다.  
HTTP의 가장 중요한 속성은 **stateless(무상태)**이지만 "연결"은 상태를 포함하는 개념이므로 작은 문제들이 발생했습니다.

## URL(uniform Resource Location)
자원의 주소를 나타냅니다. 정확한 경로는 표시하지 않습니다. URL 입력시 DNS를 통해 ip주소를 가져옵니다.  

## request method
URL을 통해 리소스를 가져오는 방식으로 대표적으로 GET(read), POST가 있습니다.\\

## 리소스를 가져와서 하는 일(HTTP 1.0)
1. 구문 분석 
2. 렌더링(렌더링 엔진을 이용하여 )

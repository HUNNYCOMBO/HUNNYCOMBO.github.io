---
title:  "커버링 인덱스"
tags: [커버링 인덱스]
excerpt: "mysql에서 주로 사용하는 커버링 인덱스에 대해 알아봅니다."
header:
  teaser: /assets/images/etc/mysql.png
---

## 참고 링크
+ [jojoldu 블로그](https://jojoldu.tistory.com/476)
+ [gywn.net 블로그](https://gywn.net/2012/04/mysql-covering-index/)
+ [사전지식 - index](https://hunnycombo.github.io/database/database-index/)

## 1. 커버링 인덱스란?
MySQL의 경우 index 안에 포함된 데이터를 사용할 수 있으므로 이를 잘 활용한다면 실제 데이터까지 접근할 필요가 없습니다.  
이처럼 query를 충족시키는데 필요한 모든 데이터를 갖고 있는 index를 커버링 인덱스라고 합니다.  
즉, SELECT, WHERE, ORDER BY, GROUP BY 등 쿼리에 사용되는 모든 컬럼이 인덱스의 구성요소인 경우를 얘기합니다.  
때문에 컬럼을 읽기 위해서 데이터 블록을 보지않고 B-Tree 스캔만으로 원하는 데이터를 인덱스에서 추출 할 수 있습니다.  
대용량 데이터 처리 시 커버링 인덱스를 활용하여 query를 작성하면 성능을 상단 부분 높일 수 있습니다.  

### 2. Using index
> 실행계획(EXPLAIN) : EXPLAIN키워드를 붙여서 실행 계획 정보를 제공받을 때 테이블 형식으로 결과를 보여줍니다.

커버링 인덱스가 적용되면 EXPLAIN 결과의 Extra 필드에 "using index"가 표기됩니다.(이떄 type필드에 index가 표기되는 것은 인덱스 풀 스캔으로 다른 의미입니다.)  
<img width="1020" alt="9986FD425E4933DF35" src="https://user-images.githubusercontent.com/78904413/163967322-402e34ef-5fb7-4038-b05b-022caf03639b.png">  


### 2.1. Clustered Key(PK) / Non Clustered Key(일반적인 인덱스)
클러스터 
미완

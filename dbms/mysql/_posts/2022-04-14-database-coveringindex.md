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

### 1. 커버링 인덱스란?
MySQL의 경우 index 안에 포함된 데이터를 사용할 수 있으므로 이를 잘 활용한다면 실제 데이터까지 접근할 필요가 없습니다.  
이처럼 query를 충족시키는데 필요한 모든 데이터를 갖고 있는 index를 커버링 인덱스라고 합니다.**(index도 데이터입니다.)**  
즉, SELECT, WHERE, ORDER BY, GROUP BY 등 쿼리에 사용되는 모든 컬럼이 인덱스의 구성요소인 경우를 얘기합니다.  
때문에 컬럼을 읽기 위해서 데이터 블록을 보지않고 B-Tree 스캔만으로 원하는 데이터를 인덱스에서 추출 할 수 있습니다.  
대용량 데이터 처리 시 커버링 인덱스를 활용하여 query를 작성하면 성능을 상단 부분 높일 수 있습니다.  

### 2. Using index
> 실행계획(EXPLAIN) : EXPLAIN키워드를 붙여서 실행 계획 정보를 제공받을 때 테이블 형식으로 결과를 보여줍니다.

커버링 인덱스가 적용되면 EXPLAIN 결과의 Extra 필드에 "using index"가 표기됩니다.(이떄 type필드에 index가 표기되는 것은 인덱스 풀 스캔으로 다른 의미입니다.)  
<img width="1020" alt="9986FD425E4933DF35" src="https://user-images.githubusercontent.com/78904413/163967322-402e34ef-5fb7-4038-b05b-022caf03639b.png">  


아래와 같은 천만 건의 데이터를 무작위로 넣었다고 가정합니다.  
```sql
create table usertest (
 userno int(11) not null auto_increment,
 userid varchar(20) not null default '',
 nickname varchar(20) not null default '',
 .. 중략 ..
 chgdate varchar(15) not null default '',
 primary key (userno),
 key chgdate (chgdate)
) engine=innodb;
```

### 3. 성능 비교

```sql
select chgdate , userno
from usertest
limit 100000, 100
```
위와 같은 select query를 실행해서

```text
************* 1. row *************
           id: 1
  select_type: SIMPLE
        table: usertest
         type: index
possible_keys: NULL
          key: CHGDATE
      key_len: 47
          ref: NULL
         rows: 9228802
        Extra: Using index
1 row in set (0.00 sec)
```
Using index의 결과를 볼 수 있는데, 이는 index만으로 원하는 데이터 추출을 하였다는 의미입니다.  
이와같이 데이터 추출을 index만으로 수행하는 것을 커버링 인덱스라고 합니다.

#### 3.1. where
1. 일반쿼리

```sql
select *
from usertest
where chgdate like '2010%'
limit 100000, 100
```
위와 같은 sql을 실행했을 때,
```text
************* 1. row *************
           id: 1
  select_type: SIMPLE
        table: usertest
         type: range
possible_keys: CHGDATE
          key: CHGDATE
      key_len: 47
          ref: NULL
         rows: 4352950
        Extra: Using where
```

실행계획에서 extra 항목에서 using where을 볼 수 있는데 이는 range검색 이후 데이터 추출은 직접 데이터 필드에 접근하여 추출한 것입니다.  
쿼리 수행 속도는 **30.37초**입니다.  
이런 일반 쿼리는 where에서 부분 처리가 된 결과set을 이용해 limit구문에서 일정 범위를 추출하고, 추출된 값을 데이터 블록에 접근하여 원하는 필드를 가져오기 때문에 수행 속도가 느립니다.  

2. 커버링 인덱스 쿼리

```sql
select a.*
from (
      select userno
      from usertest
      where chgdate like '2012%'
      limit 100000, 100
) b join usertest a on b.userno = a.userno
```
```text
************* 1. row *************
           id: 1
  select_type: PRIMARY
        table:
         type: ALL
possible_keys: NULL
          key: NULL
      key_len: NULL
          ref: NULL
         rows: 100
        Extra:
************* 2. row *************
           id: 1
  select_type: PRIMARY
        table: a
         type: eq_ref
possible_keys: PRIMARY
          key: PRIMARY
      key_len: 4
          ref: b.userno
         rows: 1
        Extra:
************* 3. row *************
           id: 2
  select_type: DERIVED
        table: usertest
         type: range
possible_keys: CHGDATE
          key: CHGDATE
      key_len: 47
          ref: NULL
         rows: 4352950
        Extra: Using where; Using index
```

이제 extra에서 using index를 확인할 수 있습니다. 쿼리는 **0.16초**로 엄청나게 단축되었습니다.  
일반 쿼리와 비슷하게 where에서 부분 처리된 결과set을 limit구문에서 일정 범위를 추출합니다.  
하지만 정작 필요한 값은 PK인 userno의 값입니다. innoDB에서 모든 인덱스 value에는 PK를 값으로 가지기 때문에(clustred index), index 접근만으로 원하는 데이터를 가져올 수 있게 됩니다.  
결과적으로 원하는 데이터 추출을 위해서 데이터 블록에 접근하는 횟수가 서브 쿼리안에 있는 결과의 수(100건)이기 때문에 일반 쿼리보다 월등히 좋은 성능이 나왔습니다.  

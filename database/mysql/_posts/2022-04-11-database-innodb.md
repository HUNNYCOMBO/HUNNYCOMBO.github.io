---
title:  "MySQL의 스토리지 엔진 - InnoDB"
tags: [innodb]
excerpt: "InnoDB에 대해 알아봅니다."
---

## 참고링크
+ [](https://joebaak.blogspot.com/2017/05/mysql-innodb.html)

## 1. 스토리지엔진
mysql은 테이블을 생성하면 테이블명과 같은 .frm파일을 만들고 그 안에 테이블의 정보를 저장합니다.  
스토리지 엔진에 따라 테이블 데이터와 인덱스를 저장하는 방식이 다릅니다.  
특정 테이블이 어떤 스토리지 엔진을 사용하는지 확인하려면 SHOW TABLE STATUS 명령을 이용합니다.  

## 2. 스토리지 엔진의 종류
- InnoDB
- MyISAM
- Memory
- Archive
- CSV
- Federated

## 3. InnoDB 엔진
가장 보편적으로 사용되는 InnoDB엔진에 대해 알아봅니다. InnoDB엔진은 트랜잭션 처리를 위해 고안됐습니다.  
InnoDB의 트랜잭션 정책은 대부분의 경우 롤백되지 않고 정상커밋되는 짧은 트랜잭션을 처리하기 좋게 되어있습니다.  
InnoDB의 테이블은 클러스터 인덱스(clustered index)위에 구성되어 있으며, 매우 신속한 기본키 조회가 가능합니다.  

### 3.1. primary key에 의한 클러스터링
모든 테이블은 기본적으로 pk를 기준으로 클러스터링되어 저장됩니다. 키값 순서대로 디스크에 저장이 되며, 이로 인해 pk에 의한 range스캔은 상당히 빨리 처리됩니다.  

> 클러스터링 : 영어 사전처럼 내용 자체가 순서대로 정렬되어 있고, 인덱스 자체가 책의 내용과 같습니다.

### 3.2. index
InnoDB는 index 테이블을 B-Tree(Balanced Tree)로 구성합니다. delete시에 실제 값을 삭제하는 것이 아닌 삭제되었다는 상태값으로 변경하여 index테이블에 성능영향을 최소화 합니다.  
index 재정렬이 일어나지않습니다.  

### 3.3. 효율
Index Range Scan은 주로 랜덤 I/O를 사용하며, Full Table Scan은 순차I/O를 사용합니다. 디스크에 데이터를 I/O하는데 걸리는 시간은 디스크 헤더를 움직여서 읽고 쓸 위치로 옮기는 단계에서 결정됩니다.  
순차I/O는 탐색을 위해 헤더를 1개씩 움직이는 반면 랜덤 I/O는 더 많이 움직입니다. 일반적으로 쿼리를 튜닝하는 것은 랜덤 I/O자체를 줄이는 것이 목적이라 할 수 있습니다.  
통계 작업등의 큰 테이블의 레코드를 읽을 때는 Full Table Scan을 사용하여 디스크 헤더의 움직임을 최소화 하는 방법이 효율적입니다.  

### 3.4. InnoDB Buffer Pool
최근 접근한 데이터는 다시 Access될 가능성이 크기 때문에, 랜덤 I/O의 비용을 줄이기 위해 InnoDB 엔진은 메모리 캐시를 이용하여 처리합니다.  

1. 변경할 B-Tree leaf nood가 Buffer Pool에 있다면 즉시 처리합니다.
2. 만약 key값이 Buffer Pool에 없다면, DB에서 불러옵니다.
3. 변경된 값을 Insert Pool에 저장시켜놓고, Disk에 쓰지않고 대기합니다.(쓰기작업시 속도 저하때문에)
4. 백그라운드 작업으로 해당 index Tree를 읽을 때마다 insert Buffer에 merge할 데이터가 있는지 체크 후 병합합니다.
5. 랜덤 I/O를 줄이기위해 변경할 데이터를 모아서 한번에 merge하거나 스레드 여유가 있을 때, 나눠서 처리합니다.

### 3.5. innoDB사용시 주의사항
1. Count(*)에 WHERE절을 사용하는 것을 권장합니다.  innoDB의 경우 Record Count를 캐시하지 않기 떄문에 where절을 사용하지 않을 경우 Full Tabel Scan이 됩니다.
2. Delete 보다는 Trucate를 성능면에서 권장합니다. MySQL은 LIMIT개수보다 record수가 많아지게되면 자체적으로 DELETE를 진행함으로서 LIMIT count를 맞추기 때문입니다.
3. FORCE index Hint를 설정해서 IN, NOT IN쿼리를 최대한 지양합니다. IN쿼리는 비교인자가 많아지면 Full Table Scan을 타는 경우가 발생하기 떄문입니다.  
4. LIMIT은 항상 조심해서 사용해야합니다. LIMIT 10000, 30이라면 10030개를 모두 select한 후 30개만 띄워주는 형식이기때문에 무리가 발생합니다.

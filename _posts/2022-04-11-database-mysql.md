---
layout: single
title:  "MySQL의 스토리지 엔진 - InnoDB"
categories: database
tags: [mysql, innodb]
toc: true
toc_sticky : true
author_profile: false
sidebar:
    nav: "docs"
search: true
---

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

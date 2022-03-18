---
layout: single
title:  "해시함수, hashmap, 해시충돌"
categories: data_structure
tags: [data_structure, hashmap, hash_fuction, hash_crush]
toc: true
author_profile: false
sidebar:
    nav: "docs"
search: true
---

+ 해쉬함수 전 보면 좋은 내용 [합의 알고리즘](https://steemit.com/kr/@yahweh87/1-consensus-problem)
+ 참조한 블로그 [yjshin](https://yjshin.tistory.com/entry/%EC%95%94%ED%98%B8%ED%95%99-%ED%95%B4%EC%8B%9C-%ED%95%A8%EC%88%98-%EC%9E%91%EC%84%B1-%EC%A4%91)
+ 참조한 블로그 [망나니개발자](https://mangkyu.tistory.com/102)


## 용어 요약
+ hashing : 해시함수를 이용하여 매핑하는 과정
+ key : 매핑 전 원래 데이터의 값
+ hash value(해시값) : 매핑 후 데이터의 값
+ hash table : 데이터의 색인 주소 + 해시값을 저장하는 자료구조

![해싱](https://user-images.githubusercontent.com/78904413/159003595-6d71e6fd-dc11-4c62-91db-fbe7d4f42def.jpg)


## 해시 함수
해시 함수는 임의의 길이의 데이터(입력)를 고정된 길이의 데이터(결과)로 매핑하는 함수 입니다. 해시 함수에 의해 얻어지는 값은 해시값, 해시코드라고 합니다. 주로 매우 빠른 데이터 검색을 위해 사용됩니다.  

해시 함수는 같은 **입력**에 대해서는 항상 같은 **출력**이 나오게 됩니다. 이러한 특징으로 무결성(조작불가, 유효성 판별)을 제공하기 위해 사용합니다. (암호학적)해시의 종류에는 md알고리즘 및 sha알고리즘이 있습니다.  

> 필자는 hascode()의 결과값을 객체의 주소값으로 알고 있었지만, hashcode는 객체의 주소값이 아니다. 단지 해시코드 규약에 따라 반환하는 고유한 정수값이다.

## 해시 사용 예
1. 비밀번호 암호화
2. 복제문서 판별(이때 고정된 길이의 해시값으로 비교하므로 속도에 유리합니다.)
3. 효율적이고 빠른 데이터 검색용도

## 해시 함수의 특징
### 1. 어떠한 길이의 입력값에도 항상 **고정된 길이의 해시값**을 출력합니다.
![해시1](https://user-images.githubusercontent.com/78904413/159002987-eaa08823-48cf-454f-a932-45f2c2976d9e.jpg)  
![해시2](https://user-images.githubusercontent.com/78904413/159003155-f6262d2b-d04f-453c-83ec-e9f4a6ef49a5.jpg)

"안녕하세요"의 입력값과 "가나다라마바사아자타카..."의 입력값의 길이가 다름에도 고정된 길이의 해시값이 출력됩니다.  

### 2. 입력값의 아주 일부만 변경되어도 **전혀 다른 해시값**을 출력합니다. = 무결성
![해시3](https://user-images.githubusercontent.com/78904413/159003185-11d50a54-5415-409d-bcd8-4116b9473e8b.jpg)  

"안녕하세요"와 "안녕하세요."의 사소한 차이에도 다른 해시값이 출력됩니다.

### 3. 그렇기에 출력된 결과 값을 토대로 입력값을 **유추할 수 없습니다**. = 암호용

## 해시 충돌
해시 함수에서 희박하게 같은 입력에 대해 다른 출력이 될 경우가 있습니다. 이는 입력값의 범위보다 해시값의 범위가 좁은 경우가 많기 때문에 발생합니다. 이런 경우를 해시 충돌이라고 표현하며, 충돌이 적은 해시 함수가 좋은 해시 함수 입니다.  

![해시충돌](https://user-images.githubusercontent.com/78904413/159003625-1b276faa-23df-43eb-86eb-26c4d709e8c5.jpg)  

위 그림에서 'john smith'와 'sandra dee'의 해시값이 같으므로 해시 충돌입니다.  

## 해시테이블
+ 충분히 큰 공간(배열)을 할당 받은 다음 해시 함수를 이용하여 고유 색인(index)을 생성합니다.
+ index를 활용해 값을 저장하거나 검색합니다.
+ (key, value)로 데이터를 저장하는 자료구조중 하나입니다.
+ 즉, 색인 주소값에 키와 해시값를 함께 저장합니다.
+ 이 값이 저장되는 곳을 버킷 혹은 슬롯이라고 칭합니다.

해시 테이블은 버킷이 비어있는 index값이 존재할 수 있습니다. 키의 전체 개수와 동일한 버킷 개수를 가진 해시테이블을 direct-address table이라고 하지만 효율적이지 못한 리소스 문제로 운용하지 않습니다.  

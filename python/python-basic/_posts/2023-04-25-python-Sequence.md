---
title: '파이썬 기초 - Sequnece'
excerpt: '순서가 있는 데이터집합인 시퀀스와 dict, set에 대하여 공부합니다.'
tags: [sequnece, List, tuple, dict, set]
---
---

데이터타입은 데이터를 다루기 위한 재료로서 자유자재로 다룰수 있어야 합니다.

## 1. List
리스트란 **순서가 있는** 데이터들의 모음입니다. 대괄호를 사용하며 각 데이터는 ,로 구분합니다.
하나의 변수에는 하나의 값만 저장할 수 있었습니다.(정확히는 주소값을 저장)
하지만 하나의 변수에 여러개의 값을 저장해야 하는 경우가 있을 수 있습니다.
예를들어 전교생이 100명이 있고 전교생의 수학성적평균을 구하고 싶은 경우라면, 100개의 변수를 사용하기보다는 list를 이용하여
하나의 변수에 저장하는 것이 효율적입니다.
문자열과 같이 +, * 연산자를 사용할 수 있습니다.

```python
name = ['순이','철수','영희']
score = [30, 50, 100]
```

![image](https://user-images.githubusercontent.com/78904413/234147377-aad34863-2862-49bd-97bc-9db9862350e4.png)

> java는 정적 타이핑 언어이기 때문에 List의 타입을 선언해주어야 했습니다. ArrayList와 LinkedList를 사용하면 여러 데이터 타입을 담을 수 있습니다.

이때 정수형 자료 1과 리스트자료형 [1]은 다른 값입니다. ( 1 != [1]  )
1은 하나의 값만을 가지고 있으며, 리스트와는 다르게 인덱싱이나 슬라이싱이 불가능합니다.
반면, [1]은 하나의 요소를 갖는 List이며, 인덱싱과 슬라이싱을 통해 요소에 접근할 수 있습니다.

> 그렇다면 파이썬의 문자열은 List라고 생각할 수있지만, 문자열은 전용 메서드가 존재하고 불변객체이기 때문에 List와는 다른 자료형이라고 볼 수 있습니다.

### 1.1. List 함수
- append : 리스트 끝에 데이터를 추가
- sort : 리스트 오름차순 정렬
- reverse : 리스트를 역순서로 정렬(sort와 같이쓰면 내림차순으로 정렬할 수 있음)
- index : 해당 요소의 index를 반환
- insert : 리스트 요소 삽입
- remove : 해당 리스트 요소 삭제
- pop : 가장 마지막에 들어온 데이터를 반환하고 해당 데이터를 삭제
- extned : 리스트확장

![image](https://user-images.githubusercontent.com/78904413/234150951-5752ff7b-f4f7-4e9a-ba5b-16ec2b96dae9.png)



## 2. tuple
리스트와 비슷하지만 **읽기전용(read-only)** 불변 자료형입니다.
즉, 데이터의 생성, 삭제, 수정이 불가능합니다. 시도시 오류가 발생합니다.
()를 사용합니다.

```python
a = ('서울', 1, 2, 4.6)
```

튜플은 인덱싱과 슬라이싱 및 +, * 연산자, len()가 사용 가능합니다.
이때, +, * 연산자는 다른 자료형과 사용할 수 없습니다.
연산자를 사용하면 튜플이 불변자료형이기 때문에 새로운 튜플이 생성되는 형식입니다.
![image](https://user-images.githubusercontent.com/78904413/234153080-a7b0fb6a-4fa8-49cd-9494-4f0afa3a8857.png)




## 3. Dict(딕셔너리)
- Key와 Value 쌍으로 구성된 자료형
- Key와 Value 는 : 으로 구분합니다.
- Key는 중복될 수 없습니다.(중복된다면 마지막으로 추가된 key와 value만 저장됩니다.)
- {}를 사용하여 ,를 이용하여 데이터를 구분합니다.
- 순서가 있는 것이 아니므로 인덱싱, 슬라이싱이 불가능(시퀀스 아님)
- JSON과 유사하기 때문에 자주 사용됩니다.

```python
user = {'name':'[lala, 경훈]', 'age':31}
# key는 name과 age이며 value는 [lala, 경훈]와 31 입니다.
```

key값으로는 숫자, 문자열, boolean, tuple 등 불변 자료형을 사용할 수 있습니다.
List는 변경 가능한 자료형이므로 사용할 수 없습니다.
이는 dict 내부의 Hash Table에서 key값의 위치가 변경되기 때문입니다.
key값이 변경되면 hash값이 변경되어 더 이상 key값을 찾을 수 없게됩니다.

![image](https://user-images.githubusercontent.com/78904413/234154733-fa658294-262c-4f9b-896c-1c975accbf2e.png)

반면, value는 변경 가능한 데이터 타입도 사용할 수 있습니다.

### 3.1. 딕셔너리 함수
- keys : 딕셔너리의 모든 key값을 반환
- values : 딕셔너리의 모든 value값을 반환
- clear : 딕셔너리의 모든 데이터를 삭제
- get : 특정 key값의 value 가져오기
- items : 딕셔너리의 모든 데이터를 key, value 묶음으로 가져오기
- in : 딕셔너리의 안의 특정key가 존재하는지 boolean으로 반환

## 4. 집합자료형(set)
- 교집합, 합집합, 차집합 등의 집합과 관련된 것을 처리하기 위한 자료형
- 데이터의 중복이 불가능(인덱싱을 지원하지 않아 List 변환 후 데이터를 가져와야 함)
- 순서대로 만들어 지지 않음(시퀀스 아님)
- 중복 데이터 삭제용으로 사용 가능

### 4.1. 집합자료형 함수
- set : 집합자료형 생성
- add : 데이터 추가
- update : 여러가지의 데이터 추가
- remove : 데이터 삭제

![image](https://user-images.githubusercontent.com/78904413/234156143-a3c6d16d-85b2-4deb-bdb3-3d4ab0d7cd28.png)

- intersection : 교집합 구하기
- union : 합집합 구하기
- difference : 차집합(공통되는 것을 삭제) 구하기
![image](https://user-images.githubusercontent.com/78904413/234277214-e6444cba-4142-445f-86c5-3eefd01da0dc.png)

## 5. bool
bool 자료형은 true(참)과 false(거짓)의 두가지 값을 가지고 있는 자료형입니다.
**조건문**에서 많이 사용됩니다.

```python
data1 = True
data2 = False

print(1<3)
# False
```

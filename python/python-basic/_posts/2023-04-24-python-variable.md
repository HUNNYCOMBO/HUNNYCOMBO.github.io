---
title:  "파이썬 기초 - 변수와 자료형"
excerpt: "주피터노트북의 설치 및 colab을 사용해보고, 변수와 자료형에 대해 공부합니다."
tags: [변수, 자료형]
header:
  teaser: 
  overlay_image: 
  overlay_filter: 0.4
---
## 참고가 된 블로그
- [메이플의 개발 스토리](https://mapled.tistory.com/entry/Jupyter-Notebook-specify-location)


## 1. 파이썬 기초
### 1.1. 파이썬의 특징
- 문법이 쉽고 간결함
- 빠른 개발속도
- 모바일프로그래밍은 불가능

### 1.2. 주피터노트북
- 오픈소스기반의 웹 플랫폼(터미널은 실행 중이어야 함)
- 개발 중간중간 프로그램을 실행하면서 결과를 확인 할 수 있음
- 시각화에 장점

<details>
<summary>설치 및 실행</summary>
  
```
pip install jupyter
jupyter notebook --notebook-dir='경로입력'
```

설치 후 콘솔에서 출력된 토큰을 브라우저 주소창에 입력합니다.
매번 이렇게 주소를 입력하는 것은 번거로우므로 설정 파일을 이용하여 실행경로를 지정해줍니다.

```
jupyter notebook --generate-config
```

C:\Users\~\.jupyter 경로에 가면 jupyter_notebook_config.py 파일이 생성되어 있을 겁니다.
해당 파일을 열어 주석을 없애고 원하는 경로로 설정합니다.
</details>

![image](https://user-images.githubusercontent.com/78904413/233944444-9a8b5ddf-5fe6-4777-bd8d-c8df046dbd35.png)
주피터노트북에서 위의 한 줄을 cell이라고 명칭합니다. 그리고 cell단위로 실행됩니다.

![cell 단위로 실행되는 모습](https://user-images.githubusercontent.com/78904413/233945525-d7d269de-fe57-4633-986e-4dfecea6dee0.png)
(cell 단위로 실행되는 모습)


### 1.3. Colab
구글 리서치 팀에서 개발한 클라우드 상에서 파이썬 코드가 작성가능한 제품으로 주피터노트북과 사용법이 비슷합니다.
저장은 구글드라이브에 저장됩니다.

![image](https://user-images.githubusercontent.com/78904413/233948539-b7ce450a-b6aa-4e22-b8ca-a39217dc4b2c.png)
(주피터노트북과 같이 cell단위로 실행되는 모습)

## 2. 변수 특징
프로그래밍이란 **data**를 가공하여 원하는 결과를 얻는 것이라 볼 수 있습니다.

- 메모리 : 데이터를 저장하는 공간으로 주소(hash)를 갖고 있음
- 변수 : 객체를 가르키는 것, 데이터의 값이 아니라 메모리에 저장된 객체의 주소를 알고 있음
- 변수 생성 규칙
  - 영어+숫자 등을 사용하여 생성
  - 반드시 문자부터 시작해야함
  - 파이썬은 앞에 들여쓰기(공백)이 의미가 있기 때문에 주의
  - 특수기호는 _ 만 사용 가능
  - 예약어(if, for, while, def, end, or ...)는 사용 불가능

![image](https://user-images.githubusercontent.com/78904413/234010623-1137f95d-e680-42b6-947a-025e31431ff0.png)

> java와는 다르게 변수의 타입을 선언해주지 않아도 되는데, 이는 js같이 동적 타이핑 언어(dynamic typing language)이기 때문입니다. 변수에 할당되는 값에 따라 자동으로 타입이 결정됩니다. 이로 인해 파이썬은 코드 작성 속도가 빠르고 유연성이 높아지지만, 컴파일 시간에 타입 error를 발견 할 수 없기 때문에 성능이 떨어지며 디버깅이 어려울 수 있고, 코드 가독성이 떨어질 수 있습니다.

## 3. 숫자형
- 정수(integer) : 양의정수, 음의정수, 숫자
- 실수(float) : 소수점이 포함된 숫자
- 8진수(Oxtal)
- 16진수(Hexadecimal)

숫자형에는 +, -, \/, \*, %(나머지), \*\*(제곱), \/\/(몫) 등의 연산자 사용 가능

> java에서 int나 double 같은 기본자료형(primitive type)은 객체가 아니라 값(데이터) 자체를 저장합니다. 하지만 파이썬에서는 모든 값이 객체로 처리됩니다. java의 기본자료형은 메모리 영역 중 stack에 저장되므로 빠른 속도와 적은 메모리 사용량을 보장하는 장점이 있습니다. 객체는 비교적 생명주기가 긴 heap 메모리에 저장됩니다.

## 4. 문자열
- 문자나 단어 등으로 이루어진 문자들의 집합
- 문자열은 "" 혹은 ''로 둘러싸여 생성

![image](https://user-images.githubusercontent.com/78904413/234016561-e0177005-2972-4b3c-bf7e-184b9852b81a.png)

### 4.1. 문자열 연산
파이썬에서는 문자열끼리 더하기연산 또는 곱하기가 가능합니다.

> java의 String도 기본적으로 더하기 연산이 가능하지만, string타입은 값이 불변(immutable)하기 때문에 연산할 때마다 새로운 객체가 생성되어 메모리 낭비가 됩니다. 이를 방지하기 위해 수정이 빈번할 때에는 StringBuilder나 StringBuffer와 같은 가변객체를 이용합니다.
> 파이썬에서도 문자열은 불변객체이지만 슬라이싱 등을 통해 새로운 문자열을 생성합니다. 문자열이 매우 큰 경우에는 파일 I/O를 이용하여 수정하는 것이 효율적일 수 있습니다.

![image](https://user-images.githubusercontent.com/78904413/234018909-3582ecbd-2e4f-464b-98fd-6f503f2dccb9.png)

### 4.2. 문자열 인덱싱, 슬라이싱
- 인덱싱 : 문자열의 한 단어(char)당 0부터 시작하는 목차를 의미
- 슬라이싱 : a부터 b까지의 문자를 가져옴

![image](https://user-images.githubusercontent.com/78904413/234021345-e1b81f5c-17a9-47b9-84e4-61d194df41e5.png)

> 인덱싱과 슬라이싱은 문자열 뿐만 아니라 list 등 다양한 곳에 활용됩니다.

### 4.3. 문자열 Formatting
%서식 지정자를 이용하여 문자열을 포맷팅 할 수 있습니다. 예를들어 "나는 %s살이고 %s를 좋아합니다."%(31, "파이썬")와 같이 사용할 수 있습니다. %s는 문자열로 변환할 값이 들어갈 자리를 의미합니다. 첫번째 자리에는 31이 들어가고, 두번째 자리에는 "파이썬"이 들어갑니다.
![image](https://user-images.githubusercontent.com/78904413/234023804-1abcf0de-e307-496b-9569-1264c528be59.png)
(추가적으로 %f 는 실수를 표현할 수 있습니다.)

혹은 문자열 포맷 함수 .format()를 이용할 수 도 있습니다.
![image](https://user-images.githubusercontent.com/78904413/234025408-7a810b32-703b-4ded-8e01-ff8e642f96de.png)

### 4.4. 문자열 함수
![image](https://user-images.githubusercontent.com/78904413/234031204-e9f23a7b-c12d-4cd6-ae69-354765359b65.png)
![image](https://user-images.githubusercontent.com/78904413/234032378-a7d39825-19b4-4d35-af03-7d14171489c0.png)








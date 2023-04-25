---
title: '파이썬기초 - 제어문'
excerpt: '프로그래밍의 기초가되는 if문, '
tags: [if문, 반복문]
---

좋은 프로그래머가 되기위해서는 프로그래밍을 어떻게 구현하고 설계할지 우선하는 것이 좋습니다.

## 1. if문
조건문은 자료형에서 다룬 데이터를 어떠한 조건에 맞춰 판단한 후 처리 할 때 사용합니다.
조건문은 우선 **조건이 True가 되는지 False가 되는지**를 판단한 후 조건에 따라 어떻게 할지 프로그래밍을 할수 있습니다.
조건문에서 조건의 참이나 거짓이 되는 조건을 판단하기 위해 사용되는 연산자로 비교연산자와, 조건연산자가 있습니다.

### 1.1. 비교연산자
 - <
 - \>
 - \=\=
 - <\=
 - \>\=
 - \!\=

### 1.2. 조건연산자
- or : **하나만 참이어도** 참(|)
- and : 모두 참이면 참(&)
- not : 거짓이면 참(~)
- in  [],(), 문자열 : 어떤 데이터가 시퀀스에 존재하면 참
- not in [], (), 문자열 : 어떤 데이터가 시퀀스에 존재하지 않으면 참

### 1.3. 조건문의 기본구조
- 만약에 조건이 맞으면 실행내용1, 2, 3.... 을 실행
- if조건 끝에는 콜론(:)으로 끝났음(코드블록의 시작)을 알립니다. (java의 세미콜론(;)과 차이)
- 실행내용은 들여쓰기(tab)로 구분. (java에서는 실행문을 {}로 구분한 것과 차이)
- 파이썬에서 공백은 들여쓰기의 의미로 사용시 주의해야 함

> java는 ;을 사용하여 문장의 끝을 구분하고, 파이썬에서는 :와 들여쓰기로 블록의 범위를 정합니다.
> 이러한 차이는 파이썬은 코드의 가독성과 간결성을 강조하는 반면, java는 코드의 명확성과 정확성을 강조하기 떄문입니다.

```python
# 문제) 점수가 100점이면 "축하합니다"를 화면에 출력하시오.
score = 100

if score == 100:    # 조건문 => 참을 return하여 아래 실행문을 모두 실행하고 조건문을 벗어남
    print("축하합니다.")    # 실행문으로 만약 들여쓰기 라인에 다른 실행문이 있으면 차례로 실행



# 문제) id가 'aaa'이고 pw가 'bbb'면 '로그인 성공'을 출력하시오.
id = 'aaa'  # 들여쓰기 라인을 벗어났으므로 실행문이 아님
pw = 'bbb'

if id=='aaa' and pw=='bbb':
    print('로그인 성공')
```

> 만약 if문 안에서 변수를 정의하면 그 변수는 지역 변수(local variable)로 해당 if문에서만 사용할 수 있습니다. if문 외부에서 변수를 정의(전역 변수)했다면 if문 밖에서도 쓸 수 있습니다.
> 지역 변수의 예시로는 함수의 매개변수나 함수 내부에서 선언된 변수가 있습니다. 이 변수는 함수 내부에서만 사용이 가능하며 함수 외부에서는 접근할 수 없습니다.

### 1.4. 다양한 조건문
- if~ else~ 구문 : 조건이 참이면 if 블록을 실행, 거짓이면 else 블록을 실행
- if~ elif~ else 구문 : if의 조건이 거짓이면 다음 elif의 조건 체크(elif는 여러번 사용 가능), 모든 elif가 거짓이면 else 블록 실행
- pass : 조건문에서 아무것도 하지 않게 할 때 사용합니다. (java의 반복문에서 사용하는 contiune, break와 유사)

```python
score = 50

if score == 100:
  print('100점입니다.')
elif score >= 50:   # score >= 50 && score <= 99 로 하는 것은 이미 if문에서 걸러졌기 떄문에 자원낭비가 됩니다.
  print('50점~99점 입니다.')
else:
  print('분발하세요.')
  
# 50점 이상입니다.
########################################################################################################

# 문제) item = ['card1', 'key']
# item에 key가 있으면 '입장완료' 없으면 '입장불가'를 출력하고
# 입장완료시 item에 card1이 있으면 '1번룸으로 가세요'를 출력 그렇지 않다면 '로비로 입장하세요'를 출력

item = ['card1', 'key']

if 'key' in item:      #가독성을 위해 참으로 비교하는 것이 일반적입니다.
    print('입장완료')
    if 'card1' in item:
        print('1번룸으로 가세요.')
    else:
        print('로비로 가세요.')
else:
    print('입장불가')
```

## 2. 반복문
반복문은 비슷한 패턴 혹은 같은 패턴의 프로그래밍을 일정 횟수나 무한으로 반복해야 하는 경우 사용합니다.
예를들어 화면에 1부터 100까지의 숫자를 출력하는 코드가 있습니다.

```python
x=0

while x <= 100: #해당 조건이 ture면 처음으로 돌아가 반복하다 조건문이 false일 경우 실행하지 않고 벗어납니다.
  x=x+1
  print(x)
```

### 2.1. while문
가장 대표적인 반복문입니다.
if문과 마찬가지로 :으로 조건문의 끝을 나타내며 들여쓰기로 실행문을 구분합니다.
조건문을 잘못 설정하면 무한히 반복하게 되므로 ^ + z 혹은 주피터노트북에선 stop버튼으로 중지합니다.

- break : while문 안에서 강제로 while문을 종료
- contiune : while문 안에서 실행시 조건문으로 이동(continue 아래의 실행문을 실행하지 않음)

```python
count=0

while count < 5 :
  pirnt(count)
  count = count + 1
  if count == 2 :
    break
# 0
# 1

count=0

while count < 5 :
  count = count +1
  if count == 2 :
    continue
  print(count)

# 1
# 3
# 4
# 5
```

### 2.2. for문
다른 프로그래밍언어에서 가장 많이 사용되는 반복문이지만 파이썬에서는 조금 다릅니다. (java의 향상된 for문과 유사)
List나 tuple의 데이터를 순서대로 하나씩 가져와서 변수에 대입한 후 반복 실행합니다.
즉, 시퀀스의 길이만큼 반복 실행 됩니다.

```python
# for 기본구조
# for 변수 in 시퀀스:
    # 실행문...
list = [1,2,3,4,5]
for num in list:    # 5번 반복하게 됩니다.
    print(num)
```
![image](https://user-images.githubusercontent.com/78904413/234305501-e03adc37-ccf4-49af-9fdd-0e2e195fbd73.png)

java의 for문과 비교해봅니다.
```java
List<Integer> list = Arrays.asList(1, 2, 3, 4, 5);
for (Integer num : list) {
    System.out.println(num);
}
```
> 파이썬은 문장이 간결하여 가독성이 좋고 자바는 명확하게 변수의 데이터 타입을 표시하고 있는 차이점을 확인할 수 있습니다.

```python
# 두개의 변수에 각각 데이터를 저장할 수도 있음
for name, age in [('lala', 31),('경훈',31)]:
    print(name)
    print(age)
```
![image](https://user-images.githubusercontent.com/78904413/234306480-b2c4b66a-51f0-4faa-b35d-344f76993705.png)

> 반복문을 반복하면서 각각 name, age라는 변수에 인덱스 순으로 값을 대입합니다.

#### 2.2.1. range 함수
for문은 list를 주로 사용함으로 list를 생성할 경우가 많습니다. range는 list를 생성해주는 함수입니다.
- range(n) : 0부터 n미만 list 생성
- range(n,m) : n부터 m미만 list 생성

```python
score = [80,20,50,30,10]

for temp in range(len(score)):   # score의 길이만큼 list가 생성됨
  print('%d번쨰 학생의 점수는 %d입니다.'%(temp+1, score[temp]))
```
![image](https://user-images.githubusercontent.com/78904413/234311589-45324fe3-8759-40d4-8b60-b8201f266856.png)

#### 2.2.2. List comprehension
리스트 안에 for문을 넣어서 표현하는 방식입니다.
아래의 코드를 변경해 보겠습니다.
```python
score = [80,20,70,30,100]
hscore = [] # 전역변수로 설정해야 for문 외부에서 사용이 가능

for temp in score:
    if temp >= 80:
        hscore.append(temp)

print(hscore)
```

list 안에 for문으로 구현한 코드
```python
score = [80,20,70,30,100]
hscore = [temp for temp in score if temp >= 80] # 간결하지만 가독성은 매우 떨어짐.
                                                # score의 길이만큼 반복하고 if 조건문에 맞으면 temp변수에 값을 넣음
print(hscore)
```
![image](https://user-images.githubusercontent.com/78904413/234314878-eafc4da1-2ab0-4f69-9508-0da83e191982.png)


---
title: '함수와 클래스'
excerpt: '파이썬의 함수와 클래스에 대해 알아보기'
tags: [class, method]
---

## 1. 함수(method)

함수란 프로그램에서 특정 기능을 하도록 이름을 붙인 코드입니다.
함수는 한번 정의하면 반복해서 호출할 수 있고 입력값(매개변수)도 매번 다르게 받을 수 있습니다.
함수를 정의할 때는 **하나의 기능**만 동작하도록 작성하는 것이 원칙입니다.(OOP)

> 매개변수 역시 지역변수로 stack 메모리에 저장되어 함수 내부에서만 사용가능합니다.

### 1.1. 함수생성

- def 라는 명령어 사용
- 끝에 소괄호를 이용하여 매개변수 등을 넣음
- 결과값을 돌려줘야 할 때는 return 명령어를 사용합니다.(return이 없으면 아무것도 전달하지 않습니다.)

```python
def 함수명(매개변수):
  # 원하는 기능작성
  
  return 결과값
###########################################
def printScore(a,b):    # 함수의 정의
    print('당신의 점수는 %d점 입니다.'%(a+b))   # 단순히 매개변수로 들어온 숫자 a,b를 더하는 함수

printScore(10,5)
```
![image](https://user-images.githubusercontent.com/78904413/234593686-ccc8cb68-c3c2-4ff9-9f76-cbb874a8ec86.png)

> 파이썬의 함수는 모듈이나 class가 로드될 때 메모리에 올라갑니다.
> 따라서 함수 호출 시 매번 함수 객체가 메모리에 다시 로드되는 일은 없습니다.

#### 1.1.1. 타입 어노테이션

만약 매개변수의 타입을 지정하고 싶다면 타입 어노테이션을 사용합니다.
타입 어노테이션은 매개변수 이름 뒤에 \:을 붙이고 그 뒤에 타입을 지정합니다.
```python
def add(x: int, y:int) -> int;
  return x + y
```
위의 코드에서는 x와 y의 매개변수 타입을 int로만 받게 지정할 뿐 아니라 return값도 int로 지정하고 있습니다.
파이썬은 동적 타이핑 언어이기 때문에 타입 어노테이션이 있어도 실제로 매개변수에 전달되는 값이 해당 타입과 일치하지 않을 수 있습니다.
따라서 타입 어노테이션은 주석이 아니며, runtime에 타입 검사가 이루어지지 않습니다.

### 1.2. 함수에서 변수 사용

함수 내부에 정의된 변수는 지역변수입니다. 함수 내부에서는 전역 변수를 참조하거나 수정할 수 없습니다.
함수 내부에서 전역 변수를 사용하는 경우, 파이썬은 먼저 함수 내부에서 지역 변수(local variable)로 선언되었는지 확인합니다.
만약 지역 변수로 선언되어 있다면 해당 지역 변수가 사용됩니다.
그러나 전역 변수로 선언되어 있다면, 함수 내부에서는 해당 전역 변수에 접근할 수 없습니다.

이때 global 키워드를 사용하면 함수 내부에서도 전역 변수에 접근할 수 있습니다.
global 키워드 뒤에 전역 변수의 이름을 지정하면 해당 함수에서는 그 변수가 전역 변수임을 인식하고,
전역 변수에 대한 참조 및 수정이 가능해집니다.

```python
a = 20    # 전역변수 a
def test():
    a = 10    # 지역변수 a

test()
print(a)
```
![image](https://user-images.githubusercontent.com/78904413/234596234-c8969d3b-8081-4f02-8d02-a83c357309d8.png)

위와 같이 원하는 대로 test함수를 호출해도 a의 값이 수정되지 않습니다. 이때 global 키워드를 사용합니다.

```python
a = 20
def test():
    global a
    a = 10

test()
print(a)
```
![image](https://user-images.githubusercontent.com/78904413/234596551-1cfed6d6-a92e-411c-b529-0d3b9ac8c4d2.png)

### 1.3. 복수의 return

return값이 여러개일 경우 List, tuple, dict 등 다양한 자료형을 사용할수 있습니다.
단 이 방법은 반환된 값들을 인덱스를 사용하여 개별적으로 접근해야 합니다.
그렇기 때문에 객체를 이용하여 여러 개의 값을 객체의 맴버 변수를 통해 반환하도록 구현하는 것이 좋습니다.

```python
def minnum(text):
    min1 = text[0:6]
    min2 = text[7:]
    return (min1, min2)
            
result = minnum('123456-5544332')
print(result)
```
![image](https://user-images.githubusercontent.com/78904413/234601608-f89ee43b-00e9-4283-8012-a3f0d7313ed5.png)

위의 튜플 반환 보다는 아래와 같이,

```python
class Person:
    def __init__(self, name, age):  # java의 생성자와 같음
        self.name = name  # 클래스 맴버 변수
        self.age = age

def get_person_info():
    person = Person("John Doe", 30)
    return person
```
Person 클래스를 정의하고, get_person_info() 함수를 이용하여 이름과 나이를 Person객체로 반환하는 방식이 더 좋습니다.

### 1.4. 여러개의 매개변수(가변인자)
매개변수를 활용하는 방법에는 매개변수 이름을 활용하는 방법이 있고 \*을 활용하는 방법이 있습니다.
\*을 이용하면 해당 매개 변수에 List 형태로 데이터가 들어갑니다.

> java에서 사용했던 가변인자(int... num)과 같다고 볼 수 있습니다.

```python
def userinfo(*data): # 가변인자
    for temp in data:
        print(temp)

userinfo('lala', 31, 'songpa')
```
![image](https://user-images.githubusercontent.com/78904413/234606991-93efe04f-6702-46b0-b81d-661458e25b48.png)

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
이때 일반적인 매개변수와 같이 사용할 때는 **반드시 가변인자가 뒤에** 와야합니다.

> java에서 사용했던 가변인자(int... num)과 같다고 볼 수 있습니다.

```python
def userinfo(*data): # 가변인자
    for temp in data:
        print(temp)

userinfo('lala', 31, 'songpa')
```
![image](https://user-images.githubusercontent.com/78904413/234606991-93efe04f-6702-46b0-b81d-661458e25b48.png)

### 1.5. \*\*kwargs

반면 \*\*을 사용하는 매개변수도 있습니다. 이 매개변수는 dict형태로 저장됩니다.
key와 value로 이루어져 있기 때문에 변수명=값 형태로 입력할 수 있습니다.

```python
def userdata(name, **data): ##kwargs
    print(name)
    print(data)

userdata('lala', age=31, add='songpa')
```
![image](https://user-images.githubusercontent.com/78904413/234609377-73fba8d9-40b8-4357-9fee-1643ad7263c4.png)

### 1.5. lambda 함수

def 명령어 대신 lambda 명령어를 사용합니다.
함수를 한줄로 정의할 수 있어 간결합니다.

```python
def userinfo(name, age):
    print('name......')
# 위의 코드를 한줄로 표현
userinfo = lambda name,age: print('name...')
```

### 1.6. input 사용자 입력

사용자가 입력한 값을 변수에 넣을 때 사용합니다.
input 키워드를 사용합니다.

```python
name = input('입력하세요.')
print('입력값 : %s'%name)
```
![image](https://user-images.githubusercontent.com/78904413/234611605-cdd39021-1f0d-44aa-a35a-79b89e21cb04.png)

### 1.6. 파일 read, write

저장공간에서 파일을 CRUD합니다.
open 키워드를 사용합니다. 모드는 w(쓰기), r(읽기), a(추가하기)가 있습니다.
반드시 close함수로 마지막 열려있는 객체를 닫아줘야 합니다.
with 키워드를 사용하면 저장과 동시에 close()를 자동으로 합니다.

```python
f = open('test.txt', 'w') # \\로 경로를 지정도 가능
f.close()

namelist = ['lala', 'lucy']

with open('name.txt' 'w') as f: # 변수명=f
  for temp in namelist:
    f.write(temp+'\n')  # 개행
```

- readline() : 파일 내용을 한줄씩 가져옵니다. r모드
- readlines() : 모든 줄을 List로 가져옵니다. r모드

## 2. 클래스

### 2.1. 객체지향프로그램(Object Oriented Programming)

클래스란 객체지향프로그래밍에서 등장하는 개념입니다.
객체지향이란 프로그램을 여러개의 오브젝트(객체) 단위로 나누어서 작업하는 방식입니다.
이 오브젝트들은 유기적으로 상호작용 합니다.
오브젝트는 클래스를 통해 만들어집니다.

각 오브젝트는 하나의 책임을 갖기 때문에 유지보수를 하기 매우 용이합니다.
예를들어 자동차를 만든다면 엔진에 문제가 생겼을 경우 엔진을 담당하는 오브젝트만 수정하면 되기 때문입니다.
이는 기존의 절차지향프로그래밍에 비해 코드 재사용 측면에서도 매우 유용합니다.

### 2.2. 클래스 생성

흔히들 클래스를 설계도, 오브젝트를 설계도를 통해 만들어진 제품으로 비유합니다.
클래스명에 첫글자는 대문자로 적는 규칙이 있습니다.
클래스 내부는 변수와 함수가 정의됩니다.

클래스는 생성자함수를 이용해 오브젝트를 생성해야만 사용할 수 있습니다.
**클래스내 함수의 매개변수의 첫번째 값은 self 키워드를 사용합니다.**
보통 호출할 때는 생략되어 매개변수로 전달 됩니다.

```python
class Car:
    def setname(self, name):    # 어떤 객체의 함수인지를 저장하고 있는 self 매개변수
                                # self를 이용하면 클래스의 인스턴스 변수를 다룰 수 있습니다.
        self.name = name    # Car클래스 인스턴스 변수인 name에 접근합니다.

car1 = Car()    # 오브젝트 생성. 기본 생성자를 이용
car1.setname('bmw') # Car클래스에 정의된 함수를 호출
                    # name만 넘겼지만 self는 자동으로 전달됌

print(car1.name)

```
![image](https://user-images.githubusercontent.com/78904413/234619695-60e0b5a6-f987-4bc3-9135-8bf9e0c72650.png)

### 2.3. 클래스 변수

클래스 변수는 기본적으로 static 변수로 해당 클래스의 모든 인스턴스에서 공유되는 변수입니다.
**클래스 이름을 통해 접근할 수있습니다.**
이는 클래스가 처음 로드 될 때 클래스 변수가 메모리의 static영역에 로드 되기 때문입니다.
static 영역에서 모든 인스턴스가 해당 변수에 접근하기 때문에 다른 인스턴스에서 변하면 모든 인스턴스에 그 변화가 영향을 받게 됩니다.

```python
class Car:
  cartype = '승용차' # 클래스 맴버 변수. 클래스가 로드 될 때 static영역에 위치
  
  def setCartype(self, name):
      self.cartype = name
  
car1 = Car()
car2 = Car()
print(car1.cartype) # '승용차'
print(car2.cartype) # '승용차'

Car.cartype = '트럭'  # 클래스 맴버 변수의 값을 변화
print(car1.cartype) # '트럭'
print(car2.cartype) # '트럭'

# 하지만 객체의 변수를 따로 지정하는 경우는
car2.setCartype('버스')
print(car1.cartype) # '트럭'
print(car2.cartype) # '버스'  # 객체의 변수를 불러오기 때문에 값이 다름
```
> 객체의 맴버 변수는 해당 객체와 함께 heap영역에 저장되기 때문에 self.cartype은 클래스 맴버 변수와 다른 값을 가지고 있는 것입니다.

### 2.4. 생성자

객체를 만들 떄 최초로 호출되는 함수입니다. 객체를 만들기 위해 초기화 할 때 사용합니다.
\_\_init\_\_() 이라는 함수를 사용하며 정의를 하지 않고 생략할 수 있습니다.(기본 생성자)
혹은 매개변수를 받게 정의할수 도 있습니다.(오버라이딩) 이때는 기본생성자 역시 작성해 주어야 합니다.

### 2.5. 상속

상속은 객체지향의 특징으로 다른 클래스의 기능을 상속받아 확장할 수 있는 클래스입니다.
class 클래스명(부모클래스, 부모클래스, ...)로 생성하며 다중상속이 가능합니다.

일반적으로 추상클래스와 추상메소드를 라는 개념을 사용합니다. 추상클래스는 직접 객체를 생성할 수 없으며,
추상클래스를 상속받은 자식 클래스에서 추상 메소드를 구현해야 합니다.

특정 기능을 필요에 따라 다르게 구현해야할 때 주로 사용합니다.
이때 자식클래스는 부모클래스의 변수나 메소드를 사용할 수 있지만, 그 반대는 불가능 합니다.
부모클래스에 접근할 때는 super 키워드를 사용합니다.

```python
from abc import ABC, abstractmethod       # abc모듈

class Animal(ABC):  # 추상클래스
    @abstractmethod
    def move(self): # 추상 메소드. 자식 클래스에서 반드시 정의해야합니다.
        pass

class Cat(Animal):  # 상속받은 자식 클래스
    def move(self):
        print("Cat moves by walking and running")

class Bird(Animal):
    def move(self):
        print("Bird moves by flying and flapping wings")

# Animal 클래스는 추상 클래스이므로 직접 객체를 생성할 수 없습니다.
# 따라서 Cat과 Bird 클래스에서 move 메서드를 구현해야 합니다.
# Cat과 Bird 클래스는 Animal 클래스를 상속받았으므로 move 메서드를 구현해야 합니다.

cat = Cat()
cat.move()   # "Cat moves by walking and running" 출력

bird = Bird()
bird.move()  # "Bird moves by flying and flapping wings" 출력
```


### 2.6. 모듈

모듈은 파이썬 파일(py파일)에 함수나 변수, 클래스 등을 모아놓은 것입니다.
만들어진 모듈은 import 키워드로 사용합니다.

만약 파일의 함수만 사용하고 싶다면 from ~ import 키워드를 사용합니다.
모듈의 변수도 파일명.변수명 으로 접근 가능합니다.

```python
from util import changeminnum

result = changeminnum('123456-654321')
print(result)
```

> 모듈(module)과 라이브러리(library)는 둘 다 코드를 재사용하고 중복을 피하기 위한 프로그래밍 개념입니다. 그러나 두 용어는 서로 다른 의미를 가지고 있습니다.

모듈(module)은 하나 이상의 함수, 클래스, 변수 등을 포함하는 단일 파일입니다. 모듈은 자체적으로 독립적인 기능을 제공하고 다른 모듈에서 재사용될 수 있습니다. 모듈은 import 키워드를 사용하여 다른 파일에서 사용될 수 있습니다.

라이브러리(library)는 모듈(module)의 집합입니다. 라이브러리는 특정 기능을 제공하는 모듈의 모음으로, 프로그래머가 자신이 필요한 기능을 쉽게 찾고 사용할 수 있도록 합니다. 예를 들어, 파이썬의 NumPy 라이브러리는 배열 및 행렬 연산에 필요한 여러 모듈을 제공합니다.

즉, 모듈은 단일 파일로 구성된 코드 블록이며, 라이브러리는 모듈의 모음입니다. 모듈은 개별적으로 사용될 수 있지만 라이브러리는 다른 모듈과 함께 사용되어 더 큰 프로그램을 작성할 수 있습니다.

### 2.7. 자주쓰는 파이썬 라이브러리

#### 2.7.1. time

- time() : 시간을 리턴
- localtime() : 년,월,일,시,분,초,요일 등의 형태로 리턴
- asctime() : 요일,월,일,시간 순으로 리턴
- sleep() : 반복문 등에서 매개변수만큼 딜레이를 줌

#### 2.7.2. 그외

- glob : 디렉토리에 있는 파일을 리스트로 저장
- shutil : 파일을 복사하거나 이동시 사용되는 모듈
- json : json 형태의 데이터를 다룰 때 사용
- pickle : 객체를 저장할 때 사용


### 2.8. 예외처리

예외처리는 프로그래밍 실행시 나오는(혹은 예상되는) 오류를 유연하게 **처리**하기 위해 사용합니다.
try, except 키워드를 사용합니다.
try는 오류가 생기지 않았을 때 실행하는 코드입니다.
except는 오류가 생겼을 때 실행하는 코드입니다.

```python
a = 3

try:
  print(b)
except:
  print('error')  # error
```

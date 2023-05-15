---
title: '파이썬의 함수'
excerpt: '파이썬의 함수 scope와 재귀함수, 익명함수에 대해 알아보기'
tags: [scope, lambda]
---

## scope
기본적으로 함수에서 선언된 변수는 local scope에 생성되며, 함수 종료시 사라집니다.
해당 스코프에 변수가 없는 경우 LEGB rule에 의해 이름을 검색합니다.(local, enclosed, global, built-in)
이떄 변수에 접근은 가능하지만, 해당 변수에 값을 재할당 할 수는 없어서 local scope의 새로운 참조가 생성되기 떄문입니다.
단, 함수 내에서 필요한 상위 scope의 변수는 인자로 넘겨서 활용합니다.(encolsed 제외)
상위 스코프에 있는 변수를 수정하고싶다면, global nonlocal 키워드를 활용 가능합니다.(권장하지 않음)


```python
num = 10  # global scope

def local_scope():  # local scope
  global num  # global 키워드로 global scope의 num을 가져옴. 해당 키워드의 유무에 따라 결과값이 다름
  num = 100 # global 키워드가 없다면, local scope영역의 메모리에 새로운 참조 num을 만들게 됨
  print(num)  # print sum 등의 함수는 built-in scope로 global scope보다 상위에 있음

  local_scope()
  print(num)
```

> 상수의 경우 java의 static final처럼 변수명을 대문자와 \_만으로 만들면 에디터에서 대문자 이름의 변수에 무언가를 할당 한다면 경고를 내줍니다.

파이썬은 타 언어와 다르게 block scope라는 개념이 없습니다. 때문에 반복문과 조건문에서의 변수는 재할당이 가능합니다.
```python
for i in range(10):
  print('hi')
  
print(i)

if True:
  x = True

print(x)
```

이떄 변수에 접근은 가능하다는것은 해당 변수의 함수도 실행할 수 있습니다. 함수를 통한 값의 조작은 scope에 영향을 받지 않습니다.
```python
numbers=[1]

def func():
  numbers.append(2)
  numbers.append(3)
  print(numbers)  # [1,2,3]

func()

print(numbers)  # [1.2.3]
```

## 얕은 복사
복사는 값은 같지만 참조는 다른 것을 말합니다. 하지만 이는 1차원 배열에서만 가능하며 2차원 이상 배열에서부터는 복사가 안되기 때문에 얕은 복사라고 부릅니다.

```python
a = [1,2]
b = a # 같은 참조

c = a[:]  # 얕은 복사
c.append(3)

d = a.copy()  # 얕은 복사
d.append(3)
################################################
# 2차원 배열 이상인 경우

a = [[1],[2]]
b = a

c a[:]
c[0].append('c')

d = a.copy()
d[1].append('d')
```

하지만 2차원 배열이상에서는 아래와 같이 참조하게 됩니다.
![image](https://github.com/lala-ogu/lala-ogu.github.io/assets/78904413/175d9230-0097-481b-93ca-be1a9602f636)

깊은 복사를 위해서는 copy의 deepycopy 함수를 사용합니다.

```python
import copy
e = copy.deepcopy(a)
e[1].append('e')
```

## 재귀함수
재귀함수는 함수가 자기 자신을 호출하는 것을 말합니다. 이를 통해 반복문과 같은 반복적인 작업을 수행할 수 있습니다.
재귀함수를 수행할 때는 종료 조건을 반드시 설정해야 합니다.
대표적으로 팩토리얼재귀함수를 예시로 들 수 있습니다.

```python
def factorial(n):
  if n == 1:  # 무한 재귀를 멈추기 위한 조건
    return 1
  else:
    return n * factorial(n-1)

factorial(7)
```

반복문과 재귀함수의 원리는 같습니다. 아래는 팩토리얼함수를 while문을 이용하여 구현한 코드입니다.

```python
def facto_while(n):
  result = 1

  while n > 0:
    result *= n
    n -= 1
    
  return result

print(facto_while(7))
```

재귀함수는 기본적으로 점점 범위가 줄어드는 문제를 풀게 됩니다.
재귀함수를 작성시에는 반드시 base case가 존재해야합니다.

> base case: 점점 범위가 줄어들어 반복되지 않는 최종점. 팩토리얼의 경우 1

이번에는 재귀함수와 반복문으로 피보나치 수열을 구현해봅니다.

```python
def fib(n):
  if n < 2:
    return n

  return fib(n-1) + fib(n-2)

fib(5)
####################################
result = [1,1]

def fib_loop(n):  # list를 사용할 경우 해당 함수를 여러번 호출 할 때 시간적 측면에서 장점이 생긴다.
  if n <= len(reuslt):
  return result[n]

  for _ in range(n-len(result)+1):
    result.append(result[-1] + result[-2])

  return result[n]

print(fib_loop(5))
#####################################
def fib_loop2(n): # 변수 두개를 사용한 방식은 메모리 측면에서 장점이 있다.
  a, b = 1, 1
  for _ in range(n-1):
    a, b = b, a+b
  return b

print(fib_loop2(5))
#######################################
def fib_while(n):
  a, b = 0, 1
  while n > 1:
    n -= 1
    a, b = b, a+b
  return b

print(fib_while(5))
```

### 반복문과 재귀함수의 차이
재귀호출은 변수 사용을 줄일 수 있습니다. 그러나 입력 값이 커질 수록 연산속도가 오래걸립니다.
재귀함수로 구현한 피보나치 수열의 시간복잡도는 O(2^n)입니다.
반복문은 재귀로 구현된 함수보다 연산 속도가 빠른 편입니다.

## 람다함수
람다식은 파이썬에서 함수를 간단하게 정의할 수 있는 방법 중 하나로, 익명함수 입니다.

> lambda 인자:표현식

위와같은 형태로 작성합니다.

```python
add = lambda x,y:x+y
print(add(1,2))

(lambda x,y:x+y)(1,2)
```

람다식은 주로 **함수를 인자**로 받는 함수에서 사용됩니다.
예를 들어, map()함수는 리스트의 모든 요소에 대해 특정 함수를 적용한 결과를 반환합니다.
이때 첫번째 인자로는 적용할 함수를 전달합니다.

```python
numbers = [1, 2, 3]
squares = list(map(lambda x: x ** 2, numbers))
print(squares)

list(filter(lambda n:n%2, range(20)))
```

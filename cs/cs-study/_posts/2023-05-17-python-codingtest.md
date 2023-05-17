---
title: '파이썬 기초 코딩테스트2'
excerpt: '파이썬의 기초 코딩테스트 풀어보기'
tags: [코딩테스트]
---

## 최대공약수, 최소공배수 구하기
> 두 수를 입력받아 두 수의 최대공약수와 최소공배수를 반환하는 함수 gcdlcm을 작성하세요.
> 배열의 맨 앞에 최대공약수, 그 다음 최소공배수를 넣어 반환하세요.
> 예를 들어 두 수 3, 12의 최대공약수는 3, 최소공배수는 12이므로 gcdlcm(3, 12)는 (3, 12)를 반환해야 합니다.

약수란, 1을 포함하여 딱 나누어 떨어지는 수를 의미한다.
최소공배수는 두 수의 곱을 최대 공약수로 나눈 것과 같다.
인자로 받은 두 정수의 약수들을 list로 담고 교집합과 max()를 이용하여 최대공약수를 구했다.

```python
def gcdlcm(a,b):
    list_a = []
    list_b = []
    for _ in range(1,a+1):
        # a의 약수를 list로
        if a % _ == 0:
            list_a.append(_)
    for _ in range(1,b+1):
        # b의 약수
        if b % _ == 0:
            list_b.append(_)

    # 최대공배수는 교집합으로 뽑아내기
    result1 = max(list(set(list_a)&set(list_b)))
    # 최소공배수는 두 수의 곱을 최대공약수로 나눈것
    result2 = int((a*b)/result1)
    return result1, result2
```

다른 풀이로는, 최대공약수의 다른 풀이로는 두 정수 중 작은 수 부터 내려가며
두 수를 동시에 딱 나누어 떨어지는 수를 찾는 방식도 있다.

```python
# solution 2
def gcdlcm2(a,b):
    big, small = a, b if a > b else b,a

    for gcd in range(small,0,-1):
        if big % gcd == 0 and small % gcd ==0:
            break
```

## 불쌍한 달팽이
> 달팽이는 낮 시간 동안에 기둥을 올라갑니다. 하지만 밤에는 잠을 자면서 어느 정도의 거리만큼 미끄러집니다. (낮 시간 동안 올라간 거리보다는 적게 미끄러집니다.)
> 달팽이가 기둥의 꼭대기에 도달하는 날까지 걸리는 시간을 반환하는 함수를 작성하세요.
> 함수의 인자는 다음과 같습니다.

> 기둥의 높이(미터)
> 낮 시간 동안 달팽이가 올라가는 거리(미터)
> 달팽이가 야간에 잠을 자는 동안 미끄러지는 거리(미터)

```python
def snail(height, clime_day, slide_night):
    # 날짜 체크
    day = 0
    while height > 0:
        day += 1
        height -= clime_day
        if height > 0:
            height += slide_night

    return day
```

## 무엇이 중복일까
> 다음 리스트에서 중복되는 요소만 뽑아서 새로운 리스트를 반환하는 함수를 작성하세요.

list의 count()를 이용하여 중복되는 요소를 뽑아 내어 set으로 중복되지 않게 추가하여 풀었다.

```python
def duplicated(elem):
    return list(set([x for x in elem if elem.count(x)>1]))
```

list만으로 해결하는 풀이도 있다.

```python
# solution 2
def dup2(chars):
    # 등장한 문자열 모으기
    registered=[]
    # 답
    answer = []

    for char in chars:
        # 등장한적 없는 알파벳
        if char not in registered:
            registered.append(char)
        # 등장한적은 있으나, 답에는 없다면
        elif char not in answer:
            answer.append(char)

    return answer
```

## 알파벳만 남기고 뒤집기
> 문자열이 주어지면, 해당 문자열 중에서 알파벳이 아닌 문자는 전부 빼고 거꾸로 뒤집어 반환하는 함수를 작성하세요.

ord함수를 써서 아스키코드를 활용하여 풀이하였다.

```python
def reverse_letter(str):
    new_str = ''
    for char in str:
        if 64 < ord(char) < 91 or 96 < ord(char) < 123:
           # print(char)
            new_str += char

    return new_str[::-1]
    
print(reverse_letter('krishan'))
print(reverse_letter('ultr53o?n'))
```
isalpha()를 활용하는 방법도 있다. 사실 그냥 아스키코드 대신 'a'를 사용해도 된다.

## 편안한 단어
> (QWERTY 키보드를 사용하여 타이핑 한다고 가정할 때) '편안한 단어'는 타이핑 할 때 손을 번갈아 칠 수 있는 단어를 말합니다.
> 단어를 인자로 받아 그것이 '편안한 단어'인지 여부를 True/False로 반환하는 함수를 작성하세요.
> 모든 단어는 a ~ z까지 오름차순으로 구성된 문자열입니다.
>> 문자 목록
>> 왼손: q, w, e, r, t, a, s, s, d, f, g, z, x, c, v, b
>> 오른손: y, u, i, o, p, h, j, k, l, n, m

```python
def comfortable_word(word):
    left = ['q', 'w', 'e', 'r', 't', 'a', 's', 'd', 'f', 'g', 'z', 'x', 'c', 'v', 'b']
    right = ['y', 'u', 'i', 'o', 'p', 'h', 'j', 'k', 'l', 'n', 'm']
    # 홀수면 right와 비교 짝수면 left와 비교
    for i in range(len(word)):
        if i % 2 == 1:
            if word[i] not in right:
                return False
        else:
            if word[i] not in left:
                return False
    return True
```
다만 이 경우에는 오른손이 먼저 오는 경우에는 오답으로 나온다. enumerate()를 활용한 반복문을 사용하여 해결하였다.
enumerate()는 index와 elements를 반환한다.

```python
# solution 2
def comf(word):
    left = ['q', 'w', 'e', 'r', 't', 'a', 's', 'd', 'f', 'g', 'z', 'x', 'c', 'v', 'b']
    right = ['y', 'u', 'i', 'o', 'p', 'h', 'j', 'k', 'l', 'n', 'm']
    
    first_char = word[0]

    if first_char in right:
        hands = [right,left]
    elif first_char in left:
        hands = [left, right]

    for i, char in enumerate(word):
        if char not in hands[i%2]:  # hands의 index는 0,1을 반복한다.
            return False
    return True
```


## 숫자패턴
> 원하는 행까지 아래의 패턴을 생성하는 함수를 작성하세요. 만약 인자가 0이나 음의 정수인 경우 빈 문자열('')을 반환하세요.
> 짝수가 인수로 전달되면 패턴은 통과된 짝수보다 작은 최대 홀수까지 계속되어야 합니다.

양의 정수가 주어질 경우 1부터 2step을 주어 풀이하였다.

```python
def pattern(i):
    if i <= 0:
        return ''
    else:
        return '\n'.join([f'{i}' * i for i in range(1, i+1, 2)])
```

해당 list가 어떻게 생성되는지는 아래 이미지를 참조.
![image](https://github.com/lala-ogu/lala-ogu.github.io/assets/78904413/153ec160-4e51-44db-8841-62c82c821c8d)

## 숫자가 좋아
> 섞여있는 문자열 속에서 정수만 뽑아내 합을 반환하는 함수 pick_and_sum(words)를 작성하세요.

re 정규표현식을 사용하여 풀이하였다.

```python
import re
def pick_and_sum(str):
    return sum(map(int,re.findall('\d+',str)))
```

findall()은 첫번째 인자에 정규표현식(패턴)과 두번째인자로 문자열을 받는다.
\\d+ 정규표현식은 한 개 이상의 숫자를 나타낸다. 123이라는 문자열이 있다면 1,2,3으로 찾을 수 도있지만,
123으로 찾을수 있게 한다.

혹은 문자 하나하나 비교하여 list로 추가하는 풀이도 있을 수 있다.

```python
# solution 2
def pas(str):
    my_list = []
    count = 0 # bool type으로 두는게 더 좋을것 같지만 우선 정수로
    new_num = ''
    for char in str:
        if 46<ord(char)<58:
            if count == 0:
                new_num += char
                count += 1
            else:
                new_num += char
        elif count != 0:
            my_list.append(int(new_num))
            new_num = ''
            count = 0
    return sum(my_list)
```

## 소대소대

> 단어의 짝수번째 알파벳은 대문자로, 홀수번째 알파벳은 소문자로 바꾼 문자열을 return 하는 함수 up_and_low을 작성하세요.

간단하게 upper()를 사용하여 해결하였다. lower()는 생략했다.

```python
def up_and_low(chars):
    my_list = []
    for i in range(len(chars)):
        if i % 2 == 0:
            my_list.append(chars[i])
        else:
            my_list.append(chars[i].upper())
    
    new_chars = ''.join(my_list)
    return new_chars
```

혹은 map()을 활용할 수도 있는데, map()에 익숙해지는게 좋은 만큼 한번 코드를 바꿔보자.

```python
# solution 2
def ual2(chars):
    def change(tuple):
        # enum은 튜플형태로 인자가 들어오므로 매개변수에서 idx, char로 받아버리면 idx range가 맞지않게된다.
        # 그러므로 함수 안에서 구분해주자
        idx, char = tuple
        return char.upper() if idx % 2 else char.lower()
        # lambda t: t[1].upper() if [0]%2 else t[1].lower()

    return ''.join(map(change,enumerate(chars)))
```

join()은 iterable하다면 모두 처리해준다. 그래서 list로 바꿔주지 않아도 join()이 가능하다.

## 통과한 시험

> 딕셔너리 형태로 언어 및 각 테스트의 결과가 주어지면 테스트 점수가 60 이상인 언어 목록의 결과를 내림차순으로 정렬된 리스트를 반환하는 passpass함수를 작성하세요. (중복되는 점수는 없습니다.)

딕셔너리 컴프리헨션과 sorted 및 람다함수에 대해 알아야 했던 문제였다.
아래의 코드는 딕셔너리의 value를 기준으로 정렬한다.

```python
def passpass(scores):
    # value기준 정렬
    sorted_dict = dict(sorted(scores.items(),key=lambda x: x[1], reverse=True))
    my_list = []
    for subject, score in sorted_dict.items():
        if score >= 60:
            my_list.append(subject)

    return my_list
```
아래의 그림을 참고하여 딕셔너리 정렬에 대해 이해해보자.
![image](https://github.com/lala-ogu/lala-ogu.github.io/assets/78904413/71c9a9b2-8d82-4303-b93f-94bc4734784b)

![image](https://github.com/lala-ogu/lala-ogu.github.io/assets/78904413/676dd750-9990-4292-9551-f4b37f72ad8e)

![image](https://github.com/lala-ogu/lala-ogu.github.io/assets/78904413/c00b9f69-e3b4-462b-9eb3-5e54771d5895)

![image](https://github.com/lala-ogu/lala-ogu.github.io/assets/78904413/514a5983-ceb8-4d03-b03f-76983a50acd4)

람다함수를 풀어쓴 풀이를 봐보자.

```python
# solution 2
def pass2(scores):
    # value정렬의 람다함수를 풀어쓴 버전이다.
    def return_score(x):
        # 딕셔너리를 list로 바꾸면 key,value가 tuple로 들어온다.
        return x[1]

    scores = list(scores.items())
    scores.sort(key=return_score, reverse=True)
    scores = list(filter(lambda elem: elem[1] >= 60, scores))

    answer = [subj for subj, score in scores]
    
    
    return  answer
```

## 삼각수

> 삼각수는 1, 1+2, 1+2+3, 1+2+3+4, ... 의 결과에 해당하는 수를 뜻합니다.
> 따라서, 1, 3, 6, 10, 15, 21, 28, 36, 45, 55, 66, 78, 91, 105, 120,..는 삼각수입니다.
> 양의 정수를 입력받아 삼각수에 해당하는지 확인하는 함수 is_triangular를 작성하세요.

함수 fn의 정의를 하는 수학적 생각이 중요한 문제였다.
```python
def is_triangular(num):
    i = 1
    # fn-1 = fn - n
    # fn = fn-1 + n
    # fn = n+(n-1)+(n-2)+(n-3)+...
    while True:
        num -= i
        if num ==  0:
            return True
        elif num < 0:
            return False
        i += 1
```

간단한 풀이도 있다. range()를 이용하여 1부터 그대로 더해가는 방법(심각한 성능문제 발생)과 공식을 이용하는 방법이있다.

```python
# sol2
def ist2(num):
    i = 1

    # while sum(range(i+1)) < num:
    #     i += 1
    while i*(i+1)//2 < num:
      i += 1

    # return sum(range(i+1)) == num
    return i*(i+1)//2 == num
```

## 나만의 딕셔너리 생성하기

> key의 리스트와 value의 리스트로 딕셔너리를 생성하여 return 하는 함수 create_dict(keys, values)를 작성하세요.
> 만약에 value의 갯수가 key의 갯수보다 부족한 경우, None을 채워 넣어야 합니다. 반대로 key의 갯수가 부족한 경우, 초과하는 value들은 무시해도 됩니다.

value가 더 많은 경우는 슬라이싱을 통해 구현하면 됐지만 key가 더많은 경우가 어려웠는데,
list도 연산이 가능하다는 것을 생각해내야했다.

```python
def create_dict(keys, values):
    if len(keys) == len(values):
        return dict(zip(keys, values))
    elif len(keys) > len(values):
        return dict(zip(keys,values +[None]*(len(keys) - len(values))))
    else:
        return dict(zip(keys,values[:len(keys)]))
```

함수를 사용하지 않는 방법도 있다.

```python
# sol2
def cd2(keys, values):
    answer = {}

    # key는 모두 소비해야하므로 len의 기준을 key로 잡는다.
    for idx in range(len(keys)):
        k = keys[idx]
        if idx < len(values):
            v = values[idx]
            answer[k]= v
        else:
            answer[k]= None
```

## 딕셔너리 뒤집기

> 딕셔너리는 기본적으로 key와 value로 이뤄져있습니다.
> 딕셔너리를 입력받아 value와 key를 뒤집은 결과를 반환하는 함수 dict_invert를 작성하세요.

zip()을 이용하면 어려울게 없는 문제였다.

```python
def dict_invert(original_dict):
    return dict(zip(original_dict.values(), original_dict.keys()))
```

하지만
```python
print(dict_invert({1: True, 2: True, 3: True}))
```
같은 경우 의도한 대로 딕셔너리가 나오지 않게 되서 코드를 수정해야했다.

```python
# sol2
def di(original_dict):
    answer={}

    for k, v in original_dict.items():
        # key 중에 v 가 없다면 [k]로 초기화
        if v not in answer:
            answer[v] =  k
        # 있다면 리스트에 추가
        else:
            answer[v].append(k)

    return answer
```

## 시험 채점 시스템

> 첫 번째 인자는 정답이 들어있는 리스트, 두 번째 인자는 사용자의 답이 들어있는 리스트입니다. 두 리스트는 비어있지 않으며 길이가 같습니다.
> 정답의 경우 +4점, 오답의 경우 -1점, 공백 응답(빈 문자열)의 경우 0점입니다. 만약, 점수가 0보다 작으면 0을 return 합니다.
> 위와 같이 시험 점수를 체크하는 함수 check_score(real_answers, my_answers)을 작성하세요.

인덱스로 비교하면 간단한 문제다.

```python
def check_score(real_answers, my_answers):
    score = 0
    for i in range(len(real_answers)):
        # 정답일 경우
        if real_answers[i] == my_answers[i]:
            score += 4
        # 오답
        elif real_answers[i] != my_answers[i] and my_answers[i] != '':
            score -= 1

    if score < 0:
        score = 0
        
    return score
```








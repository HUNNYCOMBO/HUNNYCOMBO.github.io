---
title: '코딩테스트 기초문제 풀이 모음(python)'
excerpt: 'lv0 문제들을 풀이'
tags: [코테,]
---

## 문제 1

> 입력된 모든 (숫자 \* 번째)의 합계를 반환하는 함수를 작성하세요. 함수에 전달된 인자가 없으면 0을 반환합니다.

enumerate를 활용하여 index와 정수를 뽑아내면 간단하게 해결할 수 있다.

```
def add(*numbers):
    # enumurate를 활용하여 풀이
    return sum((i+1)*num for i,num in enumerate(numbers))
```

## 문제 2

> 같은 숫자가 한개 있거나 두개가 들어있는 리스트가 주어집니다. 이러한 리스트에서 숫자가 한개만 있는 요소들의 합을 구하는 함수를 작성하세요.

중복관련 문제는 이제 익숙하게 풀 수 있는듯.

```
def repeats(numbers):
    return sum([num for num in numbers if numbers.count(num) == 1])
```

## 문제 3

> 과수원에 농부 한명이 썩은 과일이 몇개 들어있는 과일 봉지를 가지고 있습니다. (이 과일 봉지는리스트를 의미합니다.)  
> 썩은 과일 조각들을 모두 신선한 것으로 교체하는 함수를 작성하세요. (rotten과일을 신선한 과일로 바꿔야 합니다.)
> 
> > 예를 들어,  
> > \['apple', 'rottenBanana', 'apple'\] 이라는 리스트가 주어진 경우, 대체된 리스트는 \['apple', 'banana', 'apple'\] 이어야 합니다.

문자열 안에 해당 문자열이 있는지를 체크하면 되는 간단한 문제다.

```
def remove_rotten(fruits):
    my_list = []
    check_word = 'rotten'
    if len(fruits) == 0:
        return my_list

    for i,fruit in enumerate(fruits):
        if fruits[i] in check_word:
            my_list.append(fruits[i].lower())
        else:
            my_list.append(fruits[i].replace(check_word,'').lower())

    return my_list

print(remove_rotten(['apple', 'rottenBanana', 'apple'] ))
```

## 문제 4

> 마을의 신호등을 제어하는 함수를 작성하려고 합니다. 녹색 -> 노란색 -> 빨간색 -> 녹색으로 변환하는 함수가 필요합니다.  
> 현재의 불빛 상태를 나타내는 인자하고 함수를 실행 시켰을 때 변경 되어야 하는 빛의 색을 나타내는 함수를 작성하세요.

이전에 비슷한 문제로 하루동안 고민한 적이 있어서 간단하게 푼 문제.  
3의 나머지는 0,1,2만 나오고 7의 나머지는 0~6까지만 나올 수 있다는 것을 생각해보자.  
그럼 간단하게 풀린다.

```
def update_light(color):
    light = ['green', 'yellow', 'red']

    # index와 나머지 연산자를 활용
    return light[int(light.index(color)+1) % 3]
```

## 문제 5

> Arara는 셈을 한쌍으로 하는 아마존에 살고 있는 부족입니다. 이들이 행하는 셈의 방식은 다음과 같습니다.

> > 예를 들어, 1에서 8까지는 셈을 한다면,  
> > 1 = anane  
> > 2 = adak  
> > 3 = adak anane  
> > 4 = adak adak  
> > 5 = adak adak anane  
> > 6 = adak adak adak  
> > 7 = adak adak adak anane  
> > 8 = adak adak adak adak  
> > 주어진 숫자 인자를 통해 다음과 같은 함수를 작성하세요.

몫 연산자를 이용하여 풀이하면 간단하게 해결된다.  
짝수일 경우 2로 나눈 몫만큼 출력하면 되고,  
홀수일 경우 2로 나눈 목의 +1 만큼 출력하면 된다.

```
 def count_arara(num):
    # 2진법과 같다고 생각하면 된다.
    one = 'anane'
    two = 'adak'
    my_list = []

    if num % 2 == 1:
        for _ in range(num//2):
            my_list.append(two)
            if _ == (num//2)-1:
                my_list.append(one)
        # return 한 줄로 줄여보기
        return ' '.join(my_list)
    else:
        return ' '.join([two for _ in range(num//2)])
```

## 문제 6

> 제 친구 Rora는 그녀가 하고있는 밴드의 이름을 바꾸고 싶어합니다.  
> 그녀는 "The" + a 대문자 명사 형태의 밴드 이름을 원합니다. 예를 들어, "dolphin" -> "The Dolphin"와 같습니다.  
> 혹은 앞뒤가 같은 단어인 명사를 반복하여 결합하여 첫번째 문자를 대문자로 시작하는 밴드 이름을 만들고 싶어합니다. (이때는 앞쪽에 'The'가 없음) 예를 들어, "alaska" -> "Alaskaalaska"과 같습니다.  
> 명사를 문자열로 하는 함수를 작성하고 선호하는 밴드 이름을 문자열로 표시하세요.

슬라이싱을 활용하는 문제.

```
def band_name_generator(word):
    if word[0] == word[-1]:
        return word.capitalize()+word
    else:
        return 'The ' + word.capitalize()

 print(band_name_generator('dolphinyap'))
```

## 문제 7 - 메소드 없는 세상

> 우리는 문자열을 만들어 나갈 때, .join(iterable) 함수를 사용합니다.  
> .join(iterable)이 생각나지 않을 때를 위해 함수를 직접 만들어보면서 감사함을 느껴봅시다.  
> 함수 my\_join(target, word)를 작성하여 문자열을 반환하세요.  
> target은 바꿀 대상(iterable)이며, word는 합쳐지는 단어입니다.

맨 마지막에만 word를 적용하지 않게 반복문을 작성했다. 다른 풀이가 있을것 같지만 우선 이게 최선.

```
def my_join(target, word):
    new_word = ''
    for i in range(len(target)):
        new_word += target[i]
        if i != (len(target))-1:
            new_word += word

    return new_word

print(my_join('배고파', '.'))
print(my_join(['1', '2', '3'], ''))
```

## 문제 8 - 숨바꼭질

> 숫자가 주어지면, 사용되지 않은 숫자를 프린트하는 함수를 작성하세요.

중복을 제거(set)하고 차집합을 활용하였다.

```
def unused_digits(*numbers):
    my_list=['0','1','2','3','4','5','6','7','8','9']
    my_set = set()
    for num in numbers:
        for i in str(num):
            my_set.add(i)

    return ''.join(sorted(list((set(my_list)-my_set))))

print(unused_digits(12, 34, 56, 78))
print(unused_digits(2015, 8, 26))
```

## 문제 9 - 짝홀짝홀

> n개의 양의 정수 리스트가 주어지면, 홀수와 짝수를 분리하고 각각의 조건에 맞게 홀수와 짝수를 정렬하는 함수를 작성하세요.
> 
> > 조건  
> > 짝수와 홀수가 번갈아 가면서 나오게 됩니다.  
> > 짝수가 먼저 시작됩니다.  
> > 짝수는 오름차순으로 홀수는 내림차순으로 되어야합니다.

pop()을 활용해야하는 좀 어려웠던 문제. chat gpt의 도움을 받아서 pop()의 존재를 생각해냈다.  
while문에서 list의 길이가 0이되면 False를 return하는 것을 활용하여 or를 사용한 것도 생각치못했다.

```
def even_and_odd(numbers):
    even_nums = sorted([num for num in numbers if num % 2 == 0])
    odd_nums = sorted([num for num in numbers if num % 2 != 0], reverse=True)

    result = []
    while even_nums or odd_nums:
        if even_nums:
            result.append(even_nums.pop(0))
        if odd_nums:
            result.append(odd_nums.pop(0))

    return result

print(even_and_odd([7, 3, 14, 17]))
print(even_and_odd([1, 3, 5, 7, 9, 11]))
print(even_and_odd([1, 2, 2, 4, 4, 6, 6, 2004, 9, 11]))
```

## 문제 10 - 문자열 계산하기

> 아래와 같이 문자열이 주어졌을 때, 바보같은 사용자를 위해 계산을 해주려고 합니다.  
> 이 계산기는 더하기와 빼기밖에 못합니다.  
> 함수 calc(equation)을 작성하세요.

처음에는 정규표현식을 이용하여 추출하려고 했다.  
하지만 첫 숫자가 -12나 123같이 부등호가 있는 경우와 없는 경우 모두 충족하는 정규표현식이 없었다.  
(있을수 도 있지만 내 머리로는 한계)

사실, eval()을 사용하면 너무 단순한 문제다.  
하지만 eval()은 보안이슈가 있어서 권장되지 않는 메소드이다.

그렇다면 아예 반복문으로 구현할 수는 없는 걸까? 반나절을 생각하다 chat gpt의 도움을 받았다.  
파이썬 튜터를 통해 list가 어떻게 쌓이는지 꼭 확인하면서 코드를 확인해보자.

[##_Image|kage@cGOlMg/btsgne9VeuQ/90DFG1vvQ5VTZDgsqssTn0/img.png|CDM|1.3|{"originWidth":586,"originHeight":238,"style":"alignCenter","caption":"파이썬 튜터로 돌려서 확인한 일부분"}_##]

```
import re

def calc(code):
    # seperators = re.findall('[+-]\d+',code)

    # return sum(map(int,seperators))
    # return eval(code)
    # eval()은 되도록 사용하지 않는것이 권장된다.

    # chat gpt의 도움을 받은 코드
    # 덧셈과 뺄셈 기호로 식을 분리합니다.
    terms = []
    term = ''
    for char in code:
        if char in ['+', '-']:
            # 연산자를 기준으로 append 한다
            terms.append(term)
            # 연산자를 저장해둔다
            term = char
        else:
            # 연산자와 함께 숫자가 쌓인다
            term += char
    # 마지막 반복을 위한 append
    terms.append(term)

    # 시작이 +,- 기호로 시작하는 경우 빈문자열이 첫번째 요소에 있기 때문에 빈 문자열을 필터로 제거
    return sum(map(int,filter(None,terms)))

print(calc('123+2-124'))
print(calc('-12+12-7979+9191'))
print(calc('+1-1+1-1+1-1+1-1+1-1+1-1+1-1+1-1+1-1+1-1+1-1+1-1+1-1+1-1+1-1+1-1'))
```

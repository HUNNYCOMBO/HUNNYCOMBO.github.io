---
title: '파이썬 기초 코딩테스트'
excerpt: '기초적인 코딩테스트를 풀어봅니다.'
tags: [test]
---

## 1. 갯수 구하기

> 주어진 리스트는 학생 이름으로 구성되어 있다. 학생들의 수를 출력하시오. (중복제거)


```python
students = ['김철수', '이영희', '조민지', '조민지', '이영희', '김철수']

# solution 1 set 사용
count = 0
new = set(students)

print(len(new))

# solution 2 다른 list 사용
uniq_names = []

for student in students:
    if student not in uniq_names:
        uniq_names.append(student)

print(len(uniq_names))

# solution 3 dict 사용

uniq_names = {}

for student in students:
    uniq_names[student] = 0

print(len(uniq_names))
```

## 2. 최다 득표수 구하기

> 주어진 리스트는 반장 선거 투표 결과이다. 최다 득표자의 득표수를 구하시오.

```python
students = ['이영희', '김철수', '이영희', '조민지', '김철수', '조민지', '이영희', '이영희']

# 아래에 코드를 작성하시오.

new = set(students)
max = 0

for i in new:
    if max < students.count(i):
        max = students.count(i)

print(max)
# solution 2    dict 사용

votes = {}
max = 0
for student in students:
    if student not in votes:
        votes[student] = 1
    else:
        votes[student] += 1

    if votes[student] > max:
        max = votes[student]
print(max)

# solution 3    zip 사용

default = [0 for _ in range(len(students))]
votes = dict(zip(students,default))
max = 0

for student in students:
    if student in votes:
        votes[student] += 1

    if votes[student] > max:
        max = votes[student]

print(max)
```

> dict의 zip함수는 인자로 순환가능한 객체를 넣어줘야 한다.

## 3. 최솟값 구하기

> 주어진 리스트의 요소 중에서 최솟값을 구하시오.

```python
numbers = [7, 10, 22, 4, 3, 17]
first = numbers[0]

# 아래에 코드를 작성하시오.

for num in numbers:
    if num < first:
        first = num

print(first)
```

## 4. 5의 개수 구하기

> 주어진 리스트의 요소 중에서 5의 개수를 출력하시오.

```python
numbers = [7, 17, 10, 5, 4, 3, 17, 5, 2, 5]

# 아래에 코드를 작성하시오.
print(numbers.count(5))

# solution 2
count = 0
for num in numbers:
    if num == 5:
        count += 1

print(count)
```

## 5. 최댓값과 등장 횟수 구하기

> 최댓값과 등장 횟수 구하기

```python
numbers = [7, 10, 22, 7, 22, 22]

# 아래에 코드를 작성하시오.

first = numbers[0]

for num in numbers:
    if num > first:
        first = num

print(first, numbers.count(first))

# solution 2    dict로 접근

my_dict = dict(zip(numbers,list(0 for _ in range(len(numbers)))))
max = numbers[0]

for num in numbers:
    if num > max:
        max = num

for num in numbers:
    if num in my_dict:
        my_dict[num] += 1

print(max, my_dict[max])

# solution 3

max_num = numbers[0]
count = 0

for num in numbers:
    if num > max_num:
        max_num = num
        count = 1
    elif num == max_num:
        count += 1

print(max_num, count)
```

## 6. a 빼기

> 입력으로 word가 주어질 떄, 해당 단어에서 'a'를 모두 제거한 결과를 출력하시오.

```python
word = input()

# 아래에 코드를 작성하시오.
for char in word:
    if char == 'a':
        word = word.replace('a','')

print(word)

# solution 2

new_string = ''

for char in word:
    if char != 'a':
        new_string += char

print(word)

# solution 3
for char in word:
    continue

print(word, end='')
```

## 7. 단어 뒤집기

> 입력으로 word가 주어질 때, 해당 언어를 역순으로 뒤집은 결과를 출력하시오.

```python
word = input()
# 아래에 코드를 작성하시오.

for i in range(len(word)-1,-1,-1):
    print(word[i],end='')

# solution 2
print(word[::-1])

# solution 3

revers = ''

for i in range(len(word)-1,-1,-1):
    revers += word[i]

print(revers)
```

## 8. 모음 제거하기

> 주어진 문장의 모음을 제거하여 새로운 문장을 출력하시오.

```python
my_str = 'Life is too short, you need python'

# 아래에 코드를 작성하세요.
my_list = ['a','e','i','o','u']

for char in my_str:
    if char in my_list:
        my_str = my_str.replace(char,'')

print(my_str.strip())
```

## 9. 과일개수 골라내기

> 내 장바구니에 과일이 몇 개인지, 과일이 아닌 것은 몇개인지 출력하시오.

```python
basket_items = {'apples': 4, 'oranges': 19, 'kites': 3, 'sandwiches': 8}
fruits = ['apples', 'oranges', 'pears', 'peaches', 'grapes', 'bananas']

basket_items['apples']
# 아래에 코드를 작성하세요.
f_count = 0
n_count = 0
keys = list(basket_items.keys())

for item in basket_items:
    if item in fruits:
        f_count += basket_items[item]
    else:
        n_count += basket_items[item]

print(f'과일은 {f_count}개이고, {n_count}개는 과일이 아닙니다.')
```

## 10. 영어 이름 출력하기

> 영어 이름의 가운데 이름을 대문자로 축약해서 나타내는 코드를 작성하시오.

```python
name = 'Alice Betty Catherine Davis'


# 아래에 코드를 작성하세요.

# list로 반환
names = name.split()
# 중간 이름 추출
# m_name = names[1:-1]

for i in range(1,len(names)-1):
    b_word = names[i][0].upper()
    b_word += '.'
    names[i] = b_word

print(' '.join(names))
```

## 11. 구구단

> 2단부터 9단까지 반복문을 사용하여 구구단을 출력하시오.

```python
for dan in range(2,10):
    print(f'-------{dan} 단-------')
    for coe in range(1,10):
        print(f'{dan} X {coe} = {dan*coe}')
```

## 12. 개인정보보호

> 사용자의 핸드폰번호를 입력 받고, 개인정보 보호를 위하여 뒷자리 4자리를 제외하고는 마스킹 처리하세요.

```python
phone = input()
n_phone = '****'

if phone == '':
    print('핸드폰번호를 입력하세요.')
else:
    n_phone += phone[7:]

print(n_phone)
```

## 13. 정중앙

> 사용자가 입력한 문자열 중 가운데 글자를 출력하세요. 단, 문자열이 짝수라면 가운데 두글자를 출력하세요.

```python
string = input('문자열 입력:')

# 짝수일 경우
if len(string) % 2 == 0:
    print(string[int(len(string)/2)],string[int((len(string)/2)+1)])
else:
    print(string[int((len(string)/2)+1)])
```

## 14. 소수찾기

> 조건, 반복문을 이용하여 리스트의 요소들이 소수인지 아닌지 판단하는 코드를 작성하시오.

```python
numbers = [3, 26, 39, 51, 53, 57, 79, 85]

# 아래에 코드를 작성하세요.

# 소수란 1과 자기 자신만으로 나누어지는 수

for num in numbers:
    # 소수는 자기값에 절반으로 나누어서 그 수로 판별하여도 된다.
    count = 0
    
    # 유일한 예외인 1,2의 경우
    # range(2,1)및 range(2,2)라는 빈 시퀀스가 생성되기 때문에, 무조건 count가 0이게 된다.
    for sep in range(2,int((num/2)+1)):
        if num % sep == 0:
            print(f'{num}은 소수가 아닙니다. {sep}는 {num}의 인수입니다.')
            count += 1
            break
        
    if count == 0:
        print(f'{num}은 소수입니다.')
```

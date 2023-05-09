---
title: 'NLTK'
excerpt: '교육용 자연어 처리 및 문서 분석용 파이썬 패키지 NLTK에 대해 알아보기'
tags: [NLTK]
---

```python
import nltk
nltk.download("book", quiet=True)
from nltk.book import *
```

## 1. 말뭉치

말뭉치란 자연어 분석 작업을 위해 만든 샘플 문서의 집합입니다.
NLTK패키지의 corpus 서브패키지에서 말뭉치를 제공합니다.
nltk.download 명령어로 다운로드 합니다.

```python
nltk.corpus.gutenberg.fileids() # 말뭉치 목록

carroll_raw = nltk.corpus.gutenberg.raw('carroll-alice.txt')
print(carroll_raw)  # 캐롤로우 출력
```

## 2. 토큰 생성

토큰이란 자연어 문서를 분석하기 위해 긴 문자열을 분석하여 작은 단위로 나눈 것입니다.
토큰 생성 : 문자열을 토큰으로 나누는 작업

```python
from nltk.tokenize import sent_tokenize
print(sent_tokenize(carroll_raw[:1000])[0]) # 천번째 글자 중에서 첫번째 문장

from nltk.tokenize import word_tokenize
print(word_tokenize(carroll_raw[:100])) # 100개의 단어

from nltk.tokenize import RegexpTokenizer
retoken = RegexpTokenizer('[\w]+')  # 정규표현식으로 영어와 숫자만 가져오기
retoken.tokenize(carroll_raw[:100])
```

## 3. 형태소분석
형태소란 언어학에서 일정한 의미가 있는 가장 작은 말의 단위입니다.
형태소 분석이란 단얼부터 어근,접두사,점미사,품사 등 다양한 언어적 속성을 파악하고 형태소를 찾아내는 작업입니다.

- 어간추출 : 변화된 단어의 접미사나 어미를 제거하여 형태소의 기본형을 찾는 방법

```python
from nltk.stem import PorterStemmer,LancasterStemmer

stl = PorterStemmer()
stl2 = LancasterStemmer()

words = ['working', 'works','worded']

for temp in words :
  print(stl.stem(temp))
  
for temp in words :
  print(stl2.stem(temp))
```

- 원형복원 : 같은 의미를 가지는 여러 단어를 사전형으로 통합하는 작업
- 
```pyton
from nltk.stem import WordNetLemmatizer

lm = WordNetLemmatizer()

for temp in words:
  print(lm.lemmatize(temp,pos='v'))
```

## 4. 품사

품사(POS,part-of-speech)는 낱말의 문법적인 기능이나 형태, 뜻에 따라 구분한 것입니다.
품사의 구분은 언어,학자마다 다릅니다.
NLTK에서는 펜 트리뱅크 테그세트를 사용합니다.

- NNP: 단수 고유명사
- VB: 동사
- VBP: 동사 현재형
- TO: to전치사
- NN:명사
- DT: 관형사

```python
from nltk.tag import pos_tag

sents = 'What trial is it?'
tagged_list = pos_tag(word_tokenize(sents))
print(tagged_list)
```

## 5. Text클래스

문서 분석에 유용한 여러가지 메서드 제공

```python
from nltk import Text

text = Text(retoken.tokenize(carroll_raw))
text.plot(20) # 가장 많이 사용되는 단어를 그래프로 표현
```

```python
Fd = text.vocab()
from nltk import FreqDist
stopwords = ['Mr.',"Mrs.","Miss","Dear"]
carroll_tokens = pos_tag(retoken.tokenize(carroll_raw))
name_list = [t[0] for t in carroll_tokens if t[1] =='NNP' and t[0] not in stopwords]
# 특정 형태소(NNP,고유명사)를 추출
print(name_list)

fd_name = FreqDist(name_list)
fd_name.N() # 빈도수 확인
fd_name.freq('Alice') # 해당 단어가 나올 확률

```


---
title: 'Pandas'
excerpt: '파이썬의 데이터분석 라이브러리 pandas에 대해 알아보기'
tags: [pandas]
---

## 1. Pandas란?

데이터 분석에 관련된 기능을 제공하는 파이썬 라이브러리입니다.
**큰 데이터**를 indexing, slicing, sorting등 빠르게 처리합니다.
외부 데이터 csv, txt, excel등의 데이터도 처리 할 수 있습니다.
pip install pandas를 이용해 설치할 수 있습니다.

colab에서는 import하여 사용합니다.

> series: pandas를 구성하는 1차원 자료형입니다. 시퀀스와 numpy배열 모두 사용 가능합니다.

```python
# pandas

import pandas as pd
import numpy as np

data = pd.Series([1,2,3,4])
data1 = pd.Series(np.array([1,2,3,4]))
data
```

![image](https://user-images.githubusercontent.com/78904413/235352486-f47caed6-7fa0-487e-a53a-da46bc0da6b5.png)

## 2. Series

시리즈는 1차원 배열이지만 1열을 index로 2열이 values로 구분지어져 있습니다.

![image](https://user-images.githubusercontent.com/78904413/235352923-2e1af268-2390-4a28-892c-f6559dca785f.png)

- 연산 가능(인덱스가 같은 것끼리 연산)
- mean: 평균
- fillna(n): NaN(결측데이터)를 n값으로 처리(결측 데이터. null과 다르게 정의되지 않은 값으로 하나의 값으로 인식 됌)
- std: 표준편차
- describe: 통계정보

## 3. DataFrame

시리즈는 1차원 자료형이었다면, DataFrame은 2차원 데이터 자료형입니다.
Series자료형을 테이블 형태로 표현합니다. Series데이터가 뭉쳐있다고 볼 수 있습니다.
pandas 모듈에서 Sereis와 DataFrame을 사용하는
from pandas importSeries, DataFrame 구문을 자주 사용합니다.

DataFrame은 List, Dict를 활용하여 생성할 수도 있고 index(행)와 column(열)명을 설정해 줄 수 있습니다.
Dict로 생성하면 key값이 colum명이 됩니다.

![image](https://user-images.githubusercontent.com/78904413/235354950-5a1d5bc6-f6f2-49d6-aecb-52e7b7f9530d.png)

```python
from pandas import Series, DataFrame

# data = DataFrame([[1,2],[3,4],[5,6]])
data = DataFrame.from_dict({'서울':[1,2,3],'부산':[4,5,6]})
# # data = DataFrame([[1,2],[3,4],[5,6]],columns=['서울','부산'], index=[1,2,3])
data
```

### 3.1. 특정한 컬럼 가져오기

특정한 컬럼명의 데이터들을 가져와야하는 경우가 많습니다.
변수명.컬럼명으로 데이터를 조회할 수 있습니다. data.List컬럼명으로 여러개의 컬럼 데이터를 조회할 수 있습니다.
변수명.index 혹은 변수명.columns를 이용하여 인덱스명과 컬럼명을 변경할 수도 있습니다.

```python
data = DataFrame.from_dict({'서울':[1,2,3],'부산':[4,5,6]})

data[['서울','부산']]
data.서울 # 컬럼명을 변수처럼 사용
```

### 3.2. index로 가져오기
- 변수명.loc\[인덱스이름\] : 데이터 조회
- 변수명.iloc\[인덱스번호\]
- 변수명.iloc\[시작:끝\] : 인덱스 슬라이싱

![image](https://user-images.githubusercontent.com/78904413/235355698-3664cdb1-835e-41e8-9908-91e3d40ab97c.png)

인덱스와 컬럼을 동시에 사용하여 혹은 조건을 주어 데이터를 가져오는 것도 가능합니다.

```python
data.iloc[0:2,1]  # 0~2 인덱스의 1컬럼 데이터
data.loc[1,'서울']  
data[data['서울']>1]  # 조건. 전체데이터에서 서울시의 데이터 값이 1보다 큰 행을 모두 가져오기
```

## 4. DataFrame 합치기

흩어져있는 컬럼들을 모아서 합쳐야 할 경우가 많습니다.
이럴때는 merge(left,right,how,on)을 사용합니다.

- left: 합칠 왼쪽 DataFrame
- right: 합칠 오른쪽 DataFrame
- how: 합치는 방법
- on: 두 데이터를 합칠 기준 컬럼(how에서 inner, left, right일 시)

how 옵션
- Inner: left,right에서 둘다 존재하는 컬럼 데이터만 합침
- left: left데이터 프레임 기준으로 합침
- right: right데이터 프레임 기준으로 합침
- outher: left,right의 **모든** 데이터 합침(빈 데이터는 NaN)

![image](https://user-images.githubusercontent.com/78904413/235356297-6c0441a4-1e15-466e-ae07-3727c10b6c81.png)
![image](https://user-images.githubusercontent.com/78904413/235356504-31e037ee-5974-40d8-95f2-3c008911da99.png)

인덱스를 기준으로 merge도 가능합니다.

![image](https://user-images.githubusercontent.com/78904413/235356550-7b88c933-dc90-4570-9a29-7ae0e052d362.png)

> DataFrame끼리의 단순한 연산도 가능합니다.

## 5. DataFrame 파일처리

데이터 프레임을 scv, 엑셀, json, txt 등 파일로 처리합니다. 특히 csv를 자주 사용합니다.
> csv 파일 : 특정 구분자로 나누어진 파일

### 5.1. csv 불러오기
pd.read_csv(FilePath, sep, header, names, index_col, skiprows, nrows, encoding)

- FilePath: 파일경로
- sep: 구분자
- header: 컬럼명(없을경우 none)
- names: header가 없을시 컬럼명 입력 가능
- skiporws: 파일에서 행을 건너뛰고 불러옴
- index_col: 컬럼을 index로 사용
- nrows: 입력한 개수만큼의 데이터만 읽음
- encoding: 인코딩 타입 입력. **한글일 경우 'CP949'**

### 5.2. 명령어
- del 명령어: 파일을 불러왔을 때 필요없는 컬럼이 있다면 del data\[컬럼명\]으로 해당 컬럼을 지울 수 있음
- head(n): n개의 인덱스만 불러오는 함수
- describe(): 통계요약 함수
- sum(): 합계
- mean(): 평균
- std(): 표준편차
- var(): 분산
- count(): 개수
- corr(): 상관계수
- min()
- max()
- info(): 데이터타입 확인
- to_csv(): 해당 이름으로 csv파일로 저장
- sort_values(): 정렬
  - ascending: true: 오름차순, false: 내림차순
  - inplace: true면 정렬한 값을 DataFrame에 바로 반영
  - by: 정렬할 기준 변수
  - axis: 0이면 행정렬 1이면 열정렬
- sort_index(): index명 기준으로 정렬

![image](https://user-images.githubusercontent.com/78904413/235357097-4613d1cc-a14a-485f-99a9-2c8ba7aa3647.png)
![image](https://user-images.githubusercontent.com/78904413/235357397-69703781-4515-4137-af5b-d5b57bd2cf31.png)




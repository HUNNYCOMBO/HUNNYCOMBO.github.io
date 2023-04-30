---
title: 'Numpy'
excerpt: '파이썬의 강력한 행렬연산 외부 라이브러리 numpy에 대해 기초적으로 알아보기'
tags: [numpy]
---

## 1. Numpy란?

파이썬 외부 라이브러리로 행렬 연산에 다양한 기능을 제공하는 라이브러리입니다.
내부가 C언어로 작성되어 있어서 선형대수학 연산속도가 매우 빠릅니다.
복잡한 행렬계산, 선형대수, 통계등의 기능을 제공합니다.
pip install numpy 명령어로 설치합니다.

```python
# numpy의 사용
import numpy as np  # as는 DB의 as와 같습니다. 긴 이름대신 지정한 이름으로 사용하게 합니다.

np.__version__ # numpy버전
```

## 2. Numpy 배열

numpy는 행렬을 배열(ndarray)로 두고 연산합니다.
List와 유사하지만 list는 고성능 수치계산이 어려워서 numpy배열로 수치계산을 수행합니다.
numpy배열은 list와 달리 **같은 데이터 타입**만 담을 수 있습니다.
numpy배열은 다차원 배열도 지원합니다.

> 다차원 배열은 행렬 연산을 하기위한 필수조건

```python
data = np.array([1,2,3])
data1 = np.array([[1,2,3],[4,5,6]])

type(data)  # numpy.ndarray
type(data1) # numpy.ndarray

data.ndim # 몇차원 배열인지 반환하는 함수
data1.ndim # 2
```


## 3. Numpy 명령어

- shape: 크기확인(n행m열)
- dtype(매개변수): data의 타입을 지정
- dtype: 타입확인
- size: 총 데이터의 수

![image](https://user-images.githubusercontent.com/78904413/235350859-6ae7584a-c0f5-43b3-9548-af7f2646ab1c.png)



- T: 행과 열의 교환(transpose)
- linspace(start, end count): start에서 end까지를 count로 나눈 배열을 만듭니다. range함수와 비슷
- arange(start, end step): range함수와 비슷
- eye(3): 대각선으로 1이 n개 채워진 행렬

![image](https://user-images.githubusercontent.com/78904413/235351440-ab5eb80c-4158-4095-a37e-e741bbbfb774.png)

- zeros: 0으로 채워진 행렬
- ones: 1로 채워진 행렬
- full: 지정값으로 채워진 행렬
- random.radn(): 정규분포범위의 난수 생성

![image](https://user-images.githubusercontent.com/78904413/235351666-bb747aa5-0ee4-4d59-99cf-c4673a538df0.png)

> randn와 rand는 모두 난수를 생성하는 함수입니다. 그러나 rand는 0부터 1사이에서 균일한 확률 분포로 실수 난수를 생성하고, 
> randn은 기댓값이 0이고 표준편차가 1인 가우시안 표준 정규 분포를 따르는 난수를 생성합니다.

- reshape: 행렬의 형태 변경
- +, -, *, / 연산 가능

![image](https://user-images.githubusercontent.com/78904413/235351897-9ea75c91-ffd8-414b-818b-dd3a0c1712c1.png)

### 3.1. Numpy 통계

(전체, 행(axis=0), 열(axis=1)가 가능)

- sum: 전체합계, 행합계(axis=0), 열합계(axis=1)가 가능
- mean: 평균
- max: 최대값
- min: 최소값
- var: 분산(데이터가 평균으로부터 얼마나 떨어져있는 지표)

![image](https://user-images.githubusercontent.com/78904413/235352153-01ae665e-312c-4f56-a094-ff8d224bda30.png)


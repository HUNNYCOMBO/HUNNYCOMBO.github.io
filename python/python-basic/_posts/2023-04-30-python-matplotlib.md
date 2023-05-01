---
title: '시각화'
excerpt: '데이터 프레임을 시각화하는 패키지에 대해 알아보기'
tags: ['matplotlib', '시각화', 'seaborn']
---

## 1. Matplotlib

시각화는 누구나 쉽게많은 데이터의 양을 한 눈에 알아볼 수 있도록 돕습니다.
Matplotlib는 데이터프레임을 chart나 plot으로 시각화하는 패키지 라이브러리 입니다.
import matplotlib 로 사용합니다.
한글을 지원하지 않기 때문에 따로 설치해야합니다.

```python
# 시각화
# colab에서 한글 설치

!sudo apt-get install -y fonts-nanum
!sudo fc-cache - fv
!rm ~/.cache/matplotlib -rf
# 이후 재가동

# 폰트설정
import matplotlib.pyplot as plt
plt.rc('font', family='NanumBarunGothic')

plt.title('선그래프')
plt.plot([1,2,3,4,5],[4,9,4,2,10])
plt.show()
```
![image](https://user-images.githubusercontent.com/78904413/235358490-2d09ae36-8cf2-4348-93f2-37930b624ccf.png)

이때 그래프에서 축을 tic이라고 합니다.
x틱과 y틱의 이름을 설정합니다.
```python
plt.xlabel('일')
plt.ylabel('명')
```

## 2. Style

그래프의 스타일을 지정해 줄 수 있습니다.

![image](https://user-images.githubusercontent.com/78904413/235358582-abd8d32a-fb42-43bd-a83b-5b9dfc99b5cd.png)
![image](https://user-images.githubusercontent.com/78904413/235358884-2287937d-53fd-4274-85e4-d15b09f2e917.png)


xtics(원본List, 바꿀List)와 ytics로 틱들의 이름을 바꿀수 도 있습니다.

## 3. Figure

figure란 그래프가 그러지는 영역(canvas)입니다.
figure(fizgsize=(가로사이즈,세로사이즈))로 캔버스의 크기를 설정할 수 있습니다.
subplot(행,열,순서)로 캔버스를 쪼개 여러개의 그래프를 나타낼 수 있습니다.

```python
plt.figure(figsize=(6,4))
plt.subplot(2,1,1) # 캔버스를 나누는 함수
plt.plot([2,7,3,1], c='r')
plt.subplot(2,1,2)  # 2번째 캔버스
plt.plot([1,3,5,7], c='g')
plt.show()
```

![image](https://user-images.githubusercontent.com/78904413/235452294-d3037c0e-e2ef-4364-820f-02525cbf5081.png)

## 4. bar

bar차트는 막대형 그래프로 굉장히 직관적이어서 자주 사용됩니다.
기본적으로 세로막대가 나오지만 가로형으로 나타낼 수 도 있습니다.

```python
plt.title('매장별 매출데이터')
plt.bar([0,1,2],[100,50,200])
plt.xticks([0,1,2],['강남구','관악구','영등포구'])
plt.xlabel('지역명')
plt.ylabel('매장별')
plt.show()
```

![image](https://user-images.githubusercontent.com/78904413/235453374-affe8286-f223-4955-b6f0-6792a7470289.png)


```python
plt.title('매장별 매출데이터')
city = ['서울','부산','충북','광주']
y_pos = [0,1,2,3]
data = [100,80,40,30]
plt.barh(y_pos,data,alpha=0.5)
plt.yticks(y_pos,city)
plt.show()
```

![image](https://user-images.githubusercontent.com/78904413/235453392-eecdd2a6-6edb-4ac4-ae06-9bafb3ef7f09.png)

## 5. 다양한 그래프

- stem : 막대 넓이가 없는 차트
- hist : 히스토그램. 데이터분포가 어떻게 되는지 확인

```python
import matplotlib
matplotlib.rcParams['axes.unicode_minus'] = False  # 음수를 사용하기 위한 설정

plt.title('stemp plot')
plt.stem([0,1,2,3,4],[10,-5,2,9,-7],'-o') # -0는 표시자
plt.show()
```

![image](https://user-images.githubusercontent.com/78904413/235454002-83dc2d0f-18ee-44a9-a612-c7efb1c53d8c.png)


```python
import numpy as np
x = np.random.randn(100)
plt.title('histogram')
plt.hist(x,bins=10)  # bins = 집계구간
plt.show()
```

> 집계구간이란 통계학에서 사용되는 용어로, 데이터를 수집하고 분석할 때 일정한 기간 또는 구간을 나누어 그 안에서 데이터를 집계하는 것을 말합니다1. 집계구간은 데이터의 특성에 따라 다르게 설정될 수 있습니다. 예를 들어, 일주일 동안의 매출을 집계할 때는 1주일을 집계구간으로 설정할 수 있습니다1.

![image](https://user-images.githubusercontent.com/78904413/235454219-427b6c3e-1174-4409-8f6c-4911772b8b2f.png)

- 파이차트 : autopct(퍼센티지 자동계산), shadow(그림자)
- scatter : 두 데이터간의 상관관계 확인

```python
labels = ['서울','부산','광주','인천']
size = [10,50,30,80]
colors = ['y','c','b','r']
explode = (0,0.2,0,0) # 해당 데이터를 0.2만큼 떨어트린다는 의미
plt.pie(size, explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=45) # autopct는 소수점 첫쨰자리까지 나타낸다는 의미
plt.show()
```

![image](https://user-images.githubusercontent.com/78904413/235454805-cec7e61d-9e3d-4411-8aef-eef0d765101d.png)

```python
np.random.seed(0)
x = np.random.randint(0,50,100)
y = np.random.randint(0,50,100)
plt.scatter(x,y)
plt.show()
```
![image](https://user-images.githubusercontent.com/78904413/235454975-5411ca38-b64c-4168-8aa9-75abb69f64c5.png)


## 6. Seaborn 라이브러리

seaborn이란 Matplotlib를 기반으로 다양한 테마와 통계용 차트 등의 기능을 추가한 시각화 패키지입니다.
iris, titani, tips, filights 데이터를 기본으로 제공합니다.

- rugplot : 데이터 위치를 x축에 표현

```python
import seaborn as sns

iris = sns.load_dataset('iris')
titanic = sns.load_dataset('titanic')

x = iris.petal_length.values

plt.figure(figsize=(5,3))
sns.rugplot(x)  # rugplot함수를 이용하면 plt로 반환
plt.title('rug plot')
plt.show()
```
![image](https://user-images.githubusercontent.com/78904413/235455581-aaf40b3a-fffd-4157-8e09-10c3dacdb6e9.png)

![image](https://user-images.githubusercontent.com/78904413/235455530-fb99cb58-b156-4991-bd3d-89081cf5bf80.png)

1~2사이에 데이터가 있고 3~7사이에 데이터가 있다는 것을 확인할 수 있습니다.

- countplot : 카테고리별 데이터 갯수
- jointplot : 산점도그래프를 기본으로 표시하고 x,y축에 변수에 대한 히스토그램 표시, 두 변수의 관계와 데이터가 얼마나 분산되어 있는지 파악

```python
sns.countplot(x='class', data = titanic)
plt.show()
```
![image](https://user-images.githubusercontent.com/78904413/235456069-b5f7adc9-7de8-4ca5-a59f-f55d0bb74d28.png)


```python
sns.jointplot(x='sepal_length',y='sepal_width', data=iris)
plt.show()
```

![image](https://user-images.githubusercontent.com/78904413/235456210-3a73fa53-5736-489e-8d2f-c335f911e6de.png)

- pairplot : 3차원 이상의 데이터 비교 분석

```python
plt.figure(figsize=(10,10))
sns.pairplot(iris)
plt.show()
```

![image](https://user-images.githubusercontent.com/78904413/235456499-74963538-14ff-4c6f-95c9-85cd48bef643.png)

- heatmap : 데이터 값을 컬러로 변환시켜 시각적인 분석
- barplot : 카데고리 값에 따른 실수 값의 평균과 편차를 표시 평균은 막대의 높이로, 편차는 에러바로 표시
- pointplot : 점 추정치 및 신뢰구간을 표시
- boxplot : 박스와 박스 바깥의 선으로 이루어짐
  - 데이터의 구간, 이상치, 최소값, 최대값을 나타날 때 자주 사용합니다.


![image](https://user-images.githubusercontent.com/78904413/235456800-0af37809-088a-4f32-bce8-829b58698778.png)

![image](https://user-images.githubusercontent.com/78904413/235456974-2e3a2033-32e3-4f05-857c-30020ee0feb6.png)

> 신뢰구간 : 평균과 표준편차를 이용해서 어떤 데이터의 구간을 추정

- violinplot : 세로 방향으로 커널 밀도 히스토그램을 그림
- stripplot : 범주형 변수에 들어있는 각 범주별 데이터의 분포 확인
- swarmplot : stripplot과 유사하지만 데이터를 나타내는 점이 겹치지 않도록 표현
- 
![image](https://user-images.githubusercontent.com/78904413/235457514-9b8236ce-341d-4bf2-914d-5c773e5dc3e5.png)

![image](https://user-images.githubusercontent.com/78904413/235457588-6feacb86-5624-4ad1-9c43-8137b11001c5.png)




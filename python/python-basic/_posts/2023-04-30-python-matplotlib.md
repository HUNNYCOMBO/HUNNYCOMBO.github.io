---
title: '시각화'
excerpt: '데이터 프레임을 시각화하는 패키지에 대해 알아보기'
tags: ['matplotlib', '시각화']
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

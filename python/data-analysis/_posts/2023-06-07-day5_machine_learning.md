---
title:  "머신러닝 기초"
excerpt: '머신러닝 용어와 데이터전처리, 더미데이터화에 대해 알아보기'
tag: [ML, 데이터전처리, 더미데이터화]
---

<head>
  <style>
    table.dataframe {
      white-space: normal;
      width: 100%;
      height: 240px;
      display: block;
      overflow: auto;
      font-family: Arial, sans-serif;
      font-size: 0.9rem;
      line-height: 20px;
      text-align: center;
      border: 0px !important;
    }

    table.dataframe th {
      text-align: center;
      font-weight: bold;
      padding: 8px;
    }

    table.dataframe td {
      text-align: center;
      padding: 8px;
    }

    table.dataframe tr:hover {
      background: #b8d1f3; 
    }

    .output_prompt {
      overflow: auto;
      font-size: 0.9rem;
      line-height: 1.45;
      border-radius: 0.3rem;
      -webkit-overflow-scrolling: touch;
      padding: 0.8rem;
      margin-top: 0;
      margin-bottom: 15px;
      font: 1rem Consolas, "Liberation Mono", Menlo, Courier, monospace;
      color: $code-text-color;
      border: solid 1px $border-color;
      border-radius: 0.3rem;
      word-break: normal;
      white-space: pre;
    }

  .dataframe tbody tr th:only-of-type {
      vertical-align: middle;
  }

  .dataframe tbody tr th {
      vertical-align: top;
  }

  .dataframe thead th {
      text-align: center !important;
      padding: 8px;
  }

  .page__content p {
      margin: 0 0 0px !important;
  }

  .page__content p > strong {
    font-size: 0.8rem !important;
  }

  </style>
</head>


## ML(머신러닝)



과거의 데이터에서 미래의 데이터를 예측(회기 또는 분류)함.



- 정형데이터 : sklearn 모듈 | 숫자나 문서같은 데이터

- 비정형데이터 : tensorflow, pytorch | 사운드나 영상 같은 대용량 데이터



### 지도학습, 비지도학습



- 지도학습 : y값이 있음

- 비지도학습 : y값이 없음(Gan,강화학습)



### 회귀, 분류



- 회귀(regression) : y값의 결과가 임의의 숫자 1개일 때

  - 단순선형회귀 : x데이터가 한개 | $y=wx+b$

  - 다중선형회귀 : x데이터가 여러개

- 분류(classification) : 중복을 제거한 y값의 결과가 n개의 경우만 있을 때

  - 이항 : y결과가 0~1사이값이 되도록 하는 함수가 필요

  - 다항 : y결과가 카테고리 개수만큼 나올 수 있또록 하는 함수 필요



### 활성화 함수



활성한 함수란 $ y=f(x) $



x데이터와 y데이터 간의 수식을 찾는 과정

기본수식은 wx+b -> 로그값을 취하면 이항분류 -> 여러개의 로그값을 확률로 변홯나면 다항분류



회귀분석의 예측 y 값의 예 : 300

이항분류 예측 y 값의 예 : 0.2 | 사용자가 일정값을 기준으로 0과 1로 변경해야함 (임계값) - 시그모이드 함수

다항분류 예측 y 값의 예 : \[0,2,0.8\] | 사용자가 여러 값 중에 가장 큰 값이 있는 위치를 찾아야함 - 소프트맥스 함수



sklearn은 이항분류 다항분류 모두 소프트맥스함수를 사용



### 정형데이터 필수 전처리



x, y데이터는 무조건 숫자여야함(bias weight값을 구하려면 평균을 내야하는데 null이나 문자가잇으면 계산이 불가능). 결측치(null)값 안됌 



최소제곱법 : MSE | 오차의 제곱의 합이 가장 최소가 되는 지점



권장사항

- x데이터의 정규화(스케일링) : MSE(min, max), MAE(절대값)

- x데이터의 더미변수화 : one-hot encoding



### 정형, 비정형데이터 모델 작업전 사항



훈련 데이터, 테스트 데이터, 검증 데이터 분할

훈련 데이터에서 w,b값을 추출하고 테스트 데이터에서는 적용만 함.

테스트 데이터가 잘 안나오면 훈련 데이터를 변경해야 함.

테스트 데이터까지 잘 나오면 검증 데이터에 적용.

(적용: 검증 데이터의 y값과 검증 데이터의 x값으로 예측한 y값이 잘 맞는가)



```python
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

##########데이터 로드

train_df = pd.read_excel('https://github.com/cranberryai/todak_todak_python/blob/master/machine_learning/regression/%E1%84%8B%E1%85%A1%E1%84%87%E1%85%A5%E1%84%8C%E1%85%B5%E1%84%8B%E1%85%A1%E1%84%83%E1%85%B3%E1%86%AF%E1%84%8F%E1%85%B5.xlsx?raw=true', sheet_name='train')
test_df = pd.read_excel('https://github.com/cranberryai/todak_todak_python/blob/master/machine_learning/regression/%E1%84%8B%E1%85%A1%E1%84%87%E1%85%A5%E1%84%8C%E1%85%B5%E1%84%8B%E1%85%A1%E1%84%83%E1%85%B3%E1%86%AF%E1%84%8F%E1%85%B5.xlsx?raw=true', sheet_name='test')

##########데이터 분석

##########데이터 전처리

x_train = train_df.drop(['Son'], axis=1) # 아들 컬럼을 버림 train_df['Father']와 같지만 n-1개의 데이터를 넣는것 보다 전체에서 -1하는게 더 빠름
x_test = test_df.drop(['Son'], axis=1)
y_train = train_df['Son']
y_test = test_df['Son']

print(x_train.head())
'''
    Father
0  160.782
1  166.116
2  165.608
3  169.672
4  176.530
'''

x_train = x_train.to_numpy() # x_train.values
x_test = x_test.to_numpy()

# 아버지의 키를 입력하면 아들의 키를 예측(아들의 키는 무한대의 숫자 중 1개)
# 즉 가장 단순한 선형회귀(linearregression)를 사용

##########모델 생성

model = LinearRegression() # fit_intercept : bias를 살릴 것인지 체크하는 bool

##########모델 학습

model.fit(x_train, y_train)

##########W,b값 확인
model.coef_, model.intercept_ # w, b 값

##########모델 검증

print(model.score(x_test, y_test)) #0.251997790584662

##########모델 예측

x_test = np.array([
    [164.338]
])

y_predict = model.predict(x_test)

print(y_predict[0]) #169.66660924268297
```

<pre>
    Father
0  165.100
1  165.100
2  167.132
3  155.194
4  160.020
0.2519977905846619
170.46931035654347
</pre>
트레이닝 자료값의 오차가 작아야 이 w,b값을 사용할 수 있음.

훈련자료의 오차 확인하기(MSE)

`y_train - (x_train*model.coef_+model.intercept_)`

각각의 항목을 1번의 제곱근으로 작업하고, 더한 뒤 평균을 냄



```python
# print(model.score(x_test,y_test)) # 회귀 공식에서만 사용되는 R2제곱 공식, 1에 가까울수록 좋음
```


```python
# 위의 자료가 잘 나왔다면 테스트자료에 사용
model.predict(x_test)

# 기존의 y값과 비교하여 결과값이 좋다면 y값이 존재하지 않는 자료에 넣음(최종목적)
```

<pre>
array([170.46931036])
</pre>
로지스틱 회기 모델



```python
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

##########데이터 로드

# [x1,x2] 데이터
x_data = np.array([
    [2, 1],
    [3, 2],
    [3, 4],
    [5, 5],
    [7, 5],
    [2, 5],
    [8, 9],
    [9, 10],
    [6, 12],
    [9, 2],
    [6, 10],
    [2, 4]
])
y_data = np.array([0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0])

labels = ['fail', 'pass'] # 0 = fail, 1= pass로 사용자규정해 둠
```


```python
model2 = LinearRegression()
model2.fit(x_data,y_data)
model2.coef_,model2.intercept_

# 선형회귀로 했다면 [2,1]의 예측 값 공식 == predict 함수
2*model2.coef_[0]+1*model2.coef_[1]+model2.intercept_, model2.predict(x_data)[0]
```

<pre>
(-0.043413257582836484, -0.043413257582836484)
</pre>
![image.png](attachment:image.png)



```python
# 편항성 확인은 직접 코드를 짜야함
def check_bias(y_data):
    import numpy as np
    import matplotlib.pyplot as plt
    uniquedData = np.unique(y_data, return_counts=True) #편향성 확인 Ture | y값이 얼마나 한쪽에 치우쳐져 있는지 확인
    print(f"""
        데이터 단일값 : {uniquedData[0]}
        데이터 단일값 개수 : {uniquedData[1]}
        """
        )
    for idx in range(len(uniquedData[0])):
        print(uniquedData[0][idx],'==>',uniquedData[1][idx]/np.sum(uniquedData[1]))
    plt.bar(uniquedData[0],uniquedData[1])
    plt.show()
    
check_bias(y_data)
```

<pre>

        데이터 단일값 : [0 1]
        데이터 단일값 개수 : [5 7]
        
0 ==> 0.4166666666666667
1 ==> 0.5833333333333334
</pre>
<img src="data:image/png;base64,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x9ixYzsc39jYGHV1da23+vr6bk0YAOi5CofF6NGj45FHHol169bFF7/4xZg1a1Zs2rSpw/ENDQ3R3NzcemtqaurWhAGAnqvwWyH9+vWLd7zjHRERMXHixFi/fn385Cc/iV/84hd7HV8qlaJUKnVvlgBAVej2v2ORUmrzGQoA4OBV6BWLb37zmzF9+vSor6+PHTt2xC233BIrV66Me+65p1LzAwCqSKGweP7552PmzJmxbdu2qKurixNPPDHuueeeOPPMMys1PwCgihQKi8WLF1dqHgBAL+BaIQBANsICAMhGWAAA2QgLACAbYQEAZCMsAIBshAUAkI2wAACyERYAQDbCAgDIRlgAANkICwAgG2EBAGQjLACAbIQFAJCNsAAAshEWAEA2wgIAyEZYAADZCAsAIBthAQBkIywAgGyEBQCQjbAAALIRFgBANsICAMhGWAAA2QgLACAbYQEAZCMsAIBshAUAkI2wAACyERYAQDbCAgDIRlgAANkICwAgG2EBAGQjLACAbIQFAJCNsAAAsikUFo2NjXHyySfHwIEDY+jQofHRj340nnjiiUrNDQCoMoXCYtWqVTF79uxYt25drFixIl5//fWYNm1avPrqq5WaHwBQRWqLDL7nnnva3F+yZEkMHTo0NmzYEKeddlrWiQEA1adQWLxRc3NzREQMHjy4wzHlcjnK5XLr/ZaWlu7sEgDowbr84c2UUsydOzfe//73x7hx4zoc19jYGHV1da23+vr6ru4SAOjhuhwWX/rSl+LPf/5zLF26tNNxDQ0N0dzc3Hpramrq6i4BgB6uS2+FfPnLX44777wzVq9eHSNGjOh0bKlUilKp1KXJAQDVpVBYpJTiy1/+cixfvjxWrlwZxxxzTKXmBQBUoUJhMXv27Lj55pvjt7/9bQwcODCee+65iIioq6uLQw45pCITBACqR6HPWCxcuDCam5vj9NNPj2HDhrXebr311krNDwCoIoXfCgEA6IhrhQAA2QgLACAbYQEAZCMsAIBshAUAkI2wAACyERYAQDbCAgDIRlgAANkICwAgG2EBAGQjLACAbIQFAJCNsAAAshEWAEA2wgIAyEZYAADZCAsAIBthAQBkIywAgGyEBQCQjbAAALIRFgBANsICAMhGWAAA2QgLACAbYQEAZCMsAIBshAUAkI2wAACyERYAQDbCAgDIRlgAANkICwAgG2EBAGQjLACAbIQFAJCNsAAAshEWAEA2hcNi9erVcd5558Xw4cOjpqYm7rjjjgpMCwCoRoXD4tVXX413v/vdcc0111RiPgBAFast+oDp06fH9OnTKzEXAKDKFQ6LosrlcpTL5db7LS0tld4lAHCAVPzDm42NjVFXV9d6q6+vr/QuAYADpOJh0dDQEM3Nza23pqamSu8SADhAKv5WSKlUilKpVOndAAA9gH/HAgDIpvArFq+88ko89dRTrfe3bNkSjzzySAwePDje9ra3ZZ0cAFBdCofFQw89FB/84Adb78+dOzciImbNmhU33HBDtokBANWncFicfvrpkVKqxFwAgCrnMxYAQDbCAgDIRlgAANkICwAgG2EBAGQjLACAbIQFAJCNsAAAshEWAEA2wgIAyEZYAADZCAsAIBthAQBkIywAgGyEBQCQjbAAALIRFgBANsICAMhGWAAA2QgLACAbYQEAZCMsAIBshAUAkI2wAACyERYAQDbCAgDIRlgAANkICwAgG2EBAGQjLACAbIQFAJCNsAAAshEWAEA2wgIAyEZYAADZCAsAIBthAQBkIywAgGyEBQCQTZfC4rrrrotjjjkm+vfvHxMmTIj7778/97wAgCpUOCxuvfXWuPzyy+Nb3/pWbNy4MT7wgQ/E9OnTY+vWrZWYHwBQRQqHxY9+9KO49NJL43Of+1y8613viquvvjrq6+tj4cKFlZgfAFBFaosMfu2112LDhg0xb968NtunTZsWa9as2etjyuVylMvl1vvNzc0REdHS0lJ0rvu0u/z/sj8n9CaVOO8OBOc6dKxS5/me500pdTquUFi8+OKLsWvXrjjqqKPabD/qqKPiueee2+tjGhsbY/78+e2219fXF9k1kEHd1Qd6BkClVfo837FjR9TV1XX480JhsUdNTU2b+ymldtv2aGhoiLlz57be3717d/z73/+OIUOGdPiY3qSlpSXq6+ujqakpBg0adKCns98crOuOsPaDce0H67ojDt61H4zrTinFjh07Yvjw4Z2OKxQWRxxxRPTp06fdqxMvvPBCu1cx9iiVSlEqldpsO+yww4rstlcYNGjQQfOb738drOuOsPaDce0H67ojDt61H2zr7uyVij0KfXizX79+MWHChFixYkWb7StWrIj3ve99xWYHAPQ6hd8KmTt3bsycOTMmTpwYkydPjkWLFsXWrVvjsssuq8T8AIAqUjgsPvWpT8VLL70U3/3ud2Pbtm0xbty4+N3vfhcjR46sxPyqXqlUiu985zvt3g7q7Q7WdUdY+8G49oN13REH79oP1nW/GTVpX98bAQB4k1wrBADIRlgAANkICwAgG2EBAGQjLLrp5ZdfjpkzZ0ZdXV3U1dXFzJkzY/v27R2O37lzZ3zjG9+IE044IQYMGBDDhw+Piy66KJ599tk2404//fSoqalpc7vgggsqvJrOXXfddXHMMcdE//79Y8KECXH//fd3On7VqlUxYcKE6N+/f7z97W+Pn//85+3GLFu2LMaOHRulUinGjh0by5cvr9T0u6zIum+//fY488wz48gjj4xBgwbF5MmT4/e//32bMTfccEO7Y1tTUxP/+c9/Kr2UwoqsfeXKlXtd1+OPP95mXDUc84hia7/44ov3uvbjjz++dUw1HPfVq1fHeeedF8OHD4+ampq444479vmY3nKeF117bzvXs0p0y9lnn53GjRuX1qxZk9asWZPGjRuXzj333A7Hb9++PU2dOjXdeuut6fHHH09r165Np5xySpowYUKbcVOmTEmf//zn07Zt21pv27dvr/RyOnTLLbekvn37puuvvz5t2rQpzZkzJw0YMCA988wzex3/9NNPp0MPPTTNmTMnbdq0KV1//fWpb9++6Te/+U3rmDVr1qQ+ffqkK6+8Mj322GPpyiuvTLW1tWndunX7a1n7VHTdc+bMSVdddVV68MEH05NPPpkaGhpS375908MPP9w6ZsmSJWnQoEFtju22bdv215LetKJrv++++1JEpCeeeKLNul5//fXWMdVwzFMqvvbt27e3WXNTU1MaPHhw+s53vtM6phqO++9+97v0rW99Ky1btixFRFq+fHmn43vLeZ5S8bX3pnM9N2HRDZs2bUoR0eYEWbt2bYqI9Pjjj7/p53nwwQdTRLT5n9aUKVPSnDlzck63W9773vemyy67rM22MWPGpHnz5u11/Ne//vU0ZsyYNtu+8IUvpEmTJrXeP//889PZZ5/dZsxZZ52VLrjggkyz7r6i696bsWPHpvnz57feX7JkSaqrq8s1xYopuvY9YfHyyy93+JzVcMxT6v5xX758eaqpqUl///vfW7dVy3Hf48384dpbzvM3ejNr35tqPddz81ZIN6xduzbq6urilFNOad02adKkqKur6/Ay8nvT3NwcNTU17a6h8utf/zqOOOKIOP744+NrX/ta7NixI9fUC3nttddiw4YNMW3atDbbp02b1uE6165d2278WWedFQ899FDs3Lmz0zFFfu0qqSvrfqPdu3fHjh07YvDgwW22v/LKKzFy5MgYMWJEnHvuubFx48Zs886hO2sfP358DBs2LM4444y477772vyspx/ziDzHffHixTF16tR2/3BgTz/uRfWG8zyXaj3XK0FYdMNzzz0XQ4cObbd96NChHV5G/o3+85//xLx58+Izn/lMmwvZzJgxI5YuXRorV66Mb3/727Fs2bL42Mc+lm3uRbz44ouxa9eudheaO+qoozpc53PPPbfX8a+//nq8+OKLnY55s792ldaVdb/RD3/4w3j11Vfj/PPPb902ZsyYuOGGG+LOO++MpUuXRv/+/ePUU0+NzZs3Z51/d3Rl7cOGDYtFixbFsmXL4vbbb4/Ro0fHGWecEatXr24d09OPeUT3j/u2bdvi7rvvjs997nNttlfDcS+qN5znuVTruV4JXbpsem93xRVXxPz58zsds379+ohofwn5iM4vI/+/du7cGRdccEHs3r07rrvuujY/+/znP9/63+PGjYvjjjsuJk6cGA8//HCcdNJJb2YZ2b1xTfta597Gv3F70ec8ELo6x6VLl8YVV1wRv/3tb9sE6KRJk2LSpEmt90899dQ46aST4mc/+1n89Kc/zTfxDIqsffTo0TF69OjW+5MnT46mpqb4wQ9+EKeddlqXnvNA6uo8b7jhhjjssMPiox/9aJvt1XTci+gt53l39IZzPSdhsRdf+tKX9vkNjFGjRsWf//zneP7559v97F//+leHl5HfY+fOnXH++efHli1b4o9//OM+L7t70kknRd++fWPz5s37PSyOOOKI6NOnT7u/YbzwwgsdrvPoo4/e6/ja2toYMmRIp2P29Wu3v3Rl3Xvceuutcemll8Ztt90WU6dO7XTsW97yljj55JN71N9iurP2/zVp0qS46aabWu/39GMe0b21p5Til7/8ZcycOTP69evX6dieeNyL6g3neXdV+7leCd4K2YsjjjgixowZ0+mtf//+MXny5Ghubo4HH3yw9bEPPPBANDc3d3oZ+T1RsXnz5rj33ntbT8DOPProo7Fz584YNmxYljUW0a9fv5gwYUKsWLGizfYVK1Z0uM7Jkye3G/+HP/whJk6cGH379u10TGe/dvtTV9Yd8d+/vVx88cVx8803xznnnLPP/aSU4pFHHjkgx7YjXV37G23cuLHNunr6MY/o3tpXrVoVTz31VFx66aX73E9PPO5F9YbzvDt6w7leEQfiE6O9ydlnn51OPPHEtHbt2rR27dp0wgkntPu66ejRo9Ptt9+eUkpp586d6cMf/nAaMWJEeuSRR9p8BalcLqeUUnrqqafS/Pnz0/r169OWLVvSXXfdlcaMGZPGjx/f5qt7+9Oer98tXrw4bdq0KV1++eVpwIABrZ96nzdvXpo5c2br+D1fQ/vqV7+aNm3alBYvXtzua2h/+tOfUp8+fdKCBQvSY489lhYsWNDjvoZWdN0333xzqq2tTddee22HXxW+4oor0j333JP+9re/pY0bN6ZLLrkk1dbWpgceeGC/r68zRdf+4x//OC1fvjw9+eST6a9//WuaN29eioi0bNmy1jHVcMxTKr72PS688MJ0yimn7PU5q+G479ixI23cuDFt3LgxRUT60Y9+lDZu3Nj6jbXeep6nVHztvelcz01YdNNLL72UZsyYkQYOHJgGDhyYZsyY0e7rdhGRlixZklJKacuWLSki9nq77777Ukopbd26NZ122mlp8ODBqV+/funYY49NX/nKV9JLL720fxf3Btdee20aOXJk6tevXzrppJPSqlWrWn82a9asNGXKlDbjV65cmcaPH5/69euXRo0alRYuXNjuOW+77bY0evTo1Ldv3zRmzJg2fwj1FEXWPWXKlL0e21mzZrWOufzyy9Pb3va21K9fv3TkkUemadOmpTVr1uzHFb15RdZ+1VVXpWOPPTb1798/HX744en9739/uuuuu9o9ZzUc85SK/37fvn17OuSQQ9KiRYv2+nzVcNz3fGW4o9+/vfk8L7r23nau5+Sy6QBANj5jAQBkIywAgGyEBQCQjbAAALIRFgBANsICAMhGWAAA2QgLACAbYQEAZCMsAIBshAUAkI2wAACy+f/vEEr3lFyejAAAAABJRU5ErkJggg=="/>

### 훈련 데이터, 테스트 데이터 나누기(train_test_split함수 사용)



훈련자료에는 모든 클래스가 있어야 하며, 편향 없이 데이터를 잘 나누어 주어야 함.



```python
##########데이터 분석

##########데이터 전처리

x_train, x_test, y_train, y_test = train_test_split(x_data, y_data, test_size=0.3, random_state=777)
# random_state : 한번 나누어진 train, test를 유지하는데, 이는 다른 값 때문에 잘 나온 것인지 데이터를 잘 만나서 잘 나온 것인지 확인하기 위함
# stratify : 지정한 클래스(카테고리) 별 분포를 비율에 따라 맞춰줌 | 권장

check_bias(y_train), check_bias(y_test)
```

<pre>

        데이터 단일값 : [0 1]
        데이터 단일값 개수 : [3 5]
        
0 ==> 0.375
1 ==> 0.625
</pre>
<img src="data:image/png;base64,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KZ33YnSU67wtOsK1npOwOICbbrrpkO/AOOOMM+KFF16It99+u9nX/vOf/7T4MfL77dmzJ6666qrYunVr/PWvfz3kx+4OHz48unTpElu2bDniYdGrV6/o1KlTs39hvPPOOy2u87TTTjvg+M6dO0fPnj0POuZQf3ZHSmvWvd/ixYvj2muvjYceeijGjh170LEnnHBCnHPOOcfUv2Lasvb/NXr06HjggQcat4/1cx7RtrWnlOL3v/99TJo0KcrLyw869lg878XqCNd5W5X6td4e/CjkAHr16hWDBg066K1r165RU1MT9fX18dxzzzXe99lnn436+vqDfoz8/qjYsmVLPPXUU40X4MG89NJLsWfPnujTp0+WNRajvLw8RowYEcuXL2+yf/ny5S2us6amptn4v/zlLzFy5Mjo0qXLQccc7M/uSGrNuiP+718vV199dTz44INx2WWXHfI4KaXYtGnTUTm3LWnt2j9u48aNTdZ1rJ/ziLatfeXKlfH666/Htddee8jjHIvnvVgd4Tpvi45wrbeLo/GK0Y7k0ksvTcOGDUtr1qxJa9asSWeddVazt5sOHDgwPfzwwymllPbs2ZO+8pWvpH79+qVNmzY1eQtSoVBIKaX0+uuvp1mzZqV169alrVu3pscffzwNGjQonX322U3eunck7X/73bx589LmzZvT1KlTU7du3Rpf9T59+vQ0adKkxvH734b2gx/8IG3evDnNmzev2dvQ/va3v6VOnTql2bNnp5dffjnNnj37mHsbWrHrfvDBB1Pnzp3Tvffe2+JbhWfOnJmWLVuW/vGPf6SNGzema665JnXu3Dk9++yzR3x9B1Ps2n/xi1+kpUuXptdeey39/e9/T9OnT08RkZYsWdI4phTOeUrFr32/b3/722nUqFEHfMxSOO+7du1KGzduTBs3bkwRke6+++60cePGxnesddTrPKXi196RrvXchEUbvfvuu2nixImpe/fuqXv37mnixInN3m4XEWn+/PkppZS2bt2aIuKAt6effjqllNKbb76ZLrjggtSjR49UXl6ezjzzzPT9738/vfvuu0d2cR9z7733pv79+6fy8vI0fPjwtHLlysavTZ48OY0ZM6bJ+BUrVqSzzz47lZeXpzPOOCPNmTOn2WM+9NBDaeDAgalLly5p0KBBTb4JHSuKWfeYMWMOeG4nT57cOGbq1Knp9NNPT+Xl5emUU05J48aNS6tXrz6CKzp8xaz9rrvuSmeeeWbq2rVrOvnkk9P555+fHn/88WaPWQrnPKXi/77v3LkznXjiiWnu3LkHfLxSOO/73zLc0t/fjnydF7v2jnat5+Rj0wGAbLzGAgDIRlgAANkICwAgG2EBAGQjLACAbIQFAJCNsAAAshEWAEA2wgIAyEZYAADZCAsAIBthAQBk8/8BCpKXq3JmGfYAAAAASUVORK5CYII="/>

<pre>

        데이터 단일값 : [0 1]
        데이터 단일값 개수 : [2 2]
        
0 ==> 0.5
1 ==> 0.5
</pre>
<img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAiwAAAGdCAYAAAAxCSikAAAAOXRFWHRTb2Z0d2FyZQBNYXRwbG90bGliIHZlcnNpb24zLjcuMSwgaHR0cHM6Ly9tYXRwbG90bGliLm9yZy/bCgiHAAAACXBIWXMAAA9hAAAPYQGoP6dpAAAqVklEQVR4nO3dfXBUVZ7/8U9DSIe1SGNAklCEgBYmBEYmBCQJE9QCglFYrXWGWCtRLNClClcwZa20DzPiVBmp8iE8O0xFU5RriG7zNAWshBpIdNODAyZM7SoO7OIkFTvLwEo3sEsAOb8//NFlkwdyQwdOmver6lbNPf29h/PleicfbvdNu4wxRgAAABbrd6MXAAAAcDUEFgAAYD0CCwAAsB6BBQAAWI/AAgAArEdgAQAA1iOwAAAA6xFYAACA9eJu9AKi5dKlS/r22281aNAguVyuG70cAADQDcYYnT59WsOHD1e/fp3fR4mZwPLtt98qLS3tRi8DAAD0QHNzs0aMGNHp6zETWAYNGiTph4YTExNv8GoAAEB3hEIhpaWlhX+OdyZmAsvlt4ESExMJLAAA9DFX+zgHH7oFAADWI7AAAADrEVgAAID1CCwAAMB6BBYAAGA9AgsAALAegQUAAFiPwAIAAKxHYAEAANYjsAAAAOs5CixlZWWaPHmyBg0apGHDhunhhx/W119/fdXjamtrlZOTo4SEBN1+++16991329X4fD5lZWXJ7XYrKytLW7ZscbI0AAAQwxwFltraWi1evFh/+MMfVFNTo4sXL6qwsFBnz57t9Jhjx47pgQceUEFBgRoaGvTiiy/q2Weflc/nC9f4/X4VFxerpKREhw4dUklJiebOnav9+/f3vDMAABAzXMYY09OD//rXv2rYsGGqra3VtGnTOqx54YUXtH37dn311VfhsUWLFunQoUPy+/2SpOLiYoVCIe3atStcc//99+vWW29VVVVVt9YSCoXk8XgUDAb58kMAAPqI7v78vqbPsASDQUlSUlJSpzV+v1+FhYURY7NmzdKBAwd04cKFLmvq6+s7nbetrU2hUChiAwAAsSmupwcaY1RaWqqf/exnGj9+fKd1ra2tSk5OjhhLTk7WxYsXdeLECaWmpnZa09ra2um8ZWVlWr58eU+X78ioZTuuy58D9FXfvPHgjV5CVHCtA5270dd5j++wPPPMM/rTn/7UrbdsXC5XxP7ld6F+PN5RzZVjP+b1ehUMBsNbc3Ozk+UDAIA+pEd3WP7xH/9R27dvV11dnUaMGNFlbUpKSrs7JcePH1dcXJyGDBnSZc2Vd11+zO12y+1292T5AACgj3F0h8UYo2eeeUabN2/W73//e40ePfqqx+Tl5ammpiZibPfu3Zo0aZIGDBjQZU1+fr6T5QEAgBjlKLAsXrxYH3zwgT788EMNGjRIra2tam1t1f/93/+Fa7xerx5//PHw/qJFi/SXv/xFpaWl+uqrr/Tee++poqJCzz//fLhmyZIl2r17t1asWKHDhw9rxYoV2rNnj5YuXXrtHQIAgD7PUWBZv369gsGg7r33XqWmpoa36urqcE0gEFBTU1N4f/To0dq5c6f27dunn/70p/r1r3+tVatW6ZFHHgnX5Ofna9OmTXr//fd11113qbKyUtXV1ZoyZUoUWgQAAH2do8+wdOdXtlRWVrYbu+eee/TFF190edzPf/5z/fznP3eyHAAAcJPgu4QAAID1CCwAAMB6BBYAAGA9AgsAALAegQUAAFiPwAIAAKxHYAEAANYjsAAAAOsRWAAAgPUILAAAwHoEFgAAYD0CCwAAsB6BBQAAWI/AAgAArEdgAQAA1iOwAAAA6xFYAACA9QgsAADAegQWAABgPQILAACwHoEFAABYj8ACAACsR2ABAADWI7AAAADrEVgAAID1CCwAAMB6BBYAAGA9AgsAALAegQUAAFiPwAIAAKxHYAEAANYjsAAAAOsRWAAAgPUcB5a6ujrNmTNHw4cPl8vl0tatW7usnz9/vlwuV7tt3Lhx4ZrKysoOa86dO+e4IQAAEHscB5azZ89qwoQJWrNmTbfqV65cqUAgEN6am5uVlJSkX/ziFxF1iYmJEXWBQEAJCQlOlwcAAGJQnNMDioqKVFRU1O16j8cjj8cT3t+6dau+++47PfnkkxF1LpdLKSkpTpcDAABuAtf9MywVFRWaMWOG0tPTI8bPnDmj9PR0jRgxQrNnz1ZDQ0OX87S1tSkUCkVsAAAgNl3XwBIIBLRr1y4tXLgwYjwzM1OVlZXavn27qqqqlJCQoKlTp+rIkSOdzlVWVha+e+PxeJSWltbbywcAADfIdQ0slZWVGjx4sB5++OGI8dzcXM2bN08TJkxQQUGBPvroI915551avXp1p3N5vV4Fg8Hw1tzc3MurBwAAN4rjz7D0lDFG7733nkpKShQfH99lbb9+/TR58uQu77C43W653e5oLxMAAFjout1hqa2t1dGjR7VgwYKr1hpj1NjYqNTU1OuwMgAAYDvHd1jOnDmjo0ePhvePHTumxsZGJSUlaeTIkfJ6vWppadHGjRsjjquoqNCUKVM0fvz4dnMuX75cubm5GjNmjEKhkFatWqXGxkatXbu2By0BAIBY4ziwHDhwQPfdd194v7S0VJL0xBNPqLKyUoFAQE1NTRHHBINB+Xw+rVy5ssM5T506paefflqtra3yeDzKzs5WXV2d7r77bqfLAwAAMchxYLn33ntljOn09crKynZjHo9H//u//9vpMe+8847eeecdp0sBAAA3Cb5LCAAAWI/AAgAArEdgAQAA1iOwAAAA6xFYAACA9QgsAADAegQWAABgPQILAACwHoEFAABYj8ACAACsR2ABAADWI7AAAADrEVgAAID1CCwAAMB6BBYAAGA9AgsAALAegQUAAFiPwAIAAKxHYAEAANYjsAAAAOsRWAAAgPUILAAAwHoEFgAAYD0CCwAAsB6BBQAAWI/AAgAArEdgAQAA1iOwAAAA6xFYAACA9QgsAADAegQWAABgPQILAACwHoEFAABYz3Fgqaur05w5czR8+HC5XC5t3bq1y/p9+/bJ5XK12w4fPhxR5/P5lJWVJbfbraysLG3ZssXp0gAAQIxyHFjOnj2rCRMmaM2aNY6O+/rrrxUIBMLbmDFjwq/5/X4VFxerpKREhw4dUklJiebOnav9+/c7XR4AAIhBcU4PKCoqUlFRkeM/aNiwYRo8eHCHr5WXl2vmzJnyer2SJK/Xq9raWpWXl6uqqsrxnwUAAGLLdfsMS3Z2tlJTUzV9+nTt3bs34jW/36/CwsKIsVmzZqm+vr7T+dra2hQKhSI2AAAQm3o9sKSmpmrDhg3y+XzavHmzMjIyNH36dNXV1YVrWltblZycHHFccnKyWltbO523rKxMHo8nvKWlpfVaDwAA4MZy/JaQUxkZGcrIyAjv5+Xlqbm5WW+++aamTZsWHne5XBHHGWPajf2Y1+tVaWlpeD8UChFaAACIUTfksebc3FwdOXIkvJ+SktLubsrx48fb3XX5MbfbrcTExIgNAADEphsSWBoaGpSamhrez8vLU01NTUTN7t27lZ+ff72XBgAALOT4LaEzZ87o6NGj4f1jx46psbFRSUlJGjlypLxer1paWrRx40ZJPzwBNGrUKI0bN07nz5/XBx98IJ/PJ5/PF55jyZIlmjZtmlasWKGHHnpI27Zt0549e/TZZ59FoUUAANDXOQ4sBw4c0H333Rfev/w5kieeeEKVlZUKBAJqamoKv37+/Hk9//zzamlp0cCBAzVu3Djt2LFDDzzwQLgmPz9fmzZt0ssvv6xXXnlFd9xxh6qrqzVlypRr6Q0AAMQIlzHG3OhFREMoFJLH41EwGIz651lGLdsR1fmAWPPNGw/e6CVEBdc60Lneus67+/Ob7xICAADWI7AAAADrEVgAAID1CCwAAMB6BBYAAGA9AgsAALAegQUAAFiPwAIAAKxHYAEAANYjsAAAAOsRWAAAgPUILAAAwHoEFgAAYD0CCwAAsB6BBQAAWI/AAgAArEdgAQAA1iOwAAAA6xFYAACA9QgsAADAegQWAABgPQILAACwHoEFAABYj8ACAACsR2ABAADWI7AAAADrEVgAAID1CCwAAMB6BBYAAGA9AgsAALAegQUAAFiPwAIAAKxHYAEAANZzHFjq6uo0Z84cDR8+XC6XS1u3bu2yfvPmzZo5c6Zuu+02JSYmKi8vT5988klETWVlpVwuV7vt3LlzTpcHAABikOPAcvbsWU2YMEFr1qzpVn1dXZ1mzpypnTt36uDBg7rvvvs0Z84cNTQ0RNQlJiYqEAhEbAkJCU6XBwAAYlCc0wOKiopUVFTU7fry8vKI/ddff13btm3T7373O2VnZ4fHXS6XUlJSnC4HAADcBK77Z1guXbqk06dPKykpKWL8zJkzSk9P14gRIzR79ux2d2Cu1NbWplAoFLEBAIDYdN0Dy1tvvaWzZ89q7ty54bHMzExVVlZq+/btqqqqUkJCgqZOnaojR450Ok9ZWZk8Hk94S0tLux7LBwAAN8B1DSxVVVV69dVXVV1drWHDhoXHc3NzNW/ePE2YMEEFBQX66KOPdOedd2r16tWdzuX1ehUMBsNbc3Pz9WgBAADcAI4/w9JT1dXVWrBggT7++GPNmDGjy9p+/fpp8uTJXd5hcbvdcrvd0V4mAACw0HW5w1JVVaX58+frww8/1IMPPnjVemOMGhsblZqaeh1WBwAAbOf4DsuZM2d09OjR8P6xY8fU2NiopKQkjRw5Ul6vVy0tLdq4caOkH8LK448/rpUrVyo3N1etra2SpIEDB8rj8UiSli9frtzcXI0ZM0ahUEirVq1SY2Oj1q5dG40eAQBAH+f4DsuBAweUnZ0dfiS5tLRU2dnZ+uUvfylJCgQCampqCtf/5je/0cWLF7V48WKlpqaGtyVLloRrTp06paefflpjx45VYWGhWlpaVFdXp7vvvvta+wMAADHAZYwxN3oR0RAKheTxeBQMBpWYmBjVuUct2xHV+YBY880bV3+rty/gWgc611vXeXd/fvNdQgAAwHoEFgAAYD0CCwAAsB6BBQAAWI/AAgAArEdgAQAA1iOwAAAA6xFYAACA9QgsAADAegQWAABgPQILAACwHoEFAABYj8ACAACsR2ABAADWI7AAAADrEVgAAID1CCwAAMB6BBYAAGA9AgsAALAegQUAAFiPwAIAAKxHYAEAANYjsAAAAOsRWAAAgPUILAAAwHoEFgAAYD0CCwAAsB6BBQAAWI/AAgAArEdgAQAA1iOwAAAA6xFYAACA9QgsAADAeo4DS11dnebMmaPhw4fL5XJp69atVz2mtrZWOTk5SkhI0O2336533323XY3P51NWVpbcbreysrK0ZcsWp0sDAAAxynFgOXv2rCZMmKA1a9Z0q/7YsWN64IEHVFBQoIaGBr344ot69tln5fP5wjV+v1/FxcUqKSnRoUOHVFJSorlz52r//v1OlwcAAGJQnNMDioqKVFRU1O36d999VyNHjlR5ebkkaezYsTpw4IDefPNNPfLII5Kk8vJyzZw5U16vV5Lk9XpVW1ur8vJyVVVVOV0iAACIMb3+GRa/36/CwsKIsVmzZunAgQO6cOFClzX19fWdztvW1qZQKBSxAQCA2NTrgaW1tVXJyckRY8nJybp48aJOnDjRZU1ra2un85aVlcnj8YS3tLS06C8eAABY4bo8JeRyuSL2jTHtxjuquXLsx7xer4LBYHhrbm6O4ooBAIBNHH+GxamUlJR2d0qOHz+uuLg4DRkypMuaK++6/Jjb7Zbb7Y7+ggEAgHV6/Q5LXl6eampqIsZ2796tSZMmacCAAV3W5Ofn9/byAABAH+D4DsuZM2d09OjR8P6xY8fU2NiopKQkjRw5Ul6vVy0tLdq4caMkadGiRVqzZo1KS0v11FNPye/3q6KiIuLpnyVLlmjatGlasWKFHnroIW3btk179uzRZ599FoUWAQBAX+f4DsuBAweUnZ2t7OxsSVJpaamys7P1y1/+UpIUCATU1NQUrh89erR27typffv26ac//al+/etfa9WqVeFHmiUpPz9fmzZt0vvvv6+77rpLlZWVqq6u1pQpU661PwAAEANc5vInYPu4UCgkj8ejYDCoxMTEqM49atmOqM4HxJpv3njwRi8hKrjWgc711nXe3Z/ffJcQAACwHoEFAABYj8ACAACsR2ABAADWI7AAAADrEVgAAID1CCwAAMB6BBYAAGA9AgsAALAegQUAAFiPwAIAAKxHYAEAANYjsAAAAOsRWAAAgPUILAAAwHoEFgAAYD0CCwAAsB6BBQAAWI/AAgAArEdgAQAA1iOwAAAA6xFYAACA9QgsAADAegQWAABgPQILAACwHoEFAABYj8ACAACsR2ABAADWI7AAAADrEVgAAID1CCwAAMB6BBYAAGA9AgsAALBejwLLunXrNHr0aCUkJCgnJ0effvppp7Xz58+Xy+Vqt40bNy5cU1lZ2WHNuXPnerI8AAAQYxwHlurqai1dulQvvfSSGhoaVFBQoKKiIjU1NXVYv3LlSgUCgfDW3NyspKQk/eIXv4ioS0xMjKgLBAJKSEjoWVcAACCmOA4sb7/9thYsWKCFCxdq7NixKi8vV1pamtavX99hvcfjUUpKSng7cOCAvvvuOz355JMRdS6XK6IuJSWlZx0BAICY4yiwnD9/XgcPHlRhYWHEeGFhoerr67s1R0VFhWbMmKH09PSI8TNnzig9PV0jRozQ7Nmz1dDQ0OU8bW1tCoVCERsAAIhNjgLLiRMn9P333ys5OTliPDk5Wa2trVc9PhAIaNeuXVq4cGHEeGZmpiorK7V9+3ZVVVUpISFBU6dO1ZEjRzqdq6ysTB6PJ7ylpaU5aQUAAPQhPfrQrcvlitg3xrQb60hlZaUGDx6shx9+OGI8NzdX8+bN04QJE1RQUKCPPvpId955p1avXt3pXF6vV8FgMLw1Nzf3pBUAANAHxDkpHjp0qPr379/ubsrx48fb3XW5kjFG7733nkpKShQfH99lbb9+/TR58uQu77C43W653e7uLx4AAPRZju6wxMfHKycnRzU1NRHjNTU1ys/P7/LY2tpaHT16VAsWLLjqn2OMUWNjo1JTU50sDwAAxChHd1gkqbS0VCUlJZo0aZLy8vK0YcMGNTU1adGiRZJ+eKumpaVFGzdujDiuoqJCU6ZM0fjx49vNuXz5cuXm5mrMmDEKhUJatWqVGhsbtXbt2h62BQAAYonjwFJcXKyTJ0/qtddeUyAQ0Pjx47Vz587wUz+BQKDd72QJBoPy+XxauXJlh3OeOnVKTz/9tFpbW+XxeJSdna26ujrdfffdPWgJAADEGpcxxtzoRURDKBSSx+NRMBhUYmJiVOcetWxHVOcDYs03bzx4o5cQFVzrQOd66zrv7s9vvksIAABYj8ACAACsR2ABAADWI7AAAADrEVgAAID1CCwAAMB6BBYAAGA9AgsAALAegQUAAFiPwAIAAKxHYAEAANYjsAAAAOsRWAAAgPUILAAAwHoEFgAAYD0CCwAAsB6BBQAAWI/AAgAArEdgAQAA1iOwAAAA6xFYAACA9QgsAADAegQWAABgPQILAACwHoEFAABYj8ACAACsR2ABAADWI7AAAADrEVgAAID1CCwAAMB6BBYAAGA9AgsAALAegQUAAFivR4Fl3bp1Gj16tBISEpSTk6NPP/2009p9+/bJ5XK12w4fPhxR5/P5lJWVJbfbraysLG3ZsqUnSwMAADHIcWCprq7W0qVL9dJLL6mhoUEFBQUqKipSU1NTl8d9/fXXCgQC4W3MmDHh1/x+v4qLi1VSUqJDhw6ppKREc+fO1f79+513BAAAYo7jwPL2229rwYIFWrhwocaOHavy8nKlpaVp/fr1XR43bNgwpaSkhLf+/fuHXysvL9fMmTPl9XqVmZkpr9er6dOnq7y83HFDAAAg9jgKLOfPn9fBgwdVWFgYMV5YWKj6+vouj83OzlZqaqqmT5+uvXv3Rrzm9/vbzTlr1qwu52xra1MoFIrYAABAbHIUWE6cOKHvv/9eycnJEePJyclqbW3t8JjU1FRt2LBBPp9PmzdvVkZGhqZPn666urpwTWtrq6M5JamsrEwejye8paWlOWkFAAD0IXE9OcjlckXsG2PajV2WkZGhjIyM8H5eXp6am5v15ptvatq0aT2aU5K8Xq9KS0vD+6FQiNACAECMcnSHZejQoerfv3+7Ox/Hjx9vd4ekK7m5uTpy5Eh4PyUlxfGcbrdbiYmJERsAAIhNjgJLfHy8cnJyVFNTEzFeU1Oj/Pz8bs/T0NCg1NTU8H5eXl67OXfv3u1oTgAAELscvyVUWlqqkpISTZo0SXl5edqwYYOampq0aNEiST+8VdPS0qKNGzdK+uEJoFGjRmncuHE6f/68PvjgA/l8Pvl8vvCcS5Ys0bRp07RixQo99NBD2rZtm/bs2aPPPvssSm0CAIC+zHFgKS4u1smTJ/Xaa68pEAho/Pjx2rlzp9LT0yVJgUAg4neynD9/Xs8//7xaWlo0cOBAjRs3Tjt27NADDzwQrsnPz9emTZv08ssv65VXXtEdd9yh6upqTZkyJQotAgCAvs5ljDE3ehHREAqF5PF4FAwGo/55llHLdkR1PiDWfPPGgzd6CVHBtQ50rreu8+7+/Oa7hAAAgPUILAAAwHoEFgAAYD0CCwAAsB6BBQAAWI/AAgAArEdgAQAA1iOwAAAA6xFYAACA9QgsAADAegQWAABgPQILAACwHoEFAABYj8ACAACsR2ABAADWI7AAAADrEVgAAID1CCwAAMB6BBYAAGA9AgsAALAegQUAAFiPwAIAAKxHYAEAANYjsAAAAOsRWAAAgPUILAAAwHoEFgAAYD0CCwAAsB6BBQAAWI/AAgAArEdgAQAA1iOwAAAA6xFYAACA9XoUWNatW6fRo0crISFBOTk5+vTTTzut3bx5s2bOnKnbbrtNiYmJysvL0yeffBJRU1lZKZfL1W47d+5cT5YHAABijOPAUl1draVLl+qll15SQ0ODCgoKVFRUpKampg7r6+rqNHPmTO3cuVMHDx7Ufffdpzlz5qihoSGiLjExUYFAIGJLSEjoWVcAACCmxDk94O2339aCBQu0cOFCSVJ5ebk++eQTrV+/XmVlZe3qy8vLI/Zff/11bdu2Tb/73e+UnZ0dHne5XEpJSXG6HAAAcBNwdIfl/PnzOnjwoAoLCyPGCwsLVV9f3605Ll26pNOnTyspKSli/MyZM0pPT9eIESM0e/bsdndgrtTW1qZQKBSxAQCA2OQosJw4cULff/+9kpOTI8aTk5PV2trarTneeustnT17VnPnzg2PZWZmqrKyUtu3b1dVVZUSEhI0depUHTlypNN5ysrK5PF4wltaWpqTVgAAQB/Sow/dulyuiH1jTLuxjlRVVenVV19VdXW1hg0bFh7Pzc3VvHnzNGHCBBUUFOijjz7SnXfeqdWrV3c6l9frVTAYDG/Nzc09aQUAAPQBjj7DMnToUPXv37/d3ZTjx4+3u+typerqai1YsEAff/yxZsyY0WVtv379NHny5C7vsLjdbrnd7u4vHgAA9FmO7rDEx8crJydHNTU1EeM1NTXKz8/v9LiqqirNnz9fH374oR588MGr/jnGGDU2Nio1NdXJ8gAAQIxy/JRQaWmpSkpKNGnSJOXl5WnDhg1qamrSokWLJP3wVk1LS4s2btwo6Yew8vjjj2vlypXKzc0N350ZOHCgPB6PJGn58uXKzc3VmDFjFAqFtGrVKjU2Nmrt2rXR6hMAAPRhjgNLcXGxTp48qddee02BQEDjx4/Xzp07lZ6eLkkKBAIRv5PlN7/5jS5evKjFixdr8eLF4fEnnnhClZWVkqRTp07p6aefVmtrqzwej7Kzs1VXV6e77777GtsDAACxwGWMMTd6EdEQCoXk8XgUDAaVmJgY1blHLdsR1fmAWPPNG1d/q7cv4FoHOtdb13l3f37zXUIAAMB6BBYAAGA9AgsAALAegQUAAFiPwAIAAKxHYAEAANYjsAAAAOsRWAAAgPUILAAAwHoEFgAAYD0CCwAAsB6BBQAAWI/AAgAArEdgAQAA1iOwAAAA6xFYAACA9QgsAADAegQWAABgPQILAACwHoEFAABYj8ACAACsR2ABAADWI7AAAADrEVgAAID1CCwAAMB6BBYAAGA9AgsAALAegQUAAFiPwAIAAKxHYAEAANYjsAAAAOsRWAAAgPUILAAAwHo9Cizr1q3T6NGjlZCQoJycHH366add1tfW1ionJ0cJCQm6/fbb9e6777ar8fl8ysrKktvtVlZWlrZs2dKTpQEAgBjkOLBUV1dr6dKleumll9TQ0KCCggIVFRWpqampw/pjx47pgQceUEFBgRoaGvTiiy/q2Weflc/nC9f4/X4VFxerpKREhw4dUklJiebOnav9+/f3vDMAABAzXMYY4+SAKVOmaOLEiVq/fn14bOzYsXr44YdVVlbWrv6FF17Q9u3b9dVXX4XHFi1apEOHDsnv90uSiouLFQqFtGvXrnDN/fffr1tvvVVVVVXdWlcoFJLH41EwGFRiYqKTlq5q1LIdUZ0PiDXfvPHgjV5CVHCtA53rreu8uz+/45xMev78eR08eFDLli2LGC8sLFR9fX2Hx/j9fhUWFkaMzZo1SxUVFbpw4YIGDBggv9+v5557rl1NeXl5p2tpa2tTW1tbeD8YDEr6ofFou9T2v1GfE4glvXHd3Qhc60Dneus6vzzv1e6fOAosJ06c0Pfff6/k5OSI8eTkZLW2tnZ4TGtra4f1Fy9e1IkTJ5SamtppTWdzSlJZWZmWL1/ebjwtLa277QCIEk/5jV4BgN7W29f56dOn5fF4On3dUWC5zOVyRewbY9qNXa3+ynGnc3q9XpWWlob3L126pP/5n//RkCFDujwuVoRCIaWlpam5uTnqb4HZ7GbtW6L3m7H3m7Vvid5vpt6NMTp9+rSGDx/eZZ2jwDJ06FD179+/3Z2P48ePt7tDcllKSkqH9XFxcRoyZEiXNZ3NKUlut1tutztibPDgwd1tJWYkJibeFP9BX+lm7Vui95ux95u1b4neb5beu7qzcpmjp4Ti4+OVk5OjmpqaiPGamhrl5+d3eExeXl67+t27d2vSpEkaMGBAlzWdzQkAAG4ujt8SKi0tVUlJiSZNmqS8vDxt2LBBTU1NWrRokaQf3qppaWnRxo0bJf3wRNCaNWtUWlqqp556Sn6/XxUVFRFP/yxZskTTpk3TihUr9NBDD2nbtm3as2ePPvvssyi1CQAA+jLHgaW4uFgnT57Ua6+9pkAgoPHjx2vnzp1KT0+XJAUCgYjfyTJ69Gjt3LlTzz33nNauXavhw4dr1apVeuSRR8I1+fn52rRpk15++WW98soruuOOO1RdXa0pU6ZEocXY5Ha79atf/ard22Kx7mbtW6L3m7H3m7Vvid5v1t674vj3sAAAAFxvfJcQAACwHoEFAABYj8ACAACsR2ABAADWI7BY6rvvvlNJSYk8Ho88Ho9KSkp06tSpTusvXLigF154QT/5yU90yy23aPjw4Xr88cf17bffRtTde++9crlcEdujjz7ay910bd26dRo9erQSEhKUk5OjTz/9tMv62tpa5eTkKCEhQbfffrvefffddjU+n09ZWVlyu93KysrSli1bemv5Peak782bN2vmzJm67bbblJiYqLy8PH3yyScRNZWVle3Orcvl0rlz53q7Fcec9L5v374O+zp8+HBEXV8455Kz3ufPn99h7+PGjQvX9IXzXldXpzlz5mj48OFyuVzaunXrVY+Jlevcae+xdq1HlYGV7r//fjN+/HhTX19v6uvrzfjx483s2bM7rT916pSZMWOGqa6uNocPHzZ+v99MmTLF5OTkRNTdc8895qmnnjKBQCC8nTp1qrfb6dSmTZvMgAEDzG9/+1vz5ZdfmiVLlphbbrnF/OUvf+mw/r/+67/M3/zN35glS5aYL7/80vz2t781AwYMMP/yL/8Srqmvrzf9+/c3r7/+uvnqq6/M66+/buLi4swf/vCH69XWVTnte8mSJWbFihXm888/N3/+85+N1+s1AwYMMF988UW45v333zeJiYkR5zYQCFyvlrrNae979+41kszXX38d0dfFixfDNX3hnBvjvPdTp05F9Nzc3GySkpLMr371q3BNXzjvO3fuNC+99JLx+XxGktmyZUuX9bFynRvjvPdYutajjcBioS+//NJIirjw/H6/kWQOHz7c7Xk+//xzIyni/wzvueces2TJkmgu95rcfffdZtGiRRFjmZmZZtmyZR3W/9M//ZPJzMyMGPuHf/gHk5ubG96fO3euuf/++yNqZs2aZR599NEorfraOe27I1lZWWb58uXh/ffff994PJ5oLbHXOO39cmD57rvvOp2zL5xzY679vG/ZssW4XC7zzTffhMf6ynm/rDs/tGPlOr9Sd3rvSF+91qONt4Qs5Pf75fF4In5xXm5urjwej+rr67s9TzAYlMvlavcdS//8z/+soUOHaty4cXr++ed1+vTpaC3dkfPnz+vgwYMqLCyMGC8sLOy0T7/f365+1qxZOnDggC5cuNBljZO/u97Uk76vdOnSJZ0+fVpJSUkR42fOnFF6erpGjBih2bNnq6GhIWrrjoZr6T07O1upqamaPn269u7dG/Ga7edcis55r6io0IwZM8K/qPMy28+7U7FwnUdLX73WewOBxUKtra0aNmxYu/Fhw4a1+5LIzpw7d07Lli3T3//930d8edZjjz2mqqoq7du3T6+88op8Pp/+7u/+Lmprd+LEiRP6/vvv233JZXJycqd9tra2dlh/8eJFnThxosua7v7d9bae9H2lt956S2fPntXcuXPDY5mZmaqsrNT27dtVVVWlhIQETZ06VUeOHInq+q9FT3pPTU3Vhg0b5PP5tHnzZmVkZGj69Omqq6sL19h+zqVrP++BQEC7du3SwoULI8b7wnl3Khau82jpq9d6b3D8q/nRc6+++qqWL1/eZc0f//hHSZLL5Wr3mjGmw/ErXbhwQY8++qguXbqkdevWRbz21FNPhf/3+PHjNWbMGE2aNElffPGFJk6c2J02ou7Knq7WZ0f1V447nfNG6Okaq6qq9Oqrr2rbtm0RwTY3N1e5ubnh/alTp2rixIlavXq1Vq1aFb2FR4GT3jMyMpSRkRHez8vLU3Nzs958801NmzatR3PeSD1dZ2VlpQYPHqyHH344YrwvnXcnYuU6vxaxcK1HE4HlOnrmmWeu+kTOqFGj9Kc//Un//d//3e61v/71r+3+RXGlCxcuaO7cuTp27Jh+//vfX/WrySdOnKgBAwboyJEj1z2wDB06VP3792/3L6Ljx4932mdKSkqH9XFxcRoyZEiXNVf7u7teetL3ZdXV1VqwYIE+/vhjzZgxo8vafv36afLkyVb9q+taev+x3NxcffDBB+F928+5dG29G2P03nvvqaSkRPHx8V3W2njenYqF6/xa9fVrvTfwltB1NHToUGVmZna5JSQkKC8vT8FgUJ9//nn42P379ysYDCo/P7/T+S+HlSNHjmjPnj3hC7sr//Ef/6ELFy4oNTU1Kj06ER8fr5ycHNXU1ESM19TUdNpnXl5eu/rdu3dr0qRJGjBgQJc1Xf3dXU896Vv64V9b8+fP14cffqgHH3zwqn+OMUaNjY035Nx2pqe9X6mhoSGiL9vPuXRtvdfW1uro0aNasGDBVf8cG8+7U7FwnV+LWLjWe8WN+KQvru7+++83d911l/H7/cbv95uf/OQn7R5rzsjIMJs3bzbGGHPhwgXzt3/7t2bEiBGmsbEx4lG3trY2Y4wxR48eNcuXLzd//OMfzbFjx8yOHTtMZmamyc7OjnhE9Hq6/JhnRUWF+fLLL83SpUvNLbfcEn4KYtmyZaakpCRcf/lxx+eee858+eWXpqKiot3jjv/2b/9m+vfvb9544w3z1VdfmTfeeMO6xx2d9v3hhx+auLg4s3bt2k4fSX/11VfNv/7rv5r//M//NA0NDebJJ580cXFxZv/+/de9v6447f2dd94xW7ZsMX/+85/Nv//7v5tly5YZScbn84Vr+sI5N8Z575fNmzfPTJkypcM5+8J5P336tGloaDANDQ1Gknn77bdNQ0ND+AnGWL3OjXHeeyxd69FGYLHUyZMnzWOPPWYGDRpkBg0aZB577LF2j3VKMu+//74xxphjx44ZSR1ue/fuNcYY09TUZKZNm2aSkpJMfHy8ueOOO8yzzz5rTp48eX2bu8LatWtNenq6iY+PNxMnTjS1tbXh15544glzzz33RNTv27fPZGdnm/j4eDNq1Cizfv36dnN+/PHHJiMjwwwYMMBkZmZG/HCzhZO+77nnng7P7RNPPBGuWbp0qRk5cqSJj483t912myksLDT19fXXsaPuc9L7ihUrzB133GESEhLMrbfean72s5+ZHTt2tJuzL5xzY5z/937q1CkzcOBAs2HDhg7n6wvn/fKj6Z399xvL17nT3mPtWo8mlzH//5NMAAAAluIzLAAAwHoEFgAAYD0CCwAAsB6BBQAAWI/AAgAArEdgAQAA1iOwAAAA6xFYAACA9QgsAADAegQWAABgPQILAACwHoEFAABY7/8BEAPjZBwnm7MAAAAASUVORK5CYII="/>

<pre>
(None, None)
</pre>

```python
x_train, x_test, y_train, y_test = train_test_split(x_data, y_data, test_size=0.3, random_state=777, stratify=y_data)

check_bias(y_train), check_bias(y_train)
```

<pre>

        데이터 단일값 : [0 1]
        데이터 단일값 개수 : [3 5]
        
0 ==> 0.375
1 ==> 0.625
</pre>
<img src="data:image/png;base64,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KZ33YnSU67wtOsK1npOwOICbbrrpkO/AOOOMM+KFF16It99+u9nX/vOf/7T4MfL77dmzJ6666qrYunVr/PWvfz3kx+4OHz48unTpElu2bDniYdGrV6/o1KlTs39hvPPOOy2u87TTTjvg+M6dO0fPnj0POuZQf3ZHSmvWvd/ixYvj2muvjYceeijGjh170LEnnHBCnHPOOcfUv2Lasvb/NXr06HjggQcat4/1cx7RtrWnlOL3v/99TJo0KcrLyw869lg878XqCNd5W5X6td4e/CjkAHr16hWDBg066K1r165RU1MT9fX18dxzzzXe99lnn436+vqDfoz8/qjYsmVLPPXUU40X4MG89NJLsWfPnujTp0+WNRajvLw8RowYEcuXL2+yf/ny5S2us6amptn4v/zlLzFy5Mjo0qXLQccc7M/uSGrNuiP+718vV199dTz44INx2WWXHfI4KaXYtGnTUTm3LWnt2j9u48aNTdZ1rJ/ziLatfeXKlfH666/Htddee8jjHIvnvVgd4Tpvi45wrbeLo/GK0Y7k0ksvTcOGDUtr1qxJa9asSWeddVazt5sOHDgwPfzwwymllPbs2ZO+8pWvpH79+qVNmzY1eQtSoVBIKaX0+uuvp1mzZqV169alrVu3pscffzwNGjQonX322U3eunck7X/73bx589LmzZvT1KlTU7du3Rpf9T59+vQ0adKkxvH734b2gx/8IG3evDnNmzev2dvQ/va3v6VOnTql2bNnp5dffjnNnj37mHsbWrHrfvDBB1Pnzp3Tvffe2+JbhWfOnJmWLVuW/vGPf6SNGzema665JnXu3Dk9++yzR3x9B1Ps2n/xi1+kpUuXptdeey39/e9/T9OnT08RkZYsWdI4phTOeUrFr32/b3/722nUqFEHfMxSOO+7du1KGzduTBs3bkwRke6+++60cePGxnesddTrPKXi196RrvXchEUbvfvuu2nixImpe/fuqXv37mnixInN3m4XEWn+/PkppZS2bt2aIuKAt6effjqllNKbb76ZLrjggtSjR49UXl6ezjzzzPT9738/vfvuu0d2cR9z7733pv79+6fy8vI0fPjwtHLlysavTZ48OY0ZM6bJ+BUrVqSzzz47lZeXpzPOOCPNmTOn2WM+9NBDaeDAgalLly5p0KBBTb4JHSuKWfeYMWMOeG4nT57cOGbq1Knp9NNPT+Xl5emUU05J48aNS6tXrz6CKzp8xaz9rrvuSmeeeWbq2rVrOvnkk9P555+fHn/88WaPWQrnPKXi/77v3LkznXjiiWnu3LkHfLxSOO/73zLc0t/fjnydF7v2jnat5+Rj0wGAbLzGAgDIRlgAANkICwAgG2EBAGQjLACAbIQFAJCNsAAAshEWAEA2wgIAyEZYAADZCAsAIBthAQBk8/8BCpKXq3JmGfYAAAAASUVORK5CYII="/>

<pre>

        데이터 단일값 : [0 1]
        데이터 단일값 개수 : [3 5]
        
0 ==> 0.375
1 ==> 0.625
</pre>
<img src="data:image/png;base64,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KZ33YnSU67wtOsK1npOwOICbbrrpkO/AOOOMM+KFF16It99+u9nX/vOf/7T4MfL77dmzJ6666qrYunVr/PWvfz3kx+4OHz48unTpElu2bDniYdGrV6/o1KlTs39hvPPOOy2u87TTTjvg+M6dO0fPnj0POuZQf3ZHSmvWvd/ixYvj2muvjYceeijGjh170LEnnHBCnHPOOcfUv2Lasvb/NXr06HjggQcat4/1cx7RtrWnlOL3v/99TJo0KcrLyw869lg878XqCNd5W5X6td4e/CjkAHr16hWDBg066K1r165RU1MT9fX18dxzzzXe99lnn436+vqDfoz8/qjYsmVLPPXUU40X4MG89NJLsWfPnujTp0+WNRajvLw8RowYEcuXL2+yf/ny5S2us6amptn4v/zlLzFy5Mjo0qXLQccc7M/uSGrNuiP+718vV199dTz44INx2WWXHfI4KaXYtGnTUTm3LWnt2j9u48aNTdZ1rJ/ziLatfeXKlfH666/Htddee8jjHIvnvVgd4Tpvi45wrbeLo/GK0Y7k0ksvTcOGDUtr1qxJa9asSWeddVazt5sOHDgwPfzwwymllPbs2ZO+8pWvpH79+qVNmzY1eQtSoVBIKaX0+uuvp1mzZqV169alrVu3pscffzwNGjQonX322U3eunck7X/73bx589LmzZvT1KlTU7du3Rpf9T59+vQ0adKkxvH734b2gx/8IG3evDnNmzev2dvQ/va3v6VOnTql2bNnp5dffjnNnj37mHsbWrHrfvDBB1Pnzp3Tvffe2+JbhWfOnJmWLVuW/vGPf6SNGzema665JnXu3Dk9++yzR3x9B1Ps2n/xi1+kpUuXptdeey39/e9/T9OnT08RkZYsWdI4phTOeUrFr32/b3/722nUqFEHfMxSOO+7du1KGzduTBs3bkwRke6+++60cePGxnesddTrPKXi196RrvXchEUbvfvuu2nixImpe/fuqXv37mnixInN3m4XEWn+/PkppZS2bt2aIuKAt6effjqllNKbb76ZLrjggtSjR49UXl6ezjzzzPT9738/vfvuu0d2cR9z7733pv79+6fy8vI0fPjwtHLlysavTZ48OY0ZM6bJ+BUrVqSzzz47lZeXpzPOOCPNmTOn2WM+9NBDaeDAgalLly5p0KBBTb4JHSuKWfeYMWMOeG4nT57cOGbq1Knp9NNPT+Xl5emUU05J48aNS6tXrz6CKzp8xaz9rrvuSmeeeWbq2rVrOvnkk9P555+fHn/88WaPWQrnPKXi/77v3LkznXjiiWnu3LkHfLxSOO/73zLc0t/fjnydF7v2jnat5+Rj0wGAbLzGAgDIRlgAANkICwAgG2EBAGQjLACAbIQFAJCNsAAAshEWAEA2wgIAyEZYAADZCAsAIBthAQBk8/8BCpKXq3JmGfYAAAAASUVORK5CYII="/>

<pre>
(None, None)
</pre>
데이터의 개수가 적어서 `random_state`의 값과 `stratify`의 값을 주어도 차이를 볼 수 없음



```python
##########모델 생성

model = LogisticRegression(penalty='none')

##########모델 학습

model.fit(x_train, y_train)

y_predict = model.predict(x_train)

# 내가 직접 만든 score값
result = y_predict == y_train
print(result)
```

<pre>
[ True  True  True  True  True  True  True  True]
</pre>
<pre>
c:\devtools\Miniconda3\envs\meta\Lib\site-packages\sklearn\linear_model\_logistic.py:1173: FutureWarning: `penalty='none'`has been deprecated in 1.2 and will be removed in 1.4. To keep the past behaviour, set `penalty=None`.
  warnings.warn(
</pre>

```python
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import make_column_transformer
from sklearn.linear_model import Lasso
import numpy as np

##########데이터 로드

train_df = pd.read_excel('https://github.com/cranberryai/todak_todak_python/blob/master/machine_learning/regression/carprice_E1SUl6b.xlsx?raw=true', sheet_name='train')
test_df = pd.read_excel('https://github.com/cranberryai/todak_todak_python/blob/master/machine_learning/regression/carprice_E1SUl6b.xlsx?raw=true', sheet_name='test')

##########데이터 분석

##########데이터 전처리

x_train = train_df.drop(['가격'], axis=1)
x_test = test_df.drop(['가격'], axis=1)
y_train = train_df['가격']
y_test = test_df['가격']

print(x_train.head())
```

<pre>
     년식   종류    연비   마력    토크   연료  하이브리드   배기량    중량 변속기
0  2015  준중형  11.8  172  21.0  가솔린      0  1999  1300  자동
1  2015  준중형  12.3  204  27.0  가솔린      0  1591  1300  자동
2  2015   소형  15.0  100  13.6  가솔린      0  1368  1035  수동
3  2014   소형  14.0  140  17.0  가솔린      0  1591  1090  자동
4  2015   대형   9.6  175  46.0   디젤      0  2497  1990  자동
</pre>
문자 데이터는 사용할 수 없음

만약 문자 데이터를 x데이터로 사용하려면 더미데이터화 해야함

fit은 train 데이터에만 사용하는데, train데이터에는 모든 클래스를 포함하지만, test에는 그렇지 않다.

그러므로 train데이터에서 one-hot 인코딩으로 종류를 대형 소형 준준형 준형으로 나누었는데

test 데이터에서는 대형 데이터가 들어오지 않아서 one-hot 인코딩이 바뀔수 있는 이슈가 있다.


## 데이터 전처리



### 레이블 인코딩(백터화)



문자로 된 y값을 숫자로 변형해야 할 때 주로 사용.

x데이터는 one-hot 인코딩까지 해주어야 함.

train과 test로 나누기 전에 처음부터 숫자로 변경한 뒤, 나누는 것을 권장.

이미 나뉘어져 있는 자료라면 train에만 fit을 적용해야 함.



![image.png](attachment:image.png)



피팅에는 min max 스케일링을 위한 min max도 설정되는데 위의 표를보면

test 데이터의 min 값이 2이지만 test데이터에는 피팅을 하지 않으므로 min 값이 1로 계산된다.



```python
items = ('tv,냉장고,전자레인지,컴퓨터,선풍기,선풍기,믹서,믹서').split(',')
items
```

<pre>
['tv', '냉장고', '전자레인지', '컴퓨터', '선풍기', '선풍기', '믹서', '믹서']
</pre>

```python
from sklearn.preprocessing import LabelEncoder

encoder = LabelEncoder()
encoder.fit(items) # items의 중복을 제거하고 순서번호를 갖게함 | 절대 test 데이터에는 fit해선 안됌

print(encoder.classes_) # fitting하면 중복을 제거한 클래스들이 생성된다.

encoder.transform(items) # fit해서 나온 결과물을 items에 적용
```

<pre>
['tv' '냉장고' '믹서' '선풍기' '전자레인지' '컴퓨터']
</pre>
<pre>
array([0, 1, 4, 5, 3, 3, 2, 2])
</pre>

```python
encoder.fit_transform(items) # fit과 transform을 동시에 하는 함수
```

<pre>
array([0, 1, 4, 5, 3, 3, 2, 2], dtype=int64)
</pre>
## one-hot encoding



x값에서 주로 사용 0,1(no,yes) 외에 3개 이상의 카테고리 변수는 원핫인코딩을 권장

인곤지능에서는 y값도 이항 또는 다항분류에 소프트맥스 함수를 적용할 때는 반드시 원핫인코딩을 적용해야함.



더미변수화와 다른 점은 더미 전처리는 필드 별로 0,0,1,0,0 식으로 변환하고

원핫인코딩은 array로 \[0,0,1,0,0\] 식으로 변환한다.



판다스의 `get_dummies()`와 기능이 같다.



```python
from sklearn.preprocessing import OneHotEncoder

items = np.array(items).reshape(-1,1) # 원핫인코딩 피팅은 반드시 2차원 배열을 요구한다.

oh_encoder=OneHotEncoder()
oh_encoder.fit(items)
oh_encoder.categories_
```

<pre>
[array(['tv', '냉장고', '믹서', '선풍기', '전자레인지', '컴퓨터'], dtype='<U5')]
</pre>

```python
oh_lables = oh_encoder.transform(items)

oh_lables
```

<pre>
<8x6 sparse matrix of type '<class 'numpy.float64'>'
	with 8 stored elements in Compressed Sparse Row format>
</pre>
sparse matrix : 0값이 많은 행렬(희소행렬)



1. 텍스트 분석을 할 때는 희소행렬을 0값이 있는 자료를 제외하고 값이 있는 값만으로 다시 자료를 구성함.



2. 공간적인 낭비: 텍스트 데이터는 대부분이 희소한 형태를 가지며, 많은 단어가 0 또는 매우 작은 빈도로 발생합니다. 이로 인해 많은 0 값을 저장하는 것은 메모리 공간의 낭비가 될 수 있습니다.



3. 계산 비효율성: 희소 행렬은 대부분이 0 값을 가지기 때문에, 0을 고려하지 않고 행렬 연산을 수행하는 것은 비효율적입니다. 많은 연산을 수행해야 하므로 연산 시간이 길어질 수 있습니다.



4. 모델의 성능 저하: 일부 머신러닝 알고리즘은 밀집된 행렬을 기대합니다. 희소 행렬을 사용할 경우 모델의 성능이 저하될 수 있습니다. 이는 모델이 0이 아닌 값들 사이의 패턴을 파악하지 못하거나, 희소한 데이터로 인해 정보의 손실이 발생할 수 있기 때문입니다.



따라서, 텍스트 분석에서는 sparse matrix의 문제를 해결하기 위해 희소 행렬을 효율적으로 표현하고 처리하기 위한 방법을 사용합니다. 이를 위해 희소 행렬을 압축하거나, 중요한 단어나 특성을 선택하거나, 단어의 빈도를 가중치로 변환하는 등의 전처리 기법을 적용하여 문제를 해결합니다.




```python
arryData = oh_lables.toarray()
arryData
```

<pre>
array([[1., 0., 0., 0., 0., 0.],
       [0., 1., 0., 0., 0., 0.],
       [0., 0., 0., 0., 1., 0.],
       [0., 0., 0., 0., 0., 1.],
       [0., 0., 0., 1., 0., 0.],
       [0., 0., 0., 1., 0., 0.],
       [0., 0., 1., 0., 0., 0.],
       [0., 0., 1., 0., 0., 0.]])
</pre>

```python
# 역 백터화 하기

classData=('냉장고, 믹서, 선풍기, 전자레인지, 컴퓨터, tv').split(',')
max_in_data=np.argmax(arryData, axis=1) # 행단위로 가장 큰 값 찾는 함수
print(max_in_data)

for idx in max_in_data:
    print(classData[idx])
```

<pre>
[0 1 4 5 3 3 2 2]
냉장고
 믹서
 컴퓨터
 tv
 전자레인지
 전자레인지
 선풍기
 선풍기
</pre>
### 스케일링



- 표준화스케일링 : standardScaler

- 정규화스케일링 : minmaxScaler



표준편차가 필요한 이유



![image.png](attachment:image.png)



평균은 같지만 B데이터에서는 이상치라 볼 수 있는 큰 값이 들어있다.



평균이 아닌 편차로 비교하면 이상치를 확인할 수 있다.





실습



```python
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import make_column_transformer
from sklearn.linear_model import Lasso
import numpy as np

##########데이터 로드

train_df = pd.read_excel('https://github.com/cranberryai/todak_todak_python/blob/master/machine_learning/regression/carprice_E1SUl6b.xlsx?raw=true', sheet_name='train')
test_df = pd.read_excel('https://github.com/cranberryai/todak_todak_python/blob/master/machine_learning/regression/carprice_E1SUl6b.xlsx?raw=true', sheet_name='test')

# 컬럼 확인
display(train_df.head(2), test_df.head(2))

# train데이터 test 데이터 합치기
df = pd.concat([train_df,test_df])
display(df.info)
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>가격</th>
      <th>년식</th>
      <th>종류</th>
      <th>연비</th>
      <th>마력</th>
      <th>토크</th>
      <th>연료</th>
      <th>하이브리드</th>
      <th>배기량</th>
      <th>중량</th>
      <th>변속기</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1885</td>
      <td>2015</td>
      <td>준중형</td>
      <td>11.8</td>
      <td>172</td>
      <td>21.0</td>
      <td>가솔린</td>
      <td>0</td>
      <td>1999</td>
      <td>1300</td>
      <td>자동</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2190</td>
      <td>2015</td>
      <td>준중형</td>
      <td>12.3</td>
      <td>204</td>
      <td>27.0</td>
      <td>가솔린</td>
      <td>0</td>
      <td>1591</td>
      <td>1300</td>
      <td>자동</td>
    </tr>
  </tbody>
</table>
</div>


<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>가격</th>
      <th>년식</th>
      <th>종류</th>
      <th>연비</th>
      <th>마력</th>
      <th>토크</th>
      <th>연료</th>
      <th>하이브리드</th>
      <th>배기량</th>
      <th>중량</th>
      <th>변속기</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1915</td>
      <td>2015</td>
      <td>대형</td>
      <td>6.8</td>
      <td>159</td>
      <td>23.0</td>
      <td>LPG</td>
      <td>0</td>
      <td>2359</td>
      <td>1935</td>
      <td>수동</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1164</td>
      <td>2012</td>
      <td>소형</td>
      <td>13.3</td>
      <td>108</td>
      <td>13.9</td>
      <td>가솔린</td>
      <td>0</td>
      <td>1396</td>
      <td>1035</td>
      <td>자동</td>
    </tr>
  </tbody>
</table>
</div>


<pre>
<bound method DataFrame.info of       가격    년식   종류    연비   마력    토크   연료  하이브리드   배기량    중량 변속기
0   1885  2015  준중형  11.8  172  21.0  가솔린      0  1999  1300  자동
1   2190  2015  준중형  12.3  204  27.0  가솔린      0  1591  1300  자동
2   1135  2015   소형  15.0  100  13.6  가솔린      0  1368  1035  수동
3   1645  2014   소형  14.0  140  17.0  가솔린      0  1591  1090  자동
4   1960  2015   대형   9.6  175  46.0   디젤      0  2497  1990  자동
..   ...   ...  ...   ...  ...   ...  ...    ...   ...   ...  ..
26  6910  2015   대형   8.9  334  40.3  가솔린      0  3778  1915  자동
27  2545  2015   대형   8.7  175  46.0   디젤      0  2497  2383  수동
28  1960  2015   대형   9.6  175  46.0   디젤      0  2497  1990  자동
29   870  2010   소형  13.0   95  12.7  가솔린      0  1399  1046  자동
30  2879  2015   중형  14.8  200  43.0   디젤      0  2199  1760  수동

[102 rows x 11 columns]>
</pre>

```python
# 결측치 확인
df.isna().sum()
```

<pre>
가격       0
년식       0
종류       0
연비       0
마력       0
토크       0
연료       0
하이브리드    0
배기량      0
중량       0
변속기      0
dtype: int64
</pre>

```python
# x,y 변수를 나누고 y값에 영향을 주는 x값을 알기 위해서는 EDA를 실행해야 함.(이번 실습에선 제외)
# 현대자동차 가격을 예측하는 회기분석

y_data = df['가격']
x_data = df.drop(['가격'],axis=1)
display(x_data.head(2),y_data.head(2))
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>년식</th>
      <th>종류</th>
      <th>연비</th>
      <th>마력</th>
      <th>토크</th>
      <th>연료</th>
      <th>하이브리드</th>
      <th>배기량</th>
      <th>중량</th>
      <th>변속기</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2015</td>
      <td>준중형</td>
      <td>11.8</td>
      <td>172</td>
      <td>21.0</td>
      <td>가솔린</td>
      <td>0</td>
      <td>1999</td>
      <td>1300</td>
      <td>자동</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2015</td>
      <td>준중형</td>
      <td>12.3</td>
      <td>204</td>
      <td>27.0</td>
      <td>가솔린</td>
      <td>0</td>
      <td>1591</td>
      <td>1300</td>
      <td>자동</td>
    </tr>
  </tbody>
</table>
</div>


<pre>
0    1885
1    2190
Name: 가격, dtype: int64
</pre>

```python
# x데이터의 문자데이터가 어떤 자료가 있는지 확인
df.dtypes
```

<pre>
가격         int64
년식         int64
종류        object
연비       float64
마력         int64
토크       float64
연료        object
하이브리드      int64
배기량        int64
중량         int64
변속기       object
dtype: object
</pre>

```python
# 더미변수화
x_dummy=pd.get_dummies(x_data)
display(x_dummy.head(2))
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>년식</th>
      <th>연비</th>
      <th>마력</th>
      <th>토크</th>
      <th>하이브리드</th>
      <th>배기량</th>
      <th>중량</th>
      <th>종류_대형</th>
      <th>종류_소형</th>
      <th>종류_준중형</th>
      <th>종류_중형</th>
      <th>연료_LPG</th>
      <th>연료_가솔린</th>
      <th>연료_디젤</th>
      <th>변속기_수동</th>
      <th>변속기_자동</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2015</td>
      <td>11.8</td>
      <td>172</td>
      <td>21.0</td>
      <td>0</td>
      <td>1999</td>
      <td>1300</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2015</td>
      <td>12.3</td>
      <td>204</td>
      <td>27.0</td>
      <td>0</td>
      <td>1591</td>
      <td>1300</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
</div>



```python
# train, test 데이터 분리하기
x_train,x_test,y_train,y_test = train_test_split(x_dummy, y_data, test_size=0.3, random_state=777)

display(x_train.head(2),x_test.head(2),y_train.head(2),y_test.head(2))
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>년식</th>
      <th>연비</th>
      <th>마력</th>
      <th>토크</th>
      <th>하이브리드</th>
      <th>배기량</th>
      <th>중량</th>
      <th>종류_대형</th>
      <th>종류_소형</th>
      <th>종류_준중형</th>
      <th>종류_중형</th>
      <th>연료_LPG</th>
      <th>연료_가솔린</th>
      <th>연료_디젤</th>
      <th>변속기_수동</th>
      <th>변속기_자동</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>9</th>
      <td>2015</td>
      <td>14.0</td>
      <td>100</td>
      <td>13.6</td>
      <td>0</td>
      <td>1368</td>
      <td>1103</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
    </tr>
    <tr>
      <th>8</th>
      <td>2015</td>
      <td>10.8</td>
      <td>245</td>
      <td>36.0</td>
      <td>0</td>
      <td>1998</td>
      <td>1570</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
</div>


<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>년식</th>
      <th>연비</th>
      <th>마력</th>
      <th>토크</th>
      <th>하이브리드</th>
      <th>배기량</th>
      <th>중량</th>
      <th>종류_대형</th>
      <th>종류_소형</th>
      <th>종류_준중형</th>
      <th>종류_중형</th>
      <th>연료_LPG</th>
      <th>연료_가솔린</th>
      <th>연료_디젤</th>
      <th>변속기_수동</th>
      <th>변속기_자동</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>26</th>
      <td>2015</td>
      <td>11.3</td>
      <td>200</td>
      <td>44.5</td>
      <td>0</td>
      <td>2199</td>
      <td>1905</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>1</td>
    </tr>
    <tr>
      <th>61</th>
      <td>2015</td>
      <td>16.0</td>
      <td>159</td>
      <td>21.0</td>
      <td>1</td>
      <td>2359</td>
      <td>1680</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
</div>


<pre>
9    1492
8    2695
Name: 가격, dtype: int64
</pre>
<pre>
26    3585
61    3450
Name: 가격, dtype: int64
</pre>

```python
# train 데이터 스케일링
from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler()

# fit은 스케일러에 따른 필요 값을 추출하는 과정
x_train = scaler.fit_transform(x_train)

print(x_train)
```

<pre>
[[1.         0.65811966 0.01557632 ... 0.         0.         1.        ]
 [1.         0.38461538 0.46728972 ... 0.         0.         1.        ]
 [1.         0.24786325 0.58255452 ... 0.         0.         1.        ]
 ...
 [0.4        0.65811966 0.05919003 ... 0.         0.         1.        ]
 [1.         0.37606838 0.49844237 ... 1.         0.         1.        ]
 [1.         0.23076923 0.68535826 ... 0.         0.         1.        ]]
</pre>

```python
# test 데이터는 스케일링만 진행
x_test = scaler.transform(x_test)
```


```python
# 회귀분석
# 사용자가 3개 이상의 모델을 돌려서 가장 성능이 좋은 모델을 선택하게 됌
lr = LinearRegression()

lr.fit(x_train, y_train) # w,b값을 최소제곱법에 의해서 결정하는 수식 적용 | 독립변수(x)의 개수는 16개

print(f'w값: {lr.coef_}, \nb값:{lr.intercept_}')
```

<pre>
w값: [-115.19522289 1834.16515529 3329.73161962 -393.39526525  172.77975355
 5800.12995696  849.52051433 -348.92760046  389.72289904   -7.0410203
  -33.75427828  225.7595262   -73.84216155 -151.91736465  -84.30076098
   84.30076098], 
b값:-568.2001711344778
</pre>
### 분산팽창지수



x변수끼리는 독립적이어야 하는데, 이러한 독립성을 확인하는 방법으로 분산팽창지수(VIF)가 있다.



VIF가 **10 이상**이면 서로 종속적(다중공선성)이라고 볼 수 있다.



서로 연관성이 높은 변수가 있다면 하나는 제거해야 한다.



### 평가지표



![image.png](attachment:image.png)




```python
# 회기자료 에러율 및 성공률 확인
# r2 score = 성공률, 설명력

from sklearn.metrics import mean_squared_error, r2_score

# train 데이터는 볼 필요가 없다. w,b값을 구하여 정해져있기 때문에
y_preds = lr.predict(x_test) # 테스트 데이터 예측값
mse = mean_squared_error(y_test, y_preds) # 예측값과 테스트 데이터의 y값을 확인하자
rmse = np.sqrt(mse)

print('MSE : {0: .3f}, RSME : {1: 3F}'.format(mse,rmse))
print('variance score : {0: .3f}'.format(r2_score(y_test, y_preds)))
```

<pre>
MSE :  236569769906254.031, RSME :  15380824.747271
variance score : -39033813.275
</pre>
<pre>
c:\devtools\Miniconda3\envs\meta\Lib\site-packages\sklearn\base.py:432: UserWarning: X has feature names, but LinearRegression was fitted without feature names
  warnings.warn(
</pre>
성공률이 매우 낮음



1. 변수영향력을 확인함. w 값(coef)_에서 값이 클수록 영향령이 많은 변수



```python
coef = pd.Series(data=np.round(lr.coef_,1),index=x_dummy.columns)
coef.sort_values(ascending=False)
```

<pre>
배기량       5800.1
마력        3329.7
연비        1834.2
중량         849.5
종류_소형      389.7
연료_LPG     225.8
하이브리드      172.8
변속기_자동      84.3
종류_준중형      -7.0
종류_중형      -33.8
연료_가솔린     -73.8
변속기_수동     -84.3
년식        -115.2
연료_디젤     -151.9
종류_대형     -348.9
토크        -393.4
dtype: float64
</pre>
배기량 마력 연비가 가격(y)값에 가장 많은 영향을 줌

그러나 데이터개수가 적어서 신빙성은 없음


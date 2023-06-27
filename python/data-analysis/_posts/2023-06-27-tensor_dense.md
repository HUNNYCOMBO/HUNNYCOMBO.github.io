---
title:  "딥러닝 dense에 대해 알아보기"
excerpt : "18일차 수업 자료"
tag: [python, dl, dense, tensorflow]
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



```python
import numpy as np
import tensorflow as tf
from tensorflow import keras
from keras import layers
```


```python
import matplotlib.pyplot as plt
```


```python
x = np.array(range(1,7))
y = np.array([10,98,8,2,3,4])
```


```python
input_layer = layers.InputLayer(input_shape=(1,)) # 가장 상단으로 입력되는 독립변수의 개수(독립변수, 특징값 개수)
output_layer = layers.Dense(units=1) # 출력값은 하나인 이항분류 | activation이 없으면 wx+b(선형회귀)로 동작
# input과 output layer는 최소필요조건
```


```python
# tf.random.set_seed(1)
```


```python
model = keras.Sequential([ # 순차처리구조
    input_layer,
    output_layer
])
```

히든레이어의 유닛을 4로 설정한다면, 각각의 w,b 쌍이 4개(총 파라미터8개)로 각각 계산된 y값이 나오게 되는데,

이 각각의 y값 4개를 독립변수로 치환하여 다음 레이어에서 하나의 b와 4개의 w로 다시 계산하게 된다.



```python
model.summary()
```

<pre>
Model: "sequential_14"
_________________________________________________________________
 Layer (type)                Output Shape              Param #   
=================================================================
 dense_30 (Dense)            (None, 1)                 2         
                                                                 
=================================================================
Total params: 2
Trainable params: 2
Non-trainable params: 0
_________________________________________________________________
</pre>

```python
model.get_weights()
```

<pre>
[array([[-0.8584039]], dtype=float32), array([0.], dtype=float32)]
</pre>
첫번쨰는 w, 두번째는 b



```python
model.compile(loss='mse', metrics='acc')    # 예측값과 실제 y값과 비교하는 공식(loss_function|오차함수) | model.filt 할 때 화면에 출력될 사항 선택(metrics)
# model.fit할 때 오차역전파하는 방법론(최적화함수|optimizer)
history = model.fit(x,y, epochs=10, verbose=0) # epochs 옵션 사용 가능 | 변수로 저장하면 history()가 사용 가능한데, 에폭을 돌면서 나온 loss와 acc값들이 list로 들어있다.
```


```python
plt.figure(figsize=(10,3))
plt.subplot(1,2,1)
plt.plot(history.history['loss'],label='loss')
plt.title('loss')

plt.subplot(1,2,2)
plt.plot(history.history['acc'], 'r',label='acc')
plt.title('acc')
#plt.legend(loc='lower right')
```

<pre>
Text(0.5, 1.0, 'acc')
</pre>
<img src="data:image/png;base64,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AlCoEhERERERKQCFKhERERERkQJQqBIRERERESkAhSoREREREZECUKgSEREREREpAL2n6i+ysrKIi4vD2dkZk8lkdDkiIqWK2WwmOTkZLy8vrKz0m99N6ptERIyRn35Joeov4uLiqFq1qtFliIiUaidPnqRKlSpGl1FkqG8SETHWnfRLClV/4ezsDNw4cOXKlTO4GhGR0iUpKYmqVatazsVyg/omERFj5KdfUqj6i5u3VZQrV04dl4iIQXSLW3bqm0REjHUn/ZJuWhcRERERESkAhSoREREREZECUKgSEREREREpAIUqERERERGRAlCoEhERERERKQCFKhERERERkQJQqLqLrmdm8XnEcdIzsowuRURERERE7hG9p+ouGv7Nb/x84CzR8clMfaKJ3rUiIiIiIlIK6ErVXdSnlTdWJli6+xSfbjxmdDkiIiIiInIPKFTdRf713Ph390YATPs5mh+iThtckYiIiIiIFDaFqrus34PVGPRQDQBeW7qPnScuGlyRiIiIiIgUJoWqQjC+cwM63u9OemYWQxbt4sSFVKNLEhERERGRQqJQVQisrUzM6t2cplVcuHTlOs+F7eRSarrRZYmIiIiISCFQqCokjnbWzB/QkvvKOxJzIZUXv9xNWkam0WWJiIiIiMhdplBViNycHQgd+ADO9jbsOHGRcf/Zh9lsNrosERERERG5ixSqClk9D2c+fbYFNlYmlkfFMeuXI0aXJCIiIiIid5FC1T3gV6cy7wbdGGr9w3VHWLb7lMEViYiIiIjI3aJQdY/0aeXNS+1rAfD69/uIPJZgcEUiIiIiInI3KFTdQ68F1KNLE0+uZ5p58ctdHD2XYnRJIiIiIiJSQApV95CVlYkZTzalhXd5kq5l8HzYThJS0owuS0RERERECkCh6h5zsLVmfv+WeFd0IvbiFQYv2sW16xpqXURERESkuFKoMkClsvaEDnyAcg42/BZ7mVeW7iUrS0Oti4iIiIgURwpVBqntVpbP+rXE1trEyn1nmL4m2uiSRERERETkH1CoMpBvrUq837MJAJ9uPMbiHbEGVyQiIiIiIvmV71C1efNmunXrhpeXFyaTieXLl2dbbjKZcp2mTZsGwMWLFxkxYgT16tXDyckJb29vRo4cSWJiYrbtPP7443h7e+Pg4ICnpyf9+vUjLi7ulrWZzWYmTZqEl5cXjo6OtG/f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"/>


```python
model.predict(x) # 예측값
```

<pre>
array([[-0.8237646],
       [-1.6648521],
       [-2.5059395],
       [-3.347027 ],
       [-4.1881146],
       [-5.029202 ]], dtype=float32)
</pre>

```python
model.get_weights()
```

<pre>
[array([[-0.8410875]], dtype=float32), array([0.01732292], dtype=float32)]
</pre>
머신러닝은 공식을 주어주기 떄문에 w,b가 몇번을 돌려도 고정되어 있지만 딥러닝은 w가 랜덤으로 생성되기 때문에 매번 예측값이 바뀌게 된다.  

이는 초기에 어떤 w를 받느냐에 따라 성공률이 달라질 수 있다. => 정답이 없다.

초기 w를 고정하고 싶다면 model잡기 전에 seednumber|randomseed 옵션을 사용할 수 있다.



```python
input_layer = layers.InputLayer(input_shape=(1,))
output_layer = layers.Dense(units=1)
h_layer1 = layers.Dense(units=4, activation='relu') # 히든레이어
h_layer2 = layers.Dense(units=2, activation='relu') # 히든레이어2
```


```python
model = keras.Sequential([
    input_layer,
    h_layer1,
    h_layer2,
    output_layer
])
```


```python
model.compile(loss='mse', metrics='acc')
print(model.fit(x,y))
```

<pre>
1/1 [==============================] - 0s 410ms/step - loss: 1650.3927 - acc: 0.0000e+00
<keras.callbacks.History object at 0x000001499BBC66D0>
</pre>

```python
model.summary()
```

<pre>
Model: "sequential_15"
_________________________________________________________________
 Layer (type)                Output Shape              Param #   
=================================================================
 dense_32 (Dense)            (None, 4)                 8         
                                                                 
 dense_33 (Dense)            (None, 2)                 10        
                                                                 
 dense_31 (Dense)            (None, 1)                 3         
                                                                 
=================================================================
Total params: 21
Trainable params: 21
Non-trainable params: 0
_________________________________________________________________
</pre>
순서대로 히든레이어1 히든레이어2 아웃풋을 의미한다.  



0번 레이어(inputlayer와 hlayer1)는 inputlayer에서 inputshape가 1개여서 w,b를 1개씩 갖으므로 유닛 하나당 2개의 파라미터가 필요하다.  

> 만약 inputshape가 8개였다면 8개의 w와 1개의 b를 가졌을 것이다. 그렇다면 $(8+1)*4$개의 파라미터를 가졌을 것.



렐루함수 처리된 0번레이어의 유닛(w,b쌍)갯수가 1번레이어의 input이 된다. (여기선 1번레이어의 독립변수가 4개라는 뜻)  



1번 레이어는 출력유닛이 2개로 설정되어 있다. 유닛 1개당 독립변수4개의 w값과 하나의 b를 필요로하므로 5개의 파라미터가 필요하다.  

$w1x1+w2x2+w3x3+w4x4+b$를 수행하는 중간값을 2개 생성하는 것이다.



2번 레이어는 유닛갯수가 1이고 하나당 w 2개와 b 1개가 필요하다. activation이 없으므로 $wx+b$를 수행한다.



```python
model.get_weights()
```

<pre>
[array([[-0.3878749 , -0.6135069 ,  0.87405694,  0.09965609]],
       dtype=float32),
 array([ 0.        ,  0.        , -0.00316228, -0.00316228], dtype=float32),
 array([[-0.01561165,  0.8366902 ],
        [ 0.00601244,  0.6017356 ],
        [ 0.1309055 , -0.6168997 ],
        [ 0.4636773 ,  0.1700325 ]], dtype=float32),
 array([-0.00316228,  0.        ], dtype=float32),
 array([[-1.1113869],
        [ 0.5639157]], dtype=float32),
 array([0.00316228], dtype=float32)]
</pre>
- 0,1번 array : 0번레이어의 w와 b 각각의 쌍

- 2,3번 array : 0번레이어의 유닛(로우,4개)들로 이루어져 있고, 1번레이어의 유닛이 2개이므로 2개의 열을 가지며 하나의 열당 w1~4 값들을 갖고있다고 볼 수 있다.

  - 즉 5개의 파라미터로 이루어진 2개의 열

- 4,5번 array : 2번레이어의 파라미터들



```python
print(model.predict(x))
```

<pre>
WARNING:tensorflow:5 out of the last 5 calls to <function Model.make_predict_function.<locals>.predict_function at 0x0000014992C68700> triggered tf.function retracing. Tracing is expensive and the excessive number of tracings could be due to (1) creating @tf.function repeatedly in a loop, (2) passing tensors with different shapes, (3) passing Python objects instead of tensors. For (1), please define your @tf.function outside of the loop. For (2), @tf.function has experimental_relax_shapes=True option that relaxes argument shapes that can avoid unnecessary retracing. For (3), please refer to https://www.tensorflow.org/guide/function#controlling_retracing and https://www.tensorflow.org/api_docs/python/tf/function for  more details.
[[-0.1697524 ]
 [-0.34827134]
 [-0.5267902 ]
 [-0.70530903]
 [-0.8838279 ]
 [-1.0623468 ]]
</pre>

```python
print(model.evaluate(x,y))
```

<pre>
1/1 [==============================] - 0s 62ms/step - loss: 1649.4238 - acc: 0.0000e+00
[1649.423828125, 0.0]
</pre>

```python
intermediate_layer_model = tf.keras.Model(inputs=model.input, outputs=model.layers[0].output)
intermedate_output = intermediate_layer_model(x)
intermedate_output
```

<pre>
<tf.Tensor: shape=(6, 4), dtype=float32, numpy=
array([[0.        , 0.        , 0.8708947 , 0.09649381],
       [0.        , 0.        , 1.7449516 , 0.1961499 ],
       [0.        , 0.        , 2.6190085 , 0.295806  ],
       [0.        , 0.        , 3.4930654 , 0.3954621 ],
       [0.        , 0.        , 4.367122  , 0.4951182 ],
       [0.        , 0.        , 5.2411795 , 0.59477425]], dtype=float32)>
</pre>
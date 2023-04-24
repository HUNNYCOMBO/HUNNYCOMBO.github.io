---
title:  "파이썬 기초 - 변수"
excerpt: ""
tags: [변수]
header:
  teaser: 
  overlay_image: 
  overlay_filter: 0.4
---
## 참고가 된 블로그
- [메이플의 개발 스토리](https://mapled.tistory.com/entry/Jupyter-Notebook-specify-location)


## 1. 파이썬의 특징
- 문법이 쉽고 간결함
- 빠른 개발속도
- 모바일프로그래밍은 불가능

## 2. 주피터노트북
- 오픈소스기반의 웹 플랫폼(터미널은 실행 중이어야 함)
- 개발 중간중간 프로그램을 실행하면서 결과를 확인 할 수 있음
- 시각화에 장점

<details>
<summary>설치 및 실행</summary>
  
```
pip install jupyter
jupyter notebook --notebook-dir='경로입력'
```

설치 후 콘솔에서 출력된 토큰을 브라우저 주소창에 입력합니다.
매번 이렇게 주소를 입력하는 것은 번거로우므로 설정 파일을 이용하여 실행경로를 지정해줍니다.

```
jupyter notebook --generate-config
```

C:\Users\~\.jupyter 경로에 가면 jupyter_notebook_config.py 파일이 생성되어 있을 겁니다.
해당 파일을 열어 주석을 없애고 원하는 경로로 설정합니다.
</details>

![image](https://user-images.githubusercontent.com/78904413/233944444-9a8b5ddf-5fe6-4777-bd8d-c8df046dbd35.png)
주피터노트북에서 위의 한 줄을 cell이라고 명칭합니다. 그리고 cell단위로 실행됩니다.

![cell 단위로 실행되는 모습](https://user-images.githubusercontent.com/78904413/233945525-d7d269de-fe57-4633-986e-4dfecea6dee0.png)
(cell 단위로 실행되는 모습)


## 3. Colab
구글 리서치 팀에서 개발한 클라우드 상에서 파이썬 코드가 작성가능한 제품으로 주피터노트북과 사용법이 비슷합니다.
저장은 구글드라이브에 저장됩니다.

![image](https://user-images.githubusercontent.com/78904413/233948539-b7ce450a-b6aa-4e22-b8ca-a39217dc4b2c.png)
(주피터노트북과 같이 cell단위로 실행되는 모습)

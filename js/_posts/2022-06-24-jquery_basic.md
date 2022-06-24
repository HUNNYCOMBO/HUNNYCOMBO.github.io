---
title: jquery 기초
excerpt: 빠르게 배워보는 jquery기초
---

## 1. jquery란?
복잡한 js의 코드를 줄이기위한 라이브러리 입니다. 최근에는 react를 많이 사용하므로 jquery를 사용하지 않는 경우도 있습니다.  
jquery를 사용하기 위해서 jquery cdn을 이용하여 script태그를 복사해 추가하거나 js파일을 다운받아 script태그로 첨부합니다.    

버전은 여러가지가 있습니다. 
- uncompressed: 원본파일
- minified: 공백제거버전
- slim: 기능이 많이 빠진 라이트버전

## 2. jquery설치 위치
script 태그를 이용하여 아무곳에나 설치해도 사용은 할 수 있지만, 중요한 부분이 있습니다. head에 선언하게 되면 js파일을 다운받아온 다음 view가 보여지기 때문에 문제가 됩니다.  
이왕이면 body태그의 마지막에 js를 넣는 것이 좋습니다.  

## 3. jquery로 HTML변경
js의 목적인 html변경을 jquery로 경험해봅니다. jquery는 css셀렉터 처럼 $기호를 이용하여 표현할 수 있습니다.  

```javascript
...
<body>
  <h4 id="test" class="testclass">안녕하세요</h4>
  
  <script>
    document.getElementById('test').innerHTML = '자바스크립트';
    <!-- 원래 문법 --!>
    
    $('#test').html('제이쿼리');
    <!-- id가 test인것을 찾는 jquery표현 class를 표현할때는 .을 붙임 --!>
```

js에도 queryselector가 있지만 요소를 다루는 데에 있어서 jquery가 더 편리합니다. 또한 jquery표현을 사용했다면 jquery함수를 따라야 합니다. 

- html() : innerhtml과 같습니다. (안의 모든 html)
- text() : 모든 text만
- 출력을 하고싶을 때는 파라미터에 공백으로 둡니다.
- css() : 스타일 속성을 바꿉니다. (style = color: red)였다면 .css('color', 'red);
- attr() : custom속성들을 바꿉니다. .attr('src', 'ogu.jpg')

---
title: "REST API - 생활코딩 강의"
excerpt: "REST API에 대하여 유튜브 생활코딩님의 강의를 기록합니다."
tags: [REST API]
header:
  teaser: ![image](https://user-images.githubusercontent.com/78904413/173184441-5bf7b3fa-fdfb-4567-92e5-cd4ac61c1674.png)
---

## 참고링크
- [생활코딩youtue](https://www.youtube.com/watch?v=PmY3dWcCxXI)

## 1. 기계들의 대화법 - REST API
웹을 이용하여 기계와 기계가 통신할 때, 규격화 된 방식으로 통신하도록 돕는 REST API입니다.  
REST API는 웹의 통신 규약인 HTTP를 사용합니다.  

### 1.1. API란?(Application Programming Interface)
API란 컴퓨터의 기능을 실행시키는 것을 의미합니다. 언어마다 화면에 "hello world"를 출력하는 방식은 다릅니다.  
예를들면 파이썬의 경우 아래와 같을 것이고,  
```python
print('hello world')
```
JS의 경우 아래와 같습니다.
```javascript
document.wirte('hello world')
```
이런 print와 document.write 하나하나가 API라 할 수 있습니다.  

### 1.2. REST API란?
REST API도 컴퓨터의 기능을 실행시키는 명령이라 볼 수 있지만, 나의 컴퓨터가 아닌 상대의 컴퓨터를 실행 시킨다고 볼 수 있습니다.  
REST API란 특정 기술을 뜻하는 것이 아닌, [http](https://opentutorials.org/module/3621)를 이용하여 통신할 때 어떻게해야 시행착오를 줄이고 더 좋은 API 서비스를 만들 수 있는가에 대한 고민의 결과물입니다.  

```
https://www.googleapis.com/.../calendars/calendar_id
{
  "summary":"일정",
  "timeZone":"Asia/Seoul"
}
```
위와 같은 google 캘린더의 api를 이용하면, 나의 캘린더를 구글 캘린더에서 출력해줍니다. 단순히 가져오는 것 뿐만 아니라 CRUD의 작업도 가능합니다.  

### 1.3. 사례
![image](https://user-images.githubusercontent.com/78904413/173181440-7441015a-9377-42fc-9019-2f803e0bf5a6.png)  

블로그나 sns같은 서비스를 운영하고 하나하나의 글을 topic이라 부르기로 가정했다면, 위의 모습과같은 데이터들을 갖게 됩니다.  
REST API에서는 위와같은 데이터를 Resource라고 표현합니다.  
Resource는 URI를 통해서 **표현**됩니다. 전체 토픽을 식별하고 싶다면, 
```
http://exmaple.com/topics
```
같은 URI를 사용하면 됩니다. 여러 데이터들이 모인 것을 Collection이라 표현합니다. Collection은 주소에서 보듯이 복수형(s)를 사용합니다.  

반면, 데이터 하나하나는 Element라고 표현합니다. Element를 표현하기 위한 URI는 아래와같이 표현합니다.  
```
http://example.com/topics/1
http://example.com/topics/rest
// 무엇으로 식별하느냐에 다르게 표현됩니다.
```

단지 URI 표현만으로는 식별만 할 뿐 데이터의 가공(CRUD)은 하지 못합니다. 이런 데이터 가공은 REST API에서 method라고 부릅니다.  

#### 1.4. method
![image](https://user-images.githubusercontent.com/78904413/173181822-9275f492-2524-4dec-9c1a-faef80611481.png)  

http에서 create를 위해 준비된 메소드는 post 입니다. 실제 웹 애플리케이션에서 form을 이용하여 데이터를 전송하고 가공할 때 모두 post를 사용하지만,  
post는 본래 create를 위한 기능입니다. REST API는 http 메소드들을 본래의 목적에 맞게 사용하는 것도 중요한 목표입니다.  

Update의 put은 전체를 수정하는 메소드이고, patch는 부분을 수정하는 메소드 입니다.  

### 2. 실습
![image](https://user-images.githubusercontent.com/78904413/173182405-eeb82326-db1a-401c-a8b2-775d8a54c887.png)

웹브라우저에서 웹서버에 ajax를 위한 API인 fatch를 이용하여 REST API를 이용하는 실습을 해봅니다.
웹 브라우저 뿐만아니라 모바일앱이나 웹서버 등을 REST API를 이용하여 다른 서버와 통신할 수 있습니다.  
실습에서 사용하는 JS나 fatch는 단지 사례입니다. 브라우저와 서버가 어떻게 통신하는가를 중점으로 공부합니다.  

#### 2.1. 실습 소개
![image](https://user-images.githubusercontent.com/78904413/173183206-0b3e61bc-166d-4bf7-8a73-0dd666f81156.png)

왼쪽화면은 REST API를 제공하는 서버이고, 오른쪽화면은 클라이언트라고 가정합니다.  
현재 서버에는 topic과 comment라는 두개의 Resource가 존재하고, comment의 Element로 topicId가 존재하는데 이는 해당 topic id의 Element와 관계를 맺는 것입니다.  
이제 이 데이터(state)들을 어떻게 가공할 것인지 살펴봅니다.  

#### 2.2. 생성-POST
topic이라는 Resource에 데이터를 추가합니다.  
```javascript
fetch('topics', {   // Resource
  method:'POST',    // create method
  headers:{'content-type':'application/json'},    // JSON데이터라는 것을 헤더에 표현
  body:JSON.stringfy({
    title:'fetch', body:'fetch is ...'
  })
})
  .then{
    function(response){
      consle.log('status', response,status);
      return response.json()
    }
  }
  .then{
    function(result){
      console.log(result);
    }
  }
```

![image](https://user-images.githubusercontent.com/78904413/173183516-de0776bf-0bab-44aa-bd1f-ce2797edc944.png)

웹브라우저에서 개발자도구 network탭을 살펴보면 추가한 데이터를 콘솔창으로 확인할 수 있습니다.  
왼쪽의 REST API 서버에 해당 topic이 id:2로 추가되었습니다. status는 201로 정상응답을 했습니다.  
Request(클라이언트가 요청한)데이터를 좀 더 자세하게 살펴봅니다.  

![image](https://user-images.githubusercontent.com/78904413/173183628-0b0f25df-275f-4352-8b2e-aa5216334f3a.png)

첫줄에서 POST 메소드가 사용된 것과, /topics URI를 사용한 것 그 외엔 JSON데이터 타입을 사용한 것을 확인할 수 있습니다.  
이제는 서버에서 Response(응답)한 데이터를 살펴봅니다.  

![image](https://user-images.githubusercontent.com/78904413/173183698-1431d3b8-431d-4eb2-8ad8-25aa9ec0a851.png)

http 응답코드 201은 성공적으로 데이터를 생성했다는 것을 응답하는 코드입니다. REST API에서는 처리의 결과를 응답 코드와 응답 메세지를 통하여 return합니다.  
응답한 데이터는 아래와 같습니다. 마찬가지로 content-type을 헤더에 포함하여 응답합니다.  

![image](https://user-images.githubusercontent.com/78904413/173183752-4e75c781-1b91-4c92-9ce6-e8aa9333ae3e.png)

정리하자면 REST API에서 서버와 클라이언트가 어떤 데이터타입으로 통신할 것인지 규정하지 않습니다.  
URI를 통해 식별하고 method를 통해 데이터를 가공하고, 응답코드와 메시지를 통해 응답합니다.  
http 프로토콜을 http답게 사용하고자 하는것이 REST API라고 볼 수 있습니다.  

#### 2.3. GET
##### 2.3.1. Collection 전체 읽기
```javascript
fetch('topics', {method:'GET'})
.then(
  function(response){
    return response.json()
  }
)
.then(
  function(result){
    console.log(result);
  }
)
```
collection 전체를 읽어오는 GET요청을 보냅니다.  

![image](https://user-images.githubusercontent.com/78904413/173184076-cab6c57b-25a3-4317-b3ce-d2541d04bd85.png)

GET의 성공적인 응답코드는 200입니다.  

##### 2.3.2. 부분 읽기
```javascript
fetch('topics/2')
.then(
  function(response){
    return response.json()
  }
)
.then(
  function(result){
    console.log(result);
  }
)
```
Element를 읽어 올 때의 URI가 다른 것을 확인 할 수 있습니다.  

![image](https://user-images.githubusercontent.com/78904413/173184163-e715606e-2de3-49a7-aa96-b066f6cc0206.png)

#### 2.4. 수정
##### 2.4.2. 부분수정 PATCH
```javascript
fetch('topics/2', {
  method:'PATCH',
  heaers:('content-type':'application/json'),
  body:JSON.stringfy({
    title:'fetch-patch'
  })
})
.then(
  function(response){
    return response.json()
  }
)
.then(
  function(result){
    console.log(result);
  }
)
```
위의 코드는 title만 수정하는 코드입니다. 그에대한 결과로 body는 변하지 않고 title만 변한것을 확인할 수 있습니다.  

![image](https://user-images.githubusercontent.com/78904413/173184237-fadce516-3326-4e4d-837a-b739054c78e5.png)

##### 2.4.2. 전체수정 PUT
```javascript
fetch('topics/2', {
  method:'PUT',
  heaers:('content-type':'application/json'),
  body:JSON.stringfy({
    title:'fetch-patch'
  })
})
.then(
  function(response){
    return response.json()
  }
)
.then(
  function(result){
    console.log(result);
  }
)
```
반면 PUT 메소드를 사용했을 때는, title만 수정했지만 식별자를 제외하고 언급되지 않은 body 값이 사라지는 것을 볼 수 있습니다.  
![image](https://user-images.githubusercontent.com/78904413/173184261-0bb1b44c-8457-4207-8ad9-abcbb88413e2.png)

#### 2.5. DELETE
```javascript
fetch('topics/2', {
  method:'DELETE'
})
  .then(
  function(response){
    return response.json()
  }
)
.then(
  function(result){
    console.log(result);
  }
)
```
삭제를 할 때는 위와같이 Element만 삭제할 수 있고, /topics로 Collection자체를 삭제할 수도 있지만 위험한 행동으로 보통 막혀있습니다.  

#### 2.6. 관계
REST API를 사용할 때 comment처럼 Resource 간에 관계를 맺고 있는 경우 어떻게 URI로 표현하는지 애매할 수 있습니다.  
이때는, /topics/1/comments와 같이 부모 Resource를 앞에 적은 다음, 해당 element의 id값을 적고, 종속된 Resource의 이름을 적어 표현합니다.  

### 3. 마치며
REST API는 복잡한 기술이 아닌, http를 이용하여 통신할 때
Resrouce는 URI로  
행위는 method로  
결과는 응답코드로 http의 본질을 활용하는 권고안이라고 볼 수 있습니다.




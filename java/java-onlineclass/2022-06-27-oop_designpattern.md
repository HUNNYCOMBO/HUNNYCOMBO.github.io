---
title: 객체지향 디자인패턴
excerpt: 얄팍한 코딩사전 유튜브 강의 - 객체지향 디자인패턴 1입니다.
---

## 참고링크
- [얄파한 코딩사전](https://www.youtube.com/watch?v=lJES5TQTTWE)

## 1. singleton
애플리케이션을 만들다보면 인스턴스가 딱 하나만 생성되어야 하는 경우가 있습니다. 실행활을 예로 들면, 브라우저의 다크모드는 페이지를 이동해도 
계속 다크모드를 유지해야하는 경우가 있습니다.  어떤 페이지에 있든 세팅을 관리하는 객체는 하나만 만들어져야 한다는 것입니다.  

![image](https://user-images.githubusercontent.com/78904413/175941021-d8bc9e72-e8a3-4d47-9b34-2b02de782c24.png)
안드로이드 프로그래밍을 예로들면, 페이지마다 setting객체를 불러오게되어 페이지 이동을 하면 세팅 값이 달라지게 됩니다. 이럴때 싱글턴패턴이 필요합니다.  

싱글톤으로 만들기 위해선 먼저 생성자를 private로 선언합니다. private으로 선언함으로서 new 키워드를 사용하지 못하게 됩니다.  
또한 static으로 선언한 자기 자신 객체를 필드로 둡니다. static으로 선언하므로서 static메모리 영역에 딱 하나의 객체로 존재하게 됩니다.  

![image](https://user-images.githubusercontent.com/78904413/175943459-6ad66275-46cc-4fd8-baf8-9355af6bc7e7.png)

그후, getter로 객체를 생성할 때 마다 필드로 둔 자기자신 객체를 주입하도록 작성합니다.  
![image](https://user-images.githubusercontent.com/78904413/175944484-a14c583b-c12b-444e-87ef-18d7786478c5.png)

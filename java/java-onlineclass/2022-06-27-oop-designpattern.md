---
title: 객체지향 디자인패턴
excerpt: 얄팍한 코딩사전 유튜브 강의 - 객체지향 디자인패턴 1입니다.
tags: [design_pattern]
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

이제 각 페이지마다 setting객체를 불러올 때 Setting.getSetting()를 이용하여 싱글턴 패턴을 적용합니다.  

이외에도 싱글턴 패턴은 lazy loading에서 이득을 볼 수 있는 등 이점이 있지만, 이런 기본적인 싱글턴 패턴 코드는 safe-thread하지 않는 점에 유의하여 사용하여야 합니다.  

## 2. strategy
전략패턴이 필요할 때는 mode에 따라 실행방식이 달라져야할 때 사용됩니다. 예를들어,  

![image](https://user-images.githubusercontent.com/78904413/176067072-5bd337d0-5e55-410e-a75a-e18d69a193a0.png)

위와같은 화면에서 이미지, 뉴스 모드에 따른 검색이 이루어지는 방식이 달라져야 한다는 것입니다. 이를 단순하게 코드로 구현하면,  

![image](https://user-images.githubusercontent.com/78904413/176067266-30170b5d-748b-4fa5-8d0e-9d6592681cf5.png)
버튼을 누를때마다 mode변수값이 설정되고, onclick()의 if문으로 동작하게 짤 수 있지만, mode가 추가될 때마다 onclick()도 수정해야하는 번거로움이 있습니다. 즉, 코드를 유지보수하기도 어려우며 모듈화 해나가는 객체지향설계에도 어긋나게 됩니다.  

전략패턴은 모드 하나하나 들을 모듈로 분리해서 모드에 따라 모듈을 갈아끼워주는 방식으로 코드를 짜게됩니다.  
![image](https://user-images.githubusercontent.com/78904413/176067515-3d8e9e3d-636b-489e-b0f8-1f4d1019ad89.png)

이런 모듈화를 위해서는 interface설계가 필요합니다. 각각의 모듈들을 interface를 구현한 객체로 만들고, 필요에 따라 DI받고 교체될 수 있도록 설계합니다.  
![image](https://user-images.githubusercontent.com/78904413/176067787-ae20a66e-8fb8-4a58-99f9-a8776f36a955.png)

이제, 특정 모듈이 수정되야하면 해당 구현체 클래스만 수정하면되고, 특정 모드가 추가되야 하면 구현체를 추가하기만 하면 됩니다.  

## 3. state
state패턴은 전략패턴과 유사한 점이 많지만 차이점은 모니터가 꺼진 상태에서는 켜지고 켜진 상태에서는 꺼지는 전원버튼 처럼 특정 상태마다 다르게 할 일을 ㅁ도ㅠㄹ화해서 지정할떄 쓰입니다.  
![image](https://user-images.githubusercontent.com/78904413/176068325-ac4f6bba-a79f-49f0-99b6-06589ab52512.png)

예시로는 앞서 다크모드를 설정했던 상황과 전략패턴에서 사용했던 interface의 도입이 있습니다. 구현체의 toggle()들은 각각 호출되면 자신의 다른 상태를 호출해 자신의 상태를 변화시킵니다.  

![image](https://user-images.githubusercontent.com/78904413/176068912-b0e8d5d5-5eb2-431b-ae3a-145f92341f3f.png)

## 4. command
command 패턴도 전략패턴과 유사한 부분이 많습니다. 근본적인 차이는 전략패턴은 같은일을 하지만 그 방식이 바뀌는 것이라면, command 패턴은 하늘일 자체가 다르다고 볼 수 있습니다. 예시로 로봇에게 전진하기, 주어진 방향으로 회전하기, 물건 집어올리기 명령을 내리는 코드를 짜봅니다. 이때 interface를 이용하지않고 추상클래스 abstract를 이용합니다.  

![image](https://user-images.githubusercontent.com/78904413/176077285-a8d729ff-c356-453e-be1c-0257f606c258.png)

로봇이 수행할 명령들을 객체로 두고, 이 명령들을 닮은 collection을 생성해, for문을 이용하여 출력합니다.  

![image](https://user-images.githubusercontent.com/78904413/176077563-839b331e-7106-4c3d-9f01-cbe3c536f318.png)

## 5. adapter
oop에서 adapter는 보통 interface가 서로 다른 객체들이 같은 형식 아래 작동할 수 있도록 하는 역할을 합니다. 예를들어 요리사들이 요리를 하는 식당에서 디저트를 제공하기 위해 제과를 하는 파티쉐를 고용한다고 했을 때, 구분해서 명령하지 않고 파티쉐에게 adapter를 달아, 요리라는 명령이 들어왔을 때 파티쉐는 제과를 하도록 할 수 있습니다.  

![image](https://user-images.githubusercontent.com/78904413/176098570-f4cf70ba-8ff6-4c41-9cff-8c0a60cbc2b8.png)

앞선 전략패턴에서 사용했던 모듈들에서 다른 회사에서 만든 모듈을 추가한다고 가정할 때, interface도 다르고 파라미터도 다르며 메소드 명까지 다를 수 있습니다. 때문에 기존의 serachStrategy필드로 모듈을 교체하는 방식을 사용 할 수 없습니다. 이럴 때 adapter패턴이 필요합니다.  

먼저, SearchStrategy를 구현한 클래스를 생성합니다. 맴버 변수로 다른회사의 interface를 넣고 메소드를 실행하면 항상 글로벌로 검색하도록 값을 넣어줍니다.  
![image](https://user-images.githubusercontent.com/78904413/176099051-05be4e55-3725-4019-9df0-aa50dfd6de1e.png)

## 6. proxy
대리인 패턴이라고불리는 proxy패턴은 대표적으로 aop에 사용됩니다. 프로그래밍을 하다보면 객체로 여럿 생성하기가 부담되는 무거운 리소스들이 있습니다. 이럴때 그 클래스의 proxy, 대리자 역할을 하는 클래스를 두어서 대신 호출하고 실제 작업을 할 때 실제 객체가 호출되도록 하는 방식입니다.  

대표적으로 유튜브의 영상들처럼 처음에는 썸네일만 있지만 마우스오버시 동영상이 재생되는 것이 있습니다.  
썸네일을 담당하는 객체는 썸네일과 프리뷰를 두 메소드를 통해 각각 보여주기로 하되, 썸네일이 처음 화면에 나타날 때는 썸네일만 보여주는 프록시를 생성하고, 프리뷰를 보여주는 무거운 작업은 실제 클래스가 담당하게 합니다.  

![image](https://user-images.githubusercontent.com/78904413/176100062-e2684ab9-f09c-4343-a0a2-24681f9471a0.png)

```java
// 먼저 인터페이스를 둡니다.
interface Thumbnail {
  public void showTitle {};
  public void showPreview {};  
}

// 실제 동영상을 재생하는 역을 하는 클래스
class RealThumbnail implements Thumbnail {
  private String tile;
  private String movieUrl;
  
  public RealThumbnail(String _title, Stirng _movieUrl) {
    title = _title;
    movieUrl = _movieUrl;
    
    // URL로부터 영상을 다운받는 작업(시간소모)
    System.out.println("영상 다운");
  }
  
  // 제목을 보여주는 메소드뿐만아니라
  public void showTitle(){
    System.out.println("제목");
  }
  
  // 프리뷰를 재생하는 메소드도 갖고 있습니다.
  public void showPreview(){
    System.out.println("프리뷰 재생");
  }
}

// 영상을 가져오지 않기때문에 가벼운 객체입니다.
class ProxyThumbnail impl...{
  private Stirng title;
  private String movieUrl;
  
  private RealThumbnail realThumbnail;
  
  public ProxyThumbnail(String _title, Stirng _movieUrl){
    title = _title;
    movieUrl = _movieUrl;
  }
  
  public void showTitle(){
    ...
  }
  
  // 구현체이므로 메소드를 갖고는 잇지만 직접 실행하지 않습니다.
  public void showPreview(){
    if(realThumbnail == null){
      realThumbnaiil = new RealThumbnail(title, moiveUrl);
    }
    realThumbnail.showPreview();
  }
}
```
![image](https://user-images.githubusercontent.com/78904413/176105946-a9945648-6f18-4013-b335-2ef170ea82bb.png)


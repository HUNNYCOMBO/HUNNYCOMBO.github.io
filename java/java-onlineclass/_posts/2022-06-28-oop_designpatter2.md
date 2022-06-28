---
title: 객체지향 디자인패턴 part 2
excerpt: 얄팍한 코딩사전 유튜브 강의 - 객체지향 디자인패턴 2입니다.
tags: [design_pattern]
---

## 1. template-method
템플릿 메소드 패턴이란 어떤 같은 형식을 지닌 특정 작업들의 세부 방식을 다양화하고자 할 때 사용하는 패턴입니다.  

![image](https://user-images.githubusercontent.com/78904413/176171867-29e4e14a-d39b-43c8-8f66-7a1aaa384767.png)

예를들면 위의 색 조합 처럼 어떻게 조합하느냐에 따라 새로운 결과가 나오는 경우입니다. 전략패턴에서는 위 색들을 갈아끼울 수 있는 모듈로 만들었다면, 
템플릿 메소드 패턴은 다양화된 방식을 각각 자식 클래스에서 오버라이딩하는 방식으로 구현하는 것입니다. 이는 단순한 상속이 아닌 일정한 형식이 있습니다.  

부모 클래스에서 전반 과정을 수행하는 메인 메소드가 있고, 자식 클래스에 세부기능을 하는 메소드가 있습니다. 메인 메소드를 호출하면 실행주에 세부 메소드들이 호출되는 형태입니다. 
자식 과자에서는 그 세부메소드들을 오버라이딩하는 것입니다.  
부모클래스에서 색을 빨강,파랑,초록으로 정해놨다면 이것은 자식 클래스가 바꿀수는 없지만, 자식 클레스에서 자기만의 방식으로 구현해서 다양한 조합을 구현할 수 있는 것입니다.  

![image](https://user-images.githubusercontent.com/78904413/176172817-f15c851c-75ff-4091-b639-dcb8c6a8aa58.png)

템플릿 메소드의 핵심은 전반적인 과정에 공통되는 부분이 있을 때 코드를 효율적으로 짜기 위해 만들어진 패턴입니다. 보통 공통되는 부분을 템플릿으로 두고 변경되는 부분을 콜백형태의 익명클래스로 사용하는 경우가 많습니다.  

## 2.decorator
특정 클래스의 객체들이 할 수 있는 기능을 여러가지 두고 각 객체마다 사용자가 원하는대로 골라서 시키거나 기능들을 필요에 따라 장착할 수 있게 할 때 데코레이션 패턴이 사용됩니다.  
슈팅게임을 할 때 전투기가 아이템을 먹을 때 마다 공격기능이 추가되는 것이 예시입니다.  

```java
public inteface Fighter{
  public void attack(); // 공격버튼을 누르면 실행되는 메소드
}

// 구현 클래스
public class XwingFighter impl Fighter{
  public void attack(){...} // 기본적으로 탄환을 발사
}

// 공격 추가기능 클래스
public abstract class FighterDecorator impl Fighter{
  private Fighter fighter;
  
  public 생성자..(Fighter ,,,) {fighter = _fighter}
  
  // 스스로 뭘 하는것이아닌 필드의 fighter의 attack메소드를 실행합니다.
  @Override
  public void attack(){fighter.attack();}
  
  public class weapon1 extends FighterDecorator{
   public weapon1(Fighter _fighter){super(_fighter);}
   
   @Override
   public void attack(){
    super.attack();
    System.out.println("레이저발사");
   }
  }
}
```
![image](https://user-images.githubusercontent.com/78904413/176176823-0921670c-2b6a-4d82-9118-1ba41383c97d.png)

위와같은 방식으로 감싸는 방식, 객체가 생성자 변수로 다른 객체 안에 들어감으로서 그 시행하는 메소드의 행동이 추가되도록 하는 것이 데코레이터 패턴입니다.  

## 3. Factory method
팩토리 메소드 패턴은 대표적으로 객체를 생성하는 일을 팩토리 클래스에 위임함으로서 관심사를 분리하는 것입니다. 이는 DI의 대표원리입니다.  
위의 데코레이터 패턴에 팩토리 메소드패턴을 적용하면 관심사가 분리되어 더 깔끔한 코드를 짤 수 있습니다.  
![image](https://user-images.githubusercontent.com/78904413/176177752-9480715d-84ec-458e-87c4-c236951d5c34.png)

## 4. mediator
어떤 클래스의 객체에서 특정 이벤트가 발생할 때마다, 연결된 다른 클래스들에 알려야하는 경우가 있습니다. 여러 클래스들의 관계가 특정 이벤트를 중심으로 복잡하게 얽힌 설계에서 유용하게 사용됩니다.  

## 5. composite
컴포짓 패턴을 쉽게 이해하려면, 컴퓨터의 폴더 시스템을 떠올리면됩니다. 폴더에는 파일도 들어갈 수 있지만, 폴더도 들어갈 수 있습니다. 파일과 폴더는 다른 종류지만, 이름바꾸기나 삭제등 동일한 동작을 합니다. 포함하는 것들과 포함되는 것들이 
같은 방식으로 다뤄질 수 있도록 할 때, compsite패턴이 사용됩니다.  





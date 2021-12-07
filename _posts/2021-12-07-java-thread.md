---
layout: single
title:  "Thread"
categories: java
tags: [java, string, thread]
toc: true
author_profile: false
sidebar:
    nav: "docs"
search: true

---

## Thread

### 1. program , process, thread

프로그램 : 디스크 상에 저장되어 있지만 메모리에는 올라오지 않은 상태.  

프로세스 : 실행하여 **운영체제로 부터 할당받은 메모리**에 올라간 상태.   

스레드 : 프로세스의 **코드**에 정의된 절차에 따라 실행되는 특수한 경로.(jvm에 의해 관리)  

cpu의 입장에서 봤을 때 스레드가 최소작업단위가 되고,   

운영체제의 입장에서 봤을 때 프로세스가 최소작업단위가 됩니다.  

프로세스는 **프로세스 마다** 독립된(타 프로세스 접근불가) 메모리영역을,  

**code/data/stack/heap** 의 형식으로 할당합니다.  

스레드는 프로세스의 메모리영역 안에서 stack만 따로 할당받고,  

나머지(code/data/stack/heap)는 공유합니다.   

stack만 변경을 진행하기 때문에 __context-switching__ 비용이 적어서 응답시간이 빠릅니다.  

이 **공유자원** 때문에 스레드에 오류가 발생하면 다른 스레드들도 종료됩니다.  

> context-switching이란?
> 
> 현재 진행중인 task(프로세스, 스레드)의 상태를 저장하고 다음task의 상태를 읽고 적용하는 과정. 실제로 동시에 처리되는 것이 아니라 그렇게 보이게 함.

### 2. thread의 상태

- 객체 생성(new) : start()를 실행하지 않은 상태.

- 실행대기(runnable) : 스캐줄러에 의해 대기 중인 상태.

- 실행(running) : run()을 실행한 상태. 작업을 완료하지 않아도 __스캐줄러에 의해 대기상태로 돌아갈 수 있습니다.__

- 종료(terminated) : run()을 모두 수행하고 종료한 상태.

- 일시정지
  
  - waiting : 다른 스레드가 wait()를 호출하여 일시정지 된 상태. wait()을 호출한 스레드가 notify(), notifyAll()을 호출하면 실행대기상태로 돌아갑니다.
  
  - timed_waiting : sleep(n)에 의해 일정시간이 지나면 실행대기(runnable)상태로 돌아갑니다.
  
  - blocked : 동기화(synchronized)를 통해 자동으로 정지된 상태. 정지의 원인이 사라지면 실행대기상태로 돌아갑니다.

> 참고) process의 상태 : create, ready, running, waiting, terminated.

### 3. thread의 선언

#### 3-1. 직접 상속받아 스레드를 생성

Thread 클래스로 부터 제공되는 run 메소드를 오버라이딩(재정의)해서 사용합니다.

```java
class ThreadTest extends Thread{
    public void run(){
        //overidding합니다.
    }
}


class ThreadRun{
    public statick void main(String args[]){
    ThreadTest t1 = new ThreadTest();
    ThreadTest t2 = new ThreadTest();

    t1.();
    t2.run();
    }
}
```

#### 3-2. 함수형인터페이스 Runnable을 구현해서 생성

현재의 클래스가 이미 다른 클래스로부터 상속받고 있다면 Runnable 인터페이스를 이용하여 스레드를 생성할 수 있습니다.

run()에는 실행할 코드만 담고, Runnable을 구현한 클래스를 Thread 클래스의 생성자 파라미터로 넘겨서 __start()__ 로 실행합니다.

```java
class RunnableTest implements Runnable{
    public void run(){
    //재정의 합니다.
    }
}


class RunnableRun{
    public static void main(String args[]){
    RunnableTest r = new RunnableTest();

    //Thread 클래스의 생성자 파라미터로 넘깁니다.
    Thread t = new Thread(r);
    t.start();
    }
}
```

### 4. Daemon Thread

__동일한 프로세스__ 안에서 다른 스레드의 수행을 돕는(서비스) 스레드로, 다른 스레드가 모두 종료되면 자신도 종료되는 스레드입니다.  

프로그램이 종료되는 것을 막지 않습니다.  

GC(가비지 컬렉터), 메인 스레드가 데몬 스레드 입니다.  

start()를 호출하기 전에 setDaemon(true)를 이용하여 설정합니다.  

### 5. Thread pool

제한 된 개수의 스레드를 JVM이 관리합니다. 스레드가 완료된 후 반환되면 재사용합니다.  
스레드풀은 다수의 사용자요청에서 성능저하방지를 위해 사용하며, Executors 클래스, Executor Service 인터페이스로 사용합니다.  

#### 5-1. thread pool 생성

```java
   ExecutorService es1 = new Exceutors.newcachedTrheadPool();
   // 초기 코어스레드 수 : 0, 최대 스래드 수 : int의 최대        
   ExecutorService es2 = new Executors.newfixedTrheadPool();
```

- 작업 생성 : 하나의 작업단위는 Runnable 혹은 Callable을 구현한 클래스입니다.
  
  - Runnable : 작업 완료 후 return 값이 없습니다.
  
  - Callable : 작업 완료 후 return 값이 존재합니다.

- 작업 처리요청 : ExecutorService의 작업 Que에 작업 객체를 넣습니다.
  
  - execute() : Runnable 객체를 작업 Que에 저장합니다. 예외 발생시 스레드를 종료.제거 후 스레드풀을 생성합니다.(스레드 생성 오버헤드 가능성 높음)
  
  - submit() : Runnable 혹은 Callable 을 작업 Que에 저장하고 Future 객체를 return합니다. 예외 발생시 스레드풀을 재사용합니다.

- 스레드 풀 종료 : 스레드풀의 스레드는 메인 스레드가 종료되도 실행대기상태 입니다. (재활용)
  
  - shutdown() : 스레드풀의 스레드를 종료시킵니다.
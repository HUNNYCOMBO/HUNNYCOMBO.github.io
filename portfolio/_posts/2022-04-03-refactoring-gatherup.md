---
title:  "프로젝트 리팩토링 - gather up"
excerpt: "모임관리 웹사이트(백기선님 강의 참고)"
---

## 링크
+ [참조한 백기선님 온라인강의](https://www.inflearn.com/course/%EC%8A%A4%ED%94%84%EB%A7%81-JPA-%EC%9B%B9%EC%95%B1/dashboard)
+ [프로젝트 github](https://github.com/hunnycombo/lazir)


## 1. layered architecture에 기반한 설계로 전환
**패키지 재설계**
- config : 유지
- controller : presentation 패키지로 이동
- domain : jpa로 이루어져잇으므로 엔티티로서 하는 역할과 순수 자바로 이루어진 비즈니스 로직이 합쳐진 . repository와 service의 객체들을 해당 도메인 별로 구분
- form : dto객체로 재탄생.
- repository : domain영역으로 편집
- service : 비즈니스 로직에서 순수 자바로직으로 이루어지지 않는 영역(DI가 필요한부분)을 따로 분리한 클래스
- validator : presetation 패키지로 이동
- dto : 기존에 domain객체를 컨트롤러(프레젠테이션 영역)에서 그대로 사용하여 역참조가 일어났으므로, dto객체를 추가
- application : 애플리케이션 패키지를 추가, 비즈니스로직들을 호출하여usecase를 묶는 역할을 하는 패키지.
- infrastructure : 인프라스트럭쳐 패키지를 추가


## 2. RESTAPI로 재설계(JSON 응답)

기존의 AccountController클래스의 signUpSubmit메소드를 살펴보면 modelAttribute로 thymeleaf와 대응되는 Form객체를 그대로 리턴했습니다.(thymeleaf에선 객체의 필드를 그대로 사용)  
RESTAPI로 재설계하기 위해 **JSON으로 응답**하게 변경합니다.  
Controller어노테이션을 RestController로 변경하고, PostMapping 메소드들의 리턴을 변경합니다.  
파라미터로 modelAttribute로 AccoutForm객체를 받고있었는데, RequestBody 어노테이션으로 json으로 요청하도록 변경합니다.  
리턴타입은 String으로 뷰페이지를 리턴하던 방식에서 객체를 리턴하도록 정의합니다.  

ModelAttribute는 파라미터로 들어온 DTO객체에 바인딩하는 방식으로 setter 메소드가 반드시 있어야합니다.  
RequestBody는 HttpMessageConverter를 거쳐 DTO객체에 맞는 타입으로 바꿔서 바인딩 시켜줍니다.  
initbinder어노테이션(validater) 역시 수정해줍니다.

+ [modelAttribute와 RequestBody의 차이](https://tecoble.techcourse.co.kr/post/2021-05-11-requestbody-modelattribute/)

```java

// 원문
@Controller
...
public class AccountController {

   @InitBinder("accountForm")  //AccountForm요청이 들어올때 binder를 거치게된다.
   public void initBinderAccount(WebDataBinder webDataBinder){
       webDataBinder.addValidators(AccountValidator);
   }
  ...
  
   @PostMapping("/sign-up")
    public String signUpSubmit(@ModelAttribute @Valid AccountForm accountForm, Errors errors) {
        if(errors.hasErrors()){
            return "account/sign-up";
        }

        Account account = accountService.checkEmail(accountForm);
        accountService.login(account);  //회원가입 후 자동 로그인
        return "redirect:/";
    }
  
  
}

// 리팩토링

  @RestController
  ...
  public class AccountController {
     @PostMapping("/sign-up")
    public SingUpResponse signUpSubmit(@RequestBody @Valid SingUpRequest accountForm, Errors errors) {
        if(errors.hasErrors()){
            return new SingUpResponse();
        }

      
        return new SingUpResponse();
    }
  }
```

## service에서 프레젠테이션 영역의 form객체가 역참조 되는 부분 수정
기존 accountService의 checkEmail()를 살펴보면 파라미터로 form객체를 받고있습니다.  
이는 layered architecture 구조에서 보면 역참조가 일어나는 상황으로, dto객체를 참조하도록 변경합니다.  
추가적으로 메소드이름이 직관적이지 않으므로 리턴이 없는 signUp()로 변경합니다.  

```java
  @Transactional
  public Account checkEmail(AccountForm accountForm) {
      Account newAccount = createNewAccount(accountForm);
      sendSignUpEmail(newAccount);
      
      return newAccount;
    }
```


## DTO 설계
+ [참고 링크](https://velog.io/@p4rksh/Spring-Boot%EC%97%90%EC%84%9C-%EA%B9%94%EB%81%94%ED%95%98%EA%B2%8C-DTO-%EA%B4%80%EB%A6%AC%ED%95%98%EA%B8%B0)
- login service를 account 엔티티를 사용하던 것에서 login dto를 사용하도록 수정.




<details>
   <summary>미완</summary>
-
usecase - 구매
product domain 으로 상품을 조회하고, 없으면 예외처리를하고, 재고관련 domain, member, payment domain등을 활용하여 하나의 usecase로 묶어서 어플리케이션 레이어에서 처리.
? 하나의 domain을 사용하는 경우? -> domain을 직접 호출하는 경우도, 어플리케이션을 거치는 경우도 있음.(team by team)
모든 참조는 단방향으로 이루어져야한다는 규칙.
-

? querydsl
responsebody json 로 리턴하도록 
시리얼라이즈

--
1. 4개의 영역으로 나누기

컨트롤러 - 뷰 리턴할 때 restAPI  - JSON으로 리턴하게 해서 -> controller 어노테이션을 restcontroller로 반환
호출됐을때 넘어온 객체들을 validator로 검증하게끔 수정.

request - 시리얼라이즈 / response - 디시리얼라이즈

? account 도메인 객체를 그대로 리턴하지않는 이유 - > doamin 객체와 response, request객체와 분리해서 사용- >  domain에 어울리지않는 필드를 추가해야하는 경우가 생김
accountservice가 form을 참조하게되면 역방향 참조가일어나게 되므로,  프레젠테이션이나 어플리케이션에서 변환을해서 넘겨주 게된다.

변경한 부분 1.
public Account duplicatedEmail(Account account) { 이름변경

2. checkEmail(account.getEmail());  account가 아닌 email만 넘겨줘도된다.

--
? 트렌젝션 read only mysql의 트랜잭션 속성이나 rdbms 트랜잭션의 특징 ? <- 따로 공부. 트랜잭션 acid

? 트랜잭션 isolation 레벨

? mysql 스토리지엔진 이노db엔진. isolatioin 정책 레벨

db의 index를 왜쓰는지? . mysql의 index는 hash가 tree구조. 왜? 범위의 데이터를 찾는 경우 때문에. tree

모든 컬럼에 대해 index를 생성해야 하는지? index의 장단점.

? 커버링 index

? mysql 실행계획 explain

? 스프링 transation 주의할점 어떻게 동작하는지 - AOP 프록시
                                                      
 ## 도와주신분
 ben
                                                      
</details>

---
title:  "프로젝트 리팩토링 - gather up"
excerpt: "모임관리 웹사이트(백기선님 강의 참고)"
tags: [리팩토링, gather up]
---

## 링크
+ [참조한 백기선님 온라인강의](https://www.inflearn.com/course/%EC%8A%A4%ED%94%84%EB%A7%81-JPA-%EC%9B%B9%EC%95%B1/dashboard)
+ [프로젝트 github](https://github.com/hunnycombo/lazir)


## layered architecture에 기반한 설계로 전환
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


## RESTAPI로 재설계()

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

## DTO 재설계와 애매했던 메소드 이름 
+ [참고 링크](https://velog.io/@p4rksh/Spring-Boot%EC%97%90%EC%84%9C-%EA%B9%94%EB%81%94%ED%95%98%EA%B2%8C-DTO-%EA%B4%80%EB%A6%AC%ED%95%98%EA%B8%B0)
- login service를 account 엔티티를 사용하던 것에서 login dto를 사용하도록 수정.


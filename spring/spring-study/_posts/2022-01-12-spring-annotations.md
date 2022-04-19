---
title:  "스프링의 어노테이션"
excerpt: "스프링에서 자주 사용되는 어노테이션에 대해 알아봅니다."
tags: [어노테이션]
---

## @SpringBootApplication

스프링 부트의 설정정보, Bean 관리를 자동으로 설정하게 합니다.
해당 어노테이션이 등록된 클래스의 위치부터 설정을 읽어가기 때문에 이 클래스는 항상 프로젝트의 최상단에 위치해야 합니다.  

SpringApplication.run()으로 내장 WAS를 실행하므로 톰캣같은 별도의 WAS를 설치하지 않아도 됩니다. SpringBoot는 **언제 어디서나 같은 환경에서 스프링 부트를 배포**할 수 있는 내장 WAS를 권장합니다. 

## @RestController

기본적으로 @Controller에 @ResponseBody가 결합된 어노테이션입니다. 컨트롤러 클레스에 @RestController를 붙이면 클래스의 메소드에 @ResponseBody를 붙이지 않아도 문자열이나 JSON 등을 전송할 수 있습니다.

## @ControllerAdvice

모든 컨트롤러의 적용 범위 내에서 이 어노테이션이 작동합니다. 일반적으로 예외를 핸들링 할 클래스를 만들고 어떻게 처리할지 정의한 클래스에 사용합니다.  
@RestControllerAdvice는 이 어노테이션과 @ResponseBody를 합친 역할을 합니다.  

## @Configuration, @Component
@Configuration은 여러개의 @Bean 메소드를 정의한다는 의미로 일종의 xml역할을 합니다. @Bean 어노테이션을 사용하는 클래스는 반드시 Configuration 어노테이션을 함께 사용해야 합니다. 그냥 @Bean만 사용하면 싱글톤을 보장하지 못합니다. @Configuration은 내부적으로 Component가 붙으므로 자체가 Bean으로 등록이 됩니다.  

Component 어노테이션은 직접 개발한 클래스를 Bean으로 등록하고자 하는 경우에 사용합니다. Component 어노테이션을 사용하면 ComponentScan 어노테이션으로 컴포넌트를 찾는 범위를 지정해주어야 합니다.

## @Controller, @Repository, @Service
세 어노테이션 모두 Component를 담고 있어 Bean으로 등록됩니다. 관점에 따라 분리하는 것은 AOP에 도움을 줍니다.

Controller : Web MVC코드에서 사용됩니다. 이 어노테이션이 등록되야 @RequestMapping을 사용할 수 있게됩니다.

Repository : DAO를 명시하기 위한 설정입니다. 엔티티와 일정 부분 겹칠 수 있습니다.

Service : 비즈니스 로직을 담당한다는 명시적 기능외엔 Component에서 추가 된 것은 없습니다.

## JPA 관련 어노테이션
@Entity : 클래스 위에 선언하여 이 클래스가 엔티티임을 알려줍니다. JPA에서 엔티티에 정의된 필드들을 바탕으로 데이터베이스에 테이블을 만듭니다.

@Builder : 해당 클래스에 해당하는 엔티티 객체를 만들 때 빌더 패턴을 이용해서 만들 수 있도록 지정해주는 어노테이션입니다. 이렇게 선언해놓으면 나중에 다른 곳에서 Board.builder(). {여러가지 필드의 초기값 선언 }. build() 형태로 객체를 만들 수 있습니다.

@AllArgsConstructor : 선언된 모든 필드를 파라미터로 갖는 생성자를 자동으로 만들어줍니다.
@NoArgsConstructor : 파라미터가 아예없는 기본생성자를 자동으로 만들어줍니다.

@Getter : 각 필드값을 조회할 수 있는 getter메소드를 자동으로 생성해줍니다.


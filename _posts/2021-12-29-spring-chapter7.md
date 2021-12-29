---
layout: single
title:  "토비의 스프링 vol.1 7장"
categories: spring
tags: [spring, 스프링 핵심 기술의 응용]
toc: true
author_profile: false
sidebar:
    nav: "docs"
search: true
---

## 스프링 핵심 기술의 응용
지금까지 스프링의 3대 기술인 IoC/DI, 서비스 추상화, AOP에 대해 간단히 살펴보았습니다. 이 기술들은 결국 객체지향 기술입니다. 7장에서는 세 가지 기술을 활용해서 새로운 기능을 만들어보고, 스프링의 추구하는가치를 살펴봅니다.  

### 1. SQL과 DAO의 분리
우리는 JDBC작업 흐름을 인터페이스와 템플릿으로 UserDao에서 분리해냈습니다. 트랜잭션과 예외처리 작업도 서비스 추상화와 AOP 등을 처리해서 분리했습니다. 조금더 욕심을내서 변하면서 DAO가 관심을 갖지 않는 부분인 SQL을 분리해 낼 수 있습니다.  

#### 1-1. XML 설정을 이용한 분리
간단하게 sql문을 userDao의 필드로 추가하고 xml설정을 이용해 DI받도록 설정할 수 있습니다. 메소드에 따라 SQL문이 점점 많아질 것이므로, SQL문을 하나로 모아두는 방식을 활용합니다. 필드를 map타입으로 선업합니다.

```java
// UserDaoJDBC 클래스
private map<String, String> sqlMap;

public void setSqlMap(Map<Stirng, String> sqlMap){
    this.sqlMap=sqlMap;
}

public void add(User user){
    this.jdbcTemplate.update(
        this.sqlMap.get("add"); // 키를 이용해서 필요한 SQL을 가져옵니다.
    )
}

// xml 설정
	<bean id="userDao" class="springbook.user.dao.UserDaoJdbc">
		<property name="dataSource" ref="dataSource" />
		<property name="sqlMap">
			<map>
				<entry key="add" value="insert into users(id, name, password, email, level, login, recommend) values(?,?,?,?,?,?,?)" />			
				<entry key="get" value="select * from users where id = ?" />
				<entry key="getAll" value="select * from users order by id" />
				<entry key="deleteAll" value="delete from users" />
				<entry key="getCount" value="select count(*) from users" />
				<entry key="update" value="update users set name = ?, password = ?, email = ?, level = ?, login = ?, recommend = ? where id = ?"  />
			</map>
		</property>
	</bean>
```

#### 1-2. SQL 제공 서비스
다만 애플리케이션 구성정보를 가진 xml에 SQL 문장을 두는것은 바람직 하지 못합니다. 싱글톤인 DAO 인스턴스 변수에 접근해서 내용을 수정하는 것도 어렵습니다. 그래서 독립적인 SQL 제공 서비스가 필요합니다.  

SQL 서비스의 인터페이스를 설명합니다. 늘 해왔던 인터페이스로 추상화하고 구현 클래스를 DI하는 것입니다. DAO는 어떤 키값으로 SQL 서비스를 이용할 것인지만 알면 됩니다.  

```java
public interface SqlService{
    String getSql(String key) throws SqlRetrievalFailureException;
    // 런타임 예외입니다.
}

// 구현 클래스입니다.
public class SImpleSqlService implements SqlService{
    private Map<String, String> sqlMap;

    public void setSql... // 세터 메소드

    @Override
    public String getSql(String key) throws ...{
        String sql = sqlMap.get(key);
        if (sql == null) throws new ...;
        else return sql;
    }
}

// UserDaoJDBC에 DI받을 수 있도록 SqlService 타입 필드를 추가합니다.
// UserDaoJDBC의 모든 메소드가 sqlService.getSql로 sql을 가져오도록 수정합니다.
public void add(User user) {
		this.jdbcTemplate.update(
				this.sqlService.getSql("userAdd"), 
					user.getId(), user.getName(), user.getPassword(), user.getEmail(), 
					user.getLevel().intValue(), user.getLogin(), user.getRecommend());
	}
...

// xml 설정입니다.
	<bean id="userDao" class="springbook.user.dao.UserDaoJdbc">
		<property name="dataSource" ref="dataSource" />
		<property name="sqlService" ref="sqlService" />
	</bean>
	
	<bean id="sqlService" class="springbook.user.sqlservice.SimpleSqlService">
		<property name="sqlMap">
			<map>
				<entry key="userAdd" value="insert into users(id, name, password, email, level, login, recommend) values(?,?,?,?,?,?,?)" />			
				<entry key="userGet" value="select * from users where id = ?" />
				<entry key="userGetAll" value="select * from users order by id" />
				<entry key="userDeleteAll" value="delete from users" />
				<entry key="userGetCount" value="select count(*) from users" />
				<entry key="userUpdate" value="update users set name = ?, password = ?, email = ?, level = ?, login = ?, recommend = ? where id = ?"  />
			</map>
		</property>
	</bean>
```

### 2. 인터페이스의 분리와 자기참조 빈
#### 2-1. XML 파일 매핑
여전히 xml파일에 sql문을 넣는 것은 좋은 방법이 아닙니다. SQL을 저장해두는 전용 포맷을 가진 독립적인 파일을 이용하는 편이 바람직합니다. 물론 독립적으로 만든 XML파일이 가장 편리한 포맷입니다. JAXB(Java Architecture for XML Binding)은 XML에 담긴 정보를 파일에서 읽어오는 간단한 방법입니다. DOM(문서 객체 모델, 문서 내의 요소를 정의하고 접근하는 방법을 제시)은 XML의 정보를 리플랙션 방식처럼 간접적으로 접근하지만, JAXB는 XML 정보를 오브젝트 처럼 직접 다룹니다. 또, 스키마를 이용해서 매핑할 오브젝트의 클래스까지 자동으로 만들어줍니다. 이때 매핑정보는 어노테이션으로 담겨있습니다.  
JAXB API 를 이용해 xml을 자바의 오브젝트로 변환하는 것을 unmarshalling(언마샬링)이라고 부릅니다. 반대는 마샬링 입니다. 자바 오브젝트를 바이트 스트림으로 바꾸는 것을 직렬화(serialization)이라 부르는 것과 비슷합니다.

```java
// 스키마입니다.
<schema xmlns="...w3.org/20001XMLSchema">
    ...
    <element name="sqlamp"> // <sqlmap> 앨리먼트를 정의합니다.
        <complexType>
            <sequence>
                <element name="sql" maxOccurs="unbounded" type="tns:sqlType" /> // unbounded : 필요한 개수만큼 <sql>을 포함할 수 있게 합니다
                ...

        <complexType name="sqlType">  // <sql>에 대한 정의 입니다.
            <simpleContent>
                <extension base="string">   //sql 문장을 넣을 타입입니다.
                    <attribute name="key" use="required" type="string" /> // <sql>의 key 애트리뷰트는 반드시 입력해야합니다. 값은 string입니다.
                ...

// sqlmap.xsd라는 이름으로 프로젝트 루트에 저장하고 JAXB 컴파일러로 컴파일 합니다.
// 터미널
xjc -p springbook.user.sqlservice.jaxb sqlmap.xsd -d src
// 생성할 클래스의 패키지 주소 / 변환할 스키마 파일 / 생성된 파일이 저장될 위치로 src로 지정

// 이후 컴파일러가 만들어준 xml 바인딩용 클래스 SqlType.java 와 Sqlmap.java가 만들어집니다.

// SqlType 은 필드로 value와 key를 가져 <sql>태그 한개당 오브젝트 하나가 만들어집니다.
//  Sqlmap클래스는 <sql>태그의 정보를 담은 SqlTpye 오브젝트를 리스트로 갖고있습니다.
```
JAXB의 작동방식은 아래와 같습니다.

[![](https://mermaid.ink/img/eyJjb2RlIjoiZ3JhcGggTFJcbiAgICBBW3htbCDsiqTtgqTrp4hdIC0tPiBCW-yKpO2CpOuniCDsu7TtjIzsnbzrn6xdXG4gICAgQiAtLT4gQ1t4bWwg7KCV67O066W8IOuwlOyduOuUqe2VnCDrp6TtlZHsmqkg7YG0656Y7IqkXVxuICAgIEMgLS0-fOywuOqzoHwgRFvslaDtlIzrpqzsvIDsnbTshZgvSkFYQiBBUEldXG4gICAgRVt4bWwg7YyM7J28XSAtLT4gRCAtLT587Ja466eI7IOs66eBfCBGW3htbCDrrLjshJzsoJXrs7Trpbwg64u07J2AIOyYpOu4jOygne2KuCDtirjrpqxdXG4gICAgRiAtLT4gRCAtLT5866eI7IOs66eBfCBFIiwibWVybWFpZCI6eyJ0aGVtZSI6ImRhcmsifSwidXBkYXRlRWRpdG9yIjpmYWxzZSwiYXV0b1N5bmMiOnRydWUsInVwZGF0ZURpYWdyYW0iOmZhbHNlfQ)](https://mermaid.live/edit#eyJjb2RlIjoiZ3JhcGggTFJcbiAgICBBW3htbCDsiqTtgqTrp4hdIC0tPiBCW-yKpO2CpOuniCDsu7TtjIzsnbzrn6xdXG4gICAgQiAtLT4gQ1t4bWwg7KCV67O066W8IOuwlOyduOuUqe2VnCDrp6TtlZHsmqkg7YG0656Y7IqkXVxuICAgIEMgLS0-fOywuOqzoHwgRFvslaDtlIzrpqzsvIDsnbTshZgvSkFYQiBBUEldXG4gICAgRVt4bWwg7YyM7J28XSAtLT4gRCAtLT587Ja466eI7IOs66eBfCBGW3htbCDrrLjshJzsoJXrs7Trpbwg64u07J2AIOyYpOu4jOygne2KuCDtirjrpqxdXG4gICAgRiAtLT4gRCAtLT5866eI7IOs66eBfCBFIiwibWVybWFpZCI6IntcbiAgXCJ0aGVtZVwiOiBcImRhcmtcIlxufSIsInVwZGF0ZUVkaXRvciI6ZmFsc2UsImF1dG9TeW5jIjp0cnVlLCJ1cGRhdGVEaWFncmFtIjpmYWxzZX0)

#### 2-2. xml 파일을 이용하는 SQL 서비스
이제 UserDaoJdbc에서 사용할 SQL이 담긴 xml 파일을 만들어봅니다. SQL은 DAO로직의 일부라고 볼 수 있으므로 DAO와 같은 패키지에 두도록 합니다. sqlmap.xml이라는 이름으로 UserDao와 같은 패키지에 둡니다.

```java
<?xml version="1.0" encoding="UTF-8"?>
<sqlmap xmlns="http://www.epril.com/sqlmap" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
	xsi:schemaLocation="http://www.epril.com/sqlmap http://www.epril.com/sqlmap/sqlmap.xsd ">
	<sql key="userAdd">insert into users(id, name, password, email, level, login, recommend) values(?,?,?,?,?,?,?)</sql>
	<sql key="userGet">select * from users where id = ?</sql>
	<sql key="userGetAll">select * from users order by id</sql>
	<sql key="userDeleteAll">delete from users</sql>
	<sql key="userGetCount">select count(*) from users</sql>
	<sql key="userUpdate">update users set name = ?, password = ?, email = ?, level = ?, login = ?, recommend = ? where id = ?</sql>
</sqlmap>
```

다음은 sqlmap.xml에 있는 sql을 갖와 DAO에 제공해주는 SqlService 인터페이스의 구현 클래스를 만듭니다. 언제 JAXB를 사용해 xml문서를 가져올 지를 생각해야 합니다.  
DAO가 매번 요청할 때마다 xml파일을 읽는 것은 비효율 적입니다. SqlService 빈은 스프링이 관리 할 것이므로 언제 어떻게 생성될지 알 수 없습니다. 우선은 간단히 생성자에서 SQL을 읽어와 맵으로 저장해서 요청에 따라 SQL을 전달하도록 만듭니다.  

```java
public class XmlSqlService implements SqlService {
	private Map<String, String> sqlMap = new HashMap<String, String>();
    // SQL들을 읽어와서 저장해둘 곳입니다.

	public void xmlSqlService() {
        // 생성자를 이용해 스프링이 오브젝트를 만드는 시점에서 SQL을 읽어오도록 합니다.
		String contextPath = Sqlmap.class.getPackage().getName(); 
        // 전에 스키마 컴파일러로 만들어둔 Sqlmap클래스를 이용합니다.
		try {
			JAXBContext context = JAXBContext.newInstance(contextPath);
            // JAXB API를 사용하기 위해 컨텍스트를 생성합니다.
			Unmarshaller unmarshaller = context.createUnmarshaller();
            // 언마샬러 생성
			InputStream is = UserDao.class.getResourceAsStream("sqlmap.xml");
            // userDao와 같은 경로의 sqlmap.xml 파일을 변환합니다.
			Sqlmap sqlmap = (Sqlmap)unmarshaller.unmarshal(is);
            // JAXB API를 이용해 XML 문서를 오브젝트 트리로 읽어옵니다.(언마샬)

			for(SqlType sql : sqlmap.getSql()) {
				sqlMap.put(sql.getKey(), sql.getValue());
			}
            // 읽어온 SQL을 맵으로 저장합니다.
		} catch (JAXBException e) {
			throw new RuntimeException(e);
		} 
	}

	public String getSql(String key) throws SqlRetrievalFailureException {
		String sql = sqlMap.get(key);
		if (sql == null)  
			throw new SqlRetrievalFailureException(key + "�� �̿��ؼ� SQL�� ã�� �� �����ϴ�");
		else
			return sql;
	}
}
// 빈설정
<bean id="sqlService" class="XmlSqlService 경로">
```

이제 SQL 문장을 스프링의 빈 설정에서도 완벽하게 분리했습니다. 필요하다면 SQL 문장을 정의한 xml 파일로 다른 툴에서 사용할 수 있습니다.  

#### 2-3. 빈의 초기화 작업
개선할 점은 여전히 있습니다. 우선 생성자에서 예외발생 가능성이있는 복잡한 초기화 작업을 다루는 것은 좋지 않습니다. 상속하기도 불편하고 보안에도 문제가 생깁니다.  
일단 초기 상태를 가진 오브젝트를 만들어놓고 별도의 초기화 메소드를 사용하는 방법이 바람직합니다. 또, 읽어들일 파일의 위치와 이름이 코드에 고정되게 됩니다. 바뀔 가능성이 있는 내용은 외부에서 DI로 설정해줄 수 있게 해야합니다.  

```java
public class XmlSqlService implements SqlService {
	private Map<String, String> sqlMap = new HashMap<String, String>();

	private String sqlmapFile;
    // 맵 파일을 외부에서 지정할 수 있도록 필드를 추가합니다.
    // xml 설정은 생략

	public void setSqlmapFile(String sqlmapFile) {
		this.sqlmapFile = sqlmapFile;
	}

    @PostConstruct  // 아래 설명 참조
	public void loadSql() { // 별도의 초기화 메소드입니다.
		String contextPath = Sqlmap.class.getPackage().getName(); 
		try {
			JAXBContext context = JAXBContext.newInstance(contextPath);
			Unmarshaller unmarshaller = context.createUnmarshaller();
			InputStream is = UserDao.class.getResourceAsStream(this.sqlmapFile);
            // DI 받은 파일 이름을 사용합니다.
			Sqlmap sqlmap = (Sqlmap)unmarshaller.unmarshal(is);
            ...
}
```

loadSql()이라는 초기화 메소드는 오브젝트를 만드는 시점에서 초기솨 메소드를 한 번 호출하면 됩니다. 문제는 빈 이므로 제어권이 스프링에게 있습니다. 생성은 물론 초기화도 스프링에게 맡길 수 밖에 없습니다. 그래서 스프링은 미리 지정한 초기화 메소드를 호출해주는 기능을 갖고 있습니다. 전에 사용했던 빈 후처리기 중에 어노테이션을 이용한 빈 설정을 지원해주는 빈 후처리기가 있습니다. context 스키마의 annotation-config 태그를 이용하면 편리합니다. context의 네임스페이스와 스키마를 지정해주면 어노테이션을 이용해서 부가적인 빈 설정 또는 초기화 작업을 도와주는 후처리기를 등록하게 됩니다.  
@PostConstruct를 이용하면 빈 오브젝트의 초기화 메소드로 지정합니다. 빈 오브젝트를 생성하고 DI작업을 마치고 초기화 작업을 실행해 줍니다. **즉, 프로퍼티까지 모두 준비된 후에 실행된다는 것입니다.**  

#### 2-4. 변화를 위한 준비: 인터페이스 분리
xmlSqlService는 아직 확장할 영역이 많이 있습니다. 만약 xml대신 다른 포맷의 파일에서 SQL을 읽어오게 하려면 지금 구조에서는 완전히 뜯어 고쳐야합니다. 즉, SQL을 가져오는 방법이 고정되어 있습니다. 만약 HashMap이 아닌 다른 방식으로 저장해서 가져오려면 역시 새로 작성해야 합니다. 이는 단일 책임 원칙을 위반합니다. 그렇다고 아예 새로운 클래스를 만들면 상단 부분의 코드가 중복됩니다. 늘 그래왔듯 인터페이스와 DI를 이용합니다.

분리 가능한 관심사를 생각해봅니다.
1. SQL정보를 외부의 리소스로부터 읽어오는 것입니다.
2. 읽어온 SQL을 저장하고 호출할 때 제공하는 것입니다. 부가적인 책임으로 가져온 SQL을 수정하는 기능도 생각해 볼 수 있습니다.

이 두책임을 어떻게 조합할 것인지 생각해봅니다.
1. SqlService를 구현합니다.
2. DAO에 서비스를 제공해주는 오브젝트(userService)와 이 두가지 책임을 가진 오브젝트를 협력해서 동작하도록 합니다.


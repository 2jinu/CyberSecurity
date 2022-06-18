# Loose comparisons

PHP에서 "=="를 사용함으로써 의도하지 않게 프로그램이 진행될 수 있다.

# **INDEX**

**1. [Loose comparisons Table](#Loose-comparisons-Table)**

**2. [환경 구성](#환경-구성)**

**3. [로그인 인증 우회](#로그인-인증-우회)**

# **Loose comparisons Table**

|       | true  | false | 1     | 0     | -1    | "1"   | "0"   | "-1"  | null  | []    | "php" | ""    |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| true  | true  | false | true  | false | true  | true  | false | true  | false | false | true  | false |
| false | false | true  | false | true  | false | false | true  | false | true  | true  | false | true  |
| 1     | true  | false | true  | false | false | true  | false | false | false | false | false | false |
| 0     | false | true  | false | true  | false | false | true  | false | true  | false | false*| false*|
| -1    | true  | false | false | false | true  | false | false | true  | false | false | false | false |
| "1"   | true  | false | true  | false | false | true  | false | false | false | false | false | false |
| "0"   | false | true  | false | true  | false | false | true  | false | false | false | false | false |
| "-1"  | true  | false | false | false | true  | false | false | true  | false | false | false | false |
| null  | false | true  | false | true  | false | false | false | false | true  | true  | false | true  |
| []    | false | true  | false | false | false | false | false | false | true  | true  | false | false |
| "php" | true  | false | false | false*| false | false | false | false | false | false | true  | false |
| ""    | false | true  | false | false*| false | false | false | false | true  | false | false | true  |

    * PHP 8.0.0 이전은 true

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

"=="를 사용하여 인증에 취약한 페이지를 생성하자.

```php
<?php
	if (isset($_GET['userid']) && isset($_GET['password'])) {
		$conn = mysqli_connect("localhost", "root", "root", "test");
		if (!$conn) die("mysql connect error : ".mysqli_connect_error($conn));
        $sql = "SELECT id, pw FROM user WHERE id='".$_GET['userid']."'";
		$result = mysqli_query($conn, $sql);
		$row = mysqli_fetch_array($result);
		if (strcmp($row['pw'],$_GET['password']) == 0) echo "Welcome ".$row['id'];
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

# **로그인 인증 우회**

Loose comparisions table을 보면 0과 false, 0, "0", null, 문자열, ""을 비교하면 true가 반환된다.

그렇다면 strcmp의 반환 값이 위의 값 중 하나이면 if문으로 들어가게 된다.

strcmp의 인자로 Array값을 넣으면 string과 비교할 때, 반환 값으로 null이다.

| data	| value	|
| :---	| :--- 	|
| ID	| admin |
| PW	| a     |
| URL	| http://192.168.0.58/index.php?userid=admin&password[]=a |

결과는 다음과 같다.

	Welcome admin
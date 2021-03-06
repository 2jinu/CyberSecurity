# 카이사르(시저) 암호 (Caesar Cipher)

기원전 44년 줄리어스 카이사르(Gaius Julius Caesar)가 사용한 암호는 평문의 각 알파벳을 일정한 거리만큼 밀어서 다른 알파벳으로 치환하는 암호

문자 집합(A-Z)에서 지정된 수(Shift)만큼 이동하여 나온 값이 암호화의 결과가 된다.

Shift가 Z를 넘어가면 다시 A부터 남은 수만큼 이동시킨다.

![](images/2022-07-12-12-00-51.png)

암호화와 반대로 지정된 수(Shift)만큼 거꾸로 이동하여 나온 값이 복호화의 결과가 된다.

Shift가 A를 넘어가면 다시 Z부터 남은 수만큼 이동시킨다.

![](images/2022-07-12-12-00-12.png)

시저 암호로 암호화된 값을 복호화해본다.

```py
class Caesar_Cipher:
    def __init__(self, shift : int = 0):
        self.shift      = shift
        self.digits     = '0123456789'
        self.uppercase  = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.lowercase  = 'abcdefghijklmnopqrstuvwxyz'

    def encrypt(self, data : str):
        assert data, '암호화할 데이터가 존재하지 않습니다.'
        assert len(data) > 0, '암호화할 데이터가 존재하지 않습니다.'
        result  = ''
        for d in data:
            if self.digits[0] <= d <= self.digits[-1]:
                result += self.digits[(self.digits.find(d) + (self.shift % len(self.digits))) % len(self.digits)]
            elif self.uppercase[0] <= d <= self.uppercase[-1]:
                result += self.uppercase[(self.uppercase.find(d) + (self.shift % len(self.uppercase))) % len(self.uppercase)]
            elif self.lowercase[0] <= d <= self.lowercase[-1]:
                result += self.lowercase[(self.lowercase.find(d) + (self.shift % len(self.lowercase))) % len(self.lowercase)]
            else: result += d
        return result

    def decrypt(self, data : str):
        assert data, '복호화할 데이터가 존재하지 않습니다.'
        assert len(data) > 0, '복호화할 데이터가 존재하지 않습니다.'
        result  = ''
        for d in data:
            if self.digits[0] <= d <= self.digits[-1]:
                result += self.digits[self.digits.find(d) - (self.shift % len(self.digits))]
            elif self.uppercase[0] <= d <= self.uppercase[-1]:
                result += self.uppercase[self.uppercase.find(d) - (self.shift % len(self.uppercase))]
            elif self.lowercase[0] <= d <= self.lowercase[-1]:
                result += self.lowercase[self.lowercase.find(d) - (self.shift % len(self.lowercase))]
            else: result += d
        return result

caesar  = Caesar_Cipher()
for i in range(26):
    caesar.shift = i
    print('[{}] {}'.format(i, caesar.decrypt(data='HFJ09w H6uM8W')))
```

Shift가 5일때, 사람이 읽을 수 있는 문자열이 나온다.

```sh
[0] HFJ09w H6uM8W
[1] GEI98v G5tL7V
[2] FDH87u F4sK6U
[3] ECG76t E3rJ5T
[4] DBF65s D2qI4S
[5] CAE54r C1pH3R
...
```
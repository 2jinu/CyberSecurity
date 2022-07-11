# **프로세스 메모리 정보**

플러그인 : memdump

mem이라는 폴더를 생성 후 의심스러운 실행파일의 PID를 통해 메모리 추출할 수 있다.

```
volatility_2.6_win64_standalone.exe -f cridex.vmem --profile=WinXPSP2x86 memdump -p 1640 -D mem
Volatility Foundation Volatility Framework 2.6
************************************************************************
Writing reader_sl.exe [  1640] to 1640.dmp
```

strings64.exe를 통해서 connections를 통해 확인한 IP를 확인할 수 있다.

```
strings64.exe -n 6 1640.dmp | findstr 41.168.5.140:8080
http://41.168.5.140:8080/zb/v_01_a/in/
Host: 41.168.5.140:8080
...
```
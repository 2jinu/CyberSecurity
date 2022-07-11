# **파일 덤프**

플러그인 : dumpfiles, procdump

files라는 폴더를 생성 후 의심스러운 실행파일의 오프셋을 통해 파일 추출해볼 수 있다.

```
volatility_2.6_win64_standalone.exe -f cridex.vmem --profile=WinXPSP2x86 dumpfiles -Q 0x00000000023ccf90 -D files -n
Volatility Foundation Volatility Framework 2.6
ImageSectionObject 0x023ccf90   None   \Device\HarddiskVolume1\Program Files\Adobe\Reader 9.0\Reader\reader_sl.exe
DataSectionObject 0x023ccf90   None   \Device\HarddiskVolume1\Program Files\Adobe\Reader 9.0\Reader\reader_sl.exe
```

혹은 PID를 통해서 프로세스를 추출할 수 있다. 해당 파일은 Windows Defender가 탐지하였다.

```
volatility_2.6_win64_standalone.exe -f cridex.vmem --profile=WinXPSP2x86 procdump -p 1640 -D files
Volatility Foundation Volatility Framework 2.6
Process(V) ImageBase  Name                 Result
---------- ---------- -------------------- ------
0x81e7bda0 0x00400000 reader_sl.exe        OK: executable.1640.exe
```
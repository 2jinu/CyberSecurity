# **명령행 정보**

플러그인 : cmdscan, consoles, cmdline

cmd.exe를 통해 입력한 명령들을 확인할 수 있다.

```
volatility_2.6_win64_standalone.exe -f cridex.vmem --profile=WinXPSP2x86 cmdscan
Volatility Foundation Volatility Framework 2.6
```

cmd.exe의 결과와 유사하지만, 명령어의 결과도 함께 확인할 수 있다.

```
volatility_2.6_win64_standalone.exe -f cridex.vmem --profile=WinXPSP2x86 consoles
Volatility Foundation Volatility Framework 2.6
```

프로세스의 명령행 인자를 확인할 수 있다.

```
volatility_2.6_win64_standalone.exe -f cridex.vmem --profile=WinXPSP2x86 cmdline
Volatility Foundation Volatility Framework 2.6
************************************************************************
System pid:      4
************************************************************************
smss.exe pid:    368
Command line : \SystemRoot\System32\smss.exe
************************************************************************
csrss.exe pid:    584
Command line : C:\WINDOWS\system32\csrss.exe ObjectDirectory=\Windows SharedSection=1024,3072,512 Windows=On SubSystemType=Windows ServerDll=basesrv,1 ServerDll=winsrv:UserServerDllInitialization,3 ServerDll=winsrv:ConServerDllInitialization,2 ProfileControl=Off MaxRequestThreads=16
************************************************************************
winlogon.exe pid:    608
Command line : winlogon.exe
************************************************************************
services.exe pid:    652
Command line : C:\WINDOWS\system32\services.exe
************************************************************************
lsass.exe pid:    664
Command line : C:\WINDOWS\system32\lsass.exe
************************************************************************
svchost.exe pid:    824
Command line : C:\WINDOWS\system32\svchost -k DcomLaunch
************************************************************************
svchost.exe pid:    908
Command line : C:\WINDOWS\system32\svchost -k rpcss
************************************************************************
svchost.exe pid:   1004
Command line : C:\WINDOWS\System32\svchost.exe -k netsvcs
************************************************************************
svchost.exe pid:   1056
Command line : C:\WINDOWS\system32\svchost.exe -k NetworkService
************************************************************************
svchost.exe pid:   1220
Command line : C:\WINDOWS\system32\svchost.exe -k LocalService
************************************************************************
explorer.exe pid:   1484
Command line : C:\WINDOWS\Explorer.EXE
************************************************************************
spoolsv.exe pid:   1512
Command line : C:\WINDOWS\system32\spoolsv.exe
************************************************************************
reader_sl.exe pid:   1640
Command line : "C:\Program Files\Adobe\Reader 9.0\Reader\Reader_sl.exe"
************************************************************************
alg.exe pid:    788
Command line : C:\WINDOWS\System32\alg.exe
************************************************************************
wuauclt.exe pid:   1136
Command line : "C:\WINDOWS\system32\wuauclt.exe" /RunStoreAsComServer Local\[3ec]SUSDSb81eb56fa3105543beb3109274ef8ec1
************************************************************************
wuauclt.exe pid:   1588
Command line : "C:\WINDOWS\system32\wuauclt.exe"
```
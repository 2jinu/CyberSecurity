# **파일 정보**

플러그인 : filescan

메모리상에서 열린 파일들을 확인할 수 있다.

```
volatility_2.6_win64_standalone.exe -f cridex.vmem --profile=WinXPSP2x86 filescan > filescan.txt
Volatility Foundation Volatility Framework 2.6
Offset(P)            #Ptr   #Hnd Access Name
------------------ ------ ------ ------ ----
0x0000000001fd4db8      2      1 ------ \Device\Afd\Endpoint
0x0000000001fd6268      1      0 -W-r-d \Device\HarddiskVolume1\WINDOWS\system32\wbem\Logs\wbemcore.log
0x0000000001fdb490      1      0 R--r-d \Device\HarddiskVolume1\WINDOWS\system32\netui0.dll
0x0000000001fdf730      1      0 R--rwd \Device\HarddiskVolume1\Documents and Settings\Robert\Start Menu\Programs\Accessories\desktop.ini
0x0000000001fdf978      1      0 R--rwd \Device\HarddiskVolume1\Documents and Settings\Robert\Start Menu\Programs\desktop.ini
0x0000000001fdfaa0      3      1 R--rwd \Device\HarddiskVolume1\Documents and Settings\Robert\Local Settings\Application Data\Microsoft\CD Burning
0x0000000001fe1220      1      0 R--rwd \Device\HarddiskVolume1\Documents and Settings\Robert\My Documents\My Pictures\Desktop.ini
0x0000000001fe2028      1      1 ------ \Device\NamedPipe\browser
0x0000000001fe2a58      1      0 RW-rwd \Device\HarddiskVolume1\Documents and Settings\LocalService\Local Settings\desktop.ini
0x0000000001fe2df8      1      1 RW---- \Device\HarddiskVolume1\Documents and Settings\LocalService\Local Settings\Application Data\Microsoft\Windows\UsrClass.dat.LOG
0x0000000001fe4028      1      1 RW-rw- \Device\HarddiskVolume1\WINDOWS\WindowsUpdate.log
0x0000000001fe40d8      1      1 RW-rw- \Device\HarddiskVolume1\WINDOWS\WindowsUpdate.log
...
```
# **운영체제 정보**

플러그인 : imageinfo

[Volatility 예제](https://github.com/volatilityfoundation/volatility/wiki/Memory-Samples) 중 Malware - Cridex파일을 다운받는다.

먼저 메모리파일을 통해 큰 정보를 알아내면 Windows XP라는 점을 예상할 수 있다.

```
volatility_2.6_win64_standalone.exe -f cridex.vmem imageinfo
Volatility Foundation Volatility Framework 2.6
INFO    : volatility.debug    : Determining profile based on KDBG search...
          Suggested Profile(s) : WinXPSP2x86, WinXPSP3x86 (Instantiated with WinXPSP2x86)
                     AS Layer1 : IA32PagedMemoryPae (Kernel AS)
                     AS Layer2 : FileAddressSpace (C:\Users\admin\Desktop\cridex\cridex.vmem)
                      PAE type : PAE
                           DTB : 0x2fe000L
                          KDBG : 0x80545ae0L
          Number of Processors : 1
     Image Type (Service Pack) : 3
                KPCR for CPU 0 : 0xffdff000L
             KUSER_SHARED_DATA : 0xffdf0000L
           Image date and time : 2012-07-22 02:45:08 UTC+0000
     Image local date and time : 2012-07-21 22:45:08 -0400
```
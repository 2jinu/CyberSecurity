# 시스템 정보

경로 : HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion

| 값                                        | 설명  |
| :---                                      | :---  |
| CurrentBuild<br>CurrentBuildNumber        | 운영체제 세부 버전 |
| InstallDate<br>InstallTime                | 운영체제 설치 시간 |
| ProductId                                 | 운영체제 식별자 |
| ProductName                               | 운영체제 이름 |
| RegisteredOrganization<br>RegisteredOwner | 조직 이름<br>사용자 이름 |
| ReleaseId                                 | 운영체제 버전 |
| SystemRoot                                | 운영체제 설치 경로 |

## **CurrentBuild(Number)**

운영체제의 세부 버전을 나타낸다.

![](images/2022-07-10-19-19-22.png)

## **InstallDate/InstallTime**

운영체제의 설치 시간을 나타낸다.

![](images/2022-07-10-19-23-00.png)

데이터는 Unix 시간 형식을 가지고 있으며 DCode로 변환하여 운영 체제의 설치 시간을 확인할 수 있다.

![](images/2022-07-10-19-24-57.png)

InstallTime도 마찬가지로 DCode를 이용하여 시간을 구할 수 있다.

![](images/2022-07-10-19-30-07.png)

## **ProductId**

제품 ID를 나타낸다.

![](images/2022-07-10-20-24-49.png)

## **ProductName**

운영체제 이름을 나타낸다.

![](images/2022-07-10-20-26-06.png)

## **RegisteredOrganization/RegisteredOwner**

등록된 조직과 사용자를 나타낸다.

![](images/2022-07-10-20-27-52.png)

## **ReleaseId**

운영체제 버전을 나타낸다.

![](images/2022-07-10-20-30-23.png)

## **SystemRoot**

운영체제 경로를 나타낸다.

![](images/2022-07-10-20-32-45.png)
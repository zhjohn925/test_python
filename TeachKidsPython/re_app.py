import urllib.request
from re import findall
 
url = "<a href="http://www.summet.com/dmsi/html/codesamples/addresses.html">http://www.summet.com/dmsi/html/codesamples/addresses.html</a>"
 
response = urllib.request.urlopen(url)
 
html = response.read()
 
htmlStr = html.decode()
 
pdata = findall("(d{3}) d{3}-d{4}", htmlStr)
 
for item in pdata:
    print(item)

import urllib.request

import requests

url = 'https://www.cnblogs.com/to-creat/p/6438280.html'
# url = 'http://www.iachina.cn/IC/tkk/03/e00a7099-23bd-450d-b3dd-e83118becb8f_TERMS.PDF'
#
# r = requests.get(url)
# with open('1.pdf','wb') as f:
#     f.write(r.content)

# r = requests.get(url="http://www.iachina.cn/IC/tkk/03/f9f76aec-8c6e-42e1-a500-cea25e9b88aa_TERMS.PDF", stream=True)
# with open('test.pdf', 'wb') as fd:
#     for chunk in r.iter_content(500):
#         fd.write(chunk)

# url = 'http://www.iachina.cn/IC/tkk/03/e00a7099-23bd-450d-b3dd-e83118becb8f_TERMS.PDF'
# print ("downloading with urllib")
# urllib.request.urlretrieve(url, "code1.pdf")

print ("downloading with urllib2")
f = urllib.request.urlopen(url)
data = f.read()
with open("code2.html", "wb") as code:
    code.write(data)
import requests
import re
from lxml import etree

headers = {
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36"
}
url1 = "http://www.mingchaonaxieshier.com/"
page1 = requests.get(url1, headers=headers)

urls = re.findall('<td><a href="(.*?)">.*?</a></td>', page1.text)
idx = 0
line_limit = 50
with open("mcnxs.txt", 'w') as f:
    for url2 in urls:
	idx += 1
	print(url2, "第"+str(idx)+"章")
	page2 = requests.get(url2, headers=headers)
	html = etree.HTML(page2.content)
	title = html.xpath('/html/body/div[3]/h1')[0].text
	contents = html.xpath('/html/body/div[3]/div[2]/p')
	print('  ' * ((line_limit - len(title)) // 2) + title, file=f)

	for i in range(len(contents) - 1):
   	    line = contents[i].text
	    length = len(line)
	    for j in range(length // line_limit):
		print(line[(j*line_limit):(line_limit+j*line_limit)], file=f)
	    print(line[length // line_limit * line_limit:] + '\n', file=f)


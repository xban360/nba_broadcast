import sys
from web_spider.web_spider import WebSpider

webSpider = WebSpider()
if len(sys.argv) < 2:
    webSpider.helper()
else:
    print(webSpider.grep(sys.argv[1]))
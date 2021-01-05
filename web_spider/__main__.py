import sys
from web_spider.web_spider import WebSpider

if __name__ == "__main__":
    webSpider = WebSpider()
    if len(sys.argv) < 2:
        webSpider.helper()
    elif len(sys.argv) == 2:
        data = webSpider.grep(sys.argv[1])
        print(data)
    else:
        data = webSpider.grep(sys.argv[1], [sys.argv[2]])
        print(data)
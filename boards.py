import requests as req
from bs4 import BeautifulSoup

class getBoards():
    def urlRequest(self, url):
        # add headers to prevent 403
        # add cookies for enter the board which has age verification
        request = req.get(
            url = url,
            cookies = {'over18': '1'},
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36'}
        )

        if 200 != request.status_code:
            raise IOError
        else:
            request.encoding = 'utf8'
            data = BeautifulSoup(request.text, 'html.parser')

            return data

    def getBoards(self):
        data = self.urlRequest('https://www.ptt.cc/bbs/index.html')

        boardNames = data.select('div.b-ent a div.board-name')
        boardClasses = data.select('div.b-ent a div.board-class')

        boards = {}
        for boardName, boardClass in zip(boardNames, boardClasses):
            if not boards.get(boardClass.text):
                boards[boardClass.text] = []

            boards[boardClass.text].append(boardName.text)

        return boards


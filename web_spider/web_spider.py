import requests as req
import json
from urllib.parse import urlparse, parse_qs, urlunparse
from bs4 import BeautifulSoup

class WebSpider:
    def __init__(self):
        pass

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

        return request.text

    def helper(self):
        print("Please input grep Option: ")
        print("NBA - grep NBA Score")
        print("PTT {Board} - grep PTT Board Content")

    def grep(self, option, extraInfo = []):
        if option == 'NBA':
            return self.grepNBA()
        elif option == 'PTT':
            return self.grepPTT(extraInfo)

    def formatter(self, string):
        count = 0
        for char in string:
            if 127 < ord(char):
                count += 1
        return count

    def grepNBA(self):
        url = 'https://tw.global.nba.com/stats2/scores/gamedaystatus.json?locale=zh_TW'
        data = json.loads(self.urlRequest(url))
        gameDates = data['payload']['gameDates']
        ret = []

        for gameDate in gameDates:
            for game in gameDate['games']:
                gameUrl = 'https://tw.global.nba.com/stats2/game/snapshot.json?countryCode=TW&gameId=' + game['gameId'] + '&locale=zh_TW'
                gameData = json.loads(self.urlRequest(gameUrl))

                homeScore = gameData['payload']['boxscore']['homeScore']
                awayScore = gameData['payload']['boxscore']['awayScore']

                homeTeam = gameData['payload']['homeTeam']['profile']['cityEn'] + ' ' + gameData['payload']['homeTeam']['profile']['nameEn']
                awayTeam = gameData['payload']['awayTeam']['profile']['cityEn'] + ' ' + gameData['payload']['awayTeam']['profile']['nameEn']
                status = gameData['payload']['boxscore']['status']
                statusDesc = ''

                if '1' == status:
                    statusDesc = gameData['payload']['gameProfile']['dateTimeEt']
                elif '2' == status:
                    statusDesc = 'Processing'
                elif '3' == status:
                    statusDesc = 'Finish'

                ret.append({
                    'homeTeam': homeTeam,
                    'homeScore': homeScore,
                    'awayTeam': awayTeam,
                    'awayScore': awayScore,
                    'status': statusDesc,
                })
        return ret

    def grepPTT(self, extraInfo = []):
        ret = []
        prefix = 'https://www.ptt.cc'
        board = ''
        if (len(extraInfo) < 1):
            return ret
        else:
            board = extraInfo[0]

        try:
            url = prefix + '/bbs/' + board + '/index.html'
            data = self.urlRequest(url)
            data = BeautifulSoup(data, 'html.parser')
            titles = data.select('div.title a')
            for title in titles:
                ret.append({
                    'title': title.text,
                    'href': prefix+title['href']
                })
        except:
            ret = []

        return ret

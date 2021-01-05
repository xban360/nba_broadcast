import urllib.request as req
import json
from urllib.parse import urlparse, parse_qs, urlunparse
from bs4 import BeautifulSoup

class WebSpider:
    def __init__(self):
        pass

    def helper(self):
        print("Please input grep Option: ")
        print("NBA - grep NBA Score")
        print("PTT {Board} - grep PTT Board Content")

    def grep(self, option, extraInfo = []):
        if option == 'NBA':
            return self.grepNBA()
        elif option == 'PTT':
            return self.grepPTT(extraInfo)


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
        board = ''
        if (len(extraInfo) < 1):
            return ret
        else:
            board = extraInfo[0]
        url = 'https://www.ptt.cc/bbs/'+board+'/index.html'
        data = self.urlRequest(url)
        data = BeautifulSoup(data, 'html.parser')

        titleList = []
        titles = data.select('div.title a')
        for title in titles:
            if title.text not in titleList:
                titleList.append(title.text)
                ret.append({
                    'title': title.text,
                    'href': 'https://www.ptt.cc/'+title['href']
                })
        return ret

    def urlRequest(self, url):
        # add headers to prevent 403
        request = req.Request(url, headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36'
        })
        with req.urlopen(request) as response:
            data = response.read().decode('utf-8')

        return data
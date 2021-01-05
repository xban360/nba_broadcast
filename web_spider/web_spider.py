import urllib.request as req
import json
from urllib.parse import urlparse, parse_qs, urlunparse

class WebSpider:
    def __init__(self):
        pass

    def helper(self):
        print("Please input grep Option: ")
        print("1 - grep NBA Score")
        print("2 - grep PTT NBA Content")

    def grep(self, option):
        if option == '1':
            return self.grepScore()

    def grepScore(self):
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

    def urlRequest(self, url):
        # add headers to prevent 403
        request = req.Request(url, headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36'
        })
        with req.urlopen(request) as response:
            data = response.read().decode('utf-8')

        return data
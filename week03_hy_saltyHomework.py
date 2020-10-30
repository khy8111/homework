import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbsparta

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

data = requests.get('https://www.genie.co.kr/chart/top200?ditc=D&rtm=N&ymd=20200713', headers=headers)
soup = BeautifulSoup(data.text, 'html.parser')

genies = soup.select('#body-content > div.newest-list > div > table > tbody > tr')

for genie in genies:
    rank = genie.select_one('td.number').text[0:2].strip()
    #text[0:2]첫번째에서 세번째까지 슬라이싱([0:1]로하면 숫자 앞자리만 나오고 숫자2이상부터는 정상적으로 나옴)
    #strip()양쪽 공백지우기 (안할경우 한자리 숫자들에 공백이 생김)
    #text[0:1000]정도 하니까 불필요한 공백과 문장 다시 나옴(이정도는 해야 문자열에 포함?..)
    title = genie.select_one('td.info > a.title.ellipsis').text.strip()
    #strip()으로 문자열 공백 제거
    artist = genie.select_one('td.info > a.artist.ellipsis').text

    data = {
        'rank' : rank,
        'title' : title,
        'artist' : artist
    }

    print(rank, title, artist)

    db.genies.insert_one(data)
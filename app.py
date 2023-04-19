import requests
import xml.etree.ElementTree as ET
from pushbullet import Pushbullet
from flask import Flask
import eventlet
import datetime
import pytz

app = Flask(__name__)

# Pushbullet API 토큰
API_KEY = "o.ZikrMCWd9dQjxjjPeOWxaIVSaYAc8fNQ"
pb = Pushbullet(API_KEY)

url = 'http://apis.data.go.kr/1613000/ArvlInfoInqireService/getSttnAcctoSpcifyRouteBusArvlPrearngeInfoList'
params = {'serviceKey': 'ukqZ12eX9yPldvymYtMVnBuISYTZXiAMzQR5LaQwQBabEjekysM/TdZMOiQ6hlujRAJbCFm/NJoCvkJ1t/sJnw==',
          '_type': 'xml',
          'pageNo': '1',
          'numOfRows': '3',
          'cityCode': '23',
          'nodeId': 'ICB166000480',
          'routeId': 'ICB165000026'}


@app.route('/')
def home():
    while True:
        utc_now = datetime.datetime.utcnow()
        seoul_tz = pytz.timezone('Asia/Seoul')
        seoul_now = utc_now.replace(tzinfo=pytz.utc).astimezone(seoul_tz)
        print(seoul_now)
        if seoul_now.hour == 16 and 22 < seoul_now.minute < 44:
            pass
        else:
            while seoul_now.hour == 16 and 22 < seoul_now.minute < 44:
                break

        arrprevstationcnt_list = []
        arrtime_list = []

        response = requests.get(url, params=params)
        root = ET.fromstring(response.content)

        for item in root.findall('.//item'):
            arrprevstationcnt = item.find('arrprevstationcnt').text
            arrtime = item.find('arrtime').text
            arrprevstationcnt_list.append(arrprevstationcnt)
            arrtime_list.append(arrtime)

        if len(arrtime_list) == 0:
            print('버스 없음')

        elif len(arrtime_list) == 1:
            minutes1, seconds1 = divmod(int(arrtime_list[0]), 60)

            print(f'{minutes1}분 {seconds1}초')

        elif len(arrtime_list) == 2:
            minutes1, seconds1 = divmod(int(arrtime_list[0]), 60)
            minutes2, seconds2 = divmod(int(arrtime_list[1]), 60)

            print(f'{minutes1}분 {seconds1}초 // {minutes2}분 {seconds2}초')

        eventlet.sleep(10)


if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('0.0.0.0', 5000)), app)

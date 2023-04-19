import requests
import xml.etree.ElementTree as ET
from time import localtime
from pushbullet import Pushbullet
from flask import Flask
import gevent

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


@app.before_first_request
def home():
    while True:
        tm = localtime()

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
            push = pb.push_note("Bus", '버스 없음')

        elif len(arrtime_list) == 1:
            minutes1, seconds1 = divmod(int(arrtime_list[0]), 60)

            push = pb.push_note("버스", f'{minutes1}분 {seconds1}초')

        elif len(arrtime_list) == 2:
            minutes1, seconds1 = divmod(int(arrtime_list[0]), 60)
            minutes2, seconds2 = divmod(int(arrtime_list[1]), 60)

            push = pb.push_note("버스", f'{minutes1}분 {seconds1}초 // {minutes2}분 {seconds2}초')

        if tm.tm_hour == 16 and 29 < tm.tm_min < 45:
            gevent.sleep(10)
            pushes = pb.get_pushes()

            filtered_push = []

            for push in pushes:
                if push['title'] == '버스':
                    filtered_push.append(push['iden'])

            for push in filtered_push:
                pb.delete_push(push)
        else:
            while tm.tm_hour == 16 and tm.tm_min == 20:
                push = pb.push_note('잘', '되는중')
                gevent.sleep(2)


if __name__ == '__main__':
    app.before_first_request(home)
    app.run()

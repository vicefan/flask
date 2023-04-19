from flask import Flask, render_template
import requests
import xml.etree.ElementTree as ET
import datetime
import pytz
import eventlet

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html', minutes1=0, seconds1=0)


@app.route('/bus')
def bus():
    url = 'http://ws.bus.go.kr/api/rest/arrive/getArrInfoByRouteAll'
    params = {
        'ServiceKey': '인증키 입력',
        'stId': '12345',  # 정류소 ID
        'busRouteId': '123456789',  # 버스 노선 ID
        'ord': '0'
    }

    while True:
        utc_now = datetime.datetime.utcnow()
        seoul_tz = pytz.timezone('Asia/Seoul')
        seoul_now = utc_now.replace(tzinfo=pytz.utc).astimezone(seoul_tz)

        if True: # seoul_now.hour == 16 and 22 < seoul_now.minute < 44
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
                minutes1, seconds1 = 0, 0
            elif len(arrtime_list) == 1:
                minutes1, seconds1 = divmod(int(arrtime_list[0]), 60)
                print(f'{minutes1}분 {seconds1}초')
            elif len(arrtime_list) == 2:
                minutes1, seconds1 = divmod(int(arrtime_list[0]), 60)
                minutes2, seconds2 = divmod(int(arrtime_list[1]), 60)
                print(f'{minutes1}분 {seconds1}초 // {minutes2}분 {seconds2}초')

            return render_template('home.html', minutes1=minutes1, seconds1=seconds1)

        eventlet.sleep(10)


if __name__ == '__main__':
    app.run(debug=True)
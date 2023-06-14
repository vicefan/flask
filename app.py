from flask import Flask, render_template
import requests
import xml.etree.ElementTree as ET
import datetime
import pytz
import eventlet

app = Flask(__name__)


@app.route('/')
def bus():
    global minutes1, seconds1
    url = 'http://apis.data.go.kr/1613000/ArvlInfoInqireService/getSttnAcctoSpcifyRouteBusArvlPrearngeInfoList'
    params = {'serviceKey': 'ukqZ12eX9yPldvymYtMVnBuISYTZXiAMzQR5LaQwQBabEjekysM/TdZMOiQ6hlujRAJbCFm/NJoCvkJ1t/sJnw==',
              '_type': 'xml',
              'pageNo': '1',
              'numOfRows': '3',
              'cityCode': '23',
              'nodeId': 'ICB166000480',
              'routeId': 'ICB165000026'}

    while True:
        utc_now = datetime.datetime.utcnow()
        seoul_tz = pytz.timezone('Asia/Seoul')
        seoul_now = utc_now.replace(tzinfo=pytz.utc).astimezone(seoul_tz)

        if True:  # seoul_now.hour == 16 and 22 < seoul_now.minute < 44
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
                minutes1, seconds1 = ('-', '-')
                minutes2, seconds2 = ('-', '-')

            elif len(arrtime_list) == 1:
                minutes1, seconds1 = divmod(int(arrtime_list[0]), 60)
                print(f'{minutes1}분 {seconds1}초')
                minutes2, seconds2 = ('-', '-')

            elif len(arrtime_list) == 2:
                minutes1, seconds1 = divmod(int(arrtime_list[0]), 60)
                minutes2, seconds2 = divmod(int(arrtime_list[1]), 60)
                print(f'{minutes1}분 {seconds1}초 // {minutes2}분 {seconds2}초')

            eventlet.sleep(10)

            return render_template('home.html', minutes1=minutes1, seconds1=seconds1, minutes2=minutes2, seconds2=seconds2)


if __name__ == '__main__':
    app.run()

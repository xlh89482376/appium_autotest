import time, datetime, requests
from common.utils.LoggingUtil import LoggingController

class AddPoiUtil(object):

    def __init__(self, env):
        self.log4py = LoggingController()
        self.poi_type = {
            '交通检查': '10002',
            '封路': '10003',
            '施工': '10006',
            '拥堵': '10007',
            '积水': '10008',
            '浓雾': '10010',
            '结冰': '10011',
            '交通事故': '10013',
            '实时路况': '10015'
        }
        self.__env = env
        self.path = None
        if self.__env == 'online':
            self.path = r'https://dzt.xxxxxxxx.com/deva/pc/pathAndPoi/no/addInfo'
        else:
            self.path = r'https://dzt-test.xxxxxxxxxx.com/deva/pc/pathAndPoi/no/addInfo'

    def get_data(self, poi_type, direction, lat, lon):
        data = {
            " uploadUser": "123",
            "sn": 'ZD802B1932L00622',
            "sourceType": '10003',  # 新鲜事
            "poiType": poi_type,  # 交通检查
            "direction": direction,
            "nickName": "小松鼠艾德蒙",
            "likeNum": 1,
            "lat": lat,
            "lon": lon,
            "uploadTimestamp": int(round(time.time() * 1000)),
            "timeOutTimestamp": int(str((time.mktime(time.strptime((datetime.datetime.now() + datetime.timedelta(days=3)).strftime("%Y-%m-%d 00:00:00"), '%Y-%m-%d %H:%M:%S'))) * 1000).split(".")[0]),
            "uploadAddress": "安定门外大街",
            "headImgUrl": "http://yycp-static-1255510688.cos.ap-beijing.myqcloud.com/sso-server-image/1592476328925.png?sign=q-sign-algorithm%3Dsha1%26q-ak%3DAKIDvfAPQlotZ1IJ5T8cKm02oKkxub2FfySs%26q-sign-time%3D1592476329%3B1592620329%26q-key-time%3D1592476329%3B1592620329%26q-header-list%3D%26q-url-param-list%3D%26q-signature%3D66cc5afe29f73df008113bf21b8586793c151239",
            "type": 1,
            "data": "[{\"url\":\"http://petchfile-1255510688.cos.ap-beijing.myqcloud.com/sso-server-image/1592546939076.mp4?sign=q-sign-algorithm%3Dsha1%26q-ak%3DAKIDCWfcNwD5PXVWLxwejccR3Tiz5zhIkx0T%26q-sign-time%3D1592546939%3B1592550539%26q-key-time%3D1592546939%3B1592550539%26q-header-list%3D%26q-url-param-list%3D%26q-signature%3D74a4058ad7579ea210dafcf78d7a19460cffb899\",\"thumbnail\":\"http://petchfile-1255510688.cos.ap-beijing.myqcloud.com/sso-server-image/1592546956790.png?sign=q-sign-algorithm%3Dsha1%26q-ak%3DAKIDCWfcNwD5PXVWLxwejccR3Tiz5zhIkx0T%26q-sign-time%3D1592546956%3B1592550556%26q-key-time%3D1592546956%3B1592550556%26q-header-list%3D%26q-url-param-list%3D%26q-signature%3Dcc9a35349fc55e433f934af88df576ae792b3987\"}]"
        }
        return data

    def add_poi(self, poi_type, direction, lat, lon):
        r = requests.post(url=self.path, json=self.get_data(poi_type, direction, lat, lon))
        print(r.json())

if __name__ == '__main__':
    print(int(round(time.time() * 1000)))
    print(int(str((time.mktime(time.strptime((datetime.datetime.now() + datetime.timedelta(days=3)).strftime("%Y-%m-%d 00:00:00"), '%Y-%m-%d %H:%M:%S'))) * 1000).split(".")[0]))
    env = 'qa'
    a = AddPoiUtil(env)
    a.add_poi(a.poi_type['封路'], 180, 39.963789,116.407674)






import requests
from requests.adapters import HTTPAdapter
import json
import xmltodict

from app.core.config import configs

# 초단기실황, 초단기예보, 단기예보
class VilageFcst:
    BASE_DATE = '20250818'
    BASE_TIME = '2100'
    NX = 62
    NY = 128
    
    def __init__(self, base_date, base_time, nx, ny):
        self.BASE_DATE = base_date
        self.BASE_TIME = base_time
        self.NX = nx
        self.NY = ny

    def vilage_fcst_info_service(self, param):
        api = ''
        try:
            if param == 'current':
                # 초단기실황 api
                print('초단기실황 API 조회')
                api = f"http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst?serviceKey={configs.API_KEY}&numOfRows=10&pageNo=1&base_date={self.BASE_DATE}&base_time={self.BASE_TIME}&nx={self.NX}&ny={self.NY}&dataType=JSON"
            elif param == 'forecast':
                # 초단기예보 api
                print('초단기예보 API 조회')
                api = f"http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtFcst?serviceKey={configs.API_KEY}&numOfRows=60&pageNo=1&base_date={self.BASE_DATE}&base_time={self.BASE_TIME}&nx={self.NX}&ny={self.NY}&dataType=JSON"
            else:
                # 단기예보 api
                print('단기예보 API 조회')
                api = f"http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst?serviceKey={configs.API_KEY}&numOfRows=1000&pageNo=1&base_date={self.BASE_DATE}&base_time={self.BASE_TIME}&nx={self.NX}&ny={self.NY}&dataType=JSON"
            
            # response = requests.get(api)
            # contents = response.text
            # json_ob = json.loads(contents)
            session = requests.Session()
            session.mount('http://', adapter=HTTPAdapter(max_retries=3))
            response = session.get(api)
            json_ob = json.loads(response.text)
            body = json_ob['response']['body']['items']['item']
            return body
        except Exception as e:
            print(f'API 호출 중 오류 발생 {e.add_note} args: {e.args}')
            return []

# 중기육상예보, 중기기온예보
class MidFcst:
    REG_ID = '11B00000'
    TMFC = 202508180600
    
    def __init__(self, reg_id, tmfc):
        self.REG_ID = reg_id
        self.TMFC = tmfc

    def mid_fcst_info_service(self, param):
        api = ''
        try:
            if param == 'midland':
                # 중기육상예보 api
                api = f"http://apis.data.go.kr/1360000/MidFcstInfoService/getMidLandFcst?serviceKey={configs.API_KEY}&numOfRows=10&pageNo=1&regId={self.REG_ID}&tmFc={self.TMFC}&dataType=JSON"
            elif param == 'midtmp':
                # 중기기온조회 api
                api = f"http://apis.data.go.kr/1360000/MidFcstInfoService/getMidTa?serviceKey={configs.API_KEY}&numOfRows=10&pageNo=1&regId={self.REG_ID}&tmFc={self.TMFC}&dataType=JSON"
            # response = requests.get(api)
            # contents = response.text
            # json_ob = json.loads(contents)
            session = requests.Session()
            session.mount('http://', adapter=HTTPAdapter(max_retries=3))
            response = session.get(api)
            json_ob = json.loads(response.text)
            body = json_ob['response']['body']['items']['item']
            return body
        except Exception as e:
            print(f'API 호출 중 오류 발생 {e.add_note} args: {e.args}')
            return []

# 자외선지수
class LivingWthr:
    AREA_NO = '1100000000'
    TIME = 2025081806
    
    def __init__(self, area_no, time):
        self.AREA_NO = area_no
        self.TIME = time

    def living_wthr_idx_service(self, param):
        api = ''
        try:
            if param == 'uvidx':
                # 자외선지수조회 api
                api = f"http://apis.data.go.kr/1360000/LivingWthrIdxServiceV4/getUVIdxV4?serviceKey={configs.API_KEY}&pageNo=1&numOfRows=10&areaNo={self.AREA_NO}&time={self.TIME}&dataType=JSON"
            # response = requests.get(api)
            # contents = response.text
            # json_ob = json.loads(contents)
            session = requests.Session()
            session.mount('http://', adapter=HTTPAdapter(max_retries=3))
            response = session.get(api)
            json_ob = json.loads(response.text)
            body = json_ob['response']['body']['items']['item']
            return body
        except Exception as e:
            print(f'API 호출 중 오류 발생 {e.add_note} args: {e.args}')
            return []
    
# 대기오염
class Arpltn:
    STATION_NAME = '중랑구'
    
    def __init__(self, station_name):
        self.STATION_NAME = station_name

    def arpltn_info_service(self, param):
        api = ''
        try:
            if param == 'msrstn':
                # 측정소별 측정정보 조회 api
                api = f"http://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getMsrstnAcctoRltmMesureDnsty?stationName={self.STATION_NAME}&dataTerm=daily&pageNo=1&numOfRows=100&returnType=json&serviceKey={configs.API_KEY}&ver=1.3"
            # response = requests.get(api)
            # contents = response.text
            # json_ob = json.loads(contents)
            session = requests.Session()
            session.mount('http://', adapter=HTTPAdapter(max_retries=3))
            response = session.get(api)
            json_ob = json.loads(response.text)
            body = json_ob['response']['body']['items']
            return body
        except Exception as e:
            print(f'API 호출 중 오류 발생 {e.add_note} args: {e.args}')
            return []
    
# 출몰시각
class RiseSet:
    LOCDATE = 20250821
    LOCATION = '서울'
    
    def __init__(self, locdate, location):
        self.LOCDATE = locdate
        self.LOCATION = location

    def rise_set_info_service(self, param):
        api = ''
        try:
            if param == 'area':
                # 지역별 해달 출몰시각 정보조회
                api = f"http://apis.data.go.kr/B090041/openapi/service/RiseSetInfoService/getAreaRiseSetInfo?location={self.LOCATION}&locdate={self.LOCDATE}&ServiceKey={configs.API_KEY}"
            # response = requests.get(api)
            # contents = response.text
            # json_ob = json.loads(contents)
            session = requests.Session()
            session.mount('http://', adapter=HTTPAdapter(max_retries=3))
            response = session.get(api)
            # 해당 API는 XML로만 제공하므로 XML to JSON 과정 추가
            json_convert = xmltodict.parse(response.text)
            json_ob = json.loads(json.dumps(json_convert))
            body = json_ob['response']['body']['items']['item']
            return body
        except Exception as e:
            print(f'API 호출 중 오류 발생 {e.add_note} args: {e.args}')
            return []
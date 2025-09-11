import datetime
import copy
import pymysql
import time

from service.service import ApiService, SchedulingService
from core.database import MySQLDatabase
from repository.repository import Repository
from model.sql import SqlModel
from repository.api_repository import VilageFcst, MidFcst, LivingWthr, RiseSet, Arpltn
from util.logger import Logger

api_logger = Logger.get_logger('schedule_logger')

# 측정소명을 집어넣는 부분 구현
# 측정소명은 DB에서 가져오도록

class ApiServiceImpl(ApiService):
    def call_api(self, api_code, basetime):
        if basetime is not None:
            # dt_now = datetime.datetime(2025, 8, 25, 23, 50, 11)
            dt_now = datetime.datetime.now()
            # 초단기실황, 초단기예보, 단기예보
            if api_code['API_CODE'] == 'FCST_CURRENT' or api_code['API_CODE'] == 'FCST_FORECAST' or api_code['API_CODE'] == 'FCST_VILAGE':
                result = self.process_vilage_fcst(dt_now, api_code, basetime)
            elif api_code['API_CODE'] == 'MID_FCST_INFO' or api_code['API_CODE'] == 'MID_TMP_INFO':
                result = self.process_mid_fcst(dt_now, api_code, basetime)
            elif api_code['API_CODE'] == 'UV_IDX_V4_INFO':
                result = self.process_living_wthr(dt_now, api_code, basetime)
            elif api_code['API_CODE'] == 'AREA_RISE_INFO':
                result = self.process_rise_set(dt_now, api_code)
            elif api_code['API_CODE'] == 'ARPLTN_INFO':
                result = self.process_arpltn(dt_now, api_code)
        return result
    
    # 초단기실황, 초단기예보, 단기예보
    def process_vilage_fcst(self, date: datetime.datetime, parameter, basetime):
        result = {}
        now_yyyyMMdd = date.strftime('%Y%m%d')
        vilageFcst = VilageFcst(now_yyyyMMdd, basetime, parameter['NX'], parameter['NY'])
        if parameter['API_CODE'] == 'FCST_CURRENT':
            # 초단기실황
            item = vilageFcst.vilage_fcst_info_service('current')
            # API 조회 오류 등으로 item이 빈 값인 경우 다시 API를 호출하도록 개선
            if item is None or item == [] or len(item) == 0:
                item = vilageFcst.vilage_fcst_info_service('current')
                
            # print(f'초단기실황 API result : {item}')
            # 필요 데이터 추출
            # [T1H: 기온, RN1: 1시간 강수량, REH: 습도, PTY: 강수형태, VEC: 풍향, WSD: 풍속]
            value_dict = {'T1H':'WD_DAY_TMP', 'RN1':'WD_DAY_PCP', 'REH':'WD_DAY_REH', 'PTY':'WD_DAY_PTY', 'VEC':'WD_DAY_VEC', 'WSD':'WD_DAY_WSD'}
            
            try:
                for i in item:
                    # 개선
                    if i['category'] in value_dict:
                       result[value_dict[i['category']]] = i['obsrValue'] # 'WD_DAY_TMP'
            except Exception as e:
                Logger.error(api_logger, f'{e}\nargs: {e.args}')
        elif parameter['API_CODE'] == 'FCST_FORECAST':
            # 초단기예보
            item = vilageFcst.vilage_fcst_info_service('forecast')
            # API 조회 오류 등으로 item이 빈 값인 경우 다시 API를 호출하도록 개선
            if item is None or item == [] or len(item) == 0:
                item = vilageFcst.vilage_fcst_info_service('forecast')
            # 필요 데이터 추출
            # n시간 후 하늘상태, n시간 후 강수형태, n시간 후 기온, n시간 후 강수확률
            # [T1H: 기온, SKY: 하늘상태, PTY: 강수형태]
            # [WD_DAY_SKY_nHR, WD_DAY_PTY_nHR, WD_DAY_TMP_nHR, WD_DAY_POP_nHR] n: +1 ~ +6
            
            # value_dict = {'T1H':'WD_DAY_TMP', 'SKY':'', 'REH':'', 'PTY':'', 'VEC':'', 'WSD':''}
            # now = datetime.datetime.now()
                
        elif parameter['API_CODE'] == 'FCST_VILAGE':
            # 단기예보
            item = vilageFcst.vilage_fcst_info_service('vilage')
            # API 조회 오류 등으로 item이 빈 값인 경우 다시 API를 호출하도록 개선
            if item is None or item == [] or len(item) == 0:
                item = vilageFcst.vilage_fcst_info_service('vilage')
            # print(f'단기예보 API result : {item}')
            # 필요 데이터 추출
            # 시간 +1 ~ +10
            # 날짜 +1 ~ +4
            # [TMP: 1시간 기온, SKY: 하늘상태, PTY: 강수형태, POP: 강수확률, TMN: 일 최저기온, TMX: 일 최고기온]
            # [WD_DAY_SKY_nHR, WD_DAY_TMP_nHR, WD_DAY_POP_nHR, WD_DAY_TMN, WD_DAY_TMX] n: +1 ~ +10
            # [12:00, TMP: 12시 기온, 18:00, TMP: 18시 기온, TMN: 일 최저기온, TMX: 일 최고기온,
            # 12:00, POP: 12시 강수확률, 18:00, POP: 18시 강수확률]
            # [WD_WF_SKY_nAM, WD_WF_PTY_nAM, WD_WF_SKY_nPM, WD_WF_PTY_nPM, WD_MAXn, WD_MINn, WD_RNST_nAM, WD_RNST_nPM] n: +1 ~ +3
            value_dict = {'TMP':'WD_DAY_TMP_nHR', 'SKY':'WD_DAY_SKY_nHR', 'PTY':'WD_DAY_PTY_nHR', 'POP':'WD_DAY_POP_nHR',
                          'AM_SKY':'WD_WF_SKY_nAM', 'AM_PTY':'WD_WF_PTY_nAM', 'PM_SKY':'WD_WF_SKY_nPM', 'PM_PTY':'WD_WF_PTY_nPM',
                          'TMN':'WD_MINn', 'TMX':'WD_MAXn', 'AM_POP':'WD_RNST_nAM', 'PM_POP':'WD_RNST_nPM'}
            date_format = '%Y%m%d%H%M'
            convert_now = datetime.datetime.strptime(date.strftime('%Y%m%d%H00'), date_format) # 202508240500
            convert_now_day = datetime.datetime.strptime(date.strftime('%Y%m%d0000'), date_format) # 202508240000
            try:
                for i in item:
                    category = i['category'] # TMP
                    fcst_date = i['fcstDate'] # 20250824
                    fcst_time = i['fcstTime'] # 0700
                    fcst_value = i['fcstValue'] # 26
                    
                    if category in value_dict:
                        # 시간차
                        date_time = datetime.datetime.strptime(fcst_date + fcst_time, date_format)
                        diff = date_time - convert_now
                        diff_hour = int(diff.total_seconds()/3600)
                        if diff_hour > 0 and diff_hour < 11:
                            value = value_dict[category].replace('n', str(diff_hour))
                            result[value] = fcst_value
                        
                        # 일차
                        day = datetime.datetime.strptime(fcst_date + '0000', date_format)
                        diff_days = (day - convert_now_day).days
                        if diff_days > 0 and diff_days < 7:
                            # 일자가 하루 이상 차이가 나고
                            if category == 'SKY' or category == 'PTY' or category == 'POP':
                                if fcst_time == '1200':
                                    # 시간이 1200이면 오전
                                    value = value_dict['AM_' + category].replace('n', str(diff_days))
                                    result[value] = fcst_value
                                elif fcst_time == '1800':
                                    # 시간이 1800이면 오후
                                    value = value_dict['PM_' + category].replace('n', str(diff_days))
                                    result[value] = fcst_value
                            
                            if category == 'TMX' or category == 'TMN':
                                value = value_dict[category].replace('n', str(diff_days))
                                result[value] = fcst_value
            except Exception as e:
                Logger.error(api_logger, f'{e}\nargs: {e.args}')
        Logger.info(api_logger, f'result: {result}')
        return result
        
    # 중기육상예보, 중기기온조회
    def process_mid_fcst(self, date: datetime.datetime, parameter, basetime):
        result = {}
        now = date.strftime('%Y%m%d') + basetime
        mid_fcst = MidFcst(parameter['REGION_CODE'], now)
        try:
            if parameter['API_CODE'] == 'MID_FCST_INFO':
                # 중기육상예보
                item = mid_fcst.mid_fcst_info_service('midland')
                # API 조회 오류 등으로 item이 빈 값인 경우 다시 API를 호출하도록 개선
                if item is None or item == [] or len(item) == 0:
                    item = mid_fcst.mid_fcst_info_service('midland')
                # 날짜 +4 ~ +6
                value_dict = {'rnSt4Am':'WD_RNST_4AM', 'rnSt4Pm':'WD_RNST_4PM', 'rnSt5Am':'WD_RNST_5AM', 'rnSt5Pm':'WD_RNST_5PM', 'rnSt6Am':'WD_RNST_6AM', 'rnSt6Pm':'WD_RNST_6PM',
                            'wf4Am':'WD_WF_4AM', 'wf4Pm':'WD_WF_4PM', 'wf5Am':'WD_WF_5AM', 'wf5Pm':'WD_WF_5PM', 'wf6Am':'WD_WF_6AM', 'wf6Pm':'WD_WF_6PM'}
            elif parameter['API_CODE'] == 'MID_TMP_INFO':
                # 중기기온조회
                item = mid_fcst.mid_fcst_info_service('midtmp')
                # API 조회 오류 등으로 item이 빈 값인 경우 다시 API를 호출하도록 개선
                if item is None or item == [] or len(item) == 0:
                    item = mid_fcst.mid_fcst_info_service('midtmp')
                # 날짜 +4 ~ +6
                value_dict = {'taMax4':'WD_MAX4', 'taMin4':'WD_MIN4', 'taMax5':'WD_MAX5', 'taMin5':'WD_MIN5', 'taMax6':'WD_MAX6', 'taMin6':'WD_MIN6'}
                
            # 중복되는 코드 통합
            for i in item:
                for key, value in value_dict.items():
                    # result[value] = i[key]
                    if key in i.keys():
                        result[value] = i[key]
                    else:
                        Logger.info(api_logger, f'{key}없음')
        except Exception as e:
            Logger.error(api_logger, f'{e}\nargs: {e.args}')
        
        Logger.info(api_logger, f'result: {result}')
        return result
    
    # 자외선지수
    def process_living_wthr(self, date: datetime.datetime, parameter, basetime:str):
        result = {}
        now = date.strftime('%Y%m%d') + basetime.rstrip('0')
        living_wthr = LivingWthr(parameter['REGION_CODE'], now)
        
        if parameter['API_CODE'] == 'UV_IDX_V4_INFO':
            try:
                # 자외선지수 측정
                item = living_wthr.living_wthr_idx_service('uvidx')
                # API 조회 오류 등으로 item이 빈 값인 경우 다시 API를 호출하도록 개선
                if item is None or item == [] or len(item) == 0:
                    item = living_wthr.living_wthr_idx_service('uvidx')
                value_dict = {'h0':'WD_DAY_UV'}
                for i in item:
                    if i['areaNo'] == parameter['REGION_CODE'] and i['date'] == now:
                        for key, value in value_dict.items():
                            result[value] = i[key]
            except Exception as e:
                Logger.error(api_logger, f'{e}\nargs: {e.args}')
        Logger.info(api_logger, f'result: {result}')
        return result
    
    # 대기오염(미세먼지)
    def process_arpltn(self, date: datetime.datetime, parameter):
        result = {}
        now = date.strftime('%Y-%m-%d %H:00')
        arpltn = Arpltn(parameter['REGION_NAME'])
        
        if parameter['API_CODE'] == 'ARPLTN_INFO':
            # 측정소별 측정정보
            item = arpltn.arpltn_info_service('msrstn')
            # API 조회 오류 등으로 item이 빈 값인 경우 다시 API를 호출하도록 개선
            if item is None or item == [] or len(item) == 0:
                item = arpltn.arpltn_info_service('msrstn')
            value_dict = {'pm10Value':'WD_PM_10_VALUE', 'pm10Grade1h':'WD_PM_10_GRADE', 'pm25Value':'WD_PM_25_VALUE', 'pm25Grade1h':'WD_PM_25_GRADE'}
            try:
                # 조회된 결과에서 해당하는 시간대의 값만 가져옴
                for i in item:
                    if i['dataTime'] == now:
                        for key, value in value_dict.items():
                            result[value] = i[key]
                        break
                        
                # 만약 아직 생성된 데이터가 없는 경우 다시 실행?
                # 현재 시간 -1 시간의 값으로 대체
                if len(result) == 0:    # result에 입력된 값이 없는 경우
                    # 현재 시간에서 1시간 빼고 다시 처리
                    one_hour_ago:datetime.datetime = date - datetime.timedelta(hours=1)
                    ago = one_hour_ago.strftime('%Y-%m-%d %H:00')
                    for i in item:
                        if i['dataTime'] == ago:
                            for key, value in value_dict.items():
                                if i[key] == '-':
                                    result[value] = 0
                                elif i[key] == None:
                                    result[value] = 1
                                else:
                                    result[value] = i[key]
                            break
            except Exception as e:
                Logger.error(api_logger, f'{e}\nargs: {e.args}')
        Logger.info(api_logger, f'result: {result}')
        return result
        
    # 출몰시각
    def process_rise_set(self, date: datetime.datetime, parameter):
        result = {}
        now_yyyyMMdd = date.strftime('%Y%m%d')
        rise_set = RiseSet(now_yyyyMMdd, parameter['REGION_NAME'])
        
        if parameter['API_CODE'] == 'AREA_RISE_INFO':
            # 해달출몰시각
            item = rise_set.rise_set_info_service('area')
            # API 조회 오류 등으로 item이 빈 값인 경우 다시 API를 호출하도록 개선
            if item is None or item == [] or len(item) == 0:
                item = rise_set.rise_set_info_service('area')
            value_dict = {'sunrise':'WD_SUNRISE', 'sunset':'WD_SUNSET', 'moonrise':'WD_MOONRISE', 'moonset':'WD_MOONSET'}
            try:
                for key, value in value_dict.items():
                    result[value] = item[key]
            except Exception as e:
                Logger.error(api_logger, f'{e}\nargs: {e.args}')
        Logger.info(api_logger, f'result: {result}')
        return result
    
class SchedulingServiceImpl(SchedulingService):
    # 해당 시간대에 실행할 동작
    def scheduling_process(self, basetime):
        """
        - 현재 시간대에 해당하는 API 호출
        1) DB 내 최신 날씨 정보 조회
        -> WD_DATETIME DESC LIMIT 1
        -> 현재 조회한 값 중 없는 값들을 채우기 위한 용도
        2) API 목록 조회
        -> API_CODE 및 PARAMETER 추출
        3) 현재 basetime을 조건으로 조회할 API 및 시간 PARAMETER 조회
        -> 조회 값이 NULL이 아닌 항목에 대해서 API를 호출함
        4) API 호출
        -> 1)과 2)에서 얻은 값을 토대로 각 API 호출
        5) 데이터 가공
        -> API 조회 결과값에서 필요한 정보 추출 및 데이터 가공
        6) 조회한 최신 정보에서 API 호출을 통해 얻은 값만 갱신
        7) 새로 갱신된 정보로 DB에 현재 시간을 키로 insert
        """
        
        # API들로부터 조회된 값을 담아두는 dict
        result_dict = {}
        
        # DB 연결
        # conn = db_connect_manager.db_connect()
        conn = MySQLDatabase.db_connect()
        
        # DB 내 최신 날씨 정보 조회
        current_data = Repository.select(
            cursor=conn.cursor(pymysql.cursors.DictCursor),
            sql_model=SqlModel(
                select_keys=['*'],
                tbl_name='tbl_weather_data',
                sort_param='WD_DATETIME',
                sort_div='DESC',
                option='LIMIT 1'
            )
        )
        result_dict = copy.deepcopy(current_data[0])
        
        # API 목록 조회
        # -> API_CODE 및 PARAMETER 추출
        # [0]: API_CODE, [1]: API_NAME, [2]: REGION_NAME, [3]: REGION_CODE, [4]: NX, [5]: NY
        
        api_list = Repository.select(
            cursor=conn.cursor(pymysql.cursors.DictCursor),
            sql_model=SqlModel(
                select_keys=['*'],
                tbl_name='tbl_api_code_list'
            )
        )
        
        # 현재 basetime을 조건으로 조회할 API 및 시간 PARAMETER 조회
        # -> 조회 값이 NULL이 아닌 항목에 대해서 API를 호출함, NULL이면 continue
        for api_code in api_list:
            if api_code['API_CODE'] == 'STATION_NAME':
                continue
            
            select_result = Repository.select(
                cursor=conn.cursor(),
                sql_model=SqlModel(
                    select_keys=[api_code['API_CODE']],
                    tbl_name='tbl_api_basetime',
                    where_keys=['CALL_TIME'],
                    where_values=[basetime]
                )
            )
            if select_result is None or select_result[0][0] is None or select_result[0][0] == 0:
                continue
            
            # ex) basetime = '00:15'
            # api_code[0] : FCST_CURRENT
            # api_code[1] : '초단기실황'
            # api_code[2] : None
            # api_code[3] : None
            # api_code[4] : 62
            # api_code[5] : 128
            # select_result[0][0] : '0000'
            
            # API 호출
            # 각 API_CODE에 따른 API를 선택해 호출
            api_service = ApiServiceImpl()
            result = api_service.call_api(api_code=api_code, basetime=select_result[0][0])
            # result = {'key':'value'}
            # result값 result_dict로 병합
            # 조회한 최신 정보에서 API로 호출을 통해 얻은 값만 갱신
            for key, value in result.items():
                result_dict[key] = value
            # time.sleep(1)
            
        # 새로 만들어진 정보로 DB에 insert
        result_dict['WD_DATETIME'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        result = Repository.insert(
            conn=conn,
            tbl_name='tbl_weather_data',
            insert_data=result_dict
        )
        Logger.info(api_logger, f'result: {result}')
        
        # DB 연결 종료
        MySQLDatabase.db_close(conn)
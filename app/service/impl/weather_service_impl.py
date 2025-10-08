import pymysql
from datetime import datetime

from util.response import create_response
from util.result_code import ResultCode
from util.logger import Logger
from util.date import convert_nearest_basetime
from service.weather_service import WeatherService
from service.impl.service_impl import SchedulingServiceImpl
from core.database import MySQLDatabase
from repository.repository import Repository
from model.sql import SqlModel

web_logger = Logger.get_logger('web_logger')

class WeatherServiceImpl(WeatherService):
    # 최신 날씨 정보 조회
    def get_current_weather_data(self):
        Logger.info(web_logger, 'get_current_weather_data 시작')
        conn = MySQLDatabase.db_connect()
        try:
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
            result_code = ResultCode.SUCCESS
            result_msg = "SUCCESS"
        except Exception as e:
            Logger.error(web_logger, f'{e}\nargs: {e.args}')
            result_code = ResultCode.INTERNAL_SERVER_ERROR
            result_msg = "INTERNAL_SERVER_ERROR"
            current_data = []
        MySQLDatabase.db_close(conn)
        return create_response(result_code, result_msg, current_data)
        
    # 날씨 정보 새로고침
    def refresh_weather_data(self):
        Logger.info(web_logger, 'refresh_weather_data 시작')
        # 서버에게 날씨 API를 이용한 날씨 정보 조회 명령을 내림
        # 새로 생성된 최신 날씨 정보를 클라이언트로 전송함
        try:
            # 현재 시간에서 가장 가까운 basetime 생성
            # basetime -> xx:15, xx:45
            basetime = convert_nearest_basetime(datetime.now())
            print(basetime)
            # SchedulingServiceImpl.scheculing_process(basetime) 호출
            scheduling_service_impl = SchedulingServiceImpl()
            result = scheduling_service_impl.scheduling_process(basetime)
            
            if result == 1:
                # 데이터 생성 후 최신 날씨 정보 조회
                conn = MySQLDatabase.db_connect()
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
                result_code = ResultCode.SUCCESS
                result_msg = "SUCCESS"
                MySQLDatabase.db_close(conn)
                return create_response(result_code, result_msg, current_data)
        except Exception as e:
            Logger.error(web_logger, f'{e}\nargs: {e.args}')
            if conn is not None:
                MySQLDatabase.db_close(conn)
            result_code = ResultCode.INTERNAL_SERVER_ERROR
            result_msg = "INTERNAL_SERVER_ERROR"
            current_data = []
            return create_response(result_code, result_msg, current_data)
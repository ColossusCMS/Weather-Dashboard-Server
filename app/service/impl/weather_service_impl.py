import pymysql

from util.response import create_response
from util.result_code import ResultCode
from service.weather_service import WeatherService
from core.database import MySQLDatabase
from repository.repository import Repository
from model.sql import SqlModel

class WeatherServiceImpl(WeatherService):
    # 최신 날씨 정보 조회
    def get_current_weather_data(self):
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
            print(f'{e.add_note} args: {e.args}')
            result_code = ResultCode.INTERNAL_SERVER_ERROR
            result_msg = "INTERNAL_SERVER_ERROR"
            current_data = []
        return create_response(result_code, result_msg, current_data)
        
    def refresh_weather_data(self, basetime: str):
        return {'':''}
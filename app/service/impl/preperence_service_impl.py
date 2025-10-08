import pymysql

from service.preperence_service import PreperenceService
from core.database import MySQLDatabase
from model.sql import SqlModel
from repository.repository import Repository
from util.logger import Logger
from util.response import create_response
from util.result_code import ResultCode

preperence_logger = Logger.get_logger('preperence_logger')

class PreperenceServiceImpl(PreperenceService):
    # 설정값 조회
    def get_preperence_value(self, key):
        Logger.info(preperence_logger, 'get_preperence_value 시작')
        conn = MySQLDatabase.db_connect()
        
        if key == 'display':
            preperence_ctg = 'DISPLAY'
            preperence_name = 'DISPLAY_STATUS'
        
        try:
            preperence_value = Repository.select(
                cursor=conn.cursor(pymysql.cursors.DictCursor),
                sql_model=SqlModel(
                    select_keys=['PREPERENCE_VALUE'],
                    tbl_name='tbl_preperence_list',
                    where_keys=['PREPERENCE_CTG', 'PREPERENCE_NAME'],
                    where_values=[preperence_ctg, preperence_name]
                )
            )
            result_code = ResultCode.SUCCESS
            result_msg = "SUCCESS"
            Logger.info(preperence_logger, 'get_preperence_value 완료')
        except Exception as e:
            Logger.error(preperence_logger, f'{e}\nargs: {e.args}')
            result_code = ResultCode.INTERNAL_SERVER_ERROR
            result_msg = "INTERNAL_SERVER_ERROR"
            preperence_value = None
            
        MySQLDatabase.db_close(conn)
        return create_response(result_code, result_msg, preperence_value)
    
    # DISPLAY_STATUS 스위칭
    def switching_display_status(self):
        Logger.info(preperence_logger, 'switching_display_status 시작')
        conn = MySQLDatabase.db_connect()
        try:
            # 현재 값을 조회
            # dashboard <-> image
            preperence_value = Repository.select(
                cursor=conn.cursor(),
                sql_model=SqlModel(
                    select_keys=['PREPERENCE_VALUE'],
                    tbl_name='tbl_preperence_list',
                    where_keys=['PREPERENCE_CTG', 'PREPERENCE_NAME'],
                    where_values=['DISPLAY', 'DISPLAY_STATUS']
                )
            )
            
            # print(f'preperence_value: {preperence_value[0][0]}')
            switching_value = 'dashboard' if preperence_value[0][0] == 'image' else 'image'
            # print(f'switching_value: {switching_value}')
            Repository.update(
                conn,
                sql_model=SqlModel(
                    select_keys=['PREPERENCE_VALUE'],
                    update_value=[switching_value],
                    tbl_name='tbl_preperence_list',
                    where_keys=['PREPERENCE_CTG', 'PREPERENCE_NAME'],
                    where_values=['DISPLAY', 'DISPLAY_STATUS']
                )
            )
            result_code = ResultCode.SUCCESS
            result_msg = "SUCCESS"
            Logger.info(preperence_logger, 'switching_display_status 완료')
        except Exception as e:
            Logger.error(preperence_logger, f'{e}\nargs: {e.args}')
            result_code = ResultCode.INTERNAL_SERVER_ERROR
            result_msg = "INTERNAL_SERVER_ERROR"
            switching_value = None
        
        MySQLDatabase.db_close(conn)
        return create_response(result_code, result_msg, switching_value)
    
    # 현재 측정소 정보 조회
    def get_station_info(self):
        Logger.info(preperence_logger, 'get_station_info 시작')
        conn = MySQLDatabase.db_connect()
        try:
            station_info = Repository.select(
                cursor=conn.cursor(pymysql.cursors.DictCursor),
                sql_model=SqlModel(
                    select_keys=['REGION_NAME'],
                    tbl_name='tbl_api_code_list',
                    where_keys=['API_CODE'],
                    where_values=['STATION_NAME']
                )
            )
            result_code = ResultCode.SUCCESS
            result_msg = 'SUCCESS'
            result = station_info[0]
        except Exception as e:
            Logger.error(preperence_logger, f'{e}\nargs: {e.args}')
            result_code = ResultCode.INTERNAL_SERVER_ERROR
            result_msg = "INTERNAL_SERVER_ERROR"
            result = ''
        MySQLDatabase.db_close(conn)
        return create_response(result_code, result_msg, result)
    
    # 시/도 목록 조회
    def get_province_list(self):
        Logger.info(preperence_logger, 'get_province_list 시작')
        conn = MySQLDatabase.db_connect()
        try:
            province_list = Repository.select(
                cursor=conn.cursor(),
                sql_model=SqlModel(
                    select_keys=['DISTINCT PROVINCE'],
                    tbl_name='tbl_station_list'
                )
            )
            result_code = ResultCode.SUCCESS
            result_msg = 'SUCCESS'
        except Exception as e:
            Logger.error(preperence_logger, f'{e}\nargs: {e.args}')
            result_code = ResultCode.INTERNAL_SERVER_ERROR
            result_msg = "INTERNAL_SERVER_ERROR"
            province_list = []
        MySQLDatabase.db_close(conn)
        return create_response(result_code, result_msg, province_list)
    
    # 구/군/시 목록 조회
    def get_region_list(self, params):
        Logger.info(preperence_logger, 'get_region_list 시작')
        province = params.province
        
        conn = MySQLDatabase.db_connect()
        try:
            region_list = Repository.select(
                cursor=conn.cursor(),
                sql_model=SqlModel(
                    select_keys=['REGION'],
                    tbl_name='tbl_station_list',
                    where_keys=['PROVINCE'],
                    where_values=[province]
                )
            )
            result_code = ResultCode.SUCCESS
            result_msg = 'SUCCESS'
        except Exception as e:
            Logger.error(preperence_logger, f'{e}\nargs: {e.args}')
            result_code = ResultCode.INTERNAL_SERVER_ERROR
            result_msg = "INTERNAL_SERVER_ERROR"
            region_list = None
        MySQLDatabase.db_close(conn)
        return create_response(result_code, result_msg, region_list)
    
    # 측정소 정보 수정 등록
    def change_station_info(self, params):
        Logger.info(preperence_logger, 'change_station_info 시작')
        
        # 전달받은 params의 province, region 정보로 tbl_station_list에서 해당 정보를 조회
        province = params.province
        region = params.region
        
        conn = MySQLDatabase.db_connect()
        try:
            # 측정소 상세 정보를 조회
            station_value = Repository.select(
                cursor=conn.cursor(pymysql.cursors.DictCursor),
                sql_model=SqlModel(
                    select_keys=['*'],
                    tbl_name='tbl_station_list',
                    where_keys=['PROVINCE', 'REGION'],
                    where_values=[province, region]
                )
            )
            api_code_list = [
                'AREA_RISE_INFO',
                'ARPLTN_INFO',
                'FCST_CURRENT',
                'FCST_FORECAST',
                'FCST_VILAGE',
                'MID_FCST_INFO',
                'MID_TMP_INFO',
                'UV_IDX_V4_INFO',
                'STATION_NAME'
            ]
            
            station_name = f'{station_value[0]["PROVINCE"]} {station_value[0]["REGION"]}'
            
            update_set_list = [
                (('REGION_NAME', 'REGION_CODE'), (station_value[0]['PROVINCE'], station_value[0]['PROVINCE'])),
                (('REGION_NAME', 'REGION_CODE'), (station_value[0]['REGION'], station_value[0]['REGION'])),
                (('NX', 'NY'), (station_value[0]['NX'], station_value[0]['NY'])),
                (('NX', 'NY'), (station_value[0]['NX'], station_value[0]['NY'])),
                (('NX', 'NY'), (station_value[0]['NX'], station_value[0]['NY'])),
                (('REGION_NAME', 'REGION_CODE'), (station_value[0]['MID_FCST_INFO_TEXT'], station_value[0]['MID_FCST_INFO'])),
                (('REGION_NAME', 'REGION_CODE'), (station_value[0]['PROVINCE'], station_value[0]['MID_TMP_INFO'])),
                (('REGION_NAME', 'REGION_CODE'), (station_name, station_value[0]['UV_IDX_V4_INFO'])),
                (('REGION_NAME', 'REGION_CODE'), (station_name, station_name))
            ]
            
            for i in range(len(api_code_list)):
                # 조회한 데이터에 맞게 tbl_api_code_list 업데이트
                Repository.update(
                    conn,
                    sql_model=SqlModel(
                        select_keys=update_set_list[i][0],
                        update_value=update_set_list[i][1],
                        tbl_name='tbl_api_code_list',
                        where_keys=['API_CODE'],
                        where_values=[api_code_list[i]]
                    )
                )
            result_code = ResultCode.SUCCESS
            result_msg = "SUCCESS"
            result = {'province':station_value[0]["PROVINCE"], 'region':station_value[0]["REGION"]}
            Logger.info(preperence_logger, 'change_station_info 완료')
        except Exception as e:
            Logger.error(preperence_logger, f'{e}\nargs: {e.args}')
            result_code = ResultCode.INTERNAL_SERVER_ERROR
            result_msg = "INTERNAL_SERVER_ERROR"
            result = None
        MySQLDatabase.db_close(conn)
        return create_response(result_code, result_msg, result)
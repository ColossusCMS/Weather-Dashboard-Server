from model.sql import SqlModel
from util.convert import create_insert_values, convert_select_keys, convert_where_params
from util.logger import Logger

db_logger = Logger.get_logger('db_logger')

class Repository:
    # SELECT문
    def select(cursor, sql_model: SqlModel):
        try:
            select_keys = convert_select_keys(sql_model.select_keys)
        
            sql = f'SELECT {select_keys} FROM {sql_model.tbl_name}'
            
            if sql_model.where_keys is not None:
                sql += convert_where_params(sql_model.where_keys, sql_model.where_values)
                
            if sql_model.sort_param is not None:
                sql += f' ORDER BY {sql_model.sort_param} {sql_model.sort_div}'
                
            if sql_model.option is not None:
                sql += f' {sql_model.option}'
                
            Logger.info(db_logger, f'SQL : {sql}')
            cursor.execute(sql)
            results = cursor.fetchall()
            return results
        except Exception as e:
            Logger.error(db_logger, f'SELECT 중 오류 발생 {e.add_note} args: {e.args}')
            return None
    
    # INSERT문
    def insert(conn, tbl_name, insert_data: dict):
        cursor = conn.cursor()
        try:
            convert_keys = convert_select_keys(list(insert_data.keys()))
            values_params = create_insert_values(insert_data.keys())
            sql = f'INSERT INTO {tbl_name} ({convert_keys}) VALUES ({values_params})'
            
            Logger.info(db_logger, f'SQL : {sql}')
            
            cursor.execute(sql, list(insert_data.values()))
            conn.commit()
            Logger.info(db_logger, f'{cursor.rowcount}개의 행이 입력되었습니다.')
        except Exception as e:
            Logger.error(db_logger, f'INSERT 중 오류 발생 {e.add_note} args: {e.args}')
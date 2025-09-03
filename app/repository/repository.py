from model.sql import SqlModel
from util.convert import create_insert_values, convert_select_keys, convert_where_params

class Repository:
    # SELECT문
    def select(cursor, sql_model: SqlModel):
        select_keys = convert_select_keys(sql_model.select_keys)
        
        sql = f'SELECT {select_keys} FROM {sql_model.tbl_name}'
        
        if sql_model.where_keys is not None:
            sql += convert_where_params(sql_model.where_keys, sql_model.where_values)
            
        if sql_model.sort_param is not None:
            sql += f' ORDER BY {sql_model.sort_param} {sql_model.sort_div}'
            
        if sql_model.option is not None:
            sql += f' {sql_model.option}'
            
        print(sql)
        cursor.execute(sql)
        results = cursor.fetchall()
        return results
    
    # INSERT문
    def insert(conn, tbl_name, insert_data: dict):
        cursor = conn.cursor()
        try:
            convert_keys = convert_select_keys(list(insert_data.keys()))
            values_params = create_insert_values(insert_data.keys())
            sql = f'INSERT INTO {tbl_name} ({convert_keys}) VALUES ({values_params})'
            
            print(sql)
            
            cursor.execute(sql, list(insert_data.values()))
            conn.commit()
            print(f'{cursor.rowcount}개의 행이 입력되었습니다.')
            return 0
        except Exception as e:
            print(f'{e.add_note} args: {e.args}')
# list를 ,를 포함한 str로 변환
def convert_select_keys(key_list: list):
    return ','.join(key_list)

# list의 길이만큼 ,를 포함한 %s를 생성 (insert 쿼리용)
def create_insert_values(key_list: list):
    result = ''
    for i in range(len(key_list)):
        result += '%s'
        if i < len(key_list) - 1:
            result += ','
    return result

# [key], [value] => key = value
# [key1, key2], [value1, value2] => key1 = value1 AND key2 = value2
# [key1, key2, key3], [value1, value2, value3] => key1 = value1 AND key2 = value2 AND key3 = value3
def convert_where_params(where_keys: list, where_values: list):
    sql = ' WHERE'
    
    for i in range(len(where_keys)):
        sql += f' {where_keys[i]} = \'{where_values[i]}\''
        if i > 0:
            sql += f' AND {where_keys[i]} = \'{where_values[i]}\''
    return sql
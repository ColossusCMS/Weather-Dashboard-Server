class SqlModel:
    select_keys: list = []
    update_value: list = None
    tbl_name: str = ''
    where_keys: list = None
    where_values: list = None
    sort_param: str = None
    sort_div: str = None
    option: str = None
    
    def __init__(self,
                 select_keys,
                 tbl_name,
                 update_value=None,
                 where_keys=None,
                 where_values=None,
                 sort_param=None,
                 sort_div=None,
                 option=None):
        self.select_keys = select_keys
        self.update_value = update_value
        self.tbl_name = tbl_name
        self.where_keys = where_keys
        self.where_values = where_values
        self.sort_param = sort_param
        self.sort_div = sort_div
        self.option = option
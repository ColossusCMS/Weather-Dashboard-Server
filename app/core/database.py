import pymysql
from abc import ABC, abstractmethod
from core.config import configs

class Database(ABC):
    @abstractmethod
    def db_connect():
        pass
    
    @abstractmethod
    def db_close(conn):
        pass
        
class MySQLDatabase(Database):
    def db_connect():
        conn = pymysql.connect(host=configs.HOST, port=configs.PORT, user=configs.USERNAME, password=configs.PASSWORD, db=configs.DB_NAME, charset='utf8')
        print('DB 연결 완료')
        return conn
    
    def db_close(conn):
        conn.close()
        print('DB 연결 해제')
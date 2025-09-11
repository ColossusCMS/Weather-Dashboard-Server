import pymysql
from abc import ABC, abstractmethod

from core.config import configs
from util.logger import Logger

db_logger = Logger.get_logger('db_logger')

class Database(ABC):
    @abstractmethod
    def db_connect():
        pass
    
    @abstractmethod
    def db_close(conn):
        pass
        
class MySQLDatabase(Database):
    def db_connect():
        try:
            conn = pymysql.connect(host=configs.HOST, port=configs.PORT, user=configs.USERNAME, password=configs.PASSWORD, db=configs.DB_NAME, charset='utf8')
            Logger.info(db_logger, f'{configs.DB_NAME} DB 연결 완료')
            return conn
        except Exception as e:
            Logger.error(db_logger, f'{e}\nargs: {e.args}')
            Logger.error(db_logger, 'DB 연결 중 오류 발생')
            return None
        
    def db_close(conn) -> None:
        try:
            conn.close()
            Logger.info(db_logger, f'{configs.DB_NAME} DB 연결 해제 완료')
        except Exception as e:
            Logger.error(db_logger, f'{e}\nargs: {e.args}')
            Logger.error(db_logger, 'DB 연결 해제 중 오류 발생')
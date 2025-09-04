import os
import datetime
import logging
from logging.handlers import TimedRotatingFileHandler

# /app/log/
log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'log')

class Logger:
    # 여러 로그 설정을 관리하고, 관련된 기능을 제공하는 클래스
    _instance = {}
    
    @staticmethod
    def get_logger(log_file_name, sub_dir='', log_dir=log_dir):
        if log_file_name not in Logger._instance:
            # 새로운 로거 생성
            logger = logging.getLogger(log_file_name)
            
            #중복 핸들러 방지
            if not logger.handlers:
                os.makedirs(os.path.join(log_dir, sub_dir), exist_ok=True)
                log_file = os.path.join(log_dir, sub_dir, log_file_name + '.log')
                
                formatter = logging.Formatter('[%(asctime)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
                
                timed_file_handler = TimedRotatingFileHandler(filename=log_file, when='midnight', interval=1, encoding='utf-8')
                timed_file_handler.setFormatter(formatter)
                timed_file_handler.suffix = '%Y%m%d_'
                
                logger.addHandler(timed_file_handler)
                logger.setLevel(logging.INFO)
            
            Logger._instance[log_file_name] = logger
            
        return Logger._instance[log_file_name]
    
    @staticmethod
    def error(logger_instance, message):
        msg = f'[ERROR] {str(message)}'
        logger_instance.error(msg)
        _to_print(msg)
        
    @staticmethod
    def warning(logger_instance, message):
        msg = f'[WARN] {str(message)}'
        logger_instance.warning(msg)
        _to_print(msg)
        
    @staticmethod
    def info(logger_instance, message):
        msg = f'[INFO] {str(message)}'
        logger_instance.info(msg)
        _to_print(msg)
    
def _to_print(message):
    now = datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S]')
    print(f'{now} {message}')
    
Logger.get_logger('web_logger', sub_dir='web')
Logger.get_logger('schedule_logger', sub_dir='schedule')
Logger.get_logger('db_logger', sub_dir='db')
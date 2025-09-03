import os
from dotenv import load_dotenv

# .env 파일에서 환경 변수를 로드
load_dotenv()

class Config:
    API_KEY = os.getenv('API_KEY')
    
    HOST = os.getenv('DB_HOST')
    PORT = int(os.getenv('DB_PORT'))
    USERNAME = os.getenv('DB_USERNAME')
    PASSWORD = os.getenv('DB_PASSWORD')
    DB_NAME = os.getenv('DB_NAME')
    
    WEB_HOST = os.getenv('WEB_HOST')
    WEB_PORT = int(os.getenv('WEB_PORT'))
    
configs = Config()
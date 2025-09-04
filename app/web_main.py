import uvicorn
from fastapi import FastAPI
from service.impl.service_impl import SchedulingServiceImpl
from api.api_router import routers
from core.config import Config
from util.result_code import ResultCode
from util.logger import Logger

web_logger = Logger.get_logger('web_logger')

def app_creator():
    Logger.info(web_logger, '웹서버 초기화 시작')
    app = FastAPI(
        title='Weather Dashboard Server',
        summary='summary',
        description='설명',
        version='0.0.1',
    )
    # controller.py에 정의된 라우터를 메인 앱에 포함
    # prefix를 사용하여 경로를 그룹화
    app.include_router(routers)
    
    @app.get('/')
    def root():
        return {'resultCode' : ResultCode.SUCCESS, 'resultMsg': 'Service is Working'}

    Logger.info(web_logger, '웹서버 초기화 완료')
    return app

app = app_creator()

# 테스트 실행용 메소드
def test():
    scheduling_service = SchedulingServiceImpl()
    scheduling_service.scheduling_process('02:15')

if __name__ == '__main__':
    # test()
    uvicorn.run('web_main:app', host=Config.WEB_HOST, port=Config.WEB_PORT, reload=True)
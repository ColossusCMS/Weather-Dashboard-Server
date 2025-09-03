import uvicorn
from fastapi import FastAPI
from service.service import SchedulingService
from api.api_router import routers

def app_creator():
    print(f'웹서버 초기화 시작')
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
        return {'resultCode' : 200, 'resultMsg': 'Service is Working'}

    print(f'웹서버 초기화 완료')
    return app

app = app_creator()

# 테스트 실행용 메소드
def test():
    SchedulingService.scheduling_process('18:15')

if __name__ == '__main__':
    # test()
    uvicorn.run('web_main:app', host="0.0.0.0", port=9999, reload=True)
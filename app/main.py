import schedule
from fastapi import FastAPI

from app.service.service import SchedulingService
from app.core.database import MySQLDatabase
from app.repository.repository import Repository
from app.model.sql import SqlModel
from app.api.api_router import routers
from app.util.singleton import singleton

@singleton
class AppCreator:
    # 앱 초기화 작업
    def __init__(self):
        print('시스템 초기 가동 초기화 시작')
        
        self.app = FastAPI(
            title='Weather Dashboard Server',
            summary='summary',
            description='설명',
            version='0.0.1',
        )

        # controller.py에 정의된 라우터를 메인 앱에 포함
        # prefix를 사용하여 경로를 그룹화
        self.app.include_router(routers)
        
        @self.app.get('/')
        def root():
            return {'resultCode' : 200, 'resultMsg': 'Service is Working'}
        
        print('초기화 작업 완료')
        
        try:
            # DB 연결
            conn = MySQLDatabase.db_connect()
            # 스케줄 등록할 시간대 목록 조회
            basetime_list = Repository.select(
                cursor=conn.cursor(),
                sql_model=SqlModel(
                    select_keys=['CALL_TIME'],
                    tbl_name='tbl_api_basetime',
                    sort_param='SEQ',
                    sort_div='ASC'
                )
            )
            MySQLDatabase.db_close(conn)
            
            for basetime in basetime_list:
                schedule.every().day.at(basetime[0]).do(SchedulingService.scheduling_process, basetime[0])
                print(f'Create \'{basetime}\' scheduling process!!')
                
        except Exception as e:
            print(f'초기화 작업 중 오류 : {e.add_note} args: {e.args}')

app_creator = AppCreator()
app = app_creator.app

# 테스트 실행용 메소드
def test():
    SchedulingService.scheduling_process('18:15')

if __name__ == '__main__':
    # test()
    # while True:
        # schedule.run_pending()
#    app.run(debug=True, port=9999)
    import uvicorn
    uvicorn.run('main:app', host="0.0.0.0", port=9999, reload=True)
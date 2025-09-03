import schedule

from core.database import MySQLDatabase
from repository.repository import Repository
from model.sql import SqlModel
from service.service import SchedulingService

# 스케줄링 생성
def schedule_creator():
    print(f'스케줄링 초기화 시작')
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
        print(f'스케줄링 초기화 완료')
    except Exception as e:
        print(f'{e.add_note} args: {e.args}')
        print(f'스케줄링 초기화 오류')

# 스케줄링을 실행하는 무한 루프
def run_schedule_loop():
    print(f'스케줄링 루프 실행')
    while True:
        schedule.run_pending()

if __name__ == '__main__':
    schedule_creator()
    run_schedule_loop()
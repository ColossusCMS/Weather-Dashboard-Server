import datetime
import time
import os

from util.logger import Logger

logger = Logger.get_logger('schedule_logger')

log_dir = os.path.join(os.path.realpath(__file__), 'log')

# 오래된 로그 파일 삭제 함수
def delete_old_files(path_target, days_elapsed):
    path = os.path.join(log_dir, path_target)
    for f in os.listdir(path):
        f = os.path.join(path, f)
        if os.path.isfile(f):   # 선택된 항목이 파일인 경우
            timestamp_now = datetime.datetime.now().timestamp()
            # st_mtime 마지막 수정일 timestamp
            is_old = os.stat(f).st_mtime < timestamp_now - (days_elapsed * 24 * 60 * 60)
            # days_elapsed 만큼의 기간 차이가 있는 경우
            if is_old:
                try:
                    os.remove(f)
                    Logger.info(logger, f'{f} 로그파일 삭제됨')
                except OSError: # Device or resource busy
                    Logger.error(logger, f'{f} 로그 파일 삭제 오류')

# 삭제 자동 프로세스
def auto_delete_process():
    while True:
        now = datetime.datetime.now()
        Logger.info(logger, f'{now.strftime('%Y-%m-%d')} 로그 파일 삭제 프로세스 시작')
        delete_old_files('web', 7)
        delete_old_files('schedule', 7)
        time.sleep(24 * 60 * 60)    # 하루마다 실행

if __name__ == '__main__':
    # 로그 파일 자동 삭제 함수
    auto_delete_process()
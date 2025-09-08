# 날씨 대시보드 서버

## 1. 개요
### 1. 프로그램 개발환경
    - 개발 언어 : Python 3.12.2
    - 개발 툴 : VS Code
    - 개발 환경 OS : Windows 11
    - DB 구성 : MariaDB 10.6.22

### 2. 서버 환경
    - OS : Linux Mint 21.1
    - Python : 3.10.12
    - DB : MariaDB 10.6.22

## 2. 필요 pip install 목록 및 .env
### 1. 필요 pip install 목록
```
pip install -r requirements.txt
```
- pip install schedule
- pip install pymysql
- pip install keyboard
- pip install xmltodict
- pip install fastapi
- pip install uvicorn[standard]

### 2. .env 구성 및 start_app.sh 파일
- [required] .env파일 생성 후 하단의 샘플에 맞춰서 작성
```
# MySQL or MariaDB
DB_HOST = {DB 주소} -> str
DB_PORT = {DB 포트} -> int
DB_USERNAME = {DB 사용자명} -> str
DB_PASSWORD = {DB 비밀번호} -> str
DB_NAME = {DB명} -> str

# 공공데이터 API
API_KEY = {발급받은 API_KEY} -> str

# 웹서버 설정
WEB_HOST = {호스트 주소} -> str
WEB_PORT = {포트번호} -> int
```
- [optional] start_app.sh 파일 (리눅스 내 서비스 등록용)
```
# 각 서비스를 실행하기 위한 sh파일
#!/bin/bash

python3 web_main.py & # 웹서버 실행
python3 schedule_main.py & # 스케줄러 실행
python3 log_auto_delete_main.py & # 로그 파일 자동 정리 실행

# 스크립트가 종료되지 않도록 대기
wait
```

## 3. 프로그램 설명
E- Paper 날씨 대시보드 시스템의 백엔드 서버입니다.   
공공데이터 API를 이용해 여러 날씨와 관련된 정보를 조회하고 이를 가공하여 데이터 베이스에 저장, 클라이언트로 데이터 베이스 내 정보를 전송하는 역할을 담당합니다.   
공공데이터 내 활용하는 API 목록 및 활용하는 데이터 목록은 4. '활용 API 목록 및 활용 데이터 목록'에 기술되어 있습니다.   
날씨 대시보드 서버는 미리 지정된 스케줄링에 따라 자동으로 API를 호출, 데이터를 가공, 저장합니다.   
그리고 날씨 대시보드 시스템의 클라이언트가 날씨 정보 조회 API를 호출하면 데이터 베이스에서 최신 정보를 조회하여 클라이언트로 전달합니다.   
<hr />

## 4. 활용 API 목록 및 활용 데이터 목록
### 1. 활용 공공데이터 API 목록
    1) 기상청_단기예보 ((구)_동네예보) 조회서비스
        - 초단기실황조회
        - 초단기예보조회
        - 단기예보조회

    2) 기상청_중기예보 조회서비스
        - 중기육상예보조회
        - 중기기온조회

    3) 한국천문연구원_출몰시각 정보
        - 지역별 해달 출몰시각 정보조회

    4) 한국환경공단_에어코리아_대기오염정보
        - 측정소별 실시간 측정정보 조회

    5) 기상청_생활기상지수_조회서비스(3.0)
        - 자외선지수조회

### 2. 활용 데이터 목록
    1) 초단기실황조회 (현재시각 정보 조회)
        - 기온, 1시간 강수량, 습도, 강수형태, 풍향, 풍속

    2) 초단기예보조회 (+1시간 ~ +6시간 예보 조회)
        - 기온, 1시간 강수량, 하늘상태, 습도, 강수형태, 풍향, 풍속

    3) 단기예보조회 (+1일 ~ +4일 예보 조회)
        - 강수확률, 강수형태, 1시간 강수량, 습도, 1시간 신적설, 하늘상태, 1시간 기온, 일 최저기온, 일 최고기온, 풍향, 풍속

    4) 중기육상예보조회 (+4일 ~ +6일 날씨예보 및 강수확률 조회)
        - n일 후 오전 강수확률, n일 후 오후 강수확률, n일 후 오전 날씨예보, n일 후 오후 날씨예보

    5) 중기기온조회 (+4일 ~ +6일 최고기온, 최저기온 조회)
        - n일 후 예상 최저기온, n일 후 예상 최고기온

    6) 지역별 해달 출몰시각 정보조회
        - 일출 시각, 일몰 시각, 월출 시각, 월몰 시각

    7) 측정소별 실시간 측정정보 조회 (미세먼지 정보 조회)
        - 미세먼지(PM10) 농도, 미세먼지(PM10) 1시간 등급, 미세먼지(PM2.5) 농도, 미세먼지(PM2.5) 1시간 등급

    8) 자외선지수조회
        - 자외선지수


## 5. 프로젝트 구조
```
root/
├ app/
    ├ api/
        ├ endpoints/
            └ weather.py
        └ api_router.py
    ├ core/
        ├ config.py
        ├ database.py
        └ dependecies.py
    ├ log/  // 운영 시에만 생성
        ├ db/
            └ db_logger.log
        ├ schedule/
            └ schedule_logger.log
        └ web/
            └ web_logger.log
    ├ model/
        └ sql.py
    ├ repository/
        ├ api_repository.py
        └ respository.py
    ├ service/
        ├ impl/
            ├ service_impl.py
            └ weather_service_impl.py
        ├ service.py
        └ weather_service.py
    ├ util/
        ├ convert.py
        ├ logger.py
        ├ response.py
        └ result_code.py
    ├ start_apps.sh
    ├ log_auto_delete_main.py
    ├ schedule_main.py
    └ web_main.py
├ .env
├ .gitignore
├ favicon.ico
├ requirements.txt
└ README.md
```

## 6. 주요기능
1. 스케줄링
- 주기적으로 API를 호출하기 위한 30분 간격의 1일 총 48개의 스케줄링 실행
2. 공공데이터 API 호출 및 데이터 가공
- basetime에 해당하는 API 호출 및 데이터 가공 처리
3. DB Connect 및 데이터 Insert, Select
- 가공한 데이터 DB에 Insert, 최신 날씨 정보 Select
4. (웹서버) 최신 날씨 정보 전달
- 클라이언트로부터 API호출 시 최신 날씨 정보 전송

## 7. API Docs
- /docs#/

## 8. 패치노트
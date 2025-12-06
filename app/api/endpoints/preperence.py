from fastapi import APIRouter, Depends, Form

from model.preperence import PreperenceData
from model.station import StationData
from service.preperence_service import PreperenceService
from core.dependencies import get_perperence_service

router = APIRouter(
    prefix='/preperence',
    tags=['preperence']
)

# 설정값 조회
@router.post('/getPreperenceValue.do')
def get_preperence_value(item: PreperenceData, preperence_service: PreperenceService = Depends(get_perperence_service)):
    return preperence_service.get_preperence_value(item.key)

# DISPLAY_STATUS 스위칭
@router.get('/switchingDisplayStatus.do')
def swithing_display_status(preperence_service: PreperenceService = Depends(get_perperence_service)):
    return preperence_service.switching_display_status()

# 현재 측정소 정보 조회
@router.get('/getStationInfo.do')
def get_station_info(preperence_service:PreperenceService = Depends(get_perperence_service)):
    return preperence_service.get_station_info()
    
# 측정소 시/도 목록 조회
@router.get('/getProvinceList.do')
def get_province_list(preperence_service:PreperenceService = Depends(get_perperence_service)):
    return preperence_service.get_province_list()

# 구/군/시 목록 조회
@router.post('/getRegionList.do')
def get_region_list(params: StationData, preperence_service:PreperenceService = Depends(get_perperence_service)):
    return preperence_service.get_region_list(params)

# 측정소 정보 수정 등록
@router.post('/changeStationInfo.do')
def change_station_info(params: StationData, preperence_service: PreperenceService = Depends(get_perperence_service)):
    return preperence_service.change_station_info(params)

# 현재 등록된 이미지 조회
@router.get('/getUploadedImage.do')
def get_uploaded_image(preperence_service:PreperenceService = Depends(get_perperence_service)):
    return preperence_service.get_uploaded_image()

# 디지털 액자용 이미지 등록
@router.post('/uploadImage.do')
def upload_image(preperence_service:PreperenceService = Depends(get_perperence_service)):
    return preperence_service.upload_image()
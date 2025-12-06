from abc import ABC, abstractmethod
from typing import Any

class PreperenceService(ABC):
    # 설정값 조회
    def get_preperence_value(self, key) -> Any: ...
    
    # DISPLAY_STATUS 스위칭
    def switching_display_status(self) -> Any: ...
    
    # 현재 측정소 정보 조회
    def get_station_info(self) -> Any: ...

    # 측정소 시/도 목록 조회
    def get_province_list(self) -> Any: ...

    # 구/군/시 목록 조회
    def get_region_list(self, params) -> Any: ...

    # 측정소 정보 수정 등록
    def change_station_info(self, params) -> Any: ...

    # 현재 등록된 이미지 조회
    def get_uploaded_image(self) -> Any: ...

    # 디지털 액자용 이미지 등록
    def upload_image(self) -> Any: ...
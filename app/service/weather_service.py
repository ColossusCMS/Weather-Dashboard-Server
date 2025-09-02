from abc import ABC, abstractmethod
from typing import Any

class WeatherService(ABC):
    # 최신 날씨 정보 조회
    @abstractmethod
    def get_current_weather_data(self) -> Any: ...
    
    @abstractmethod
    def refresh_weather_data(self, basetime: str) -> Any: ...
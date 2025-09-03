from fastapi import APIRouter, Depends

from service.weather_service import WeatherService
from core.dependencies import get_weather_service

router = APIRouter(
    prefix='/weather',
    tags=['weather']
)

# 최신 날씨 정보 조회
@router.get('/getRecentWeatherData.do')
def get_recent_weather_data(weather_service: WeatherService = Depends(get_weather_service)):
    return weather_service.get_current_weather_data()

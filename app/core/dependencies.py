from service.weather_service import WeatherService
from service.preperence_service import PreperenceService
from service.impl.weather_service_impl import WeatherServiceImpl
from service.impl.preperence_service_impl import PreperenceServiceImpl

def get_weather_service() -> WeatherService:
    return WeatherServiceImpl()

def get_perperence_service() -> PreperenceService:
    return PreperenceServiceImpl()
from service.weather_service import WeatherService
from service.impl.weather_service_impl import WeatherServiceImpl

def get_weather_service() -> WeatherService:
    return WeatherServiceImpl()
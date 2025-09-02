from app.service.weather_service import WeatherService
from app.service.impl.weather_service_impl import WeatherServiceImpl

def get_weather_service() -> WeatherService:
    return WeatherServiceImpl()
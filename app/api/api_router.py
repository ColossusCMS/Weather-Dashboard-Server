from fastapi import APIRouter

from api.endpoints.weather import router as weather_router

routers = APIRouter()
router_list = [weather_router]

for router in router_list:
    # router.tags = routers.tags.append('v1')
    routers.include_router(router)
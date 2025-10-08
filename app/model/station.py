from pydantic import BaseModel

class StationData(BaseModel):
    province: str
    region: str
from pydantic import BaseModel

class GetOrgByTitle(BaseModel):
    title: str
    
class GetOrgsByAddress(BaseModel):
    city: str | None = None
    street_title: str | None = None
    house_num: str | None = None
    lat: float | None = None
    lng: float | None = None
    
class GetOrgsByActivity(BaseModel):
    activity: str
    
class GetOrgsInRadius(BaseModel):
    lat: float
    lng: float
    radius: int
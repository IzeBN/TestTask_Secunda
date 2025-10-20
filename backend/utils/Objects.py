from pydantic import BaseModel

class CoordinatesObject(BaseModel):
    lat: float
    lng: float

class AddressObject(BaseModel):
    city: str
    street_title: str
    house_num: str
    coordinates: CoordinatesObject
    
class ContactObject(BaseModel):
    type: str
    value: str
    
class OrganizationObject(BaseModel):
    id: int
    title: str
    address: AddressObject
    contacts: list[ContactObject] | None = None
    activities: list[str] | None = None
    
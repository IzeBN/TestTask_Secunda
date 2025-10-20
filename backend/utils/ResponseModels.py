from pydantic import BaseModel

from . import Objects as obj

class OrganizationResponse(BaseModel):
    organization: obj.OrganizationObject | None
    
class OrganizationListResponse(BaseModel):
    organizations: list[obj.OrganizationObject] | None
    
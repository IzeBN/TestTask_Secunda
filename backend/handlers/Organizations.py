from fastapi import APIRouter, Depends, HTTPException

from backend.utils import verify, responses, requests

from config import config

db = config.database.model

router = APIRouter(prefix='/organizations', 
                   tags=['Организации'], 
                   dependencies=[Depends(verify.api_key)])

@router.get('/{organization_id}', response_model=responses.OrganizationResponse, name='Получить организацию по ID')
async def get_org_by_id(organization_id: int):
    org = await db.find_organization(organization_id)
    if not org: raise HTTPException(404, 'Organization not found')
    
    return { 'organization': org }

@router.post('/', response_model=responses.OrganizationResponse, name='Получить организацию по наименованию')
async def get_org_by_title(req: requests.GetOrgByTitle):
    org = await db.find_organization(req.title)
    if not org: raise HTTPException(404, 'Organization not found')
    
    return { 'organization': org }

@router.post('/address', response_model=responses.OrganizationListResponse, name='Организации в здании')
async def get_orgs_by_address(req: requests.GetOrgsByAddress):
    """### Передается либо адрес, либо координаты. При наличии всех данных в приоритете координаты"""
    if not all([req.city, req.house_num, req.street_title]) and \
        not all([req.lat, req.lng]): raise HTTPException(400)
    orgs = await db.find_organizations_by_address(req.city, req.street_title, req.house_num, req.lat, req.lng)
    if not orgs: raise HTTPException(404)
    
    return {'organizations': orgs}

@router.post('/activities', response_model=responses.OrganizationListResponse, name='Организации по деятельностям')
async def get_orgs_by_activity(req: requests.GetOrgsByActivity):
    orgs = await db.find_organizations_by_activity(req.activity)
    if not orgs: raise HTTPException(404)
    
    return {'organizations': orgs}

@router.post('/radius', response_model=responses.OrganizationListResponse, name='Организации в радиусе координат')
async def get_orgs_in_radius(req: requests.GetOrgsInRadius):
    """### Радиус в метрах"""
    orgs = await db.find_organizations_in_radius(req.lat, req.lng, req.radius)
    if not orgs: raise HTTPException(404)
    
    return {'organizations': orgs}
    

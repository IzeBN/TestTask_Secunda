import asyncpg, json

from contextlib import asynccontextmanager

from .utils import q

class Database:
    def __init__(self, dsn: str):
        self.db: asyncpg.Pool = None
        self.dsn: str = dsn

    async def __connect(self):
        if self.db: return
        self.db = await asyncpg.create_pool(self.dsn, min_size=10, max_size=100)

    async def _ensure_connected(self):
        if self.db is None: await self.__connect()
        

    @asynccontextmanager
    async def connection(self):
        await self._ensure_connected()
        conn = await self.db.acquire()
        try: yield conn
        finally: await self.db.release(conn)
    
    @asynccontextmanager
    async def transaction(self):
        await self._ensure_connected()
        async with self.db.acquire() as conn:
            async with conn.transaction():
                yield conn
                
    async def create_tables(self):
        async with self.transaction() as conn:
            await conn.execute(q.CREATE_TABLES)
            
    async def organization_to_dict(self, org):
        result = dict(org)
        result['address'], result['contacts'] = json.loads(result['address']), json.loads(result['contacts'])
        return result 
    
    async def find_organization(self, data: str | int):
        """### Получить организацию по ID или названию"""
        async with self.connection() as conn:
            params = (data, None) if isinstance(data, int) else (None, data)
            org = await conn.fetchrow(q.org.FIND_BY_ID_OR_TITLE, *params)
            return None if not org else await self.organization_to_dict(org)
        
    async def find_organizations_by_address(self, city: str | None = None,
                                            street: str | None = None,
                                            house_num: str | None = None,
                                            lat: float | None = None, lng: float | None = None):
        """### Получить все организации в одном здании
        Широта и долгота имеют приоритет."""
        async with self.connection() as conn:
            orgs = await conn.fetch(q.org.FIND_BY_FULL_ADDRESS, str(lat or city), str(lng or street), house_num)
            return None if not orgs else [await self.organization_to_dict(org) for org in orgs]

    async def find_organizations_by_activity(self, activity: str):
        async with self.connection() as conn:
            orgs = await conn.fetch(q.org.FIND_BY_ACTIVITIES, activity)
            return None if not orgs else [await self.organization_to_dict(org) for org in orgs]
            
    async def find_organizations_in_radius(self, lat: float, lng: float, radius: int):
        """### Получить организации в заданом радиусе
        Радиус в метрах"""
        async with self.connection() as conn:
            orgs = await conn.fetch(q.org.FIND_ALL_IN_RADIUS, lat, lng, radius)
            return None if not orgs else [await self.organization_to_dict(org) for org in orgs]
        
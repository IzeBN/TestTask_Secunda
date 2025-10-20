from typing import NamedTuple

from database import Database

class DatabaseConf(NamedTuple):
    dsn: str
    model: Database
    
    
class Config(NamedTuple):
    database: DatabaseConf
    api_token: str = 'TEST_TOKEN'
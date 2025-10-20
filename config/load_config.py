from .models import Config, DatabaseConf

from dotenv import load_dotenv
import os

from database import Database

load_dotenv()

config = Config(
    database=DatabaseConf(
        dsn=os.getenv('DB_DSN') or '',
        model=Database(os.getenv('DB_DSN') or '')
    )
)
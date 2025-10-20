from fastapi import FastAPI

from backend import r

app = FastAPI()

app.include_router(r.Organizations.router)
    
    
    


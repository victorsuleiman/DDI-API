from fastapi import FastAPI

from routers.zones import router as zones_router

from routers.records import router as records_router

app = FastAPI(title="DDI API")

app.include_router(zones_router)

app.include_router(records_router)
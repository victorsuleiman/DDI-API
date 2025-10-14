from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime

from models.zone import Zone

app = FastAPI(title="DDI API")

DB: dict[int, Zone] = {}

#Zone CRUD
@app.get("/zones")
def list_zones():
    return list(DB.values())

@app.post("/zones", status_code=201)
def create_zone(zone: Zone):
    if zone.id in DB:
        raise HTTPException(status_code=409, detail="Item exists")
    DB[zone.id] = zone
    return zone

@app.get("/zones/{zone_id}")
def get_zone_by_id(zone_id: int):
    if zone_id not in DB:
        raise HTTPException(status_code=404, detail="Not found")
    return DB[zone_id]

@app.get("/zones/by-name/{zone_name}")
def get_zone_by_name(zone_name: str):
    for zone in DB.values():
        if zone.name == zone_name:
            return zone
    raise HTTPException(status_code=404, detail="Not found")

@app.put("/zones/{zone_id}")
def update_zone(zone_id: int, zone: Zone):
    if zone_id not in DB:
        raise HTTPException(status_code=404, detail="Not found")
    DB[zone_id] = zone
    return zone

@app.delete("/zones/{zone_id}", status_code=204)
def delete_zone(zone_id: int):
    if zone_id not in DB:
        raise HTTPException(status_code=404, detail="Not found")
    del DB[zone_id] 

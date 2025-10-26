from fastapi import APIRouter, HTTPException

from models.zone import Zone

router = APIRouter(prefix="/zones", tags=["zones"])

DB: dict[int, Zone] = {}

@router.get("", status_code=200)
def list_zones():
    return list(DB.values())

#TODO: test for all validations with bad and good examples
@router.post("", status_code=201)
def create_zone(zone: Zone):
    if zone.id in DB:
        raise HTTPException(status_code=409, detail="Item exists")
    if _name_exists(zone.name):
        raise HTTPException(409, "Zone name already exists")
    DB[zone.id] = zone
    return zone


@router.get("/{zone_id}", status_code=200)
def get_zone_by_id(zone_id: int):
    if zone_id not in DB:
        raise HTTPException(status_code=404, detail="Not found")
    return DB[zone_id]


@router.get("/by-name/{zone_name}")
def get_zone_by_name(zone_name: str):
    for zone in DB.values():
        if zone.name == zone_name:
            return zone
    raise HTTPException(status_code=404, detail="Not found")


@router.put("/{zone_id}")
def update_zone(zone_id: int, zone: Zone):
    if zone_id not in DB:
        raise HTTPException(status_code=404, detail="Not found")
    DB[zone_id] = zone
    return zone


@router.delete("/{zone_id}", status_code=204)
def delete_zone(zone_id: int):
    if zone_id not in DB:
        raise HTTPException(status_code=404, detail="Not found")
    del DB[zone_id]


def _name_exists(name: str, exclude_id: int | None = None) -> bool:
    for z in DB.values():
        if z.name == name and z.id != exclude_id:
            return True
    return False

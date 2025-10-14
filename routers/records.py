from fastapi import APIRouter, HTTPException

from models.record import Record

router = APIRouter(prefix="/records", tags=["records"])

DB: dict[int, Record] = {}

@router.get("")
def list_records():
    return list(DB.values())

#TODO add validation: zone_id is the foreign key. if zone_id doesn't exist in zones, the appropriate HTTP error should be thrown.
@router.post("", status_code=201)
def create_zone(record: Record):
    if record.id in DB:
        raise HTTPException(status_code=409, detail="Item exists")
    DB[record.id] = record
    return record


@router.get("/{record_id}")
def get_record_by_id(record_id: int):
    if record_id not in DB:
        raise HTTPException(status_code=404, detail="Not found")
    return DB[record_id]


@router.get("/by-name/{record_name}")
def get_record_by_name(record_name: str):
    for record in DB.values():
        if record.name == record_name:
            return record
    raise HTTPException(status_code=404, detail="Not found")

@router.get("/by-type/{record_type}")
def get_record_by_type(record_type: str):
    for record in DB.values():
        if record.type == record_type:
            return record
    raise HTTPException(status_code=404, detail="Not found")


@router.put("/{record_id}")
def update_record(record_id: int, record: Record):
    if record_id not in DB:
        raise HTTPException(status_code=404, detail="Not found")
    DB[record_id] = record
    return record


@router.delete("/{record_id}", status_code=204)
def delete_zone(record_id: int):
    if record_id not in DB:
        raise HTTPException(status_code=404, detail="Not found")
    del DB[record_id]

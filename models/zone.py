from pydantic import BaseModel


class SOA(BaseModel):
    primary_ns : str
    admin_email : str
    serial : int
    refresh : int
    retry: int 
    expire : int
    minimum : int

class Zone(BaseModel):
    id: int
    name: str
    kind : str
    default_ttl : int
    nameservers : list[str]
    soa : SOA
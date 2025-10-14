from pydantic import BaseModel
from typing import Optional, Literal

class Record(BaseModel):
    id: int
    zone_id: int              # “foreign key” to Zone.id (no DB rules yet)
    name: str                 # "" for apex, or "www", "api", etc.
    type: Literal["A","AAAA","CNAME","MX","NS","TXT","SRV","CAA","PTR"]
    ttl: Optional[int] = None # None => use zone.default_ttl when you answer/serve
    # generic payload
    data: Optional[str] = None
    # type-specific (unused unless needed)
    preference: Optional[int] = None  # MX
    exchange: Optional[str] = None    # MX
    priority: Optional[int] = None    # SRV
    weight: Optional[int] = None      # SRV
    port: Optional[int] = None        # SRV
    target: Optional[str] = None      # SRV
    flags: Optional[int] = None       # CAA
    tag: Optional[str] = None         # CAA
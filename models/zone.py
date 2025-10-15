#logic to create a Zone object. 
#A Zone is a specific portion of the Domain Name System (DNS) namespace that an administrator or organization manages, containing the DNS records for that domain.

from pydantic import BaseModel, field_validator, model_validator
from typing import Literal
from .validators_dns import is_fqdn, canonical_zone_name, canonical_fqdn

class SOA(BaseModel):
    primary_ns : str
    admin_email : str
    serial : int
    refresh : int
    retry: int 
    expire : int
    minimum : int

    @field_validator("primary_ns", "admin_email")
    @classmethod
    def _fqdn_like(cls, v: str):
        if not is_fqdn(v):
            raise ValueError("must be a valid FQDN (e.g., ns1.example.net.)")
        # store canonical with trailing dot
        return canonical_fqdn(v)

    @field_validator("serial")
    @classmethod
    def _serial_positive(cls, v: int):
        if v <= 0:
            raise ValueError("serial must be > 0")
        if v > 2_147_483_647:
            raise ValueError("serial too large (keep ≤ 2_147_483_647)")
        return v

    @field_validator("refresh", "retry", "expire", "minimum")
    @classmethod
    def _positive(cls, v: int, info):
        if v <= 0:
            raise ValueError(f"{info.field_name} must be > 0")
        return v
    

    @model_validator(mode="after")
    def _soa_relationships(self):
        if not (self.retry < self.refresh < self.expire):
            raise ValueError("SOA timing must satisfy retry < refresh < expire")
        if not (300 <= self.minimum <= 86_400):
            raise ValueError("minimum TTL should be between 300 and 86400")
        return self

class Zone(BaseModel):
    id: int
    name: str
    kind : str
    default_ttl : int
    nameservers : list[str]
    soa : SOA

    @field_validator("name")
    @classmethod
    def _zone_name_ok(cls, v: str):
        if not is_fqdn(v):
            raise ValueError("zone name must be a valid FQDN")
        # reverse naming hint (not strict parsing of IP blocks, just suffix check)
        cname = canonical_zone_name(v)
        if cname.endswith("in-addr.arpa") or cname.endswith("ip6.arpa"):
            # if using reverse suffix, kind should be reverse (soft rule—warn or enforce)
            pass
        return canonical_zone_name(v)
    
    @field_validator("default_ttl")
    @classmethod
    def _ttl_range(cls, v: int):
        if not (30 <= v <= 2_592_000):  # 30s .. 30 days
            raise ValueError("default_ttl must be between 30 and 2,592,000 seconds")
        return v

    @field_validator("nameservers")
    @classmethod
    def _ns_list(cls, v: list[str]):
        if len(v) < 2:
            raise ValueError("provide at least two nameservers")
        canon = []
        for ns in v:
            if not is_fqdn(ns):
                raise ValueError(f"invalid nameserver: {ns}")
            canon.append(canonical_fqdn(ns))
        return canon
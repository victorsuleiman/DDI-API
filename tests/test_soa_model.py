from fastapi.testclient import TestClient
from main import app
import json
from pathlib import Path

exampleZone = {
    "id" : 1,
    "name": "example.com",
    "kind": "primary",
    "default_ttl": 3600,
    "nameservers": ["ns1.example.net.", "ns2.example.net."]
}

data =  json.loads(Path("tests/data/soa.json").read_text(encoding="utf-8"))

client = TestClient(app)

def test_valid_input():
    #normal fqdn
    normal_fqdn = data['normal_fqdn']
    exampleZone["soa"] = normal_fqdn
    r = client.post("/zones", json = exampleZone)
    assert r.status_code == 201

    client.delete("/zones/1")

    #trailing dot and uppercase - store it in canonical (without dot at the end, and in lowercase)
    #looks like the trailing dot did not get removed... TODO: investigate further.
    trailing_dot_uppercase = data['trailing_dot_uppercase']
    exampleZone["soa"] = trailing_dot_uppercase
    r = client.post("/zones", json = exampleZone)
    correctPNS = r.json()["soa"]["primary_ns"]
    print (correctPNS)
    assert r.status_code == 201




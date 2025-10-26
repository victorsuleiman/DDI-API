from fastapi.testclient import TestClient
from main import app
import json
from pathlib import Path
import copy

client = TestClient(app)

exampleZoneFull = {
    "id" : 1,
    "name": "example.com",
    "kind": "primary",
    "default_ttl": 3600,
    "nameservers": ["ns1.example.net.", "ns2.example.net."],
    "soa": {
        "primary_ns": "example.com.",
        "admin_email": "hostmaster.example.com.",
        "serial": 2025101301,
        "refresh": 7200,
        "retry": 3600,
        "expire": 1209600,
        "minimum": 300
    },
}

def test_empty_get():
    r = client.get("/zones")
    assert r.status_code == 200 and r.json() == []

def test_valid_post_no_text_manip():
    r = client.post("/zones",json=exampleZoneFull)
    assert r.status_code == 201
    assert r.json() == exampleZoneFull

def test_conflicting_post():
    testZone1 = copy.deepcopy(exampleZoneFull)
    testZone1["id"] = 2
    r = client.post("/zones",json=testZone1)
    assert r.status_code == 409

    testZone2 = copy.deepcopy(exampleZoneFull)
    r = client.post("/zones",json=testZone2)
    assert r.status_code == 409

def test_not_empty_get():
    r = client.get("/zones")
    assert r.status_code == 200 and r.json() != []

def test_get_by_id():
    r = client.get(f"/zones/{exampleZoneFull["id"]}")
    assert r.status_code == 200
    r = client.get(f"/zones/99999999")
    assert r.status_code == 404

def test_get_by_name():
    r = client.get(f"/zones/by-name/{exampleZoneFull["name"]}")
    assert r.status_code == 200
    r = client.get(f"/zones/by-name/wrongname")
    assert r.status_code == 404

def test_update():
    testZone = copy.deepcopy(exampleZoneFull)
    testZone["name"] = "demonstration.com"
    r = client.put((f"/zones/{exampleZoneFull["id"]}"),json=testZone)
    assert r.status_code == 200 and r.json() == testZone
    r = client.put("/zones/999999999",json=testZone)
    assert r.status_code == 404

def delete_zone():
    r = client.delete(f"/zones/99999999999")
    assert r.status_code == 404
    r = client.delete(f"/zones/{exampleZoneFull["id"]}")
    assert r.status_code == 204

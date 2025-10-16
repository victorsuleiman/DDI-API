from fastapi.testclient import TestClient
from main import app
import json
from pathlib import Path
import copy

exampleZone = {
    "id" : 1,
    "name": "example.com",
    "kind": "primary",
    "default_ttl": 3600,
    "nameservers": ["ns1.example.net.", "ns2.example.net."]
}

exampleZoneFull = {
    "id" : 1,
    "name": "example.com",
    "kind": "primary",
    "default_ttl": 3600,
    "nameservers": ["ns1.example.net.", "ns2.example.net."],
    "soa": {
        "primary_ns": "example.com",
        "admin_email": "hostmaster.example.com.",
        "serial": 2025101301,
        "refresh": 7200,
        "retry": 3600,
        "expire": 1209600,
        "minimum": 300
    },
}

data_positive =  json.loads(Path("tests/data/soa_positive.json").read_text(encoding="utf-8"))

client = TestClient(app)

def test_valid_input_primary_ns():

    #normal fqdn
    r = client.post("/zones", json = exampleZoneFull)
    assert r.status_code == 201
    client.delete("/zones/1")

    testZone = copy.deepcopy(exampleZoneFull)

    # uppercase - store it in canonical (in lowercase, dot at the end allowed)
    testZone["soa"]["primary_ns"] = "ExaMple.cOm."
    r = client.post("/zones", json = testZone)
    correctPNS = r.json()["soa"]["primary_ns"]
    assert r.status_code == 201 and correctPNS.islower()
    client.delete("/zones/1")

# 2-point Boundary-value analysis for serial
def test_valid_input_serial():

    testZone = exampleZoneFull
    testZone["soa"]["serial"] = 1
    serial = 1
    r = client.post("/zones", json = testZone)
    correctSerial = r.json()["soa"]["serial"]
    assert r.status_code == 201 and correctSerial == serial

    client.delete("/zones/1")

    serial = 2_147_483_646
    testZone["soa"]["serial"] = 2_147_483_646
    r = client.post("/zones", json = testZone)
    correctSerial = r.json()["soa"]["serial"]
    assert r.status_code == 201 and correctSerial == serial

    client.delete("/zones/1")

    serial = 2_147_483_647
    testZone["soa"]["serial"] = 2_147_483_647
    r = client.post("/zones", json = testZone)
    correctSerial = r.json()["soa"]["serial"]
    assert r.status_code == 201 and correctSerial == serial

    client.delete("/zones/1")

def test_valid_input_refresh_plus_3():
    correctValues = [2, 1, 3, 500]
    test_case = data_positive['refresh+3_positive']
    exampleZone["soa"] = test_case
    r = client.post("/zones", json = exampleZone)
    correctValuesR = [r.json()["soa"]["refresh"], r.json()["soa"]["retry"], r.json()["soa"]["expire"], r.json()["soa"]["minimum"]]
    
    assert r.status_code == 201 and correctValues == correctValuesR

    client.delete("/zones/1")





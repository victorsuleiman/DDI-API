from fastapi.testclient import TestClient
from main import app
from pathlib import Path
import json

client = TestClient(app)
payload = json.loads(Path("zone_example.json").read_text(encoding="utf-8"))
client.post("/zones", json = payload)
def test_root(client):
    r = client.get("/")
    assert r.status_code == 200 and r.get_json()["status"] == "running"
def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200 and r.get_json() == {"status": "healthy"}
def test_api_health(client):
    r = client.get("/api/health")
    assert r.status_code == 200 and r.get_json()["status"] == "healthy"


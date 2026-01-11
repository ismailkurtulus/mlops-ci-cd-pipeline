from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_predict_endpoint():
    response = client.post(
        "/predict",
        json={"user_id": "u1", "item_id": "i1"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "prediction" in data

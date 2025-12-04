import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# Sample customer data
def sample_customer():
    return {"name": "John Doe"}

def test_add_customer():
    response = client.post("/api/v1/customer", json=sample_customer())
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "John Doe"
    assert "id" in data

def test_get_customer():
    # Add customer first
    post_resp = client.post("/api/v1/customer", json=sample_customer())
    customer_id = post_resp.json()["id"]
    get_resp = client.get(f"/api/v1/customer/{customer_id}")
    assert get_resp.status_code == 200
    data = get_resp.json()
    assert data["id"] == customer_id
    assert data["name"] == "John Doe"

def test_patch_customer():
    post_resp = client.post("/api/v1/customer", json=sample_customer())
    customer_id = post_resp.json()["id"]
    patch_data = {"name": "Jane Doe"}
    patch_resp = client.patch(f"/api/v1/customer/{customer_id}", json=patch_data)
    assert patch_resp.status_code == 200
    data = patch_resp.json()
    assert data["name"] == "Jane Doe"

def test_delete_customer():
    post_resp = client.post("/api/v1/customer", json=sample_customer())
    customer_id = post_resp.json()["id"]
    del_resp = client.delete(f"/api/v1/customer/{customer_id}")
    assert del_resp.status_code == 200
    assert del_resp.json()["detail"] == "Customer deleted"
    # Ensure customer is deleted
    get_resp = client.get(f"/api/v1/customer/{customer_id}")
    assert get_resp.status_code == 404

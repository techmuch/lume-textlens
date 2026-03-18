import pytest
from fastapi.testclient import TestClient
from main import app
from src.processor import TextProcessor

client = TestClient(app)

def test_phi_masking_unit():
    processor = TextProcessor(policy="no-phi")
    input_text = "Call me at 555-0199 or maybe 555-555-0199"
    result = processor.analyze(input_text)
    
    assert result["has_violation"] is True
    assert len(result["violations"]) == 2
    assert result["violations"][0]["type"] == "Phone Number"

def test_phi_masking_ssn():
    processor = TextProcessor(policy="no-phi")
    input_text = "My SSN is 123-45-6789"
    result = processor.analyze(input_text)
    
    assert result["has_violation"] is True
    assert result["violations"][0]["match"] == "123-45-6789"

def test_clean_text():
    processor = TextProcessor(policy="no-phi")
    input_text = "I am a normal person writing a normal biography."
    result = processor.analyze(input_text)
    
    assert result["has_violation"] is False
    assert len(result["violations"]) == 0
    assert result["score"] == 1.0

def test_api_endpoint_clean():
    response = client.post(
        "/analyze",
        json={"text": "Just a regular sentence.", "policy": "no-phi"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["has_violation"] is False
    assert data["score"] == 1.0
    assert "inference_time_ms" in data

def test_api_endpoint_violation():
    response = client.post(
        "/analyze",
        json={"text": "Contact me at 555-1234.", "policy": "no-phi"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["has_violation"] is True
    assert data["score"] < 1.0
    assert len(data["violations"]) > 0

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert "Lume" in response.json()["message"]

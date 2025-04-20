import pytest
from ..tests.conftest import client

print("test_API_model.py --- imporst done")

def test_request_example(client):
    response = client.get("/")
    print("response", response)
    assert response.status_code == 200
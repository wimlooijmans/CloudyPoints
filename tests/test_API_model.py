import pytest
from ..tests.conftest import client

def test_request_home(client):
    response = client.get("/")
    print("response", response)
    assert response.status_code == 200
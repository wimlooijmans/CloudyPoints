import pytest
from ..tests.conftest import client


def test_request_home(client):
    """
    Test if homepage is available and returns response code 200
    """
    response = client.get("/")
    print("response", response)
    assert response.status_code == 200


def test_predict_image(client):
    """
    Test if image can be uploaded to /predict and image is returned
    """

    image = "src/berlin_000000_000019_left_image.png"
    data = {"image": (open(image, "rb"), image)}
    response = client.post("/predict", data=data)

    assert response.status_code == 201
    assert response.headers["Content-Type"] == "image/png"

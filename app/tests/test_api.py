from uuid import UUID

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_healthz():
    response = client.get("/healthz")

    assert response.status_code == 200
    assert response.json() == {"status": "alive"}


def test_ready():
    response = client.get("/ready")

    assert response.status_code == 200
    assert response.json() == {"status": "ready"}


def test_create_order():
    response = client.post(
        "/orders",
        json={
            "product": "laptop",
            "quantity": 2,
        },
    )

    assert response.status_code == 201

    body = response.json()

    assert UUID(body["id"])
    assert body["product"] == "laptop"
    assert body["quantity"] == 2
    assert body["status"] == "CREATED"


def test_get_order():
    create_response = client.post(
        "/orders",
        json={
            "product": "keyboard",
            "quantity": 1,
        },
    )

    order_id = create_response.json()["id"]

    response = client.get(f"/orders/{order_id}")

    assert response.status_code == 200
    assert response.json()["id"] == order_id


def test_get_nonexistent_order():
    response = client.get(
        "/orders/550e8400-e29b-41d4-a716-446655440000"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "order not found"


def test_create_order_with_invalid_quantity():
    response = client.post(
        "/orders",
        json={
            "product": "laptop",
            "quantity": 0,
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "quantity must be greater than zero"
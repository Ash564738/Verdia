from io import BytesIO

from fastapi.testclient import TestClient
from PIL import Image

from app.main import app


client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_diagnose_image() -> None:
    image = Image.new("RGB", (64, 64), "green")
    pixels = image.load()
    for y in range(64):
        for x in range(64):
            pixels[x, y] = (35 + (x % 40), 120 + (y % 60), 45)
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    response = client.post(
        "/api/v1/diagnose",
        files={"file": ("leaf.png", buffer.getvalue(), "image/png")},
    )
    assert response.status_code == 200
    assert response.json()["model"]["version"] == "1.0.0"
    assert response.json()["status"] in {"diagnosed", "healthy", "uncertain", "unsupported_crop", "unknown_disease"}


def test_qa() -> None:
    response = client.post("/api/v1/qa", json={"question": "How often should I water?"})
    assert response.status_code == 200
    assert "Water" in response.json()["answer"]


def test_diagnose_root() -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["docs"] == "/docs"


def test_dashboard_after_login() -> None:
    email = "dashboard-test@example.com"
    register = client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": "password123", "name": "Dashboard Test"},
    )
    if register.status_code == 409:
        login = client.post("/api/v1/auth/login", json={"email": email, "password": "password123"})
    else:
        login = register
    token = login.json()["access_token"]
    response = client.get(
        "/api/v1/analytics/dashboard",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert "total_plants" in response.json()


def test_plant_catalog_contains_only_supported_species() -> None:
    response = client.get("/api/v1/plants")
    assert response.status_code == 200
    assert len(response.json()) == 14
    assert {item["id"] for item in response.json()} == {
        "Apple", "Bell pepper", "Blueberry", "Cherry", "Corn", "Grape", "Orange",
        "Peach", "Potato", "Raspberry", "Soybean", "Squash",
        "Strawberry", "Tomato",
    }


def test_disease_library_has_all_model_classes() -> None:
    response = client.get("/api/v1/diseases")
    assert response.status_code == 200
    assert len(response.json()) >= 38


def test_private_user_data_is_not_visible_cross_user() -> None:
    first = client.post(
        "/api/v1/auth/register",
        json={"email": "owner-test@example.com", "password": "password123", "name": "Owner"},
    )
    if first.status_code == 409:
        first = client.post(
            "/api/v1/auth/login",
            json={"email": "owner-test@example.com", "password": "password123"},
        )
    owner_token = first.json()["access_token"]

    second = client.post(
        "/api/v1/auth/register",
        json={"email": "other-test@example.com", "password": "password123", "name": "Other"},
    )
    if second.status_code == 409:
        second = client.post(
            "/api/v1/auth/login",
            json={"email": "other-test@example.com", "password": "password123"},
        )
    other_token = second.json()["access_token"]

    created = client.post(
        "/api/v1/my-plants",
        json={"name": "Private Plant", "species": "Tomato"},
        headers={"Authorization": f"Bearer {owner_token}"},
    )
    assert created.status_code == 201
    plant_id = created.json()["id"]

    denied = client.get(
        f"/api/v1/my-plants/{plant_id}",
        headers={"Authorization": f"Bearer {other_token}"},
    )
    assert denied.status_code == 404

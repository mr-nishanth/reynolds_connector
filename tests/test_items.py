def test_list_items_returns_sample_items(client):
    response = client.get("/api/v1/items")
    assert response.status_code == 200
    items = response.json()
    assert isinstance(items, list)
    assert len(items) >= 1
    for item in items:
        assert set(item) == {"id", "name", "description", "price"}


def test_get_existing_item(client):
    response = client.get("/api/v1/items/1")
    assert response.status_code == 200
    body = response.json()
    assert body["id"] == 1
    assert isinstance(body["name"], str)


def test_get_unknown_item_returns_404(client):
    response = client.get("/api/v1/items/99999")
    assert response.status_code == 404


def test_get_item_with_zero_id_returns_422(client):
    response = client.get("/api/v1/items/0")
    assert response.status_code == 422


def test_get_item_with_non_integer_id_returns_422(client):
    response = client.get("/api/v1/items/abc")
    assert response.status_code == 422


def test_create_item_returns_201_and_is_retrievable(client):
    payload = {"name": "Test Item", "description": "desc", "price": 12.5}
    response = client.post("/api/v1/items", json=payload)
    assert response.status_code == 201
    created = response.json()
    assert created["name"] == "Test Item"
    assert created["description"] == "desc"
    assert created["price"] == 12.5
    assert isinstance(created["id"], int)

    fetched = client.get(f"/api/v1/items/{created['id']}")
    assert fetched.status_code == 200
    assert fetched.json() == created


def test_create_item_without_description(client):
    response = client.post("/api/v1/items", json={"name": "No Desc", "price": 1})
    assert response.status_code == 201
    assert response.json()["description"] is None


def test_create_item_missing_name_returns_422(client):
    response = client.post("/api/v1/items", json={"price": 1.0})
    assert response.status_code == 422


def test_create_item_empty_name_returns_422(client):
    response = client.post("/api/v1/items", json={"name": "", "price": 1.0})
    assert response.status_code == 422


def test_create_item_negative_price_returns_422(client):
    response = client.post("/api/v1/items", json={"name": "Bad", "price": -1})
    assert response.status_code == 422


def test_create_item_wrong_price_type_returns_422(client):
    response = client.post("/api/v1/items", json={"name": "Bad", "price": "free"})
    assert response.status_code == 422


def test_create_item_missing_body_returns_422(client):
    response = client.post("/api/v1/items")
    assert response.status_code == 422

import io
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

from app.main import app

client = TestClient(app)


# Мок для save_file, щоб не залучати AWS
@pytest.fixture(autouse=True)
def mock_save_file():
    with patch("app.main.save_file") as mock_func:
        mock_func.return_value = "/media/test.jpg"
        yield mock_func


# Тест: створення друга без обов'язкових полів
def test_create_friend_without_required_fields():
    response = client.post("/friends", data={})
    assert response.status_code == 422  # ValidationError через Form(...)


# Тест: створення друга з валідним фото
def test_create_friend_with_photo():
    file_content = io.BytesIO(b"fake image data")
    files = {"photo": ("test.jpg", file_content, "image/jpeg")}
    data = {"name": "Kolya", "profession": "Developer"}

    response = client.post("/friends", data=data, files=files)
    assert response.status_code == 200 or response.status_code == 201
    json_data = response.json()
    assert json_data["name"] == "Kolya"
    assert json_data["profession"] == "Developer"
    assert json_data["photo_url"] == "/media/test.jpg"
    assert "id" in json_data

    client.delete(f"/friends/{response.json()['id']}")


# Тест: отримання списку друзів
def test_list_friends():
    # Створимо друга для перевірки списку
    file_content = io.BytesIO(b"fake image data")
    files = {"photo": ("test2.jpg", file_content, "image/jpeg")}
    data = {"name": "TestFriend", "profession": "Tester"}

    client.post("/friends", data=data, files=files)

    response = client.get("/friends")
    assert response.status_code == 200
    friends = response.json()
    assert isinstance(friends, list)
    assert any(f["name"] == "TestFriend" for f in friends)

    # Видалення тестових друзів
    for friend in friends:
        if friend["name"] == "TestFriend":
            client.delete(f"/friends/{friend['id']}")


# Тест: отримання конкретного друга по id
def test_get_friend():
    # Створимо друга
    file_content = io.BytesIO(b"fake image data")
    files = {"photo": ("test3.jpg", file_content, "image/jpeg")}
    data = {"name": "FriendID", "profession": "IDTester"}

    post_response = client.post("/friends", data=data, files=files)
    friend_id = post_response.json()["id"]

    # GET по id
    get_response = client.get(f"/friends/{friend_id}")
    assert get_response.status_code == 200
    friend = get_response.json()
    assert friend["id"] == friend_id
    assert friend["name"] == "FriendID"

    # GET неіснуючого id
    bad_response = client.get("/friends/nonexistent-id")
    assert bad_response.status_code == 404

    # Видалення тестового друга
    client.delete(f"/friends/{friend_id}")

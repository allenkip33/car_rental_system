from services.auth import AuthService
from services.data_manager import DataManager


def test_register_user(tmp_path):
    manager = DataManager()
    users_file = tmp_path / "test_users.json"
    auth = AuthService(manager, str(users_file))

    result = auth.register("testuser", "password123")

    assert result is True


def test_login_user(tmp_path):
    manager = DataManager()
    users_file = tmp_path / "test_users.json"
    auth = AuthService(manager, str(users_file))

    auth.register("testuser2", "password123")
    user = auth.login("testuser2", "password123")

    assert user.username == "testuser2"


def test_wrong_password(tmp_path):
    manager = DataManager()
    users_file = tmp_path / "test_users.json"
    auth = AuthService(manager, str(users_file))

    auth.register("testuser3", "password123")
    user = auth.login("testuser3", "wrongpassword")

    assert user is None

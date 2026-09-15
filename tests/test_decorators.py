from services.auth import AuthService
from services.data_manager import DataManager
from models.customer import Customer
from models.admin import Admin
from utils.decorators import login_required, admin_required


def test_login_required_blocks_logged_out_user(capsys):
    manager = DataManager()
    auth = AuthService(manager, "data/test_users.json")

    @login_required(auth)
    def test_function():
        print("Access granted")

    test_function()

    output = capsys.readouterr().out

    assert "Please login first." in output
    assert "Access granted" not in output


def test_login_required_allows_logged_in_user():
    manager = DataManager()
    auth = AuthService(manager, "data/test_users.json")
    auth.current_user = Customer("john", "password_hash")

    @login_required(auth)
    def test_function():
        return "Access granted"

    result = test_function()

    assert result == "Access granted"


def test_admin_required_blocks_customer(capsys):
    manager = DataManager()
    auth = AuthService(manager, "data/test_users.json")
    auth.current_user = Customer("john", "password_hash")

    @admin_required(auth)
    def test_function():
        print("Admin access")

    test_function()

    output = capsys.readouterr().out

    assert "Admin access required." in output
    assert "Admin access\n" not in output


def test_admin_required_allows_admin():
    manager = DataManager()
    auth = AuthService(manager, "data/test_users.json")
    auth.current_user = Admin("admin", "password_hash")

    @admin_required(auth)
    def test_function():
        return "Admin access granted"

    result = test_function()

    assert result == "Admin access granted"
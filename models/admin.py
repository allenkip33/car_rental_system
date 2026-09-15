from models.user import User


class Admin(User):
    def __init__(self, username, password_hash):
        super().__init__(username, password_hash, "Admin")

    def can_manage_cars(self):
        return True

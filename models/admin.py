from models.user import User


class Admin(User):
    # Create an admin
    def __init__(self, username, password_hash):
        super().__init__(username, password_hash, "Admin")

    # Admin can add and remove cars
    def can_manage_cars(self):
        return True

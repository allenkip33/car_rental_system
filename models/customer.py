from models.user import User


class Customer(User):
    def __init__(self, username, password_hash):
        super().__init__(username, password_hash, "Customer")

    def can_rent(self):
        return True

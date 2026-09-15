import hashlib

from models.customer import Customer
from models.admin import Admin


class AuthService:
    def __init__(self,data_manager,users_file):
        self.data_manager = data_manager
        self.users_file = users_file
        self.current_user =None

    def hash_password(self,password):
        return hashlib.sha256(password.encode()).hexdigest()

    def register(self, username, password,role="Customer"):
        users = self.data_manager.load_data(self.users_file)

        for user in users:
            if user["username"] == username:
                return False

        password_hash = self.hash_password(password)

        if role == "Admin":
            user = Admin(username, password_hash)
        else:
            user = Customer(username, password_hash)

        users.append(user.to_dict())
        self.data_manager.save_data(self.users_file, users)

        return True

    def login(self, username,password):
        users = self.data_manager.load_data(self.users_file)
        password_hash = self.hash_password(password)

        for user in users:
            if (
                user["username"] == username
                and user["password_hash"] == password_hash
            ):
                if user["role"] == "Admin" :
                    self.current_user = Admin(username, password_hash)
                else:
                    self.current_user = Customer(username, password_hash)

                return self.current_user

        return None

    def logout(self):
        self.current_user = None

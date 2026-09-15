class User:
    def __init__(self, username, password_hash, role):
        self._username = username
        self._password_hash = password_hash
        self._role = role

    @property
    def username(self):
        return self._username

    @property
    def password_hash(self):
        return self._password_hash

    @property
    def role(self):
        return self._role

    def to_dict(self):
        return {
            "username": self._username,
            "password_hash": self._password_hash,
            "role": self._role
        }

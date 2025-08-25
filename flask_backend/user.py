from flask_login import LoginManager, UserMixin

# from pymongo.database import Collection


class User(UserMixin):
    def __init__(self, email: str, anon=False):
        self.anon = anon
        # id do medico
        self.id = str(email)
        self.active = True

    @staticmethod
    def get_user(email):
        return User(email)

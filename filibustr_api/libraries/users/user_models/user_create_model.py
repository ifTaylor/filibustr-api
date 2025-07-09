from .user_model import UserModel


class UserCreateModel(UserModel):
    password: str

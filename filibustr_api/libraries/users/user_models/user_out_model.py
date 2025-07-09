from .user_model import UserModel


class UserOutModel(UserModel):
    id: int
    is_active: int

    class Config:
        orm_mode = True

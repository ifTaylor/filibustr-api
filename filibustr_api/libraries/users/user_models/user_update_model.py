from pydantic import BaseModel, EmailStr


class UserUpdateModel(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    password: str | None = None

from dataclasses import asdict, dataclass

from src.domain.user.entities import User
from src.infra.auth.jwt import PasswordManager
from src.domain.user.protocols import UserRepo


@dataclass
class LoginCommand: ...


@dataclass
class RegisterUserDto:
    name: str
    surname: str
    username: str
    password: str
    email: str
    

@dataclass
class RegisterCommand:
    user_repo: UserRepo
    password_manager: PasswordManager
    
    async def __call__(self, dto: RegisterUserDto):
        user = await self.user_repo.get_user_by_username(dto.username)
        if user:
            ...
        identity = self.user_repo.new_id()
        password = self.password_manager.hash_password(dto.password)
        print(password)
        item = User.create(identity, **asdict(dto))
        await self.user_repo.register(item)
        return item


@dataclass
class LogoutCommand: ...

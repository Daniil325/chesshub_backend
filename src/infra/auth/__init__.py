from dishka import Provider, Scope, provide

from src.infra.auth.jwt import JWTService, PasswordManager


class JwtProvider(Provider):
    scope = Scope.REQUEST
    
    def __init__(self, settings):
        super().__init__()
        self.settings = settings
        
    @provide
    def get_jwt_service(self) -> JWTService:
        return JWTService(self.settings)
    
    @provide
    def get_password_manager(self) -> PasswordManager:
        return PasswordManager()
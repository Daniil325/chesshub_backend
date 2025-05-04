from dishka import Provider, Scope, provide

from src.application.user.usecases import RegisterCommand, LoginCommand


class UserProvider(Provider):
    scope = Scope.REQUEST
    
    def __init__(self):
        super().__init__()
        
    register_command = provide(RegisterCommand)
    login_command = provide(LoginCommand)
from dishka import Provider, Scope, provide

from src.application.user.usecases import RegisterCommand


class UserProvider(Provider):
    scope = Scope.REQUEST
    
    def __init__(self):
        super().__init__()
        
    register_command = provide(RegisterCommand)
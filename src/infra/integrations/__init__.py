from dishka import Provider, Scope, provide


class IntegrationsProvider(Provider):
    scope = Scope.REQUEST
    
    def __init__(self):
        super().__init__()
        
    @provide
    def get_lichess(self)
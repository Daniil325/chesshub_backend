from dishka import Provider, Scope, provide

from src.application.article.tag import CreateTagCommand, DeleteTagCommand, UpdateTagCommand


class ArticleCommandsProvider(Provider):
    scope = Scope.REQUEST

    def __init__(self):
        super().__init__()

    create_tag_command = provide(CreateTagCommand)
    update_tag_command = provide(UpdateTagCommand)
    delete_tag_command = provide(DeleteTagCommand)

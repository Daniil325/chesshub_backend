from dishka import Provider, Scope, provide

from src.application.article.tag import (
    CreateTagCommand,
    DeleteTagCommand,
    UpdateTagCommand,
)
from src.application.article.article import (
    CreateArticleCommand,
    UpdateArticleCommand,
    DeleteArticleCommand,
)


class ArticleCommandsProvider(Provider):
    scope = Scope.REQUEST

    def __init__(self):
        super().__init__()

    create_tag_command = provide(CreateTagCommand)
    update_tag_command = provide(UpdateTagCommand)
    delete_tag_command = provide(DeleteTagCommand)

    create_article_command = provide(CreateArticleCommand)
    update_article_command = provide(UpdateArticleCommand)
    delete_article_command = provide(DeleteArticleCommand)

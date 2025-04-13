from dishka import Provider, Scope, provide

from src.application.article.category import (
    CreateCategoryCommand,
    UpdateCategoryCommand,
    DeleteCategoryCommand,
)
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
from src.application.article.article_tag import (
    CreateArticleTagCommand,
    UpdateArticleTagCommand,
    DeleteArticleTagCommand,
)
from src.application.article.article_reaction import (
    CreateArticleReactionCommand,
    UpdateArticleReactionCommand,
    DeleteArticleReactionCommand,
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

    create_category_command = provide(CreateCategoryCommand)
    update_category_command = provide(UpdateCategoryCommand)
    delete_category_command = provide(DeleteCategoryCommand)

    create_article_tag_command = provide(CreateArticleTagCommand)
    update_article_tag_command = provide(UpdateArticleTagCommand)
    delete_article_tag_command = provide(DeleteArticleTagCommand)

    create_article_reaction_command = provide(CreateArticleReactionCommand)
    update_article_reaction_command = provide(UpdateArticleReactionCommand)
    delete_article_reaction_command = provide(DeleteArticleReactionCommand)
class AppError(Exception):
    pass


class RepositoryError(AppError):
    pass


class FieldNotFound(AppError):
    pass

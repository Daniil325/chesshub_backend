from sqlalchemy.orm import registry

mapper_registry = registry()
metadata = mapper_registry.metadata

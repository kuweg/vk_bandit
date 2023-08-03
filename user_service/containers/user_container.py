from dependency_injector import containers, providers
from services.user import User


class UserContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    user_service = providers.Singleton(
        User,
        preferences=config,
    )

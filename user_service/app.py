from blueprints import user_routes
from containers.user_container import UserContainer
from flask import Flask
from omegaconf import OmegaConf

# Running inside docker container
PREFERENCES = "configs/widget_preferences.yaml"
APP_CONF = "configs/app.yaml"

# Local runnig
# PREFERENCES = "configs/user_service/widget_preferences.yaml"
# APP_CONF = "configs/user_service/app.yaml"


def create_app(user_preferences: OmegaConf) -> Flask:
    app = Flask(__name__)
    app.register_blueprint(user_routes.user_bp)
    app.logger.setLevel("DEBUG")

    container = UserContainer()
    container.config.from_dict(user_preferences)
    container.wire(modules=[user_routes])

    @app.route("/")
    def health_check():
        return "Server is running"

    return app


if __name__ == "__main__":
    preferences = OmegaConf.load(PREFERENCES)
    app_conf = OmegaConf.load(APP_CONF)
    app = create_app(user_preferences=preferences)
    app.run(
        host=app_conf.user_service.host,
        port=app_conf.user_service.port,
    )

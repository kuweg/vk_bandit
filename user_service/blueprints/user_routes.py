from containers.user_container import UserContainer
from dependency_injector.wiring import Provide, inject
from flask import Blueprint, jsonify, request
from logger import get_logger
from services.user import User

logger = get_logger(name="USER_TIMESPENT", log_filename="timespent.log")

user_bp = Blueprint("user_bp", __name__)


@user_bp.route("/watch", methods=["GET"])
@inject
def show_widgets_to_user(
    service: User = Provide[UserContainer.user_service],
) -> dict:
    """Get request from Agent for gain arm's reward.

    Returns:
        dict: list of timespents for requested widgets.
    """
    widgets = request.get_json()["widgets"]
    widgets_timespent = service.watch_widgets(widgets)
    logger.info(" ".join(map(str, widgets)) + " " + str(sum(widgets_timespent)))
    return jsonify({"timespent": widgets_timespent})

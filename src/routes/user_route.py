from flask import Blueprint, request


user_route = Blueprint("user_route",__name__, url_prefix="/api")
from flask import Blueprint, request


account_route = Blueprint("account_route",__name__, url_prefix="/api/accounts")
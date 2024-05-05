from flask import Blueprint, request


transaction_route = Blueprint("transaction_route",__name__, url_prefix="/api/transactions")
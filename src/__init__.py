from flask import Flask, request


from src.helper.Helper import Helper
from datetime import timedelta
from dotenv import dotenv_values

app = Flask(__name__)
# connection to db
ENV_CONFIG = dotenv_values(".env")
helper = Helper()

from src.routes.user_route import user_route
from src.routes.transaction_route import transaction_route
from src.routes.account_route import account_route

app.register_blueprint(user_route)
app.register_blueprint(account_route)
app.register_blueprint(transaction_route)


@app.route("/", methods =["GET"])
def hello_world():
    if request.method == "GET":
        location_ip = helper.reveal_location(request.remote_addr)
        return helper.response_message(result={
           "result":location_ip
        })

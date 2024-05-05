from webargs import fields, ValidationError, flaskparser, validate
    
# USER PARSERS
REGISTER_REQUESTS= {
    'email': fields.Email(required=True, validate=[validate.Length(min=1, max=9999)]),
    'password': fields.Str(required=True),
    'firstname': fields.Str(required=True),
    'lastname': fields.Str(required=True),
    'phone_number': fields.Str(required=True),
}

LOGIN_REQUESTS= {
    'email': fields.Email(required=True, validate=[validate.Length(min=1, max=9999)]),
    'password': fields.Str(required=True),
}

USER_UPDATE_REQUESTS= {
    'firstname': fields.Str(required=True),
    'lastname': fields.Str(required=True),
    'phone_number': fields.Str(required=True),
}

# ACCOUNT PARSERS
ACCOUNT_UPDATE_REQUESTS= {
    'firstname': fields.Str(required=True),
    'lastname': fields.Str(required=True),
    'phone_number': fields.Str(required=True),
}

ACCOUNT_TRANSACTION_REQUESTS= {
    'amount': fields.Str(required=True),
    'description': fields.Str(required=True),
}

ACCOUNT_TRANSACTION_REQUESTS= {
    'email': fields.Email(required=True, validate=[validate.Length(min=1, max=9999)]),
    'password': fields.Str(required=True),
}


# ACCOUNT PARSERS
SEARCH_TRANSACTION_REQUESTS= {
    'email': fields.Email(required=True, validate=[validate.Length(min=1, max=9999)]),
    'password': fields.Str(required=True),
    'firstname': fields.Str(required=True),
    'lastname': fields.Str(required=True),
    'phone_number': fields.Str(required=True),
}

CREDIT_TRANSACTION_REQUESTS= {
    'firstname': fields.Str(required=True),
    'lastname': fields.Str(required=True),
    'phone_number': fields.Str(required=True),
}

DEBIT_TRANSACTION_REQUESTS= {
    'email': fields.Email(required=True, validate=[validate.Length(min=1, max=9999)]),
    'password': fields.Str(required=True),
    'firstname': fields.Str(required=True),
    'lastname': fields.Str(required=True),
    'phone_number': fields.Str(required=True),
}


FORM_REQS= {
    'email': fields.Email(required=True, validate=[validate.Length(min=1, max=9999)]),
    'password': fields.Str(required=True),
    'firstname': fields.Str(required=True),
    'lastname': fields.Str(required=True),
    'phone_number': fields.Str(required=True),
}

from flask import request,Blueprint
from webargs.flaskparser import use_args
user_route = Blueprint("user_route",__name__, url_prefix="/api")
from src import helper

@user_route.route("/add-register", methods=["POST"])
@use_args(FORM_REQS, location="json")
def add_register(args):
    if request.method=="POST":
        try:
            user = {
                "firstname":args['firstname'],
                "lastname": args['lastname'],
                "email":args['email'],
                "password": args["password"],
                "phone_number":args["phone_number"]
            }
            return helper.response_message(result=user)
        
        except ValidationError:
            raise ValidationError("Issues with your inputs")
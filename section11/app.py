""" EXTERNAL MODULES """
import os
import re
from flask import Flask, jsonify, session
from flask_cors import CORS
from flask_restful import Api
from flask_jwt_extended import JWTManager
""" INTERNAL MODULES """
from db import db
from resources.user import UserRegister, User, UserLogin, UserLogout, TokenRefresh
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from models.user import UserModel
from models.item import ItemModel
from models.store import StoreModel
from blocklist import BLOCKLIST

uri = os.getenv("DATABASE_URL") or "sqlite:///data.db"  # or other relevant config var
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)

# Init app
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = uri or "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True # allows us to see Flask-JWT-specific errors instead of 500 Internal Server errors.
app.config["JWT_BLACKLIST_LOADER"] = True
app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = ["access", "refresh"]
app.config["JWT_SECRET_KEY"] = "rc"
CORS(app)
# app.secret_key = "rc"
api = Api(app)
db.init_app(app)

# Create the DB
@app.before_first_request
def create_tables():
    UserModel.__table__.create(db.session.bind, checkfirst=True)
    StoreModel.__table__.create(db.session.bind, checkfirst=True)
    ItemModel.__table__.create(db.session.bind, checkfirst=True)
    

jwt = JWTManager(app) # this will not create a new endpoint called "/auth"

@jwt.additional_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1: # instead of hard-coding, you should read from a config file or a database.
        return {"is_admin": True}
    return {"is_admin": False}

@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, jwt_payload):
    return jwt_payload["jti"] in BLOCKLIST

@jwt.expired_token_loader
def expired_token_callback():
    """ When flask-jwt-extended recognizes that the token has been expired (lasts 5 minutes), it will call this function to tell the user what message should it sent back to the user telling them that the token is expired. """
    return jsonify({
        "description": "The token has expired.",
        "error": "token_expired"
    }), 401

@jwt.invalid_token_loader # The token they send us in the auth header is not a JWT token
def invalid_token_callback(error):
    return jsonify({
        "description": "Signature verification failed.",
        "error": "invalid_token"
    }), 401

@jwt.unauthorized_loader # They don't send a JWT at all
def missing_token_callback(error):
    return jsonify({
        "description": "Request does not contain an access token.",
        "error": "authorization_required"
    }), 401

@jwt.needs_fresh_token_loader # they send a non-fresh token but the enpoint require a fresh token
def token_not_fresh_callback():
    return jsonify({
        "description": "The token is not fresh.",
        "error": "fresh_token_required"
    }), 401

@jwt.revoked_token_loader # this tells the user has been revoked access to the site.
def revoked_token_callback(jwt_header, jwt_payload):
    return jsonify({
        "description": "The token has been revoked",
        "error": "token_revoked"
    }), 401

# Routes
api.add_resource(Store, "/api/store/<string:name>")
api.add_resource(StoreList, "/api/stores")
api.add_resource(Item, "/api/item/<string:name>")
api.add_resource(ItemList, "/api/items")
api.add_resource(UserRegister, "/api/user/register")
api.add_resource(UserLogin, "/api/user/login")
api.add_resource(UserLogout, "/api/user/logout")
api.add_resource(User, "/api/user/<int:user_id>")
api.add_resource(TokenRefresh, "/refresh")

if __name__ == "__main__":
    app.run(port=6000, debug=True)
from flask import Flask, session
from flask_cors import CORS
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity
from db import db
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from models.user import UserModel
from models.item import ItemModel
from models.store import StoreModel

# Init app
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
CORS(app)
app.secret_key = "rc"
api = Api(app)
db.init_app(app)

# Create the DB
@app.before_first_request
def create_tables():
    UserModel.__table__.create(db.session.bind, checkfirst=True)
    ItemModel.__table__.create(db.session.bind, checkfirst=True)
    StoreModel.__table__.create(db.session.bind, checkfirst=True)
jwt = JWT(app, authenticate, identity) # this creates a new endpoint called "/auth"

# Routes
api.add_resource(Store, "/api/store/<string:name>")
api.add_resource(StoreList, "/api/stores")
api.add_resource(Item, "/api/item/<string:name>")
api.add_resource(ItemList, "/api/items")
api.add_resource(UserRegister, "/api/user/register")

if __name__ == "__main__":
    app.run(port=6000, debug=True)
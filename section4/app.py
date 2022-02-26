from flask import Flask, request
from flask_cors import CORS
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from security import authenticate, identity

app = Flask(__name__)
CORS(app)
app.secret_key = "rc"
api = Api(app)
jwt = JWT(app, authenticate, identity) # this creates a new endpoint called "/auth"

items = []

class Student(Resource):
    def get(self, name):
        return {
            "Student": name
        }

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("price",
        type=float, # turns to float
        required=True, # is required
        help="This field cannot be left blank"
    )

    @jwt_required()
    def get(self, name):
        # for item in items:
        #     if item["name"] == name:
        #         return item

        item = next(filter(lambda x: x["name"] == name, items), None)
        if item is not None:
            return item
        return False, 404
    
    # @jwt_required()
    def post(self, name):
        if next(filter(lambda x: x["name"] == name, items), None) is not None:
            # If item exists
            return False, 400

        data = Item.parser.parse_args()
        
        item = {
            "name": name,
            "price": data["price"]
        }
        items.append(item)
        return True, 201

    # @jwt_required()
    def delete(self, name):
        global items
        items = list(filter(lambda x: x["name"] != name, items))
        return True

    # @jwt_required()
    def put(self, name):
        # data = request.get_json()
        data = Item.parser.parse_args()
        # print(data["another"])
        item = next(filter(lambda x: x["name"] == name, items), None)
        if item is None:
            # Creates an item if item name is not found
            item = {
                "name": name, 
                "price": data["price"]
            }
            items.append(item)
        else:
            item.update(data)
        return True


class ItemList(Resource):
    def get(self):
        return items

api.add_resource(Student, "/api/student/<string:name>") # http://localhost:5000/api/student/Rolf
api.add_resource(Item, "/api/item/<string:name>")
api.add_resource(ItemList, "/api/items")

if __name__ == "__main__":
    app.run(port=6000)
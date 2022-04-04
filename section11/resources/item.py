from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("price",
        type=float, # turns to float
        required=True, # is required
        help="This field cannot be left blank."
    )
    parser.add_argument("store_id",
        type=int, # turns to float
        required=True, # is required
        help="Every item needs a store id."
    )

    @jwt_required(fresh=True) # analogy: In Javascript terms, this is the "auth.verify"
    def get(self, name):
        try:
            item = ItemModel.find_by_name(name)
            if item:
                # If item is found
                return item.json()
        except:
            return False, 500
        # If item not found
        return False, 404

    @jwt_required(fresh=True) # analogy: In Javascript terms, this is the "auth.verify"
    def post(self, name):
        if ItemModel.find_by_name(name):
            # If item already exists return false
            return False, 404
        
        data = Item.parser.parse_args()
        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return False, 500

        return True, 201

    @jwt_required(fresh=True) # analogy: In Javascript terms, this is the "auth.verify"
    def delete(self, name):
        claims = get_jwt()
        if not claims["is_admin"]:
            return False, 401

        item = ItemModel.find_by_name(name)

        if item:
            item.delete_from_db()
            return True, 201

        return False, 404

    @jwt_required(fresh=False) # analogy: In Javascript terms, this is the "auth.verify"
    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:
            # If item does not exist create one.
            item = ItemModel(name, data["price"], data["store_id"]) 
        else:
            # If item exists update the existing item.
            item.price = data["price"]
            if data["store_id"]:
                item.store_id = data["store_id"]

        item.save_to_db()
        return True, 201


class ItemList(Resource):
    @jwt_required(optional=True) # analogy: In Javascript terms, this is the "auth.verify"
    def get(self):
        user_id = get_jwt_identity() # analogy: this is the "auth.decode" in Python. Returns "None" if jwt is optional
        items = [item.json() for item in ItemModel.find_all()]
        if user_id:
            return items, 200

        return {
            "items": [item["name"] for item in items],
            "message": "More data available if you login."
        }, 200
        # return [item.json() for item in ItemModel.query.all()] # for "pythonic" code, we use list comprehensions and for performance benefits
        # return list(map(lambda x: x.json(), ItemModel.query.all())) # for "non-pythonic" code.
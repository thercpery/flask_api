from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
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

    @jwt_required()
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

    @jwt_required()
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

    @jwt_required()
    def delete(self, name):
        item = ItemModel.find_by_name(name)

        if item:
            item.delete_from_db()
            return True, 201

        return False, 404

    @jwt_required()
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
    def get(self):
        return [item.json() for item in ItemModel.query.all()] 
        # return list(map(lambda x: x.json(), ItemModel.query.all()))
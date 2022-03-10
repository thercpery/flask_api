import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

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

        # item = next(filter(lambda x: x["name"] == name, items), None)
        # if item is not None:
        #     return item
        # return False, 404

        # connection = sqlite3.connect("data.db")
        # cursor = connection.cursor()
        # query = "SELECT * FROM items WHERE name=?"
        # result = cursor.execute(query, (name,))
        # row = result.fetchone()
        # connection.close()

        # if row:
        #     # If item is found
        #     return {
        #         "name": row[0],
        #         "price": row[1]
        #     }
        try:
            item = self.find_by_name(name)
            if item:
                # If item is found
                return item
        except:
            return False, 500
        # If item not found
        return False, 404
    
    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            # If item is found
            return {
                "name": row[0],
                "price": row[1]
            }

    # @jwt_required()
    def post(self, name):
        # if next(filter(lambda x: x["name"] == name, items), None) is not None:
        #     # If item exists
        #     return False, 400

        if self.find_by_name(name):
            # If item already exists return false
            return False, 404
        
        data = Item.parser.parse_args()
        
        item = {
            "name": name,
            "price": data["price"]
        }
        # items.append(item)

        # Connect to DB
        # connection = sqlite3.connect("data.db")
        # cursor = connection.cursor()

        # query = 'INSERT INTO items VALUES (?, ?)'
        # cursor.execute(query, (item["name"], item["price"]))

        # connection.commit()
        # connection.close()
        try:
            self.insert(item)
        except:
            return False, 500

        return True, 201

    @classmethod
    def insert(cls, item):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = 'INSERT INTO items VALUES (?, ?)'
        cursor.execute(query, (item["name"], item["price"]))

        connection.commit()
        connection.close()

    @jwt_required()
    def delete(self, name):
        # global items
        # items = list(filter(lambda x: x["name"] != name, items))
        if not self.find_by_name(name):
            return False, 404

        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = 'DELETE FROM items WHERE name=?'
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()

        return True

    # @jwt_required()
    def put(self, name):
        # data = request.get_json()
        data = Item.parser.parse_args()

        # print(data["another"])

        # item = next(filter(lambda x: x["name"] == name, items), None)
        # if item is None:
        #     # Creates an item if item name is not found
        #     item = {
        #         "name": name, 
        #         "price": data["price"]
        #     }
        #     items.append(item)
        # else:
        #     item.update(data)

        item = self.find_by_name(name)
        updated_item = {
            "name": name,
            "price": data["price"] 
        }
        if item is None:
            try:
                self.insert(updated_item)
            except:
                return False, 500
        else:
            try:
                self.update(updated_item)
            except:
                return False, 500

        return True

    @classmethod
    def update(cls, item):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = 'UPDATE items SET price=? WHERE name=?'
        cursor.execute(query, (item["price"], item["name"]))

        connection.commit()
        connection.close()


class ItemList(Resource):
    def get(self):
        items = []
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "SELECT * FROM items"
        results = cursor.execute(query)

        for result in results:
            items.append({
                "name": result[0],
                "price": result[1]
            })
        connection.close()
        
        return items
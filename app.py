from flask import Flask, jsonify, request, render_template # classes are capitalized, packages/methods are not.
from flask_cors import CORS

app = Flask(__name__) # "__name__" gives each file a unique name
CORS(app)
stores = [
    {
        "name": "My Wonderful Store",
        "items": [
            {
                "name": "My Item",
                "price": 15.99
            }
        ]
    }
]

# Test route
@app.route("/") # "http://www.google.com/"
def index():
    # return "Welcome to our store!"
    return render_template("index.html")

# POST - used to recieve data.
# GET - used to send data back only.

# POST /store data: {name:}
@app.route("/store", methods=["POST"])
def create_store():
    request_data = request.get_json()
    new_store = {
        "name": request_data["name"],
        "items": []
    }
    stores.append(new_store)
    return jsonify(True)

# GET /store/<string:name>
@app.route("/store/<string:name>") # "http:localhost:5000/store/<name>"
def get_one_store(name: str):
    # Iterate over stores.
    # If the store name matches, display it.
    # If none matches, return false
    for store in stores:
        if store["name"] == name:
            return jsonify(store)
    return jsonify(False)

# GET /store
@app.route("/store")
def get_all_stores():
    return jsonify(stores)

# POST /store/<string:name>/item {name:, price}
@app.route("/store/<string:name>/item", methods=["POST"]) # "http:localhost:5000/store/<name>"
def create_store_item(name: str):
    for store in stores:
        if store["name"] == name:
            new_item = {
                "name": request.get_json()["name"],
                "price": request.get_json()["price"],
            }
            store["items"].append(new_item)
            return jsonify(True)
    
    # If store name is not found.
    return jsonify(False)

# GET /store/<string:name>/item
@app.route("/store/<string:name>/item")
def get_store_item(name: str):
    for store in stores:
        if store["name"] == name:
            return jsonify(store["items"])

    # If item is not found
    return jsonify(False)

if __name__ == "__main__":
    app.run(port=6000)
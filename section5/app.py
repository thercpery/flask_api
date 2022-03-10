from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity
from user import UserRegister
from item import Item, ItemList

app = Flask(__name__)
CORS(app)
app.secret_key = "rc"
api = Api(app)
jwt = JWT(app, authenticate, identity) # this creates a new endpoint called "/auth"


# class Student(Resource):
#     def get(self, name):
#         return {
#             "Student": name
#         }

# api.add_resource(Student, "/api/student/<string:name>") # http://localhost:5000/api/student/Rolf
api.add_resource(Item, "/api/item/<string:name>")
api.add_resource(ItemList, "/api/items")
api.add_resource(UserRegister, "/api/user/register")

if __name__ == "__main__":
    app.run(port=6000, debug=True)
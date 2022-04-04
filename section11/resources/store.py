from flask_restful import Resource
from flask_jwt_extended import jwt_required
from models.store import StoreModel

class Store(Resource):
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return False, 404

    @jwt_required(fresh=True)
    def post(self, name):
        if StoreModel.find_by_name(name):
            return False, 400

        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return False, 500
        return True, 201
    
    @jwt_required(fresh=True)
    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()

        return True


class StoreList(Resource):
    def get(self):
        return [store.json() for store in StoreModel.find_all()]
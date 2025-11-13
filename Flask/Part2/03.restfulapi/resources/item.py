from flask import request
from flask_restful import Resource

items = []

class Item(Resource):

    def get(self, name):
        for item in items:
            if item["name"] == name:
                return item
        return {"msg":"Item not found"}, 404
    
    # 아이템 생성
    def post(self, name):
        for item in items:
            if item["name"] == name:
                return {"msg":"Item Already exists"}, 400
            
        data = request.get_json()

        new_item = {"name": name, "price": data["price"]}
        items.append(new_item)

        return new_item

    # 아이템 업데이트
    def put(self, name):
        data = request.get_json()

        for item in items:
            if item["name"] == name:
                # name 값이 이미 있는 것일 때 item에 있는 price를 입력해준 data price로 바꿔줌
                item["price"] = data["price"]
                return item
            
        new_item = {"name": name, "price": data["price"]}
        items.append(new_item)

        return new_item

    def delete(self, name):
        global items
        items = [item for item in items if item["name"] != name]

        return {"msg":"Item Deleted"}
    
from flask import Flask
from flask_restful import Api

# resuorces폴더에 있는 item.py파일에서 Item 클래스를 불러오는 것
from resources.item import Item

app = Flask(__name__)

api = Api(app)

api.add_resource(Item, '/item/<string:name>')

if __name__ == "__main__":
    app.run(debug=True)
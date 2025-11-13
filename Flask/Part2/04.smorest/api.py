from flask.views import MethodView
# Blueprint => 작은 Flask 앱
from flask_smorest import Blueprint, abort
from schemas import ItemSchema

# 1. 첫번째 "items" => blp의 이름 (고유식별자)
# 2. 두번째 "items" => 현재 blp의 이름
# => 파일에서 직접 실행할 때 => __name__ == "__main__" => __name__ (권장)
# => 파일을 다른 파일에서 import (import items) 할 때 =>  __name__ == 모듈이름
# 3. url_prefix="/items" => 이 블루프린트에 포함된 모든 라우트 앞에 자동으로 붙는 URL 경로
# => 예) @blp.route('/') => /items/
# 4. description="Operations on items" => 문서 설명
# blp = Blueprint(...) => /items 로 시작하는 라우트를 blp에 전부 등록
blp = Blueprint("items", "items", url_prefix="/items", description="Operations on items")

# 간단한 데이터 저장소 역할을 하는 리스트
items = []

# 'ItemList' 클래스 - GET 및 POST 요청을 처리
# /items/
@blp.route('/')

# MethodView => get, post, put, delete에 맞게 함수를 정의하면 Flask가 자동으로 매핑해 줌
# => 예) def get() / def post() / def put() / def delete()
class ItemList(MethodView):
    # 이 함수(get)가 성공하면 상태코드 200으로 응답
    # 두 번째 인자가 없어서 관계없는 값이 있어도 반환됨
    @blp.response(200)
    def get(self):
        # 모든 아이템을 반환하는 GET 요청 처리
        return items
    
    # ItemSchmea 클래스에 정의된 구조대로(id, name, description) 들어와야지 바로 밑에서 데이터를 POST할 수 O
    # 칼럼명과 타입이 다 검증되면 post()함수의 첫 번째 인자인 new_data에 파이썬 딕셔너리 형태로 전달
    # 단일 Item 객체를 받도록 설정
    @blp.arguments(ItemSchema)

    # description => 상태코드에 대한 응답 설명 텍스트 (postman에선 안보임)
    @blp.response(201, description="Item added")
    def post(self, new_data):
        items.append(new_data)
        return new_data
    
# 'Item' 클래스 - GET, PUT, DELETE 요청을 처리
# 예) /items/123
@blp.route('/<int:item_id>')
class Item(MethodView):
    @blp.response(200)

    #  예) route(/123) => item_id는 1
    def get(self, item_id):
        # route에서 입력한 아이디인지 아닌지 확인
        # next() => 반복문에서 값이 있으면 값 반환하고 없으면 None을 반환
        # next는 조건을 만족하는 첫 번째 아이템을 반환하고, 그 이후의 아이템은 무시함
        item = next((item for item in items if item["id"] == item_id), None)
        if item is None:
            abort(404, message="Item not found")
        return item
    # GET에서는 @blp.arguments(ItemSchema) 필요 X
    # @blp.arguments(ItemSchema) => GET, PUT에서만 씀
    @blp.arguments(ItemSchema)
    @blp.response(200, description="Item updated")

    # 입력한 json 데이터가 클래스에 적합한게 검증되면 첫 번째 인자로 전달 => new_data
    # item_id = > URL 경로에서 받은 ID
    def put(self, new_data, item_id):
        # next(..., None) => 조건에 맞는게 있으면 그걸 반환하고 없으면 None 반환
        item = next((item for item in items if item["id"] == item_id), None)
        if item is None:
            abort(404, message="Item not found")
        # id가 같다면 그걸 위에서 item으로 가져온 것에 새로운 데이터를 업데이트함
        item.update(new_data)
        return item
    
    @blp.response(204, description="Item deleted")
    def delete(self, item_id):
        global items
        if not any(item for item in items if item["id"] == item_id):
            abort(404, message="Item not found")
        # 경로에서 언급한 item_id와 같지 않은 아이디의 딕셔너리만 items에 담김
        items = [item for item in items if item["id"] != item_id]

        # 리턴값 아무것도 없음 (응답코드 204는 뜸)
        return ''

# 여기에선 필요 X
# 각 클래스를 블루프린트에 등록
# (등록할 MethodView 클래스, 뷰 이름, URL 경로)
# 뷰 이름 => 클래스 이름과 비슷하게 지음 => url_for() 쓸 때 헷갈리지 않게
# blp.register_view(ItemList, "item_list", '/')
# blp.register_view(Item, "item", '/<int:item_id>')
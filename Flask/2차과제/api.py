from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import BookSchema

book_blp = Blueprint("books", "books", url_prefix="/books", description="Operations on books")

books = []

@book_blp.route('/')
class BookList(MethodView):
    # 두 번째 인자인 BookSchema(many=True) => 단일 객체를 받는 @blp.arguments(ItemSchema) 이거랑 같은 원리
    # => 칼럼명과 타입 검증
    # 응답 => BookSchema(many=True) / 요청 => @blp.arguments(ItemSchema)

    # 예) books = [{"id": 1, "title": "Harry Potter", "extra": "무시됨"}]
    #     BookSchema:
    #                 id: Int
    #                 title: Str   이거 라면
    # (200, BookSchema(many=True)) => [{"id": 1, "title": "Harry Potter"}]
    # (200) => [{"id": 1, "title": "Harry Potter", "extra": "무시됨"}]

    # (many=True) => 응답 데이터가 여러 개의 값으로 이루어져있을거라고 알려주는 것
    # @book_blp.response(200, BookSchema) => 이건 데이터가 단일 구조일 때만 사용할 수 O

    # (200, BookSchema(many=True)) 
    # => 가져오는 데이터 값들 중 하나라도 클래스의 구조에 맞지 않는다면
    # 예) books = [
    #     {"id": 1, "title": "Flask for Beginners", "author": "John"},  
    #     {"title": "No ID Book", "author": "Jane"}                      
    # ]
    # => 에러남

    # @book_blp.response(200, BookSchema(many=True))
    # => 200으로 응답할 때, 반환되는 데이터가 여러 개의 객체 형태일 것이고, 
    # 그 안의 각 개체를 BookSchema 클래스 구조로 검증 및 직렬화해서 json으로 내보내겠다
    @book_blp.response(200, BookSchema(many=True))
    def get(self):
        return books
        
    @book_blp.arguments(BookSchema)
    @book_blp.response(201, BookSchema)
    def post(self, new_data):
        new_data['id'] = len(books) + 1
        books.append(new_data)
        return new_data
    
@book_blp.route("/<int:book_id>")
class Book(MethodView):
    @book_blp.response(200, BookSchema)
    def get(self, book_id):
        book = next((book for book in books if book["id"] == book_id), None)
        if book is None:
            abort(404, message="Book not found.")
        return book
    
    @book_blp.arguments(BookSchema) # 요청을 검증
    @book_blp.response(200, BookSchema) # 응답을 검증
    def put(self, new_data, book_id):
        book = next((book for book in books if book["id"] == book_id), None)
        if book is None:
            abort(404, message="Book not found.")
        # 기존에 있던 데이터를. 업데이트한다. 새로운 데이터로 (books.update(new_data) 아님 !!!!)
        book.update(new_data)
        return book
    
    @book_blp.response(204)
    def delete(self, book_id):
        global books
        
        # 변수 book은 그저 밑에 있는 if문에서 없는 book_id면 오류구문을 반환하려고 만든 것
        book = next((book for book in books if book["id"] == book_id), None)
        if book is None:
            abort(404, message="Book not found.")
        books = [book for book in books if book["id"] != book_id]
        return ''



from flask import request, jsonify
from flask_smorest import Blueprint
from flask.views import MethodView
from db import db
from models import Board

board_blp = Blueprint("Boards", "boards", description="Operations on boards", url_prefix="/board")

# API list
# /board
@board_blp.route('/')

# MethodView => Get,POST,PUT,DELETE의 메서드를 이름으로 정의하면 Flaks가 자동으로 매핑
# def get(slef): 이렇게 쓰면 Flask가 알아서 GET 요청인걸 안다 (Flask 똑똑함)
class BoardList(MethodView):
    # 전체 게시글 불러오기 (GET)
    def get(self):
        boards = Board.query.all()  # Board클래스의 모든 쿼리를 가져와서 리스트로 반환
        # for board in boards:
        #     print('id', board.id)
        #     print('user_id', board.user_id)
        #     print('title', board.title)
        #     print('content', board.content)
        #     print('author_name', board.author.name)
        #     print('author_email', board.author.email)
        # return "success"

        # 위 for문의 간단버전
        return jsonify([{"id":board.id, "user_id":board.user_id, 'title':board.title, 
                            'content':board.content, 'author_name':board.author.name} for board in boards])
  
    # 게시글 작성 (POST)
    def post(self):
        data = request.json # request로 받은 데이터를 json 형태로 받겠다
        new_board = Board(title=data["title"], content=data["content"], user_id=data["user_id"])
        db.session.add(new_board)
        db.session.commit()

        return jsonify({"msg": "success create board"}), 201


# /<int: board_id>
@board_blp.route('/<int:board_id>')

# 모델명이 Board이기때문에 클래스명을 Board로 하면 X
class BoardResource(MethodView):
    # 하나의 게시글 불러오기 (GET)
    def get(self, board_id):
        # Board 테이블에서 PK = board_id인 게시글을 찾고
        # => 있으면 boards에 그 객체 저장 / 없으면 404 Not Found 응답보냄
        board = Board.query.get_or_404(board_id)

        return jsonify({"id": board_id,
                        "title": board.title,
                        "content": board.content,
                        "author": board.author.name})
        # 이건 JSON으로 바로 변환할 수 X => 오류남
        # return jsonify({board})

# 특정 게시글 수정하기 (PUT)
    def put(self, board_id):
        board = Board.query.get_or_404(board_id)
        data = request.json

        board.title = data["title"]
        board.content = data["content"]

        db.session.commit()

        return jsonify({"msg":"Successfully updated board data"}), 201

# 특정 게시글 삭제하기 (DELETE)
    def delete(self, board_id):
        board = Board.query.get_or_404(board_id)

        db.session.delete(board)
        db.session.commit()

        # 응답코드 204는 postman에서 바디(메세지)가 보이지 X
        return jsonify({"msg":"Successfully deleted board data"}), 204
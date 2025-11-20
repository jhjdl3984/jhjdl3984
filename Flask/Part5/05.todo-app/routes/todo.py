from flask import request, jsonify
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Todo, User, db

todo_blp = Blueprint("todo", "todo", url_prefix="/todo", description="Operations on todos")

# Todo에 새 레코드 추가 (POST)
@todo_blp.route('/', methods=["POST"])
@jwt_required()   # 요청에 유효한 JWT 토큰이 접근했는지 => 인증된 유저인지 아닌지
def create_todo():
    if not request.is_json():
        return jsonify({"msg": "Missing JSON in request"}), 400
    
    title = request.json.get("title", None)
    if not title:
        return jsonify({"msg": "Missing title"}), 400
    
    # auth.py에서 create_access_token(identity=username) 했던 것
    # => 토큰을 가지고 있는 사람의(로그인한 사람의) username을 꺼내는 것
    username = get_jwt_identity()

    # User 테이블에서 username이 get_jwt_identity()로 가져온 username과 같은지 비교하고,
    # 같으면 그 중 첫 번째 유저 객체를 반환
    user = User.query.filter_by(username=username).first()

    # Todo(...) => Todo 테이블에 들어갈 새 레코드를 만드는 것
    # title=title => Todo 모델의 컬럼명 = 위에서 request로 가져온 값
    # user_id=user.id => Todo 모델의 컬럼명 = 위에서 가져온 로그인한 user 객체의 id
    new_todo = Todo(title=title, user_id=user.id)
    db.session.add(new_todo)
    db.session.commit()

    return jsonify({"msg": "Todo created", "id": new_todo.id}), 201

# Todo 조회 (GET)
@todo_blp.route('/', methods=["GET"])
@jwt_required()
def get_todos():
    username = get_jwt_identity()
    user = User.query.filter_by(username=username).first()
    todos = Todo.query.filter_by(user_id=user.id).all()
    
    return jsonify([{"id": todo.id, "title": todo.title, "completed": todo.completed} for todo in todos])

# Todo 수정 (PUT)
@todo_blp.route('/<int:todo_id>', methods=["PUT"])
@jwt_required()
def update_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    if "title" in request.json:
        todo.title = request.json["title"]

    if "completed" in request.json:
        todo.completed = request.json["completed"]

    db.session.commit()

    return jsonify({"msg": "Todo updated", "id": todo.id})

# Todo 삭제 (DELETE)
@todo_blp.route('/<int:todo_id>', methods=["DELETE"])
@jwt_required()
def delete_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)

    db.session.delete(todo)
    db.session.commit()

    return jsonify({"msg": "Todo deleted", "id": todo_id})




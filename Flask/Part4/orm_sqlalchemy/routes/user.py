from flask import request, jsonify
from flask_smorest import Blueprint
from flask.views import MethodView
from db import db
from models import User

user_blp = Blueprint("Users", "users", description="Operations on users", url_prefix="/user")

# API LIST
@user_blp.route('/')
class UserList(MethodView):
    # (1) 전체 유저 데이터 조회 (GET)
    def get(self):
        users = User.query.all()

        user_data = [
            {"id":user.id, "name":user.name, "email":user.email} for user in users
        ]

        return jsonify(user_data)

    # (2) 유저 생성 (POST)
    def post(self):
        data = request.json
        new_user = User(name=data["name"], email=data["email"])

        db.session.add(new_user)
        db.session.commit()

        return jsonify({"msg":"successfully created new user"}), 201

@user_blp.route('/<int:user_id>')
class UserResource(MethodView):
    # (1) 특정 유저 데이터 조회 (GET)
    def get(self, user_id):
        user = User.query.get_or_404(user_id)
        
        return jsonify({"name":user.name, "email":user.email})

    # (2) 특정 유저 데이터 업데이트 (PUT)
    def put(self, user_id):
        user = User.query.get_or_404(user_id)
        data = request.json

        # user는 SQLAlchemy모델 객체 => 속성 접근 (user.name, user.email)
        # data는 josn인 dict형태 => 키 접근 (data["name"], data["email"])
        user.name = data["name"]
        user.email = data["email"]

        db.session.commit()

        return jsonify({"msg":"Successfully updated user data"})

    # (3) 특정 유저 삭제 (DELETE)
    def delete(self, user_id):
        user = User.query.get_or_404(user_id)

        db.session.delete(user)
        db.session.commit()

        return jsonify({"msg":"Successfully deleted user data"})
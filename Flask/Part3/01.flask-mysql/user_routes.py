from flask_smorest import Blueprint, abort
from flask import request

# mysql => app.py에서 mysql = MySQL(app)에 있는 mysql임
def create_user_blueprint(mysql):
    # Blueprint 객체를 생성
    user_blp = Blueprint("user_routes", __name__, url_prefix="/users")

    # 전체 유저 데이터를 불러오는 코드
    @user_blp.route("/", methods=["GET"])
    def get_users():
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()   # return 결과 타입 => 튜플
        cursor.close()

        # REST API로 내려줄 때는 {} 형태여하므로 딕셔너리로 변환
        users_list = []

        for user in users:
            users_list.append({
                'id': user[0],
                'name': user[1],
                'email': user[2]
            })

        return users_list
    
    # 유저 생성하는 함수
    @user_blp.route('/', methods=["POST"])
    def add_user():
        # request.json = request.get_json() 같은것
        # 클라이언트가 보낸 json 데이터를 파이썬의 딕셔너리로 가져옴
        user_data = request.json

        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO users(name, email) VALUES(%s, %s)",
                       (user_data["name"], user_data["email"]))
        mysql.connection.commit()
        cursor.close()

        return {"msg":"successfully added user"}, 201
    
    # 유저 업데이트하는 함수
    @user_blp.route("/<int:user_id>", methods=["PUT"])
    def update_user(user_id):
        user_data = request.json

        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE users SET name=%s, email=%s WHERE id=%s",
                       (user_data["name"], user_data["email"], user_id))
        mysql.connection.commit()
        cursor.close()

        return {"msg":"successfully updated user"}, 201
    
    # 유저 삭제하는 함수
    @user_blp.route("/<int:user_id>", methods=["DELETE"])
    def delete_user(user_id):
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM users WHERE id=%s",
                       (user_id, ))
        mysql.connection.commit()
        cursor.close()
    
        return {"msg":"successfully deleted user"}, 201

    # create_user_blueprint(mysql) 함수가 블루프린트를 반환해야 함
    return user_blp

    # 웹에서 입력한 값이 db에도 저장이 됨 !!



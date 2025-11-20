from db import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))   # 비번을 해시 형태로 저장

    def set_password(self, password):
        # generate_password_hash(password) => 사용자가 입력한 password를 해시로 변환
        # 해시는 단방향 암호화 => 해시값에서 원본 비번으로 되돌릴 수 X
        # 예) alice와 leo의 비밀번호가 같아도 => alice의 비번 해시값과 leo의 비번 해시값은 다름
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        # self.password_hash => 알고리즘 정보 + salt + 실제 해시값 으로 이루어짐
        # => 알고리즘 정보와 salt 추출하고 => 입력한 password + salt로 새로 해시 생성 => 저장된 해시와 비교(True or False)
        return check_password_hash(self.password_hash, password)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
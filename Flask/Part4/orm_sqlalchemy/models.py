# Model을 만든다 => Table을 만든다
# 게시글 - board / 유저 - user (모델은 단수)

from db import db

class User(db.Model):
    __tablename__ = "users"
    
    # SQULAlchemy는 primary_key=True로 Integer 컬럼을 만들면 AUTO_INCREMENT컬럼으로 자동 설정함
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(30), nullable=False) # nullalbe=False == not null
    email = db.Column(db.String(100), unique=True, nullable=False)
    address = db.Column(db.String(200), nullable=False)

    # relationship => 두 테이블 관계 연결
    # "Board" => 참조할 모델 이름
    # back_populates="author" => Board 모델의 author relationship속성과 연결 (양방향 관계 연결할때 사용)
    # lazy="dynamic" => 필요할 때 쿼리 실행, 필요한 데이터만 filter 가능
    boards = db.relationship('Board', back_populates="author", lazy="dynamic")

class Board(db.Model):
    __tablename__ = "boards"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(300))
    # Board:User => 1:N (단일 객체에는 lazy="dynamic"을 쓸 수 X)
    author = db.relationship("User", back_populates="boards")



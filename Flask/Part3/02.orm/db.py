from flask_sqlalchemy import SQLAlchemy

# SQLAlchemy 객체를 하나 생성
# 이 db 객체를 app.py 뿐만 아니라 다른 곳에서도 사용하기 위해서 db.py로 따로 빼준 것!
db = SQLAlchemy()
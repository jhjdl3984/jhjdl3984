
# UserMixin => Flask-Login과 호환되는 기본 메서드 제공
from flask_login import UserMixin

users = {"admin": {"password":"pw123"}}

class User(UserMixin):
    def __init__(self, username):   # __init__ => username을 받아서 세션 ID로 사용
        self.id = username

    @staticmethod   ############
    def get(user_id):
        if user_id in users:
            return User(user_id)
        
        return None
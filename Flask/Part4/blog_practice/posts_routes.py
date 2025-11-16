# flask에 abort => abort에 작성한 메세지가 postman에 뜨지 않음
from flask import request, jsonify
# flask_smorest => abort에 작성한 메세지 postman에 뜸
from flask_smorest import Blueprint, abort

# mysql을 받아오기 위해서 posts 관련 route를 가진 Blueprint를 생성하고 반환하는 함수를 만들어줌
def create_posts_blueprint(mysql):
    posts_blp = Blueprint("Posts", __name__, description="posts api", url_prefix="/posts")

    @posts_blp.route('/', methods=["GET", "POST"])
    def posts():
        cursor = mysql.connection.cursor()
        if request.method == "GET":     # 요청이 GET 방식이라면
            sql = "SELECT * FROM posts"
            cursor.execute(sql)     # mysql 서버에서 변수 sql을 실행만 함

            # 실행된 결과를 파이썬으로 가져옴 (select에서만 사용함)
            posts = cursor.fetchall()
            cursor.close()

            post_list = []

            for post in posts:
                post_list.append({
                    "id": post[0],
                    "title": post[1],
                    "content": post[2]
                })

            return jsonify(post_list)
        
        if request.method == "POST":
            title = request.json.get('title')
            content = request.json.get('content')

            if not title or not content:
                abort(400, message="Title or Content cannot be empty")

            sql = "INSERT INTO posts(title, content) VALUES(%s, %s)"
            cursor.execute(sql, (title, content))
            mysql.connection.commit()

            return jsonify({"msg":"successfully created post data", "title":title, "content":content}), 201
            
    @posts_blp.route('/<int:id>', methods=["GET", "PUT", "DELETE"])
    def post(id):
        cursor = mysql.connection.cursor()
        sql = f"SELECT * FROM posts WHERE id = {id}"
        cursor.execute(sql)
        post = cursor.fetchone()

        # 특정 id의 게시글만 조회
        if request.method == "GET":
            if not post:
                abort(404, "Not found post")
            return ({"id": post[0],
                    "title": post[1],
                    "content": post[2]})
        # 특정 id의 게시글 업데이트
        elif request.method == "PUT":
            title = request.json.get('title')
            content = request.json.get('content')

            if not post:
                abort(404, "Not found post")
                
            if not title or not content:
                abort(400, "Not found title, content")

            sql = f"UPDATE posts SET title={title}, content={content} WHERE id={id}"
            cursor.execute(sql)
            mysql.connection.commit()

            return jsonify({"msg":"successfully updated title & content"})
        # 특정 id의 게시글 삭제
        elif request.method == "DELETE":
            if not post:
                abort(404, "Not found post")

            sql = f"DELETE FROM posts WHERE id={id}"
            cursor.execute(sql)
            mysql.connection.commit()

            return jsonify({"msg":"Successfully deleted title & content"})
    
    return posts_blp

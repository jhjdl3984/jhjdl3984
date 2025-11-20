from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# 임시 사용자 데이터
users = [
    {"username": "traveler", "name": "Alex"},
    {"username": "photographer", "name": "Sam"},
    {"username": "gourmet", "name": "Chris"}
]

@app.route('/')
def index():
    return render_template('index.html', users=users)

# 사용자 추가
@app.route('/add', methods=["GET", "POST"])
def add_user():
    if request.method == "POST":
        # request.form은 딕셔너리처럼 key로 접근해야 함
        username = request.form["username"]
        name = request.form["name"]

        users.append({"username":username, "name":name})    # 리스트는 append

        return redirect(url_for("index"))    # url_for() 안에는 함수명 써야함
    
    return render_template("add_user.html")

# 수정
# HTML에 method="POST"라 methods=["GET", "POST"]로 접근해야 함
@app.route('/edit/<username>', methods=["GET", "POST"])
def edit_user(username):
    user = next((user for user in users if user["username"] == username), None)

    if not user:
        return redirect(url_for("index"))
    
    if request.method == "POST":
        user["name"] = request.form["name"]
        return redirect(url_for("index"))
    # user=user => edit_user.html 템플릿 변수에 user 값을 전달하여 사용할 수 있게 함
    # GET => 여기선 수정 페이지만 보여주는 용도
    return render_template('edit_user.html', user=user)

# 삭제
@app.route('/delete/<username>')
def delete_user(username):
    # global은 전역 변수 수정할 때만 사용 => 위의 수정 route에서는 읽기만 하니까 global 필요 X
    global users
    user = next((user for user in users if user["username"] == username), None)

    if user:
        users.remove(user)
    
    return redirect(url_for("index"))
    






if __name__ == '__main__':
    app.run(debug=True)
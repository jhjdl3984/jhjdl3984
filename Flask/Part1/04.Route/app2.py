from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, This is Main Page!"

# 옵션 + shift + 화살표 위/아래 => 복사
@app.route('/about')
def about():
    return "This is the about page!"

# http://127.0.0.1:5000/user/hyunjung
# 1. URL에서 사용자한테 값을 받음 => /user/hyunjung
# 2. 함수 파라미터가 URL 값을 받음 => username = 'hyunjung'
# 3. f-string의 값에 들어감 => {username} = 'hyunjung'
@app.route('/user/<username>')
def user_profile(username):
    return f"UserName : {username}"

# URL을 숫자로 받고 싶을 때 => <int:...>
@app.route('/number/<int:number>')
def number(number):
    return f"Number : {number}"

# post 요청 날리는 법
# (1) postman
# (2) requests
import requests # pip install requests
@app.route('/test')
def test():
    url = 'http://127.0.0.1:5000/submit'
    data = 'test data'
    response = requests.post(url=url, data=data)
    return response

@app.route('/submit', methods=['GET', 'POST', 'PUT', 'DELETE'])
def submit():
    print(request.method)
    # return ''

    if request.method == 'GET':
        print("GET method")

    if request.method == 'POST':
        print("POST method", request.data)

    return "success"

if __name__ == '__main__':
    app.run()

# 폴더 내에 파일이 1개라면 => flask run 만 해도 Falsk가 자동으로 파일을 찾고 실행
# 파일이 여러개라면 => python 파일명 으로 명시해서 실행
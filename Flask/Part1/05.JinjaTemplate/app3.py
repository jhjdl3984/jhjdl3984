from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    data = {
        'title': 'Flask Jinja Template',
        'user': 'Inseop',
        'is_admin': True,
        # .items => 딕셔너리의 내장 메서드 이름이기 때문에
        # => index.html에서 data.items 로 불러오면 겹쳐서 X
        'item_list': ['Item 1', 'Item 2', 'Item 3']
    }
    # render_template(rendering할 html 파일명, html로 넘겨줄 데이터)
    return render_template('index.html', data=data)

if __name__ == '__main__':
        # debug=True => 코드가 변경됐을 때 새로고침 하지 않아도 바로 반영이 됨.
        app.run(debug=True)
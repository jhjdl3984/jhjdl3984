from flask import Flask, jsonify, request

app = Flask(__name__)

# GET
# (1) 전체 게시글을 불러오는 API
@app.route('/api/v1/feeds', methods=["GET"])
def show_all_feeds():
    # 딕셔너리 => 순서가 보장 X => json 변환 중 순서가 달라질 수 O
    data = {'result':'success', 'data':{'feed1':'data1', 'feed2':'data2'}}

    # return jsonify(data) => data를 json 형식으로 변환 (이게 안전하긴 함)
    # => data가 딕셔너리기 때문에 flask에서 자동으로 json데이터로 바꿔주므로 data만 써도됨
    return data

# (2) 특정 게시글을 불러오는 API
@app.route('/api/v1/feeds/<int:feed_id>', methods=["GET"])
def show_one_feed(feed_id):
    print(feed_id)
    data = {'result':'success', 'data':{'feed1':'data1'}}

    return data

# POST
# (1) 게시글을 작성하는 API
# 브라우저 주소창에서 입력하고 엔터 치면 기본적으로 GET 요청이 보내지기때문에
# => POST는 postman같은 API 테스트 툴 사용
@app.route('/api/v1/feeds', methods=["POST"])
def create_one_feed():
    # request.form => 사용자가 폼에 입력한 키-값
    # ['name'] => 'name' 이라는 키를 찾아서 해당 키의 값을 가져옴
    name = request.form['name']
    age = request.form['age']

    # postman에 입력한 값 출력됨
    print(name, age)

    # POST 요청이 제대로 들어왔는지 확인하기 위해 그냥 확인용으로 작성
    return jsonify({'result':'success'})

datas = [{'items': [{'name': 'item1', 'price': 10}]}]

@app.route('/api/v1/datas', methods=["GET"])
def get_datas():
    # 'datas'라는 새로운 딕셔너리 키를 만들어서 값으로 datas를 넣음
    return {'datas':datas}
    # {'datas':[{'items': [{'name': 'item1', 'price': 10}]}]}를 리턴한다는 뜻

@app.route('/api/v1/datas', methods=["POST"])
def create_data():
    # 요청을 받은 JSON을 python 딕셔너리로 변환
    request_data = request.get_json()

    # 앞에 있는 'items' => 새로운 딕셔너리에 새로운 키 생성
    # .get('items', []) => request_data 딕셔너리에서 items라는 키를 찾고
    # => 키가 있으면 그 값을 가져오고, 없으면 빈 리스트[] 사용
    new_data = {'items': request_data.get('items', [])}
    datas.append(new_data)

    return new_data, 201

# flask run => app.run()이 있든 없든 Flask 서버를 실행시킴
# python app.py => app.run()이 없으면 실행 XX
if __name__ == "__main__":
    app.run(debug=True)
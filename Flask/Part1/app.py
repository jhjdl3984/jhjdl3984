from flask import Flask
# test.py 파일을 모듈로 불러온 것
import test

app = Flask(__name__)

host = '127.0.0.1'
port = '8000'

if __name__ == '__main__':
    app.run(host=host, port=port)
    # print('__name__: ', __name__)
    # app.run()

# 다른 모듈에서 임포트 되면(test가 app에서 임포트) __name__은 모듈의 이름이 됨
# app.py에서 실행 => test.py => __name__ : test
#                  __name__:  __main__

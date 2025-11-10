from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

# pymysql => 파이썬에서 mysql 데이터베이스와 연결하고 조작할 수 O
import pymysql

# webdriver.common.by => 웹 요소를 찾는 다양한 방법
# By => selenium이 웹에서 어떤 기준으로 HTML 요소를 찾을지 알려주는 클래스
from selenium.webdriver.common.by import By

# 키보드 키값을 코드에서 사용하기 위해 Keys 클래스를 불러옴
from selenium.webdriver.common.keys import Keys

url = "https://kream.co.kr"

# '이 요청은 Mac OS X(10.15.7)에서 실행 중인 Chrome 브라우저(버전135)로부터 온 것'이라고 서버에 자신을 소개하는 문자열
# 프로그램으로 접속할건데 서버에는 사람이 브라우저에 접속하는것처럼 보이게함
header_user = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
options_ = Options()
options_.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=options_)
driver.get(url)
time.sleep(1)

# driver.find_element() => HTML 요소 찾기
# By.CSS_SELECTOR => CSS 선택자 문법으로 HTML 요소를 지정
# .click() => 버튼 클릭
# <차이점>
# soup.select() => HTML 텍스트 안에서 요소를 찾아 리스트로 반환 (클릭같은 조작 불가능)
# driver.find_element(By.CSS_SELECTOR,'...') => 브라우저 화면 속 실제 요소를 찾아 클릭같은 조작을 함
# 아래 코드는 돋보기 버튼을 누르는 것.
driver.find_element(By.CSS_SELECTOR, ".btn_search.header-search-button.search-button-margin").click()
time.sleep(1.5)     # 검색버튼을 누르고 검색창이 뜨고 1.5초 후에 밑에 코드 실행

# 검색 입력창에 키보드 입력으로 '슈프림'을 입력하는 동작을 함
driver.find_element(By.CSS_SELECTOR, ".input_search.show_placeholder_on_focus").send_keys("슈프림")
time.sleep(1)       # 슈프림을 다 입력 후 1초 후에 밑에 코드 실행

# 키보드의 엔터 키를 누르는 동작
driver.find_element(By.CSS_SELECTOR, ".input_search.show_placeholder_on_focus").send_keys(Keys.ENTER)
for i in range(20):
    # By.TAG_NAME => HTML 태그 이름으로 요소를 찾는 방법
    # 'body' => HTML문서의 <body> 전체를 선택
    # keys.PAGE_DOWN => 키보드의 page Down 키를 누름 => 한번의 스크롤이 일어남
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
    time.sleep(0.3)

html = driver.page_source
soup = BeautifulSoup(html, "html.parser")

# <a> 태그이면서 클래스가 product_card이고, data-sdui-id 속성이 있고 그 값이 'product_card/'로 시작하는 모든 요소
# 예) <a class="product_card" data-sdui-id="product_card/12345"> ... </a> => 부합함
items =soup.select('a.product_card[data-sdui-id^="product_card/"]')

product_list = []

for item in items:
    category = "상의"

    # text-element, text-lookup, display_paragraph 세 클래스를 모두 가진 <p> 요소들 중에서
    # semibold 클래스가 없는(즉 굵게 처리되지 않은) 요소를 선택
    name = item.select_one('p.text-element.text-lookup.display_paragraph:not(.semibold)')

    # name.get_text => 위에서 가져온 <p> 태그 내부 텍스트를 가져오고, 
    # (strip=True) => 양쪽 공백 제거 (예) <p>  후드티  </p> => '후드티')
    product_name = name.get_text(strip=True)

    if "후드" in product_name:
        # data-sdui-id 속성이 "product_brand_name/"로 시작하는 요소 안에 포함된 semibold 클래스를 가진 <p> 요소를 선택
        brand = item.select_one('[data-sdui-id^="product_brand_name/"] p.semibold')
        product_brand = brand.get_text(strip=True)

        # 클래스 price-info-container 안쪽의 클래스 .label-text-container 안쪽에 있는 <p>태그 중 클래스가 semibold인 것 선택
        # 공백 => 부모-자식 관계
        price = item.select_one(".price-info-container .label-text-container p.semibold")
        product_price = price.get_text(strip=True)

        # category => 위에서 '상의'로 정의해줬기때문에 무조건 '상의'로 나옴
        product_info = [category, product_brand, product_name, product_price]
        product_list.append(product_info)


        # print(f"카테고리 : {category}")
        # print(f"브랜드 : {product_brand}")
        # print(f"제품명 : {product_name}")
        # print(f"가격 : {product_price}")
        # print()

driver.quit()

# pymysql.connect() => 파이썬에서 mysql 데이터베이스와 연결
connection = pymysql.connect(
    host = '127.0.0.1',
    user = 'root',
    password = '3039483',
    db = 'kream',
    charset = 'utf8mb4'
)
# query => 실행할 sql문 (SELECT, INSERT 등)
# args=None => SELECT처럼 VALUES 값이 필요 없는 쿼리도 실행 가능하게 함
# args 라고만 쓰면 => SELECT 쓰는 경우에 TypeError남
def execute_query(connection, query, args=None):
    # with => 작업 후 자동으로 cursor.close()됨
    # DB에 쿼리를 실행할면 cursor 필요 => cursor로 sql실행, 결과 조회 가능하게 됨
    with connection.cursor() as cursor:
        # cursor.execute() => 이 커서로 DB에게 sql을 실행하라 명령 (실행 가능)
        # query => 실제로 실행할 명령 내용 (무엇을 실행할지) (예) SELECT * FROM KREAM => query)
        # args가 None이면 () 사용
        cursor.execute(query, args or ())

        # query.strip() => sql 앞뒤 공백 제거 (예) '   SELECT * FROM KREAM WHERE category='상의';   ')
        # .startswith("SELECT") => SELECT 쿼리인지 확인
        if query.strip().upper().startswith("SELECT"):
            # SELECT 쿼리면 모든 결과를 리스트로 반환
            return cursor.fetchall()
        else:
            # INSERT/UPDATE/DELETE 쿼리면 DB에 변경 내용을 저장하여 적용
            connection.commit()

for i in product_list:
    execute_query(connection, "INSERT INTO KREAM (category, brand, product_name, price) VALUES (%s, %s, %s, %s)",(i[0],i[1],i[2],i[3]))

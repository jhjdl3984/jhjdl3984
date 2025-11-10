# selenium => 브라우저를 자동으로 다루는 전체 시스템(페이지 열기, 스크롤 등) => 틀
# requests랑 다른 점: reiquests는 HTML 코드만 가져오고 selenium은 브라우저 창을 실제로 띄움
# webdriver => 그 시스템 안에서 실제 브라우저(크롬 등)를 자동으로 열고 조작하는 실행 => 실제 실행
# selenium : webDriver = Beautiful : html.parser
from selenium import webdriver

# selenium - selenium안에 있는 webdriver모듈 - webdriver안에 있는 chrome모듈 - chrome안에 있는 options모듈
# options 모듈 안에 있는 Options 클래스
# chrome모듈이 있으니 여기선 Options는 chrome 브라우저 옵션을 설정할 때 사용
from selenium.webdriver.chrome.options import Options

import time
from bs4 import BeautifulSoup

keyword = input('검색어를 입력해주세요: ')
url = 'https://search.naver.com/search.naver?ssc=tab.blog.all&sm=tab_jum&query=' + keyword

# Options => 브라우저가 켜질 때 어떤 환경 설정을 적용할지 정해 담는 상자
options_ = Options()

# options_.add_experimental_option('detach', )
# => selenium 스크립트(selenium으로 브라우저를 조작하는 코드 전체) 종료 후에 브라우저 창을 유지할건지 닫을건지 정한 설정을 options_에 담음
# ('detach', True) + driver.quit() == ('detach', False)
options_.add_experimental_option('detach', True)

# webdriver.Chrome() => Chrome 브라우저 실제로 실행
# Chrome() => 함수
# options=options_
# => options_에는 Chrome 브라우저를 실행할 때 selenium 스크립트가 종료돼도 브라우저 창을 유지하는 설정이 담겨 있음
# => 그걸 Chrome() 함수 안에 기본적으로 있는 options 매개변수에 담음
# webdriver.Chrome(options_)
# => selenium이 업데이트 되면서 첫 번째 매개변수가 service가 되면 options_가 service에 적용될 수 있어서
# 매개변수인 options에 넣는게 안전함 !!
driver = webdriver.Chrome(options=options_)
driver.get(url)
time.sleep(1)

for i in range(5):
    # driver => 현재 열려있는 브라우저를 조작
    # .execute_script() => 브라우저 안에 있는 javascript 코드를 실행
    # window.scrollTo(x, y) => 브라우저 창에서 스크롤 위치를 이동 (x = 수평 y = 수직)
    # document.body.scrollHeight => 문서 전체 길이
    # 문서 전체의 길이가 스크롤을 10번 해야 끝나는데 range(5) => 스크롤 5번만 내리고 나머지 5번은 보지 X
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')

    # 한번 내릴때 0.5초 후 다시 내리기
    time.sleep(0.5)
# ---------------------------------------------------------------------------
# driver.page_source
# => 브라우저가 현재 보여주고 있는 페이지의 전체 HTML 코드를 "문자열"로 가져옴 (js의 내용까지 포함)
# rep.text (requests) => JS가 만들어낸 글을 못 보고 => js의 텍스트가 ... 으로 나옴
# driver.page_source (Selenium, JS 실행 후) => 브라우저에서 JS까지 실행된 후 글까지 다 볼 수 있음
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
result = soup.select('.sds-comps-vertical-layout.sds-comps-full-layout.IoSVvu2hEbI_In6t6FAw')

# 위의 모든 클래스가 있는 html코드가 몇개 있는지 확인
print(len(result))

for i in result:
    ad = i.select_one('vZ_ErVj5n5d07m6XzhoL')

    if not ad:
        title = i.select_one('.sds-comps-text.sds-comps-text-ellipsis.sds-comps-text-ellipsis-1.sds-comps-text-type-headline1.sds-comps-text-weight-sm').text
        writer = i .select_one('.sds-comps-text.sds-comps-text-ellipsis.sds-comps-text-ellipsis-1').text
        dsc = i.select_one('.sds-comps-text.sds-comps-text-type-body1.sds-comps-text-weight-sm').text
        link = i.select_one('.ialLiYPc7XEN3dJ4Tujv.pHHExKwXvRWn4fm5O0Hr')['href']

        print(f'제목: {title}')
        print(f'작성자: {writer}')
        print(f'글요약: {dsc}')
        print(f'링크: {link}')
        print()

driver.quit()
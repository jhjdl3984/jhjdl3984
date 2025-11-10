# import 라이브러리 => 사용하려면 항상 라이브러리이름.도구 로 접근
# 예) response = requests.get()
# requests => 웹페이지에 요청을 보내서 그 서버(웹페이지)가 보내주는 응답 데이터를 가져오는 기능
import requests  

# bs4 라이브러리 안에 있는 BeautifulSoup 클래스를 가져온다 => bs4 안에 있는 BeautifulSoup 도구를 가져와서 쓴다
# BeautifulSoup => (예쁘게 해석 해주는 도구) 받은 HTML 코드를 파이썬이 이해할 수 있게 트리구조로 구조화하겠다는 틀
from bs4 import BeautifulSoup   

# url = 'url 주소' + input한 변수
# 예) input으로 손흥민을 줬으면 url = 'url주소' + '손흥민'
keyword = input('검색어를 입력해주세요 : ')
url = 'https://search.naver.com/search.naver?ssc=tab.blog.all&sm=tab_jum&query=' + keyword

# get() => get(기능의 이름) + ()(실행시킨다는 의미)
# requests.get(url) => 서버에 GET요청을 보내서 응답(HTML코드, 상태코드 등)을 가져옴
rep = requests.get(url)

# print(rep)          # 라이브러리 응답 객체 출력 => 예) <Response [200]> => HTTP 상태코드 (정상적으로 요청 성공)
# print(rep.text)     # 응답 중 HTML코드만 문자열로 추출 => 예) <!doctype html><html lang="ko"><head>...

html = rep.text

# 받아온 html, css, js 코드를 python은 하나도 모름 => 번역 도와줄 조력자 필요함
# BeautifulSoup => HTML을 트리구조를 만들겠다는 틀만 있음
# html.parser => HTML을 트리구조로 만드는걸 실행
soup = BeautifulSoup(html, 'html.parser')

# select() => ()안의 모든 클래스를 가지고 있는 html코드들을 리스트로 추출
# 공백은 클래스 개수를 뜻함. 공백 지우고 . 붙이기
result = soup.select('.sds-comps-vertical-layout.sds-comps-full-layout.IoSVvu2hEbI_In6t6FAw')

for i in result:
    # print(i)        # result에 들어간 html코드 그자체
    # print(i.text)   # result에 들어간 html코드 태그 안의 텍스트만

    # 광고 관련 태그는 여기
    # select_one() => ()안의 클래스를 가지고 있는 태그중 첫 번째에 있는 태그 하나만 찾음
    # 저 쿨래스가 없다면 ad는 None
    ad = i.select_one('vZ_ErVj5n5d07m6XzhoL')

    # ad가 None일 때
    if not ad:
        # 제목, 링크, 작성자, 글요약
        # i 안에서 해당 클래스들을 모두 가진 첫번째 태그를 찾고 => 그 태그의 텍스트를 추출
        title = i.select_one('.sds-comps-text.sds-comps-text-ellipsis.sds-comps-text-ellipsis-1.sds-comps-text-type-headline1.sds-comps-text-weight-sm').text
        writer = i .select_one('.sds-comps-text.sds-comps-text-ellipsis.sds-comps-text-ellipsis-1').text
        dsc = i.select_one('.sds-comps-text.sds-comps-text-type-body1.sds-comps-text-weight-sm').text
        
        # i 안에서 해당 클래스들을 모두 가진 첫번째 태그를 찾고 => 그 태그의 링크를 추출
        link = i.select_one('.ialLiYPc7XEN3dJ4Tujv.pHHExKwXvRWn4fm5O0Hr')['href']
        # .text => BeautifulSoup이 미리 만들어 놓은 속성이라 .붙여서 사용
        # ['href'] => href는 HTML 태그 안에 들어있음 (예) <a href='링크'></a>)
        # BeautifulSoup에서 HTML 태그의 원래 속성은 딕셔너리처럼 접근 => ' ' 붙여야함

        # 블로그 글 오약
        print(f'제목: {title}')
        print(f'작성자: {writer}')
        print(f'글요약: {dsc}')
        print(f'링크: {link}')
        print()



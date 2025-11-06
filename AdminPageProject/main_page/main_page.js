// 페이지네이션
/* (1) 한 페이지당 4개의 품목만 보이게 설정 */
const itemsPerPage = 4; // 한 페이지에 보여줄 상품 개수
let currentPage = 1; // 현재 페이지 번호를 초기값으로 1 설정

// (2) 테이블 렌더링 함수
/* 매개변수 page: 표시할 페이지 번호
   역할: 선택된 페이지에 맞는 상품 데이터만 테이블에 출력 */
function renderTable(page) {
    // 기존테이블 내용 초기화하여 새로운 데이터를 추가할 공간 확보
    product_data_Table.innerHTML = '';

    // 현재 페이지에 표시할 데이터 범위 계산

    /* 현재 페이지에서 몇 번째부터 보여줄지
       예) page = 2 => 1 * 4 = 4 번째 인덱스부터 시작 */
    const start = (page - 1) * itemsPerPage;

    /* 현재 페이지에서 몇 번째까지 보여줄지
       예) start = 4면 4번째 인덱스부터 => 4+4(개의 상품)=8번째 인덱스 */
    const end = start + itemsPerPage; 

    /* slice(star, end) => start 부터 end 직전까지 잘러서 반환
       예) slince(4, 8) => 4번 ~ 7번 인덱스 상품 */
    // currentItems => 현재 페이지의 상품들만 담긴 배열
    const currentItems = product_data.slice(start, end);

    // 테이블에 현재 페이지 상품 추가
      
    // forEach => currentItems에 있는 각 요소를 하나씩 꺼내서 반복 작업
    // item => 꺼낸 한 상품 객체 예) { category: "상의", brand: 'Supreme', product: '슈프림 박스로고 후드티', price: '390,000' }
    currentItems.forEach(item => {    //
        const row = product_data_Table.insertRow();   // 새로운 행(row) 생성
        row.insertCell(0).innerText = item.category;  // 첫번째 열: 카테고리
        row.insertCell(1).innerText = item.brand;     // 두번째 열: 브랜드
        row.insertCell(2).innerText = item.product;   // 세번째 열: 상품명
        row.insertCell(3).innerText = item.price;     // 네번째 열: 가격
    });
}

/* (3) 페이지 이동 버튼 클릭 시 동작 */
const pagination = document.querySelector('.pagination');
pagination.addEventListener('click', (e) => {       //e => 클릭 이벤트 객체로, 클릭된 요소에 대한 정보를 담고있음
    e.preventDefault();     // 페이지 버튼을 눌러도 새로고침 되지 않게 함
    const target = e.target;    // 예) <a class='page-link'>2</a>를 누르면 target은 '2'가 들어 있는 <a> 태그
    
    // 클릭된 요소가 .page-link를 갖고 있지 않다면 함수 종료 (페이지 버튼이 아닌 빈공간 같은 곳을 누르면 아무일도 X 라는 뜻)
    if (!target.classList.contains('page-link')) return;

    // previous를 눌렀고, 현재페이지(currentPage)가 1보다 클때만 이전 페이지로 이동
    if (target.textContent === 'previous' && currentPage > 1) {
        currentPage--;
    } 
    /* Next를 눌렀고, 아직 마지막 페이지가 아닐 때 다음 페이지로 이동
       Math.ceil(product_data.length / itemsPerPage) => 계산하고 올림 계산
       예) 상품이 10개, 한 페이지에 상품 4개면 Math.ceil(10/4) = 3 (전체 페이지 수 구하기) */
    else if (target.textContent === 'Next' && currentPage < Math.ceil(product_data.length / itemsPerPage)) {
        currentPage++;
    }
    /* !isNaN => !is Not a Number => 숫자가 맞는가?(true)
       예) '2'버튼을 누르면 parseInt('2') => 2로 변환 되어 currentPage = 2 */
    // 페이지 번호 버튼을 눌렀을 때 그 페이지로 바로 이동
    else if (!isNaN(target.textContent)) {
        currentPage = parseInt(target.textContent);
    }
    // 위에서 바뀐 currentPage 값을 이용해 테이블 새로 그림 (현재 페이지에 해당하는 상품 데이터만 다시 보여줌)
    renderTable(currentPage);
});

  // 위에서 두번째 줄에서 쓴 let currentPage = 1;을 활용해서 초기 시작 페이지를 1페이지로 설정
  renderTable(currentPage);
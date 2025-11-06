// 제출 이벤트를 받는다 (이벤트 핸들링)
const form = document.getElementById('form')

form.addEventListener('submit', function(event){
    event.preventDefault();

    let userId = event.target.id.value   // 아이디칸의 값
    let userPw1 = event.target.pw1.value
    let userPw2 = event.target.pw2.value
    let userName = event.target.name.value
    let userPhone = event.target.phone.value
    let userGender = event.target.gender.value
    let userEmail = event.target.email.value
    
    // 7글자 이상인지
    if(userId.length < 6){
        alert('아이디가 너무 짧습니다. 6자 이상 입력해주세요.')
        return
    }

    // 공백 여부 확인
    if(/\s/.test(userId)){
        alert('아이디에 공백은 넣을 수 없습니다.')
        return
    }
    
    // 대소문자 영어, 숫자만 사용
    if(!/^[A-Za-z0-9]+$/.test(userId)){
        alert('아이디는 대소문자 영어와 숫자만 사용 가능합니다.')
        return
    }

    // 아이디 중복인지 확인
    const existingIds = ['candyboy', 'ozcoding'];
    if(existingIds.includes(userId)){
        alert('이미 사용중인 아이디입니다. 다른 아이디를 입력해주세요');
        return;
    }

    // 비밀먼호 8자 이상
    if(userPw1.length < 7){
        alert('비밀번호는 8글자 이상으로 입력해주세요')
        return
    }

    if(userPw1 !== userPw2){
        alert('비밀번호가 일치하지 않습니다.')
        return
    }

    // 공백 사용 불가
    if(/\s/.test(userPw1)){
        alert('비밀번호에는 공백을 넣을 수 없습니다.')
        return
    }

    // 공백 사용 불가
    if(/\s/.test(userName)){
        alert('이름에는 공백을 넣을 수 없습니다.')
        return
    }

    // 특수문자 사용 제한
    if(!/^[A-Za-z가-힣]+$/.test(userName)){
        alert('이름은 영어 또는 한글로 입력해주세요.')
        return
    }

    // 핸드폰 : 숫자만 입력
    if(!/^[0-9]+$/.test(userPhone)){
        alert('핸드폰 번호는 숫자로만 작성해주세요.')
        return
    }

    // 핸드폰 : 11글자
    if(userPhone.length !== 11){
        alert('핸드폰 번호는 숫자 11자로 작성해주세요.')
        return
    }

    alert(`회원 가입 시 입력하신 내역은 다음과 같습니다.\n
        아이디: ${userId}\n
        이름: ${userName}\n
        전화번호: ${userPhone}`);

    // 성공 페이지 이동
    window.location.href = 'success.html';
    document.write(`<p><span style='color: orange';><strong>${userId}님 환영합니다</span></strong></p>`)
})

    // 다크모드
    const toggleBtn = document.getElementById('darkModeToggle');
    toggleBtn.addEventListener('click', () => {
        document.body.classList.toggle('dark-mode');
        document.documentElement.classList.toggle('dark-mode');
        toggleBtn.textContent = document.body.classList.contains('dark-mode') ? '다크모드' : '일반모드';
    });
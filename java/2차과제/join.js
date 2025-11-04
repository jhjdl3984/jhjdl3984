// 제출 이벤트를 받는다 (이벤트 핸들링)
const form = document.getElementById('form')

form.addEventListener('submit', function(event){
    event.preventDefault()

    let userId = event.target.id.value   // 아이디칸의 값
    let userPw1 = event.target.pw1.value
    let userPw2 = event.target.pw2.value
    let userName = event.target.name.value
    let userPhone = event.target.phone.value
    let userPosition = event.target.position.value
    let userGender = event.target.gender.value
    let userEmail = event.target.email.value
    let userIntro = event.target.intro.value
    
    // 입력값에 문제가 있는 경우 이를 감지한다
    if(userId.length < 6){
        alert('아이디가 너무 짧습니다. 6자 이상 입력해주세요.')
        return
    }

    if(userPw1 !== userPw2){
        alert('비밀번호가 일치하지 않습니다.')
        return
    }

    // 제출된 입력 값들을 참조하고 가입 환영 인사를 제공
    document.body.innerHTML = ''    // 제출 누르면 새창으로 새로고침 되면서 아무것도 없는 body태그로 바뀜
    document.write(`<p><span style='color: orange';><strong>${userId}님 환영합니다</span></strong><br>
        회원 가입 시 입력하신 내역은 다음과 같습니다.<br>
        아이디 : ${userId}<br>
        이름 : ${userName}<br>
        전화번호 : ${userPhone}<br>
        원하는 직무 : ${userPosition}</p>`)
})
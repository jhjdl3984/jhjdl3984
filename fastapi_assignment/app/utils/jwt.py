from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timezone, timedelta
import jwt
from typing import Annotated    # Annotated[타입, meta]로 쓰임 => 추가 정보를 함께 전달
from fastapi import Depends, HTTPException, status     # HTTPException => HTTP 요청 처리 중에 오류를 클라이언트에게 알려줄 때 사용
from jwt.exceptions import InvalidTokenError
from app.models.users import UserModel

SECRET_KEY = "radadssadadqwe1231eszdas12e1dasdsad12"    # 임의로 정하는 값
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30    # 생성할 액세스 토큰의 만료기간 30분으로 설정

# OAuth2PasswordBearer => 클라이언트 요청의 Authorization 헤더에서 토큰을 꺼내줌
# => 예) Authorization: Bearer abcdef.12345.ghijk
#           ↓
#       abcdef.12345.ghijk
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='users/login')    # tokenUrl='users/login' => 토큰 발급 받을 로그인 경로

def create_access_token(data: dict):
    # data.copy() => 원본 dict data를 그대로 복사해서 새로운 dict to_encode를 만든다
    # => 원본 data는 그대로 유지할 수 O
    to_encode = data.copy()

    # timezone.utc => UTC 기준 시간 ( 예) # 2025-11-24 06:45:12.123456+00:00 ) => UTC 시간대는 끝에 +00:00이 붙음
    # timedelta => 시간 차이
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    # "exp" => JWT 내부에서 쓰면 무조건 "만료시간"을 뜻하는 키이름 (but, 여기선 아직 JWT 내부인지는 모름)
    to_encode.update({"exp": expire})

    # 여기에서 to_encode가 JWT로 인코딩된다는 것을 알 수 O => "exp"가 JWT의 만료시간 키이름
    # to_encode => JWT payload(내용) / SECRET_KEY => JWT 서명에 사용되는 비밀키 / algorithm => 서명 방식
    # => 이 3가지로 JWT를 만들어 문자열로 변환
    # jwt.encode는 함수 => (to_encode, SECRET_KEY, algorithm=ALGORITHM) 얘네는 파라미터
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

# Depends => 함수 => oauth2_scheme에서 추출한 토큰을 자동으로 token 파라미터에 그 값을 넣는 것을 의미
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",    # 클라이언트에게 보여줄 오류 메시지
        headers={"WWW-Authenticate": "Bearer"},     # 클라이언트가 401 오류를 받으면 이 API는 Bearer 토큰을 사용해야한다고 알려줌
    )   # 출력예시
        # HTTP/1.1 401 Unauthorized
        # WWW-Authenticate: Bearer
        #
        # {
        #   "detail": "Could not validate credentials"
        # }
    try:
        # jwt.decode() => 내부 내용을 추출하는 함수
        # token, SECRET_KEY, algorithms=[ALGORITHM]
        # => token을 header.payload.signature로 나눠서 header의 alg이 지정한 algorithms인지 확인하고,
        #    signature == header + "." + payload를 SECRET_KEY의 암호화 키를 사용해서 재계산 => 같은지 확인
        # => 같다면 payload = JWT 데이터 가 담김
        # => 다르면 except의 오류 발생
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            raise credentials_exception     # 위에서 정의한 예외
    except InvalidTokenError:       # InvalidTokenError => signature가 틀리거나, 토큰 구조가 이상하거나, 만료된 토큰
        credentials_exception.detail = "Invalid token."     # 위에 정의한 예외의 detail이 이 메시지로 덮어짐
        raise credentials_exception

    user = UserModel.get(id=user_id)    # UserModel에서 id가 user_id인 객체
    if user is None:
        credentials_exception.detail = "User not found."
        raise credentials_exception
    return user
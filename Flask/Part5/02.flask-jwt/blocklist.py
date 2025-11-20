# 블록리스트 관리 파일

# 사용자가 로그아웃 => 그 토큰을 BLOCKLIST에 추가
# 서버는 BLOCKLIST에 있는 토큰이면 인증 거부
# set() => 중복 X
BLOCKLIST = set()

# BLOCKLIST에 추가해서 해당 토큰 차단
# jti => JWT 토큰마다 부여되는 고유 ID
def add_to_blocklist(jti):
    BLOCKLIST.add(jti)

# BLOCKLIST에서 제거해서 해당 토큰 차단 해제
def remove_from_blocklist(jti):
    BLOCKLIST.discard(jti)
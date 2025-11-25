from fastapi import FastAPI
from app.models.users import UserModel
from app.models.movies import MovieModel
from app.routers.movies import movie_router
from app.routers.users import user_router

app = FastAPI()

UserModel.create_dummy()    # API 테스트를 위한 더미를 생성하는 메서드 입니다.
MovieModel.create_dummy()

# fastapi 앱에 user_router, movie_router를 등록
app.include_router(user_router)
app.include_router(movie_router)

if __name__ == "__main__":
    import uvicorn

    # uvicorn.run => 비동기
    # import asyncio
    #
    # async def task1():
    #     print("Task1 시작")
    #     await asyncio.sleep(3)  # 3초 기다리는 동안 다른 작업 가능
    #     print("Task1 끝")
    #
    # async def task2():
    #     print("Task2 시작")
    #     await asyncio.sleep(2)
    #     print("Task2 끝")
    # => 둘 다 해서 3초정도 걸림

    # 비동기 처리 하려면 async def 로 엔드포인트를 정의해야함
    uvicorn.run(app, host="0.0.0.0", port=8000)
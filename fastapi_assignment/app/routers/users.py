from fastapi import APIRouter, HTTPException, Path, Query   # HTTPException => fastapi 라이브러리의 클래스
from app.schemas.users import UserCreateRequest, UserUpdateRequest, UserSearchParams
from app.models.users import UserModel
from typing import Annotated

user_router = APIRouter(prefix="/users", tags=["user"])

# prefix URL이 /users 로 기본경로가 되었기 때문에 router 데코레이터의 경로가 ('/users') 였던걸 ('')로 변경
@user_router.post('')
async def create_user(data: UserCreateRequest):
	user = UserModel.create(**data.model_dump())
	return user.id

@user_router.get('')
async def get_all_users():
	result = UserModel.all()
	if not result:
		raise HTTPException(status_code=404)
	return result

@user_router.get('/search')
async def search_users(query_params: Annotated[UserSearchParams, Query()]):
    valid_query = {key: value for key, value in query_params.model_dump().items() if value is not None}
    filtered_users = UserModel.filter(**valid_query)
    if not filtered_users:
        raise HTTPException(status_code=404)
    return filtered_users

@user_router.get('/{user_id}')
async def get_user(user_id: int = Path(gt=0)):
	user = UserModel.get(id=user_id)
	if user is None:
		raise HTTPException(status_code=404)
        return user

@user_router.patch('/{user_id}')
async def update_user(data: UserUpdateRequest, user_id: int = Path(gt=0)):
	user = UserModel.get(id=user_id)
	if user is None:
		raise HTTPException(status_code=404)
	user.update(**data.model_dump())
	return user

@user_router.delete('/{user_id}')
async def delete_user(user_id: int = Path(gt=0)):
	user = UserModel.get(id=user_id)
	if user is None:
		raise HTTPException(status_code=404)
	user.delete()

	return {'detail': f'User: {user_id}, Successfully Deleted.'}

@user_router.post('/login', response_model=Token)
async def login_user(data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = UserModel.authenticate(data.username, data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"user.id": user.id})
    user.update(last_login=datetime.now())
    return Token(access_token=access_token, token_type="bearer")

@user_router.get('/me')
async def get_user(user: Annotated[UserModel, Depends(get_current_user)]):
	return user


@user_router.patch('/me')
async def update_user(
	user: Annotated[UserModel, Depends(get_current_user)],
	data: UserUpdateRequest,
):
	if user is None:
		raise HTTPException(status_code=404)
	user.update(**data.model_dump())
	return user


@user_router.delete('/me')
async def delete_user(user: Annotated[UserModel, Depends(get_current_user)]):
	user.delete()
	return {'detail': 'Successfully Deleted.'}








from typing import List, Optional, Any

from fastapi import APIRouter, status, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

from sqlalchemy.ext.asyncio import AsyncSession

from schemas.user_schema import UserSchemaBase, UserSchemaCreate, UserSchemaUp
from models.user_model import UserModel
from core.database import get_session
from core.deps import get_current_user
# from core.security import checked_password, generate_hash_password
from core.auth import authenticate, create_token_acess

from repositories.user_repository import UserRepository


router = APIRouter()

user_repository = UserRepository()

# ---------------------------------------------------------

@router.get('/logado', response_model=UserSchemaBase)
def get_logado(usuario_logado: UserModel = Depends(get_current_user)):
    return usuario_logado


# signUp
@router.post('/signup', status_code=status.HTTP_201_CREATED, response_model=UserSchemaBase)
async def post_usuario_jwt(
    user: UserSchemaCreate, 
    db: AsyncSession = Depends(get_session)
):
    return await user_repository.create(user, db)


@router.post('/login')
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: AsyncSession = Depends(get_session)
):
    user = await authenticate(
        email=form_data.username, 
        password=form_data.password, 
        db=db
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail='Dados de acesso incorretos.'
        )
    return JSONResponse(
        content=dict(acess_token=create_token_acess(sub=user.id), token_type="bearer"), 
        status_code=200)

# ---------------------------------------------------------


@router.get('/', status_code=status.HTTP_200_OK, response_model=List[UserSchemaBase])
async def get_users(db: AsyncSession = Depends(get_session)):
    result = await user_repository.list_users(db=db)
    return result


@router.get('/{user_id}', status_code=status.HTTP_200_OK, response_model=UserSchemaBase)
async def get_user(user_id: int, db: AsyncSession = Depends(get_session)):
    result = await user_repository.show(id=user_id, db=db)
    return result


@router.put('/{user_id}', status_code=status.HTTP_202_ACCEPTED, response_model=UserSchemaUp)
async def put_user(user_id: int, user: UserSchemaUp, db: AsyncSession = Depends(get_session)):
    result = await user_repository.alter(id=user_id, body=user, db=db)
    return result


@router.delete('/{user_id}', status_code=status.HTTP_202_ACCEPTED)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_session)):
    result = await user_repository.delete(id=user_id, db=db)
    return result
        


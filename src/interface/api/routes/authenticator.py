from fastapi import APIRouter, HTTPException
from src.service.authentication.authentication_users import AuthService
from src.domain.entities.usuario import LoginData, TokenData, Usuario
from src.repository.usuario_repository import UsuarioRepository
from passlib.context import CryptContext

# Inicializando o repositório e o serviço de autenticação
usuario_repository = UsuarioRepository()
auth_service = AuthService(repository=usuario_repository)

# Contexto de hash de senhas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

auth_router = APIRouter()

# Rota para login de usuários
@auth_router.post("/login", response_model=TokenData)
async def login(data: LoginData):
    """Realiza a autenticação e retorna um token."""
    # Chama o serviço de autenticação
    token = auth_service.autenticar_usuario(data.username, data.password)

    if not token:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    return {"access_token": token, "token_type": "bearer"}

# Rota para registro de novos usuários
@auth_router.post("/register", response_model=TokenData)
async def register(usuario: Usuario):
    """Realiza o registro de um novo usuário e retorna o token."""
    # Chama o serviço de autenticação para registrar o usuário
    token = auth_service.registrar_usuario(usuario.nome, usuario.email, usuario.senha)

    if not token:
        raise HTTPException(status_code=400, detail="Falha ao registrar usuário")

    return {"access_token": token, "token_type": "bearer"}

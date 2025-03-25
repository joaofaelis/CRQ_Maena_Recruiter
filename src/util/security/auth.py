import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from decouple import config
from jose import JWTError
from typing import Optional
from src.repository.usuario_repository import UsuarioRepository
from src.domain.entities.usuario import UsuarioBase  # Corrigido para importar o modelo adequado

# Configurações do JWT e senha
SECRET_KEY = config("SECRET_KEY", default="sua_chave_secreta")  # Recomendado usar variáveis de ambiente
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Função para verificar a senha
def verificar_senha(plain_password: str, hashed_password: str) -> bool:
    """Verifica se a senha fornecida bate com o hash da senha armazenada"""
    return pwd_context.verify(plain_password, hashed_password)


# Função para criar o JWT
def criar_token_jwt(dados: dict) -> str:
    """Cria o token JWT com os dados fornecidos"""
    to_encode = dados.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# Função para verificar o token e retornar o usuário
def verificar_token(token: str, repository: UsuarioRepository) -> Optional[UsuarioBase]:
    """Verifica a validade do token JWT e retorna o usuário se válido"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        usuario_email: str = payload.get("sub")
        if usuario_email is None:
            raise JWTError("Token inválido")

        # Usando UsuarioBase para garantir que o retorno seja compatível com a entidade definida
        usuario = repository.buscar_usuario_por_email(usuario_email)
        if usuario is None:
            raise JWTError("Usuário não encontrado")

        return usuario
    except JWTError:
        raise JWTError("Token inválido ou expirado")

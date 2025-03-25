from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from decouple import config
from src.repository.usuario_repository import UsuarioRepository
from src.domain.entities.usuario import UsuarioBase  # Corrigido para retornar a entidade correta

SECRET_KEY = config("SECRET_KEY", default="sua_chave_secreta")
ALGORITHM = "HS256"
security = HTTPBearer()

# Função para obter o usuário autenticado a partir do token
def obter_usuario_atual(credentials: HTTPAuthorizationCredentials = Security(security), repository: UsuarioRepository = Depends()) -> dict:
    """Valida o token e retorna o usuário autenticado como um dicionário"""
    token = credentials.credentials  # Obtém o token JWT enviado pelo usuário
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")

        if not email:
            raise HTTPException(status_code=401, detail="Token inválido")

        # Busca o usuário no banco de dados
        usuario = repository.buscar_usuario_por_email(email)
        if not usuario:
            raise HTTPException(status_code=401, detail="Usuário não encontrado")

        # Retorna o usuário como um dicionário
        return {
            "id": usuario.id,
            "nome": usuario.nome,
            "email": usuario.email,
            "tipo_usuario": usuario.tipo_usuario
        }

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")


from fastapi import APIRouter, HTTPException, Depends
from src.repository.usuario_repository import UsuarioRepository
from src.util.security.auth import criar_token_jwt, verificar_senha
from src.domain.entities.usuario import UsuarioCreate, UsuarioLogin

router = APIRouter()

# Instanciando o repositório
usuario_repository = UsuarioRepository()

@router.post("/registro/")
def registrar_usuario(usuario: UsuarioCreate):
    # Verifica se o usuário já existe no banco de dados
    usuario_existente = usuario_repository.buscar_usuario_por_email(usuario.email)
    if usuario_existente:
        raise HTTPException(status_code=400, detail="Email já cadastrado")

    # Cria o usuário no banco de dados
    return usuario_repository.criar_usuario(usuario.nome, usuario.email, usuario.senha, usuario.tipo_usuario)

@router.post("/login/")
def login(usuario: UsuarioLogin):
    # Busca o usuário no banco de dados
    usuario_db = usuario_repository.buscar_usuario_por_email(usuario.email)
    if not usuario_db:
        raise HTTPException(status_code=400, detail="Email ou senha incorretos")

    # Desempacota os valores do usuário retornado do banco
    id, nome, email, senha_hash, tipo_usuario = usuario_db

    # Verifica se a senha fornecida bate com a senha armazenada
    if not verificar_senha(usuario.senha, senha_hash):
        raise HTTPException(status_code=400, detail="Email ou senha incorretos")

    # Gera o token JWT
    token = criar_token_jwt({"sub": email, "tipo_usuario": tipo_usuario})

    return {"access_token": token, "token_type": "bearer"}

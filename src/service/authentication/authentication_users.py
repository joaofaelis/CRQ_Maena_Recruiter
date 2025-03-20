from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from typing import Optional
from src.repository.usuario_repository import UsuarioRepository
from src.domain.entities.usuario import Usuario

# Configuração do JWT
SECRET_KEY = "seu_segredo_super_secreto"  # Substituir por uma chave segura
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Hash de senhas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    def __init__(self, repository: UsuarioRepository):
        self.repository = repository

    def verificar_senha(self, senha: str, senha_hash: str) -> bool:
        """Verifica se a senha fornecida bate com o hash da senha armazenada"""
        return pwd_context.verify(senha, senha_hash)

    def gerar_hash_senha(self, senha: str) -> str:
        """Gera o hash da senha para armazenamento seguro"""
        return pwd_context.hash(senha)

    def gerar_token(self, usuario: Usuario) -> str:
        """Gera o token JWT para o usuário"""
        expiracao = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        payload = {"sub": usuario.email, "exp": expiracao}
        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    def autenticar_usuario(self, email: str, senha: str) -> Optional[str]:
        """Autentica o usuário e retorna o token se válido"""
        usuario = self.repository.buscar_por_email(email)
        if not usuario:
            print(f"Usuário não encontrado para o email: {email}")  # Debugging
            return None
        if not self.verificar_senha(senha, usuario.senha):
            print(f"Senha inválida para o usuário: {email}")  # Debugging
            return None
        return self.gerar_token(usuario)

    def verificar_token(self, token: str) -> Usuario:
        """Verifica a validade do token JWT e retorna o usuário"""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            usuario_email: str = payload.get("sub")
            if usuario_email is None:
                raise JWTError("Token inválido")
            usuario = self.repository.buscar_por_email(usuario_email)
            if usuario is None:
                raise JWTError("Usuário não encontrado")
            return usuario
        except JWTError:
            raise JWTError("Token inválido ou expirado")

    def registrar_usuario(self, nome: str, email: str, senha: str) -> Optional[str]:
        """Registra um novo usuário no banco de dados"""
        # Verifica se o email já está cadastrado
        usuario_existente = self.repository.buscar_por_email(email)
        if usuario_existente:
            print(f"Email {email} já cadastrado.")  # Debugging
            return None

        # Gera o hash da senha
        senha_hash = self.gerar_hash_senha(senha)

        # Cria um novo objeto Usuario
        novo_usuario = Usuario(nome=nome, email=email, senha=senha_hash)

        # Salva o novo usuário no banco de dados
        self.repository.salvar_usuario(novo_usuario, senha_hash)

        # Retorna um token para o novo usuário
        return self.gerar_token(novo_usuario)

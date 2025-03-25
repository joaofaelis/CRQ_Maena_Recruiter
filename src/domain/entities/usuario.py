from pydantic import BaseModel, EmailStr

class UsuarioBase(BaseModel):
    nome: str
    email: EmailStr
    tipo_usuario: str  # 'ADM' ou 'USUARIO'

class UsuarioCreate(UsuarioBase):
    senha: str  # Senha será convertida para hash antes de salvar

class UsuarioLogin(BaseModel):
    email: EmailStr
    senha: str

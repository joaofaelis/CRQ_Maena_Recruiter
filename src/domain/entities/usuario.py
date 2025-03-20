from pydantic import BaseModel, EmailStr

# Entidade de Usuario
class Usuario(BaseModel):
    id: int | None = None  # Permitindo que o id seja opcional
    nome: str
    email: EmailStr
    senha: str | None = None  # Senha não será retornada nas respostas

    class Config:
        from_attributes = True  # Garantindo que o Pydantic v2 mapeie atributos do banco corretamente

# Modelo de Login
class LoginData(BaseModel):
    username: str
    password: str

# Modelo de Token
class TokenData(BaseModel):
    access_token: str
    token_type: str

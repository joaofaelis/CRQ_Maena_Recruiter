from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class Cadastro(BaseModel):
    nome_completo: str
    cpf: str
    telefone: Optional[str]
    email: Optional[str]
    estado: Optional[str]
    bairro: Optional[str]
    sexo: Optional[str]
    idade: int
    assunto: Optional[str]
    data_participacao: Optional[datetime]
    metodologia: Optional[str]
    cliente: Optional[str]
    classe_social: Optional[str]
    ocupacao: Optional[str]
    nome_recrutador: Optional[str]
    digitador: Optional[str]
    id: Optional[int] = None

    class Config:
        from_attributes = True  # Alteração aqui de 'orm_mode' para 'from_attributes'

    def __repr__(self):
        return f"<Cadastro {self.nome_completo} - {self.cpf}>"

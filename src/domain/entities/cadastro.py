from datetime import datetime
from typing import Optional

class Cadastro:
    def __init__(
        self,
        nome_completo: str,
        cpf: str,
        telefone: Optional[str],
        email: Optional[str],
        estado: Optional[str],
        bairro: Optional[str],
        sexo: Optional[str],
        idade: int,
        assunto: Optional[str],
        data_participacao: Optional[datetime],
        metodologia: Optional[str],
        cliente: Optional[str],
        classe_social: Optional[str],
        ocupacao: Optional[str],
        nome_recrutador: Optional[str],
        digitador: Optional[str],
        id: int = None,
        carimbo_data_hora: datetime = datetime.now()
    ):
        self.id = id
        self.carimbo_data_hora = carimbo_data_hora
        self.nome_completo = nome_completo
        self.cpf = cpf
        self.telefone = telefone
        self.email = email
        self.estado = estado
        self.bairro = bairro
        self.sexo = sexo
        self.idade = idade
        self.assunto = assunto
        self.data_participacao = data_participacao
        self.metodologia = metodologia
        self.cliente = cliente
        self.classe_social = classe_social
        self.ocupacao = ocupacao
        self.nome_recrutador = nome_recrutador
        self.digitador = digitador

    def __repr__(self):
        return f"<Cadastro {self.nome_completo} - {self.cpf}>"

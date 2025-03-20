from fastapi import FastAPI
from src.service.cadastro_service.services import CadastroService
from src.domain.entities.cadastro import Cadastro
from typing import List

app = FastAPI()

# Instanciando o serviço
cadastro_service = CadastroService()

@app.post("/cadastro/", response_model=Cadastro)
async def criar_cadastro(cadastro: Cadastro):
    """Cria um novo cadastro."""
    cadastro_criado = cadastro_service.criar_cadastro(cadastro)
    return cadastro_criado

@app.get("/cadastro/{cpf}", response_model=Cadastro)
async def buscar_cadastro(cpf: str):
    """Busca cadastro pelo CPF."""
    cadastro = cadastro_service.buscar_por_cpf(cpf)
    if cadastro:
        return cadastro
    return {"message": "Cadastro não encontrado"}

@app.get("/cadastros/", response_model=List[Cadastro])
async def listar_todos_cadastros():
    """Lista todos os cadastros."""
    cadastros = cadastro_service.listar_todos_cadastros()
    return cadastros

@app.put("/cadastro/{cpf}", response_model=Cadastro)
async def atualizar_cadastro(cpf: str, cadastro: Cadastro):
    """Atualiza um cadastro existente."""
    cadastro.cpf = cpf  # Garantir que o cpf é atualizado corretamente
    cadastro_atualizado = cadastro_service.atualizar_cadastro(cadastro)
    return cadastro_atualizado

@app.delete("/cadastro/{cpf}")
async def deletar_cadastro(cpf: str):
    """Deleta um cadastro."""
    cadastro_service.deletar_cadastro(cpf)
    return {"message": "Cadastro deletado com sucesso"}

from fastapi import APIRouter
from src.service.cadastro_service.services import CadastroService
from src.domain.entities.cadastro import Cadastro
from typing import List

cadastro_router = APIRouter()
cadastro_service = CadastroService()

@cadastro_router.post("/", response_model=Cadastro)
async def criar_cadastro(cadastro: Cadastro):
    """Cria um novo cadastro."""
    return cadastro_service.criar_cadastro(cadastro)

@cadastro_router.get("/{cpf}", response_model=Cadastro)
async def buscar_cadastro(cpf: str):
    """Busca cadastro pelo CPF."""
    cadastro = cadastro_service.buscar_por_cpf(cpf)
    if cadastro:
        return cadastro
    return {"message": "Cadastro não encontrado"}

@cadastro_router.get("/", response_model=List[Cadastro])
async def listar_todos_cadastros():
    """Lista todos os cadastros."""
    return cadastro_service.listar_todos_cadastros()

@cadastro_router.put("/{cpf}", response_model=Cadastro)
async def atualizar_cadastro(cpf: str, cadastro: Cadastro):
    """Atualiza um cadastro existente."""
    cadastro.cpf = cpf
    return cadastro_service.atualizar_cadastro(cadastro)

@cadastro_router.delete("/{cpf}")
async def deletar_cadastro(cpf: str):
    """Deleta um cadastro."""
    cadastro_service.deletar_cadastro(cpf)
    return {"message": "Cadastro deletado com sucesso"}

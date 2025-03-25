from fastapi import APIRouter, HTTPException
from src.service.cadastro_service.services import CadastroService
from src.domain.entities.cadastro import Cadastro, AtualizarCadastro
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
    try:
        cadastro = cadastro_service.buscar_por_cpf(cpf)
        if not cadastro:
            raise HTTPException(status_code=404, detail="Cadastro não encontrado")
        return cadastro
    except ValueError as e:
        # Erro caso o CPF não seja válido
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Captura qualquer outro erro e retorna uma mensagem mais detalhada
        raise HTTPException(status_code=500, detail=f"Erro ao encontrar o cadastro: {str(e)}")

@cadastro_router.get("/", response_model=List[Cadastro])
async def listar_todos_cadastros():
    """Lista todos os cadastros."""
    return cadastro_service.listar_todos_cadastros()

@cadastro_router.put("/{cpf}", response_model=AtualizarCadastro)
async def atualizar_cadastro(cpf: str, cadastro: AtualizarCadastro):
    """Atualiza um cadastro existente."""
    # O CPF está na URL, então não é necessário incluí-lo no modelo.
    return cadastro_service.atualizar_cadastro(cpf, cadastro)


@cadastro_router.delete("/{cpf}")
async def deletar_cadastro(cpf: str):
    """Deleta um cadastro."""
    try:
        # Chama o serviço para deletar o cadastro
        cadastro_service.deletar_cadastro(cpf)
        return {"message": "Cadastro deletado com sucesso!"}
    except ValueError as e:
        # Erro caso o CPF não seja válido
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Captura qualquer outro erro e retorna uma mensagem mais detalhada
        raise HTTPException(status_code=500, detail=f"Erro ao deletar o cadastro: {str(e)}")
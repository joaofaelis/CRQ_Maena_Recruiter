from fastapi import APIRouter, HTTPException, Depends
from src.service.cadastro_service.services import CadastroService
from src.domain.entities.cadastro import Cadastro, AtualizarCadastro
from src.util.security.dependencies import obter_usuario_atual
from typing import List

cadastro_router = APIRouter()
cadastro_service = CadastroService()

@cadastro_router.post("/", response_model=Cadastro)
async def criar_cadastro(cadastro: Cadastro, usuario: dict = Depends(obter_usuario_atual)):
    """Cria um novo cadastro (Apenas usuários autenticados podem criar)."""
    if usuario["tipo_usuario"] != "ADM":  # Verifica se o usuário tem permissões adequadas
        raise HTTPException(status_code=403, detail="Permissão negada")
    return cadastro_service.criar_cadastro(cadastro)

@cadastro_router.get("/{cpf}", response_model=Cadastro)
async def buscar_cadastro(cpf: str, usuario: dict = Depends(obter_usuario_atual)):
    """Busca cadastro pelo CPF (Apenas usuários autenticados podem buscar)."""
    try:
        cadastro = cadastro_service.buscar_por_cpf(cpf)
        if not cadastro:
            raise HTTPException(status_code=404, detail="Cadastro não encontrado")
        return cadastro
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao encontrar o cadastro: {str(e)}")

@cadastro_router.get("/", response_model=List[Cadastro])
async def listar_todos_cadastros(usuario: dict = Depends(obter_usuario_atual)):
    """Lista todos os cadastros (Apenas usuários autenticados podem listar)."""
    if usuario["tipo_usuario"] != "ADM":  # Verifica se o usuário é ADMIN para listar todos os cadastros
        raise HTTPException(status_code=403, detail="Acesso negado. Usuário não é ADMIN.")
    return cadastro_service.listar_todos_cadastros()

@cadastro_router.put("/{cpf}", response_model=AtualizarCadastro)
async def atualizar_cadastro(cpf: str, cadastro: AtualizarCadastro, usuario: dict = Depends(obter_usuario_atual)):
    """Atualiza um cadastro existente (Apenas usuários autenticados podem atualizar)."""
    return cadastro_service.atualizar_cadastro(cpf, cadastro)

@cadastro_router.delete("/{cpf}")
async def deletar_cadastro(cpf: str, usuario: dict = Depends(obter_usuario_atual)):
    """Deleta um cadastro (Apenas usuários autenticados podem deletar)."""
    if usuario["tipo_usuario"] != "ADM":  # Verifica se o usuário é ADMIN para deletar cadastros
        raise HTTPException(status_code=403, detail="Permissão negada")
    try:
        cadastro_service.deletar_cadastro(cpf)
        return {"message": "Cadastro deletado com sucesso!"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao deletar o cadastro: {str(e)}")

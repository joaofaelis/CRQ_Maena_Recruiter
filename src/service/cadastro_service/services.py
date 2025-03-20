from src.repository.cadastro_repository import CadastroRepository
from src.domain.entities.cadastro import Cadastro
from typing import List, Optional


class CadastroService:
    def __init__(self):
        self.repo = CadastroRepository()

    def criar_cadastro(self, cadastro: Cadastro) -> Cadastro:
        """Cria um novo cadastro no sistema."""
        # Validações podem ser feitas aqui antes de chamar o repositório
        if not cadastro.cpf or len(cadastro.cpf) != 11:
            raise ValueError("CPF inválido.")

        # Chama o repositório para inserir o cadastro
        return self.repo.inserir(cadastro)

    def buscar_por_cpf(self, cpf: str) -> Optional[Cadastro]:
        """Busca um cadastro pelo CPF."""
        if not cpf or len(cpf) != 11:
            raise ValueError("CPF inválido.")

        # Chama o repositório para buscar o cadastro
        return self.repo.buscar_por_cpf(cpf)

    def listar_todos_cadastros(self) -> List[Cadastro]:
        """Retorna todos os cadastros do sistema."""
        # Chama o repositório para listar todos os cadastros
        return self.repo.listar_todos()

    def atualizar_cadastro(self, cadastro: Cadastro) -> None:
        """Atualiza um cadastro existente."""
        if not cadastro.cpf:
            raise ValueError("CPF do cadastro é necessário para atualização.")

        # Chama o repositório para atualizar o cadastro
        self.repo.atualizar(cadastro)

    def deletar_cadastro(self, cpf: str) -> None:
        """Deleta um cadastro pelo CPF."""
        if not cpf:
            raise ValueError("CPF do cadastro é necessário para deletar.")

        # Chama o repositório para deletar o cadastro
        self.repo.deletar(cpf)

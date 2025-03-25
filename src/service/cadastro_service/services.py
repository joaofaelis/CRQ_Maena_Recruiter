from src.repository.cadastro_repository import CadastroRepository
from src.domain.entities.cadastro import Cadastro, AtualizarCadastro
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

    def atualizar_cadastro(self, cpf: str, cadastro: AtualizarCadastro):
        """Atualiza um cadastro existente e retorna o cadastro atualizado."""
        # Chama o método de atualizar no repositório, passando cpf e cadastro
        self.repo.atualizar(cpf, cadastro)
        return cadastro

    def deletar_cadastro(self, cpf: str) -> None:
        """Deleta um cadastro pelo CPF após validação."""
        if not cpf:
            raise ValueError("CPF do cadastro é necessário para deletar.")

        try:
            # Chama o repositório para deletar o cadastro
            self.repo.deletar(cpf)
        except Exception as e:
            # Se ocorrer um erro, propaga uma exceção com uma mensagem mais detalhada
            raise Exception(f"Erro ao tentar deletar o cadastro com CPF {cpf}: {str(e)}")

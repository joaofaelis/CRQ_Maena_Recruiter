import pytest
from src.service.cadastro_service.services import CadastroService
from src.domain.entities.cadastro import Cadastro
from unittest.mock import MagicMock
from typing import Optional


# Configuração do mock do repositório
@pytest.fixture
def mock_cadastro_repository():
    mock_repo = MagicMock()
    service = CadastroService()
    service.repo = mock_repo
    return service, mock_repo


def test_criar_cadastro(mock_cadastro_repository):
    service, mock_repo = mock_cadastro_repository

    # Criação do cadastro fictício
    cadastro = Cadastro(
        id=None,  # O ID será gerado pelo banco de dados
        nome_completo="João da Silva",
        cpf="12345678901",
        telefone="999999999",
        email="joao.silva@email.com",
        estado="PE",
        bairro="Centro",
        sexo="M",
        idade=30,
        assunto="Entrevista",
        data_participacao="2025-03-20",
        metodologia="Qualitativa",
        cliente="Cliente X",
        classe_social="A",
        ocupacao="Analista",
        nome_recrutador="Recrutador Y",
        digitador="Digitador Z",
        carimbo_data_hora="2025-03-20 10:00:00"
    )

    # O repositório irá retornar o cadastro com um ID gerado
    cadastro.id = 1  # Simulando a geração de ID
    mock_repo.inserir.return_value = cadastro

    # Chama o método de criar cadastro
    resultado = service.criar_cadastro(cadastro)

    # Verifica se a função do repositório foi chamada
    mock_repo.inserir.assert_called_once_with(cadastro)

    # Verifica o resultado retornado
    assert resultado.id is not None
    assert resultado.id == 1  # Verifica se o ID gerado é 1
    assert resultado.nome_completo == "João da Silva"
    assert resultado.cpf == "12345678901"


def test_buscar_por_cpf(mock_cadastro_repository):
    service, mock_repo = mock_cadastro_repository

    # Criação do cadastro fictício
    cadastro = Cadastro(
        id=1,
        nome_completo="João da Silva",
        cpf="12345678901",
        telefone="999999999",
        email="joao.silva@email.com",
        estado="PE",
        bairro="Centro",
        sexo="M",
        idade=30,
        assunto="Entrevista",
        data_participacao="2025-03-20",
        metodologia="Qualitativa",
        cliente="Cliente X",
        classe_social="A",
        ocupacao="Analista",
        nome_recrutador="Recrutador Y",
        digitador="Digitador Z",
        carimbo_data_hora="2025-03-20 10:00:00"
    )

    # O repositório irá retornar o cadastro quando buscado por CPF
    mock_repo.buscar_por_cpf.return_value = cadastro

    # Chama o método de buscar por CPF
    resultado = service.buscar_por_cpf("12345678901")

    # Verifica se a função do repositório foi chamada com o CPF correto
    mock_repo.buscar_por_cpf.assert_called_once_with("12345678901")

    # Verifica o resultado retornado
    assert resultado is not None
    assert resultado.cpf == "12345678901"
    assert resultado.nome_completo == "João da Silva"


def test_listar_todos_cadastros(mock_cadastro_repository):
    service, mock_repo = mock_cadastro_repository

    # Criação de uma lista de cadastros fictícios
    cadastro1 = Cadastro(
        id=1,
        nome_completo="João da Silva",
        cpf="12345678901",
        telefone="999999999",
        email="joao.silva@email.com",
        estado="PE",
        bairro="Centro",
        sexo="M",
        idade=30,
        assunto="Entrevista",
        data_participacao="2025-03-20",
        metodologia="Qualitativa",
        cliente="Cliente X",
        classe_social="A",
        ocupacao="Analista",
        nome_recrutador="Recrutador Y",
        digitador="Digitador Z",
        carimbo_data_hora="2025-03-20 10:00:00"
    )
    cadastro2 = Cadastro(
        id=2,
        nome_completo="Maria Oliveira",
        cpf="98765432100",
        telefone="988888888",
        email="maria.oliveira@email.com",
        estado="PE",
        bairro="Centro",
        sexo="F",
        idade=28,
        assunto="Treinamento",
        data_participacao="2025-03-21",
        metodologia="Quantitativa",
        cliente="Cliente Y",
        classe_social="B",
        ocupacao="Consultora",
        nome_recrutador="Recrutador Z",
        digitador="Digitador W",
        carimbo_data_hora="2025-03-21 11:00:00"
    )

    mock_repo.listar_todos.return_value = [cadastro1, cadastro2]

    # Chama o método de listar todos os cadastros
    resultado = service.listar_todos_cadastros()

    # Verifica se a função do repositório foi chamada
    mock_repo.listar_todos.assert_called_once()

    # Verifica o resultado retornado
    assert len(resultado) == 2
    assert resultado[0].nome_completo == "João da Silva"
    assert resultado[1].nome_completo == "Maria Oliveira"


def test_atualizar_cadastro(mock_cadastro_repository):
    service, mock_repo = mock_cadastro_repository

    # Criação do cadastro fictício
    cadastro = Cadastro(
        id=1,
        nome_completo="João da Silva",
        cpf="12345678901",
        telefone="999999999",
        email="joao.silva@email.com",
        estado="PE",
        bairro="Centro",
        sexo="M",
        idade=30,
        assunto="Entrevista",
        data_participacao="2025-03-20",
        metodologia="Qualitativa",
        cliente="Cliente X",
        classe_social="A",
        ocupacao="Analista",
        nome_recrutador="Recrutador Y",
        digitador="Digitador Z",
        carimbo_data_hora="2025-03-20 10:00:00"
    )

    # Chama o método de atualizar cadastro
    service.atualizar_cadastro(cadastro)

    # Verifica se a função do repositório foi chamada
    mock_repo.atualizar.assert_called_once_with(cadastro)


def test_deletar_cadastro(mock_cadastro_repository):
    service, mock_repo = mock_cadastro_repository

    # Chama o método de deletar cadastro
    service.deletar_cadastro(1)

    # Verifica se a função do repositório foi chamada com o ID correto
    mock_repo.deletar.assert_called_once_with(1)

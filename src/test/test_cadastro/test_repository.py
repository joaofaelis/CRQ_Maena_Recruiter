import pytest
from unittest.mock import MagicMock
from src.domain.entities.cadastro import Cadastro
from src.infrastructure.SQL.main import InfrastructureSQL
from src.repository.cadastro_repository import CadastroRepository


@pytest.fixture
def mock_db(mocker):
    mock_db_instance = MagicMock(spec=InfrastructureSQL)
    mocker.patch('src.repository.cadastro_repository.InfrastructureSQL', return_value=mock_db_instance)
    return mock_db_instance


@pytest.fixture
def cadastro():
    return Cadastro(
        id=None,
        nome_completo="João da Silva",
        cpf="12345678900",
        telefone="123456789",
        email="joao@email.com",
        estado="PE",
        bairro="Centro",
        sexo="M",
        idade=30,
        assunto="Assunto 1",
        data_participacao="2025-03-20",
        metodologia="Metodologia 1",
        cliente="Cliente 1",
        classe_social="Classe 1",
        ocupacao="Ocupacao 1",
        nome_recrutador="Recrutador 1",
        digitador="Digitador 1",
        carimbo_data_hora="2025-03-20 10:00:00"
    )


def test_inserir(mock_db, cadastro):
    # Definindo o comportamento do mock
    mock_cursor = MagicMock()
    mock_db.cursor_db.return_value = mock_cursor
    mock_cursor.fetchone.return_value = [1]  # Simula o retorno de um ID gerado no banco

    repo = CadastroRepository()

    # Chama o método
    result = repo.inserir(cadastro)

    # Verifica se o ID foi atualizado
    assert result.id == 1
    mock_cursor.execute.assert_called_with("SELECT SCOPE_IDENTITY()")


def test_buscar_por_cpf(mock_db, cadastro):
    # Configura o mock para o resultado da busca
    mock_cursor = MagicMock()
    mock_db.cursor_db.return_value = mock_cursor
    mock_cursor.fetchone.return_value = (
        1, "2025-03-20 10:00:00", "João da Silva", "12345678900", "123456789", "joao@email.com", "PE", "Centro", "M",
        30,
        "Assunto 1", "2025-03-20", "Metodologia 1", "Cliente 1", "Classe 1", "Ocupacao 1", "Recrutador 1", "Digitador 1"
    )

    repo = CadastroRepository()

    # Chama o método
    result = repo.buscar_por_cpf(cadastro.cpf)

    # Verifica se o resultado é um objeto Cadastro correto
    assert result is not None
    assert result.cpf == "12345678900"
    assert result.nome_completo == "João da Silva"


def test_listar_todos(mock_db, cadastro):
    # Configura o mock para o resultado da busca
    mock_cursor = MagicMock()
    mock_db.cursor_db.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [
        (1, "2025-03-20 10:00:00", "João da Silva", "12345678900", "123456789", "joao@email.com", "PE", "Centro", "M",
         30,
         "Assunto 1", "2025-03-20", "Metodologia 1", "Cliente 1", "Classe 1", "Ocupacao 1", "Recrutador 1",
         "Digitador 1")
    ]

    repo = CadastroRepository()

    # Chama o método
    result = repo.listar_todos()

    # Verifica se o resultado é uma lista e contém o Cadastro correto
    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0].nome_completo == "João da Silva"


def test_atualizar(mock_db, cadastro):
    # Mocking cursor
    mock_cursor = MagicMock()
    mock_db.cursor_db.return_value = mock_cursor

    repo = CadastroRepository()

    # Chama o método
    repo.atualizar(cadastro)

    # Verifica se o método de execução foi chamado corretamente
    mock_cursor.execute.assert_called_with(
        """
        UPDATE CADASTRO SET
            Nome_Completo = ?, CPF = ?, Telefone = ?, Email = ?, Estado = ?, Bairro = ?, Sexo = ?, Idade = ?, Assunto = ?, 
            Data_participacao = ?, Metodologia = ?, Cliente = ?, Classe_Social = ?, Ocupacao = ?, 
            Nome_recrutador = ?, Digitador = ?, Carimbo_Data_Hora = ?
        WHERE ID = ?
        """,
        (cadastro.nome_completo, cadastro.cpf, cadastro.telefone, cadastro.email,
         cadastro.estado, cadastro.bairro, cadastro.sexo, cadastro.idade, cadastro.assunto,
         cadastro.data_participacao, cadastro.metodologia, cadastro.cliente, cadastro.classe_social,
         cadastro.ocupacao, cadastro.nome_recrutador, cadastro.digitador, cadastro.carimbo_data_hora, cadastro.id)
    )


def test_deletar(mock_db):
    # Mocking cursor
    mock_cursor = MagicMock()
    mock_db.cursor_db.return_value = mock_cursor

    repo = CadastroRepository()

    # Chama o método
    repo.deletar(1)

    # Verifica se a execução do delete foi chamada corretamente
    mock_cursor.execute.assert_called_with("DELETE FROM CADASTRO WHERE ID = ?", (1,))

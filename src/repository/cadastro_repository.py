from src.infrastructure.SQL.main import InfrastructureSQL
from src.domain.entities.cadastro import Cadastro
from typing import List, Optional

class CadastroRepository:
    def __init__(self):
        self.db = InfrastructureSQL()

    def inserir(self, cadastro: Cadastro) -> Cadastro:
        """Insere um novo cadastro no banco de dados e retorna o cadastro com o ID gerado."""
        query = """
        INSERT INTO CADASTRO (
            Nome_Completo, CPF, Telefone, Email, Estado, Bairro, Sexo, Idade, Assunto, 
            Data_participacao, Metodologia, Cliente, Classe_Social, Ocupacao, 
            Nome_recrutador, Digitador, Carimbo_Data_Hora
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        valores = (
            cadastro.nome_completo, cadastro.cpf, cadastro.telefone, cadastro.email,
            cadastro.estado, cadastro.bairro, cadastro.sexo, cadastro.idade, cadastro.assunto,
            cadastro.data_participacao, cadastro.metodologia, cadastro.cliente, cadastro.classe_social,
            cadastro.ocupacao, cadastro.nome_recrutador, cadastro.digitador, cadastro.carimbo_data_hora
        )

        try:
            cursor = self.db.cursor_db()
            cursor.execute(query, valores)
            cursor.commit()

            # Recupera o ID gerado pelo banco de dados
            cursor.execute("SELECT SCOPE_IDENTITY()")  # Para SQL Server
            cadastro.id = cursor.fetchone()[0]  # Atualiza o ID no objeto Cadastro

            return cadastro
        except Exception as e:
            print(f"Erro ao inserir cadastro: {e}")
            raise
        finally:
            self.db.close_connection()

    def buscar_por_cpf(self, cpf: str) -> Optional[Cadastro]:
        """Busca um cadastro pelo CPF."""
        query = """
        SELECT 
            ID, Carimbo_Data_Hora, Nome_Completo, CPF, Telefone, Email, Estado, Bairro, Sexo, Idade, 
            Assunto, Data_participacao, Metodologia, Cliente, Classe_Social, Ocupacao, 
            Nome_recrutador, Digitador
        FROM CADASTRO WHERE CPF = ?
        """
        try:
            cursor = self.db.cursor_db()
            cursor.execute(query, (cpf,))
            row = cursor.fetchone()

            if row:
                return Cadastro(
                    id=row[0],
                    carimbo_data_hora=row[1],
                    nome_completo=row[2],
                    cpf=row[3],
                    telefone=row[4],
                    email=row[5],
                    estado=row[6],
                    bairro=row[7],
                    sexo=row[8],
                    idade=row[9],
                    assunto=row[10],
                    data_participacao=row[11],
                    metodologia=row[12],
                    cliente=row[13],
                    classe_social=row[14],
                    ocupacao=row[15],
                    nome_recrutador=row[16],
                    digitador=row[17]
                )
            return None
        except Exception as e:
            print(f"Erro ao buscar cadastro por CPF: {e}")
            raise
        finally:
            self.db.close_connection()

    def listar_todos(self) -> List[Cadastro]:
        """Lista todos os cadastros."""
        query = """
        SELECT 
            ID, Carimbo_Data_Hora, Nome_Completo, CPF, Telefone, Email, Estado, Bairro, Sexo, Idade, 
            Assunto, Data_participacao, Metodologia, Cliente, Classe_Social, Ocupacao, 
            Nome_recrutador, Digitador
        FROM CADASTRO
        """
        try:
            cursor = self.db.cursor_db()
            cursor.execute(query)
            rows = cursor.fetchall()

            return [
                Cadastro(
                    id=row[0],
                    carimbo_data_hora=row[1],
                    nome_completo=row[2],
                    cpf=row[3],
                    telefone=row[4],
                    email=row[5],
                    estado=row[6],
                    bairro=row[7],
                    sexo=row[8],
                    idade=row[9],
                    assunto=row[10],
                    data_participacao=row[11],
                    metodologia=row[12],
                    cliente=row[13],
                    classe_social=row[14],
                    ocupacao=row[15],
                    nome_recrutador=row[16],
                    digitador=row[17]
                )
                for row in rows
            ]
        except Exception as e:
            print(f"Erro ao listar cadastros: {e}")
            raise
        finally:
            self.db.close_connection()

    def atualizar(self, cadastro: Cadastro) -> None:
        """Atualiza um cadastro existente."""
        query = """
        UPDATE CADASTRO SET
            Nome_Completo = ?, CPF = ?, Telefone = ?, Email = ?, Estado = ?, Bairro = ?, Sexo = ?, Idade = ?, Assunto = ?, 
            Data_participacao = ?, Metodologia = ?, Cliente = ?, Classe_Social = ?, Ocupacao = ?, 
            Nome_recrutador = ?, Digitador = ?, Carimbo_Data_Hora = ?
        WHERE CPF = ?
        """
        valores = (
            cadastro.nome_completo, cadastro.cpf, cadastro.telefone, cadastro.email,
            cadastro.estado, cadastro.bairro, cadastro.sexo, cadastro.idade, cadastro.assunto,
            cadastro.data_participacao, cadastro.metodologia, cadastro.cliente, cadastro.classe_social,
            cadastro.ocupacao, cadastro.nome_recrutador, cadastro.digitador, cadastro.carimbo_data_hora
        )

        try:
            cursor = self.db.cursor_db()
            cursor.execute(query, valores)
            cursor.commit()
        except Exception as e:
            print(f"Erro ao atualizar cadastro: {e}")
            raise
        finally:
            self.db.close_connection()

    def deletar(self, cpf: str) -> None:
        """Deleta um cadastro pelo CPF."""
        query = "DELETE FROM CADASTRO WHERE CPF = ?"
        try:
            cursor = self.db.cursor_db()
            cursor.execute(query, (cpf,))
            cursor.commit()
        except Exception as e:
            print(f"Erro ao deletar cadastro: {e}")
            raise
        finally:
            self.db.close_connection()
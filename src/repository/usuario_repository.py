from src.infrastructure.SQL.main import InfrastructureSQL
from src.domain.entities.usuario import Usuario
from typing import Optional

class UsuarioRepository:
    def __init__(self):
        self.conn = InfrastructureSQL()  # Inicializa a conexão com o banco

    def buscar_por_email(self, email: str) -> Optional[Usuario]:
        """Busca um usuário pelo email e retorna um objeto Usuario"""
        query = "SELECT id, nome, email, senha_hash FROM USERS WHERE email = ?"
        cursor = self.conn.cursor_db()  # Obtendo o cursor da conexão
        cursor.execute(query, (email,))
        row = cursor.fetchone()
        if row:
            # Criando um objeto Usuario a partir do resultado da consulta
            return Usuario(id=row[0], nome=row[1], email=row[2], senha=row[3])
        return None

    def salvar_usuario(self, usuario: Usuario, senha_hash: str) -> None:
        """Salva um novo usuário no banco de dados"""
        cursor = self.conn.cursor_db()  # Obtendo o cursor da conexão
        query = "INSERT INTO USERS (nome, email, senha_hash) VALUES (?, ?, ?)"
        cursor.execute(query, (usuario.nome, usuario.email, senha_hash))
        self.conn.conn.commit()  # Commit para garantir que a transação seja salva
        cursor.close()  # Fechando o cursor após a execução

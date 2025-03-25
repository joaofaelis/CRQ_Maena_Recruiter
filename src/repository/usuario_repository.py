from passlib.context import CryptContext
from src.infrastructure.SQL.main import InfrastructureSQL
from src.domain.entities.usuario import UsuarioBase, UsuarioLogin, UsuarioCreate
from typing import Optional
from fastapi import HTTPException


class UsuarioRepository:
    def __init__(self):
        self.conn = InfrastructureSQL()  # Inicializa a conexão com o banco
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    # Função para buscar o usuário no banco pelo email
    def buscar_usuario_por_email(self, email: str):
        query = "SELECT * FROM USUARIOS WHERE email = ?"
        valores = (email,)

        try:
            cursor = self.conn.cursor_db()  # Obtenha o cursor diretamente
            if cursor is None:
                raise HTTPException(status_code=500, detail="Falha na conexão com o banco de dados.")

            cursor.execute(query, valores)
            usuario = cursor.fetchone()  # Retorna uma tupla se o email existir

            if usuario is None:
                return None
            else:
                return usuario  # Retorna a tupla com o usuário encontrado
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao buscar usuário: {str(e)}")

    # Função para criar o usuário no banco
    def criar_usuario(self, nome: str, email: str, senha: str, tipo_usuario: str):
        # Verifica se o email já está cadastrado
        usuario_existente = self.buscar_usuario_por_email(email)  # Realiza a busca primeiro
        if usuario_existente is not None:  # Verifica se já existe
            return {"error": "O email já está cadastrado."}

        senha_hash = self.pwd_context.hash(senha)
        query = """ 
            INSERT INTO USUARIOS (nome, email, senha, tipo_usuario) 
            VALUES (?, ?, ?, ?)
        """
        valores = (nome, email, senha_hash, tipo_usuario)

        try:
            cursor = self.conn.cursor_db()  # Obtenha o cursor diretamente
            if cursor is None:
                raise HTTPException(status_code=500, detail="Falha na conexão com o banco de dados.")

            cursor.execute(query, valores)
            cursor.commit()  # Confirma a transação no banco

            # Verifica se a inserção foi bem-sucedida
            cursor.execute("SELECT * FROM USUARIOS WHERE email = ?", (email,))
            usuario_inserido = cursor.fetchone()
            if usuario_inserido:
                return {"msg": "Usuário criado com sucesso"}
            else:
                return {"error": "Erro ao criar o usuário. Usuário não foi inserido no banco."}
        except Exception as e:
            return {"error": str(e)}

    # Função para autenticar o usuário (login)
    def login_usuario(self, email: str, senha: str):
        usuario = self.buscar_usuario_por_email(email)

        if usuario is None:
            return {"error": "Usuário não encontrado."}

        if self.pwd_context.verify(senha, usuario["senha"]):
            return {"msg": "Login bem-sucedido", "usuario": usuario}
        else:
            return {"error": "Senha incorreta."}

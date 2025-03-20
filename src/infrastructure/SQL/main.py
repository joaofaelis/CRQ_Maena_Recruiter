import pyodbc
from decouple import config

class InfrastructureSQL:
    def __init__(self):
        self.server = config('SERVER')
        self.database = config('DATABASE')
        self.use_trusted_connection = config('USE_TRUSTED_CONNECTION', default="false").lower() == "true"
        self.username = config('USERNAME', default="")
        self.password = config('PASSWORD', default="")
        self.UID = config('UID', default="")

        self.conn = None

    def connect(self):
        try:
            if self.use_trusted_connection:
                # Autenticação Windows (Trusted Connection)
                conn_str = (
                    f'DRIVER={{ODBC Driver 18 for SQL Server}};'
                    f'SERVER={self.server};'
                    f'DATABASE={self.database};'
                    f'TRUSTED_CONNECTION=yes;'
                    f'Encrypt=no;'  # 🔴 Desativando criptografia para evitar erro de certificação
                )
            else:
                # Autenticação com usuário e senha
                conn_str = (
                    f'DRIVER={{ODBC Driver 18 for SQL Server}};'
                    f'SERVER=tcp:{self.server},1433;'
                    f'DATABASE={self.database};'
                    f'UID={self.UID};'
                    f'PWD={self.password};'
                    f'Encrypt=yes;'
                    f'TrustServerCertificate=no;'
                    f'Connection Timeout=30;'
                )

            self.conn = pyodbc.connect(conn_str)
            print("Conexão estabelecida com sucesso!")

        except Exception as e:
            print(f"Erro ao conectar ao SQL Server: {e}")
            self.conn = None

    def close_connection(self):
        try:
            if self.conn:
                self.conn.close()
        except Exception as e:
            print(f"Erro ao fechar conexão: {e}")

    def cursor_db(self):
        self.connect()
        if self.conn:
            return self.conn.cursor()
        else:
            return None


if __name__ == "__main__":
    db = InfrastructureSQL()
    cursor = db.cursor_db()


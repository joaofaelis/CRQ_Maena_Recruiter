from fastapi import FastAPI
from src.interface.api.routes.authenticator import router  # Certifique-se de importar o router
from src.interface.api.routes.cadastro import cadastro_router  # Certifique-se de importar o router

app = FastAPI()

# Incluindo os módulos de rotas
app.include_router(router, prefix="/auth", tags=["Autenticação"])
app.include_router(cadastro_router, prefix="/cadastro", tags=["Cadastro"])

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8000)

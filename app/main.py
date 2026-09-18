from fastapi import FastAPI

from app.routers import auth, chamados, usuarios


app = FastAPI(
    title="DevDesk API",
    description="API para gerenciamento de chamados de TI",
    version="1.0.0",
)


app.include_router(auth.router)
app.include_router(usuarios.router)
app.include_router(chamados.router)


@app.get("/")
def root():
    return {
        "mensagem": "DevDesk API funcionando!",
        "versao": "1.0.0",
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "servico": "DevDesk API",
    }
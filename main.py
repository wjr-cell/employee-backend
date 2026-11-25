from fastapi import FastAPI
from routers.employees import router

app = FastAPI(title="Employee Management API")

app.include_router(router)


@app.get("/health")
def health():
    return {"status": "ok"}

from fastapi import FastAPI

from .api.v1 import auth, document, query


app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(document.router, prefix="/document", tags=["document"])
app.include_router(query.router, prefix="/query", tags=["query"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the document management system!"}

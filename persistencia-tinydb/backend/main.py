from fastapi import FastAPI

from routers.contacts import router as contacts_router


app = FastAPI()


@app.get("/")
def health_check():
    return {"message": "API working"}


app.include_router(contacts_router)
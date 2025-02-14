from fastapi import FastAPI # Librería API
import uvicorn # Libreria de servidor local
from app.routers import user, payment, notification, group
from app.database.database import Base, engine

app = FastAPI()
app.include_router(user.router)
app.include_router(payment.router)
app.include_router(notification.router)
app.include_router(group.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
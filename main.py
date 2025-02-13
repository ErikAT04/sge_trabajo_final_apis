from fastapi import FastAPI # Librería API
import uvicorn # Libreria de servidor local
from app.routers import user, payment, notification, group
from app.database.database import Base, engine
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)

app = FastAPI(docs_url=None, redoc_url=None)
app.include_router(user.router)
app.include_router(payment.router)
app.include_router(notification.router)
app.include_router(group.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
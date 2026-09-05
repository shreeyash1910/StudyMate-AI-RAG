from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from sqlalchemy import text

from app.database import engine, Base

from app.models.user import User
from app.models.document import Document
from app.models.conversation import Conversation

from app.routes.upload import router as upload_router
from app.routes.search import router as search_router
from app.routes.chat import router as chat_router
from app.routes.users import router as users_router
from app.routes.conversation import router as conversation_router
from app.routes.messages import router as message_router

# Create database tables
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Chat With Your Study Material",
    description="Full-stack RAG-based study assistant",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
        "http://localhost:5175",
        "http://127.0.0.1:5175",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Register routes
app.include_router(upload_router)
app.include_router(search_router)
app.include_router(chat_router)
app.include_router(users_router)
app.include_router(conversation_router)
app.include_router(message_router)




@app.get("/")
def root():
    return {
        "message": "Chat With Your Study Material API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.get("/db-test")
def database_test():

    try:

        with engine.connect() as connection:

            result = connection.execute(
                text("SELECT 1")
            )

            value = result.scalar()

        return {
            "database": "connected",
            "result": value
        }

    except Exception as e:

        return {
            "database": "connection failed",
            "error": str(e)
        }
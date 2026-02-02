from fastapi import FastAPI
from api.quiz_api import router as quiz_router
from api.flashcard_api import router as flashcard_router
from api.upload_api import router as upload_router
from api.auth_api import router as auth_router
from api.document_api import router as document_router

app = FastAPI(
    title="AI Study Agent Backend",
    version="1.0.0"
)

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for simplicity in this demo. For prod, set specific domains.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(upload_router)
app.include_router(flashcard_router)
app.include_router(quiz_router)
app.include_router(document_router)


@app.get("/")
def root():
    return {"message": "🚀 Backend is running"}

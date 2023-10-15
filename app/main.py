import os
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from dotenv import load_dotenv
load_dotenv()

from api.routes.user_route import router as user_router
from api.routes.recipe_route import router as recipe_router
from api.routes.review_route import router as review_router
from api.routes.auth_route import router as auth_router
from api.routes.file_route import router as file_router


app = FastAPI()

# Allow all origins to make requests
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Total-Count"]
)

app.include_router(user_router, prefix="/user", tags=["User"])
app.include_router(recipe_router, prefix="/recipe", tags=["Recipe"])
app.include_router(review_router, prefix="/review", tags=["Review"])
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(file_router, prefix="/file", tags=["File"])


@app.exception_handler(HTTPException)
async def custom_exception_handler(request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content=exc.detail)

HOST = os.getenv("HOST")
PORT = int(os.getenv("PORT"))


if __name__ == "__main__":
   uvicorn.run("main:app", host=HOST, port=PORT, reload=True)


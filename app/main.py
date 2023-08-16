import uvicorn
from fastapi import FastAPI

from api.routes.user_route import router as user_router
from api.routes.recipe_route import router as recipe_router
from api.routes.auth_route import router as auth_router


app = FastAPI()


app.include_router(user_router, prefix="/user", tags=["User"])
app.include_router(recipe_router, prefix="/recipe", tags=["Recipe"])
app.include_router(auth_router, prefix="/auth", tags=["Auth"])


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8080, reload=True)
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from router import router as book_router
from models import admin_router


app = FastAPI()
app.include_router(book_router)
app.include_router(admin_router)

@app.get("/", tags=["Start page"])
async def root() -> HTMLResponse:
    return HTMLResponse(
        """
        <head>
        <title>
        my little library app
        </title>
        </head>
        <body>
        <h1 style="font-size: 50px; text-align: center">
        WELCOME TO MY LIBRARY!
        </h1>
        </body>
        """
    )
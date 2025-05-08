from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from router import router as book_router


app = FastAPI()
app.include_router(book_router)

@app.get("/", tags=["Start page"])
async def root():
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
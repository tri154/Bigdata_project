from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Frontend origin
    # allow_origins=["*"],  # Frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

image_path = os.path.join(os.path.dirname(os.getcwd()), 'consumer', 'last_img.jpg' )
@app.get("/get_image")
async def get_image():
    return FileResponse(image_path)

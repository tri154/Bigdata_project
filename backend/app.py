from fastapi import FastAPI
from fastapi.responses import PlainTextResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from read_video import read_frame
from fastapi import Response
from fastapi.middleware.cors import CORSMiddleware
import cv2
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/api/image", response_class=Response)
def get_image():
    frame = read_frame()  # or any other frame number
    if frame is None:
        return Response(content="Frame not found", status_code=404)
    
    ret, buffer = cv2.imencode('.jpg', frame)
    if not ret:
        return Response(content="Failed to encode frame", status_code=500)

    return Response(content=buffer.tobytes(), media_type="image/jpeg")
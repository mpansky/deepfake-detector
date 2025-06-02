from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import shutil
import uuid
import os

app = FastAPI()

# Create a temp directory if it doesn't exist
TEMP_DIR = "temp_uploads"
os.makedirs(TEMP_DIR, exist_ok=True)

def stub_image_detection(file_path: str) -> dict:
    # Placeholder logic – replace with actual model inference
    return {
        "type": "image",
        "file": os.path.basename(file_path),
        "result": "fake",  # or "real"
        "confidence": 0.92
    }

def stub_video_detection(file_path: str) -> dict:
    # Placeholder logic – replace with actual model inference
    return {
        "type": "video",
        "file": os.path.basename(file_path),
        "result": "real",  # or "fake"
        "confidence": 0.81
    }

@app.post("/detect/image/")
async def detect_image(file: UploadFile = File(...)):
    ext = os.path.splitext(file.filename)[-1].lower()
    if ext not in [".jpg", ".jpeg", ".png", ".bmp"]:
        return JSONResponse(status_code=400, content={"error": "Invalid image format"})

    temp_filename = f"{uuid.uuid4()}{ext}"
    temp_path = os.path.join(TEMP_DIR, temp_filename)

    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = stub_image_detection(temp_path)
    os.remove(temp_path)
    return result

@app.post("/detect/video/")
async def detect_video(file: UploadFile = File(...)):
    ext = os.path.splitext(file.filename)[-1].lower()
    if ext not in [".mp4", ".avi", ".mov", ".mkv"]:
        return JSONResponse(status_code=400, content={"error": "Invalid video format"})

    temp_filename = f"{uuid.uuid4()}{ext}"
    temp_path = os.path.join(TEMP_DIR, temp_filename)

    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = stub_video_detection(temp_path)
    os.remove(temp_path)
    return result

import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
from fastapi import File, UploadFile
from PIL import Image
import io
import tensorflow as tf
from pydantic import BaseModel
from database import get_waste_info


app = FastAPI(title="Binbot Backend API")

#-------------------------------------------------------------------------------------------------------------------------------------
#Hattam(member-3), server config and middleware
# Enable CORS for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Get the absolute path to the frontend directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

@app.get("/api/health")
async def health_check():
    return {"status": "ok", "message": "Binbot API is running"}


#-------------------------------------------------------------------------------------------------------------------------------------
#Himanshu(member-4), api routes and ml classification logic

#text classifiction api route
class ClassifyRequest(BaseModel):
    item: str

@app.post("/api/classify")
async def classify_item(req: ClassifyRequest):
    result = get_waste_info(req.item)
    if result:
        return {
            "success": True,
            "item": req.item,
            "category": result["category"],
            "bin": result.get("bin", "Unknown"),
            "tip": result.get("tip", "")
        }
    else:
        return {
            "success": False,
            "message": f"Item '{req.item}' not found in database.",
        }
        

#tensorflow and mobileNetV2 setup for image classification
model = tf.keras.applications.MobileNetV2(weights="imagenet")

def preprocess(image_bytes: bytes):
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    img = img.resize((224, 224))
    arr = tf.keras.applications.mobilenet_v2.preprocess_input(
        np.array(img, dtype=np.float32)
    )
    return np.expand_dims(arr, axis=0)

@app.post("/api/classify-image")
async def classify_image(file: UploadFile = File(...)):
    image_bytes = await file.read()
    tensor = preprocess(image_bytes)
    predictions = tf.keras.applications.mobilenet_v2.decode_predictions(
        model.predict(tensor), top=3
    )[0]

    top_label = predictions[0][1].replace("_", " ")
    confidence = float(predictions[0][2])

    result = get_waste_info(top_label)

    return {
        "success": bool(result),
        "item": top_label,
        "confidence": round(confidence, 2),
        "category": result.get("category") if result else None,
        "bin": result.get("bin") if result else "Unknown",
        "tip": result.get("tip", "") if result else ""
    }



#-------------------------------------------------------------------------------------------------------------------------------------
#Hattam(member-3), static files and frontend routes

app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")
no_cache_headers = {
    "Cache-Control": "no-cache, no-store, must-revalidate",
    "Pragma": "no-cache",
    "Expires": "0",
}

#Root route
@app.get("/")
async def serve_index():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"), headers=no_cache_headers)

#error handling for static assets
@app.get("/{file_name}.{extension}")
async def serve_assets(file_name: str, extension: str):
    file_path = os.path.join(FRONTEND_DIR, f"{file_name}.{extension}")
    if os.path.exists(file_path):
        return FileResponse(file_path, headers=no_cache_headers)
    return {"error": "File not found", "status_code": 404}

@app.get("/js/{file_name}.{extension}")
async def serve_js(file_name: str, extension: str):
    file_path = os.path.join(FRONTEND_DIR, "js", f"{file_name}.{extension}")
    if os.path.exists(file_path):
        return FileResponse(file_path, headers=no_cache_headers)
    return {"error": "File not found", "status_code": 404}

#frontend pages
@app.get("/{page_name}")
async def serve_page(page_name: str):
    target_file = page_name if page_name.endswith(".html") else f"{page_name}.html"
    file_path = os.path.join(FRONTEND_DIR, target_file)
    
    if os.path.exists(file_path):
        return FileResponse(file_path, headers=no_cache_headers)
    return {"error": "Page not found", "status_code": 404}







from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import shutil
import os
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from bgm_rem import remove_background
from bin_img import binary_image_conversion
from num_image import numerize_image

app = FastAPI()

# Mount static directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Ensure directories exist
UPLOAD_DIR = "uploads"
OUTPUT_DIR = "static/outputs"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Jinja2 templates
templates = Jinja2Templates(directory="static")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload/")
async def upload_image(request: Request, image: UploadFile = File(...), choice: str = Form(...)):
    file_path = os.path.join(UPLOAD_DIR, image.filename)
    
    # Save uploaded file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    # Step 1: Remove Background
    no_bg_path = os.path.join(OUTPUT_DIR, f"no_bg_{image.filename}")
    remove_background(file_path, no_bg_path)

    # Step 2: Convert to Binary
    bin_path = binary_image_conversion(no_bg_path)

    # Step 3: Overlay Numbers
    final_output = numerize_image(bin_path, "numbers", OUTPUT_DIR, choice)

    if final_output and os.path.exists(final_output):
        # Get relative path for HTML rendering
        processed_image_url = f"/static/outputs/{os.path.basename(final_output)}"

        return templates.TemplateResponse(
            "result.html", 
            {"request": request, "processed_image": processed_image_url}
        )
    else:
        return {"error": "Processing failed"}


from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import easyocr
import numpy as np
import cv2
import logging

app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development only
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize EasyOCR reader (simplified version)
try:
    reader = easyocr.Reader(['ar'], gpu=False)  # Force CPU mode
    logger.info("EasyOCR initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize EasyOCR: {str(e)}")
    raise RuntimeError("Failed to initialize OCR engine") from e

@app.get("/")
async def health_check():
    return {"status": "running", "message": "OCR API is ready"}

@app.post("/ocr")
async def process_image(file: UploadFile = File(...)):
    try:
        # Read image file directly
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if img is None:
            raise HTTPException(status_code=400, detail="Invalid image file")
        
        # Preprocess image
        img = cv2.resize(img, None, fx=1.5, fy=1.5)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Perform OCR
        results = reader.readtext(img, paragraph=True, beamWidth=10)
        extracted_text = " ".join([result[1] for result in results])
        
        return {
            "status": "success",
            "text": extracted_text,
            "char_count": len(extracted_text)
        }
        
    except Exception as e:
        logger.error(f"OCR processing failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"OCR processing failed: {str(e)}"
        )
    
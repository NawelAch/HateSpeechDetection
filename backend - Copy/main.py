from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import easyocr
import numpy as np
import cv2
import io
import fitz  # PyMuPDF for PDF handling
import logging
import os
from typing import List

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

async def extract_text_from_image(image):
    """Extract text from an image using EasyOCR"""
    # Preprocess image
    img = cv2.resize(image, None, fx=1.5, fy=1.5)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Perform OCR
    results = reader.readtext(img, paragraph=True, beamWidth=10)
    extracted_text = " ".join([result[1] for result in results])
    
    return extracted_text

async def extract_text_from_pdf(pdf_bytes):
    """Extract text from a PDF file"""
    text_parts = []
    
    try:
        # Open PDF from memory
        with fitz.open(stream=pdf_bytes, filetype="pdf") as doc:
            # Check if PDF has embedded text
            has_text = False
            for page in doc:
                if page.get_text().strip():
                    has_text = True
                    text_parts.append(page.get_text())
            
            # If no embedded text, perform OCR on each page
            if not has_text:
                logger.info("PDF has no embedded text, performing OCR")
                for page_num, page in enumerate(doc):
                    # Render page to image
                    pix = page.get_pixmap(matrix=fitz.Matrix(1.5, 1.5))
                    img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
                    
                    # Convert to BGR if needed
                    if pix.n == 4:  # RGBA
                        img = cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)
                    elif pix.n == 1:  # GRAY
                        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
                    
                    # Extract text from the page image
                    page_text = await extract_text_from_image(img)
                    text_parts.append(page_text)
    except Exception as e:
        logger.error(f"PDF processing error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"PDF processing failed: {str(e)}")
    
    return " ".join(text_parts)

@app.post("/ocr")
async def process_file(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        filename = file.filename.lower()
        
        # Determine file type and process accordingly
        if filename.endswith('.pdf'):
            logger.info("Processing PDF file")
            extracted_text = await extract_text_from_pdf(contents)
        else:
            # Process as image
            logger.info("Processing image file")
            nparr = np.frombuffer(contents, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            if img is None:
                raise HTTPException(status_code=400, detail="Invalid image file")
            
            extracted_text = await extract_text_from_image(img)
        
        return {
            "status": "success",
            "text": extracted_text,
            "char_count": len(extracted_text)
        }
        
    except Exception as e:
        logger.error(f"File processing failed: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Processing failed: {str(e)}"
        )

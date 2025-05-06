# import tensorflow as tf
# from transformers import AutoTokenizer
# import os
# from fastapi import FastAPI, HTTPException, Query, UploadFile, File
# from pydantic import BaseModel
# from typing import Optional
# import numpy as np
# from fastapi.middleware.cors import CORSMiddleware
# from gemini import predict_hate_category
# from dotenv import load_dotenv
# from fastapi.responses import JSONResponse
# from trends import get_google_trends
# import easyocr
# import cv2
# import logging
# from report import enhance_report, enlarge_report_output
# from pydantic import BaseModel
# from typing import Optional, Dict, Any
# # Configure logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)
# # Create the FastAPI app
# app = FastAPI(
#     title="Arabic Hate Speech Detection API",
#     description="API for detecting and classifying hate speech in Arabic text",
#     version="1.0.0",
#     docs_url="/docs",
#     redoc_url="/redoc"
# )

# # Enable CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# load_dotenv()

# # Model path and global variables
# MODEL_PATH = os.path.abspath("models/my_arabert_model")
# model = None
# tokenizer = None

# # Define the request and response models
# class TextRequest(BaseModel):
#     text: str

# class PredictionResponse(BaseModel):
#     is_hate_speech: bool
#     confidence: float
#     category: Optional[str] = None
#     category_confidence: Optional[float] = None
#     report: Optional[str] = None  # ✅ Set report as a string

# @app.on_event("startup")
# async def load_model():
#     global model, tokenizer
#     try:
#         print(f"Attempting to load model from: {MODEL_PATH}")
#         model = tf.saved_model.load(MODEL_PATH)
#         print("TensorFlow model loaded successfully.")

#         print("Attempting to load tokenizer from: aubmindlab/bert-base-arabertv02")
#         tokenizer = AutoTokenizer.from_pretrained("aubmindlab/bert-base-arabertv02")
#         print("Tokenizer loaded successfully.")

#         print("✅ Models and tokenizer loaded successfully!")
#     except Exception as e:
#         print(f"❌ Error loading models: {str(e)}")
#         raise e

# @app.get("/")
# async def root():
#     return {"message": "Welcome to Arabic Hate Speech Detection API"}

# @app.post("/predict", response_model=PredictionResponse)
# async def predict_hate_speech(request: TextRequest):
#     if not model or not tokenizer:
#         raise HTTPException(status_code=500, detail="Models not loaded")

#     try:
#         # Process text with tokenizer
#         encoded = tokenizer(
#             request.text,
#             padding='max_length',
#             truncation=True,
#             return_tensors="tf",
#             max_length=128
#         )

#         # Perform prediction
#         prediction = model(encoded)
#         prediction_values = prediction['logits'].numpy()

#         # Get predicted class and confidence
#         softmax = tf.nn.softmax(prediction_values, axis=-1).numpy()[0]
#         predicted_class = prediction_values.argmax(axis=-1)[0]
#         is_hate_speech = predicted_class == 1
#         hate_confidence = softmax[predicted_class] * 100

#         response = {
#             "is_hate_speech": is_hate_speech,
#             "confidence": float(hate_confidence)
#         }

#         # If it's hate speech, get category using Gemini
#         if is_hate_speech:
#             gemini_result = predict_hate_category(request.text)
#             response["category"] = gemini_result["category"]
#             response["category_confidence"] = gemini_result["confidence"]
#             # Generate report from your existing functions
#             enhanced_report = enhance_report(request.text, gemini_result["category"])
#             larger_report = enlarge_report_output(enhanced_report)

#             # Add the report to the response
#             response["report"] = larger_report
#         return response

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

# @app.get("/api/trends")
# def trends(terms: str = Query(..., description="Comma-separated search terms in Arabic")):
#     try:
#         search_terms = [term.strip() for term in terms.split(",") if term.strip()]
#         trends_data = get_google_trends(search_terms)
#         return JSONResponse(content=trends_data)
#     except Exception as e:
#         return JSONResponse(content={"error": str(e)}, status_code=500)
# try:
#     reader = easyocr.Reader(['ar'], gpu=False)  # Force CPU mode
#     logger.info("EasyOCR initialized successfully")
# except Exception as e:
#     logger.error(f"Failed to initialize EasyOCR: {str(e)}")
#     raise RuntimeError("Failed to initialize OCR engine") from e

# @app.get("/")
# async def health_check():
#     return {"status": "running", "message": "OCR API is ready"}

# @app.post("/ocr")
# async def process_image(file: UploadFile = File(...)):
#     try:
#         # Read image file directly
#         contents = await file.read()
#         nparr = np.frombuffer(contents, np.uint8)
#         img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
#         if img is None:
#             raise HTTPException(status_code=400, detail="Invalid image file")
        
#         # Preprocess image
#         img = cv2.resize(img, None, fx=1.5, fy=1.5)
#         img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
#         # Perform OCR
#         results = reader.readtext(img, paragraph=True, beamWidth=10)
#         extracted_text = " ".join([result[1] for result in results])
        
#         return {
#             "status": "success",
#             "text": extracted_text,
#             "char_count": len(extracted_text)
#         }
        
#     except Exception as e:
#         logger.error(f"OCR processing failed: {str(e)}")
#         raise HTTPException(
#             status_code=500,
#             detail=f"OCR processing failed: {str(e)}"
#         )
    
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)


import tensorflow as tf
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import os
from fastapi import FastAPI, HTTPException, Query, UploadFile, File, Form
from pydantic import BaseModel
from typing import Optional, Dict, Any
import numpy as np
from fastapi.middleware.cors import CORSMiddleware
from gemini import predict_hate_category
from dotenv import load_dotenv
from fastapi.responses import JSONResponse
from trends import get_google_trends
import easyocr
import cv2
import logging
from report import enhance_report, enlarge_report_output
from store_input import store_user_input, store_report

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Model wrapper classes
class ArabicHateSpeechModel:
    def __init__(self, model_path="models/my_arabert_model"):
        self.model = tf.saved_model.load(model_path)
        self.tokenizer = AutoTokenizer.from_pretrained("aubmindlab/bert-base-arabertv02")
        
    def predict(self, text):
        encoded = self.tokenizer(
            text,
            padding='max_length',
            truncation=True,
            return_tensors="tf",
            max_length=128
        )
        
        prediction = self.model(encoded)
        prediction_values = prediction['logits'].numpy()
        
        # Get predicted class and confidence
        softmax = tf.nn.softmax(prediction_values, axis=-1).numpy()[0]
        predicted_class = prediction_values.argmax(axis=-1)[0]
        is_hate_speech = predicted_class == 1
        hate_confidence = softmax[predicted_class] * 100

        store_user_input(text, bool(is_hate_speech))
        
        return {
            "is_hate_speech": is_hate_speech,
            "confidence": float(hate_confidence)
        }

class DarijaHateSpeechModel:
    def __init__(self, model_path="models/darija_model"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_path)
    
    def predict(self, text):
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, 
                                padding=True, max_length=256)
        with torch.no_grad():
            outputs = self.model(**inputs)
        
        logits = outputs.logits
        predicted_class = torch.argmax(logits, dim=1).item()
        is_hate_speech = predicted_class == 1
        
        # Calculate confidence using softmax
        probs = torch.nn.functional.softmax(logits, dim=1)
        confidence = float(probs[0][predicted_class]) * 100

        store_user_input(text, bool(is_hate_speech))
        
        return {
            "is_hate_speech": is_hate_speech,
            "confidence": confidence
        }

# Model factory for managing model instances
class ModelFactory:
    _instances = {}
    
    @staticmethod
    def get_model(language):
        """Get the appropriate model based on language"""
        if language not in ModelFactory._instances:
            if language == "arabic":
                ModelFactory._instances[language] = ArabicHateSpeechModel()
            elif language == "darija":
                ModelFactory._instances[language] = DarijaHateSpeechModel()
            else:
                raise ValueError(f"Unsupported language: {language}")
        
        return ModelFactory._instances[language]

# Create the FastAPI app
app = FastAPI(
    title="Arabic & Darija Hate Speech Detection API",
    description="API for detecting and classifying hate speech in Arabic and Darija text",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv()

# Define the request and response models
class TextRequest(BaseModel):
    text: str
    language: str = "arabic"  # Default to Arabic, can be "darija"

class PredictionResponse(BaseModel):
    is_hate_speech: bool
    confidence: float
    category: Optional[str] = None
    category_confidence: Optional[float] = None
    report: Optional[str] = None

@app.on_event("startup")
async def load_models():
    # Load models on startup
    try:
        # Pre-initialize both models
        arabic_model = ModelFactory.get_model("arabic")
        print("Arabic model loaded successfully")
        
        darija_model = ModelFactory.get_model("darija")
        print("Darija model loaded successfully")
        
        print("✅ All models loaded successfully!")
    except Exception as e:
        print(f"❌ Error loading models: {str(e)}")
        raise e

@app.get("/")
async def root():
    return {"message": "Welcome to Arabic & Darija Hate Speech Detection API"}

@app.post("/predict", response_model=PredictionResponse)
async def predict_hate_speech(request: TextRequest):
    try:
        # Get the appropriate model based on language
        model = ModelFactory.get_model(request.language)
        
        # Perform initial prediction
        prediction = model.predict(request.text)
        
        # Initialize base response
        response = {
            "is_hate_speech": prediction["is_hate_speech"],
            "confidence": prediction["confidence"],
            "category": None,
            "category_confidence": None,
            "report": None
        }
        
        # If it's hate speech, use Gemini to classify category and generate report
        if prediction["is_hate_speech"]:
            gemini_result = predict_hate_category(request.text)
            response["category"] = gemini_result["category"]
            response["category_confidence"] = gemini_result["confidence"]
            
            enhanced_report = enhance_report(request.text, gemini_result["category"])
            larger_report = enlarge_report_output(enhanced_report)
            response["report"] = larger_report
            
        return response
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")


@app.post("/report")
async def report_wrong_prediction(
    text: str = Form(...),
    predicted_label: str = Form(...)
):
    try:
        # Convert predicted_label from string to boolean
        is_hate_speech = predicted_label.lower() == 'true'
        store_report(text, is_hate_speech)  # <-- call your function here
        return JSONResponse(content={"message": "Report received. Thank you for helping us improve!"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving report: {str(e)}")


@app.get("/api/trends")
def trends(terms: str = Query(..., description="Comma-separated search terms in Arabic")):
    try:
        search_terms = [term.strip() for term in terms.split(",") if term.strip()]
        trends_data = get_google_trends(search_terms)
        return JSONResponse(content=trends_data)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

# Initialize OCR reader
try:
    reader = easyocr.Reader(['ar'], gpu=False)  # Force CPU mode
    logger.info("EasyOCR initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize EasyOCR: {str(e)}")
    raise RuntimeError("Failed to initialize OCR engine") from e

@app.get("/health")
async def health_check():
    return {"status": "running", "message": "API is ready"}

@app.post("/ocr")
async def process_image(file: UploadFile = File(...), language: str = "arabic"):
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
        
        # Analyze the extracted text for hate speech if requested
        if len(extracted_text) > 0:
            model = ModelFactory.get_model(language)
            prediction = model.predict(extracted_text)
            
            return {
                "status": "success",
                "text": extracted_text,
                "char_count": len(extracted_text),
                "analysis": {
                    "is_hate_speech": prediction["is_hate_speech"],
                    "confidence": prediction["confidence"]
                }
            }
        else:
            return {
                "status": "success",
                "text": extracted_text,
                "char_count": len(extracted_text),
                "message": "No text detected in image"
            }
        
    except Exception as e:
        logger.error(f"OCR processing failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"OCR processing failed: {str(e)}"
        )
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
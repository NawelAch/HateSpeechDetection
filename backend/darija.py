# models/darija_model.py
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

class DarijaHateSpeechModel:
    def __init__(self, model_path="models/darija/best_model"):
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
        
        return {
            "is_hate_speech": is_hate_speech,
            "confidence": confidence
        }
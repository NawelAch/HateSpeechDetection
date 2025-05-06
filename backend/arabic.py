# models/arabic_model.py
import tensorflow as tf
from transformers import AutoTokenizer

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
        
        return {
            "is_hate_speech": is_hate_speech,
            "confidence": float(hate_confidence)
        }
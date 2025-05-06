import tensorflow as tf
from transformers import AutoTokenizer
import os

MODEL_PATH = os.path.abspath("models/my_arabert_model")

try:
    # Load the model
    model = tf.saved_model.load(MODEL_PATH)
    print("✅ Model loaded successfully!")
    
    # Load tokenizer
    tokenizer = AutoTokenizer.from_pretrained("aubmindlab/bert-base-arabertv02")
    print("✅ Tokenizer loaded successfully!")
    
    # Test prediction
    test_text = "انت قذر و كلب"
    encoded = tokenizer(
        test_text,
        padding='max_length',
        truncation=True,
        return_tensors="tf",
        max_length=128
    )
    
    # Perform prediction
    prediction = model(encoded)
    
    # Convert prediction tensor to numpy array
    prediction_values = prediction['logits'].numpy()
    print(f"Test prediction logits: {prediction_values}")
    
    # Determine the predicted class (argmax gives the index of the highest logit)
    predicted_class = prediction_values.argmax(axis=-1)[0]  # Accessing the first value from the array
    print(f"Predicted class: {predicted_class}")
    
    # Map prediction to label (1 for hate speech, 0 for not hate speech)
    if predicted_class == 1:
        print("🚫 This is hate speech!")
    else:
        print("✓ This is not hate speech!")
        
    # Print the confidence scores as percentages
    softmax = tf.nn.softmax(prediction_values, axis=-1).numpy()[0]
    print(f"Confidence scores: Not hate speech: {softmax[0]*100:.2f}%, Hate speech: {softmax[1]*100:.2f}%")
    
except Exception as e:
    print(f"❌ Error: {str(e)}")
import re
import google.generativeai as genai
from typing import Dict

# Configure the model with explicit safety settings
genai.configure(api_key="AIzaSyBYj1F3wJt-2TYYFC8WQ61ETdScLz54Oa4")
model = genai.GenerativeModel(
    'gemini-1.5-flash',  # Changed to Gemini Flash 1.5
    generation_config={
        'temperature': 0.3,
        'max_output_tokens': 100
    },
    safety_settings={
        'HARM_CATEGORY_HATE_SPEECH': 'BLOCK_NONE',
        'HARM_CATEGORY_DANGEROUS_CONTENT': 'BLOCK_NONE'
    }
)

# def predict_hate_category(text: str) -> Dict[str, str]:
#     """
#     Predicts hate speech category for Arabic text with improved parsing
#     Returns: {'category': '...', 'confidence': float}
#     """
#     # Structured prompt with forced response format
#     prompt = f"""\
# النص التالي صنفه في واحدة فقط من هذه الفئات:
# [عنصرية، عنف، كراهية النساء، إساءة، رهاب المثلية، سياسية]

# المطلوب:
# 1. اسم الفئة بالضبط كما في القائمة
# 2. نسبة الثقة بين 0-100

# مثال للإجابة:
# الفئة: عنصرية
# الثقة: 95%

# النص: "{text}"
# """
    
#     try:
#         response = model.generate_content(prompt)
#         output = response.text.strip()
#         print(f"🔍 Raw Response: {output}")

#         # Normalize Arabic/English digits and symbols
#         arabic_to_latin = str.maketrans('٠١٢٣٤٥٦٧٨٩٪', '0123456789%')
#         normalized = output.translate(arabic_to_latin)
        
#         # Strict regex pattern for category and confidence
#         category_match = re.search(
#             r'الفئة:\s*([^\n]+)', 
#             normalized, 
#             re.IGNORECASE
#         )
        
#         confidence_match = re.search(
#             r'الثقة:\s*(\d+\.?\d*)%?', 
#             normalized, 
#             re.IGNORECASE
#         )

#         # Valid categories mapping
#         CATEGORY_MAP = {
#             "عنصرية": "racism",
#             "عنف": "violence",
#             "كراهية النساء": "misogyny",
#             "إساءة": "offensive",
#             "رهاب المثلية": "homophobia",
#             "سياسية": "political"
#         }

#         if category_match and confidence_match:
#             ar_category = category_match.group(1).strip()
#             confidence = min(100, max(0, float(confidence_match.group(1))))
            
#             return {
#                 "category": CATEGORY_MAP.get(ar_category, "unknown"),
#                 "confidence": confidence
#             }

#         # Fallback: Check for any category mention
#         for ar_cat in CATEGORY_MAP:
#             if ar_cat in normalized:
#                 return {
#                     "category": CATEGORY_MAP[ar_cat],
#                     "confidence": 75.0  # Default confidence
#                 }

#         return {"category": "unknown", "confidence": None}

#     except Exception as e:
#         print(f"⚠️ Error: {str(e)}")
#         return {"category": "error", "confidence": None}
def predict_hate_category(text: str) -> Dict[str, str]:
    """
    Predicts hate speech category for Arabic text with improved parsing
    Returns: {'category': '...', 'confidence': float}
    """
    prompt = f"""\ 
النص التالي صنفه في واحدة فقط من هذه الفئات:
[عنصرية، عنف، كراهية النساء، إساءة، رهاب المثلية، سياسية]

المطلوب:
1. اسم الفئة بالضبط كما في القائمة
2. نسبة الثقة بين 0-100

مثال للإجابة:
الفئة: عنصرية
الثقة: 95%

النص: "{text}"
"""
    
    try:
        response = model.generate_content(prompt)
        output = response.text.strip()
        print(f"🔍 Raw Gemini Output:\n{output}")

        # Normalize Arabic digits and symbols
        arabic_to_latin = str.maketrans('٠١٢٣٤٥٦٧٨٩٪', '0123456789%')
        normalized = output.translate(arabic_to_latin)

        CATEGORY_MAP = {
            "عنصرية": "racism",
            "عنف": "violence",
            "كراهية النساء": "misogyny",
            "إساءة": "offensive",
            "رهاب المثلية": "homophobia",
            "سياسية": "political"
        }

        # Try strict matching
        category_match = re.search(r'الفئة:\s*([^\n]+)', normalized)
        confidence_match = re.search(r'الثقة:\s*(\d+\.?\d*)%?', normalized)

        if category_match and confidence_match:
            ar_category = category_match.group(1).strip()
            confidence = min(100, max(0, float(confidence_match.group(1))))
            return {
                "category": CATEGORY_MAP.get(ar_category, "unknown"),
                "confidence": confidence
            }

        # Fallback if strict match failed
        for ar_cat, en_cat in CATEGORY_MAP.items():
            if ar_cat in normalized:
                print(f"⚡ Detected Category by fallback: {ar_cat}")
                return {
                    "category": en_cat,
                    "confidence": 75.0  # Assume 75% if not specified
                }

        print("⚠️ No category detected.")
        return {"category": "unknown", "confidence": None}

    except Exception as e:
        print(f"⚠️ Error: {str(e)}")
        return {"category": "error", "confidence": None}
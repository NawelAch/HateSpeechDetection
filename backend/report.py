# from typing import List, Dict, Optional
# import re
# import unicodedata
# import requests
# from googletrans import Translator
# from deep_translator import GoogleTranslator

# # Create a translator instance for translation functions
# try:
#     translator = Translator()
# except Exception as e:
#     translator = None
#     print(f"Error initializing translator: {e}")



# def translate_to_english(text: str) -> str:
#     """
#     Translate Arabic text to English using deep_translator library.
#     Falls back to placeholder if translation fails.

#     Args:
#         text: Arabic text to translate

#     Returns:
#         English translation or placeholder message
#     """
#     try:
#         translator = GoogleTranslator(source='ar', target='en')
#         translation = translator.translate(text)
#         return translation
#     except Exception as e:
#         print(f"Translation error using deep_translator: {e}")
#         return f"[Translation unavailable for: {text}]"

# def get_transliteration(text: str) -> str:
#     """
#     Simple transliteration for Arabic text using character mapping.
#     This is a basic implementation - for production, use a specialized library.

#     Args:
#         text: Arabic text to transliterate

#     Returns:
#         Transliterated text
#     """
#     # Basic mapping of Arabic characters to Latin equivalents
#     ar_to_en = {
#         'ا': 'a', 'أ': 'a', 'إ': 'i', 'آ': 'aa',
#         'ب': 'b', 'ت': 't', 'ث': 'th',
#         'ج': 'j', 'ح': 'h', 'خ': 'kh',
#         'د': 'd', 'ذ': 'dh', 'ر': 'r',
#         'ز': 'z', 'س': 's', 'ش': 'sh',
#         'ص': 's', 'ض': 'd', 'ط': 't',
#         'ظ': 'dh', 'ع': '\'', 'غ': 'gh',
#         'ف': 'f', 'ق': 'q', 'ك': 'k',
#         'ل': 'l', 'م': 'm', 'ن': 'n',
#         'ه': 'h', 'و': 'w', 'ي': 'y',
#         'ى': 'a', 'ة': 'h', 'ء': '\'',
#         ' ': ' ', '،': ',', '.': '.'
#     }

#     # Fall back to this if character-by-character replacement fails
#     try:
#         result = ''
#         for char in text:
#             result += ar_to_en.get(char, char)
#         return result
#     except Exception as e:
#         print(f"Transliteration error: {str(e)}")
#         return f"[Transliteration unavailable]"

# def identify_key_phrases(text: str, category: str) -> List[Dict]:
#     """
#     Identify key phrases in the text that indicate hate speech.
#     Uses pattern matching to extract relevant phrases based on category.

#     Args:
#         text: The original Arabic text
#         category: The detected hate speech category

#     Returns:
#         List of dictionaries containing phrase and explanation
#     """
#     # Define patterns and explanations for different categories
#     category_patterns = {

#         "misogyny": {
#             r'مكانك\s+المطبخ': "Telling a woman her place is the kitchen",
#             r'انتي\s+بس\s+اتجوزي\s+وسكتي': "Telling a woman to just get married and be quiet",
#             r'ليش\s+بتشتغلي\s+\?': "Questioning why a woman works",
#             r'البنات\s+ما\s+بينفعوا\s+للشغل': "Claiming women are unfit for work",
#             r'المرأة\s+ناقصه\s+دين\s+وعقل': "Religious/cultural claim of women's inferiority",
#             r'ما\s+في\s+بنت\s+تفهم\s+بالسياسة': "Saying women shouldn't be involved in politics",
#             r'مش\s+لازم\s+تدرسي\s+أكتر\s+من\s+هيك': "Telling a woman she doesn't need to study more",
#             r'تأدبك\s+ببيتك': "Suggesting that a woman's dignity is only preserved at home",
#             r'المرأة\s+تتبهدل\s+لما\s+تشتغل': "Saying working women lose respect",
#             r'ما\s+حدا\s+بياخد\s+البنت\s+اللي\s+بتطلع\s+كتير': "Shaming socially active women",
#             r'البنت\s+لازم\s+تغطي\s+وتسكت': "Imposing silence and control over women's appearance",
#             r'اللي\s+بتحكي\s+كثير\s+ما\s+بتتجوز': "Discouraging women from speaking out",
#             r'ما\s+تفرجي\s+رأيك،\s+انتي\s+بنت': "Telling women they can't have opinions",
#             r'الحرمة\s+بس\s+للولادة': "Reducing a woman's role to reproduction",
#             r'ليش\s+ما\s+طبختي': "Criticizing women for not doing domestic chores",
#             r'ما\s+تفكري،\s+انتي\s+بنت': "Discouraging women from thinking independently"
#         },
#         "racism": {
#             r'عرب': "Potentially derogatory reference to Arabs",
#             r'أجنبي': "Potentially derogatory reference to foreigners",
#             r'أسود': "Potentially racist reference to skin color",
#             r'زنجي': "Derogatory racial term",
#             r'يهود': "Potentially antisemitic reference",
#             r'غجر': "Derogatory reference to Roma people"
#         },
#         "violence": {
#             r'اقتل': "Explicit call for killing",
#             r'ضرب': "Reference to physical violence",
#             r'دم': "Reference to blood or bloodshed",
#             r'موت': "Reference to death or dying",
#             r'سلاح': "Reference to weapons",
#             r'تهديد': "Threat or intimidation"
#         },
#         "homophobia": {
#             r'شاذ': "Derogatory term for LGBTQ+ individuals",
#             r'مثلي': "Potentially derogatory reference to homosexuality",
#             r'لوطي': "Derogatory term for gay men",
#             r'مخنث': "Derogatory term for effeminate men",
#             r'متحول': "Potentially derogatory reference to transgender individuals"
#         },
#         "offensive": {
#             r'كلب': "Dehumanizing animal comparison",
#             r'حمار': "Dehumanizing animal comparison",
#             r'غبي': "Insulting intelligence",
#             r'حقير': "Degrading personal attack",
#             r'قذر': "Dehumanizing reference to uncleanliness"
#         },
#         "political": {
#             r'خائن': "Accusation of treason",
#             r'عميل': "Accusation of being an agent for foreign powers",
#             r'تخريب': "Accusation of sabotage",
#             r'إرهاب': "Association with terrorism",
#             r'فاسد': "Accusation of corruption"
#         }
#     }

#     # Get patterns for the specified category, with fallback to default patterns
#     patterns = category_patterns.get(category, {})
#     if not patterns:
#         # Default patterns for when category is not recognized
#         patterns = {
#             r'[!؟]': "Use of strong punctuation indicating confrontational tone",
#             r'انت': "Direct confrontation using second person",
#             r'أنت': "Direct confrontation using second person"
#         }

#     # Find matches in the text
#     matches = []
#     for pattern, explanation in patterns.items():
#         if re.search(pattern, text, re.IGNORECASE):
#             # Extract the actual matched text
#             match = re.search(pattern, text, re.IGNORECASE)
#             if match:
#                 matched_text = match.group(0)
#                 matches.append({
#                     "phrase": matched_text,
#                     "explanation": explanation
#                 })

#     # If no specific patterns matched, return the whole text as a phrase
#     if not matches:
#         return [{
#             "phrase": text,
#             "explanation": "This statement as a whole constitutes hate speech"
#         }]

#     return matches

# def extract_targeted_group(text: str, category: str) -> str:
#     """
#     Attempt to extract the targeted group from the text.
#     Uses pattern matching based on category to identify targeted groups.

#     Args:
#         text: The original Arabic text
#         category: The detected hate speech category

#     Returns:
#         String describing the targeted group
#     """
#     # Define patterns to identify targeted groups based on category
#     targeted_group_patterns = {
#         "racism": {
#             r'عرب': "Arabs",
#             r'أفارقة': "Africans",
#             r'سود': "Black individuals",
#             r'أجانب': "Foreigners",
#             r'مهاجرين': "Immigrants",
#             r'يهود': "Jewish people",
#             r'فلسطيني': "Palestinians",
#             r'أمازيغ': "Amazigh people"
#         },
#         "misogyny": {
#             r'نساء': "women",
#             r'بنات': "women and girls",
#             r'زوجات': "wives",
#             r'أمهات': "mothers",
#             r'غادة': "the woman mentioned (Ghada)",
#             r'هي': "the woman referenced"
#         },
#         "homophobia": {
#             r'مثلي': "LGBTQ+ individuals",
#             r'مثليين': "LGBTQ+ individuals",
#             r'شواذ': "LGBTQ+ individuals (derogatory)",
#             r'متحولين': "transgender individuals"
#         },
#         "political": {
#             r'حزب': "members of a political party",
#             r'معارضة': "political opposition",
#             r'حكومة': "government officials",
#             r'رئيس': "leadership figures",
#             r'سياسيين': "politicians"
#         }
#     }

#     # Get patterns for the specified category
#     patterns = targeted_group_patterns.get(category, {})

#     # Check for matches
#     for pattern, group in patterns.items():
#         if re.search(pattern, text, re.IGNORECASE):
#             return group

#     # Default responses based on category if no specific match
#     category_defaults = {
#         "racism": "specific ethnic or racial groups",
#         "misogyny": "women",
#         "homophobia": "LGBTQ+ individuals",
#         "violence": "targeted individuals or groups",
#         "offensive": "the addressed individuals",
#         "political": "political opponents"
#     }

#     return category_defaults.get(category, "the specified group")

# def generate_detailed_explanation(text: str, category: str, analysis: Dict) -> str:
#     """
#     Generate a detailed explanation for why the text falls into a particular hate speech category.

#     Args:
#         text: The original Arabic text
#         category: The detected hate speech category
#         analysis: The detailed analysis dictionary containing:
#             - 'phrase_matches': List of identified key phrases
#             - 'targeted_group': Extracted group name

#     Returns:
#         A detailed explanation of why the text constitutes hate speech
#     """
#     phrase_matches = analysis.get("phrase_matches", [])
#     targeted_group = analysis.get("targeted_group", "a group")
#     translation = translate_to_english(text)

#     explanation_parts = [f"The text, which translates to '\"{translation}\"', is categorized as {category} hate speech."]

#     if targeted_group:
#         explanation_parts.append(f"It specifically targets {targeted_group}.")

#     if phrase_matches:
#         phrase_explanations = []
#         for item in phrase_matches:
#             phrase = item.get("phrase", "")
#             reason = item.get("explanation", "")
#             phrase_explanations.append(f"The phrase '\"{phrase}\"' is indicative of hate speech because: {reason}.")
#         explanation_parts.extend(phrase_explanations)
#     else:
#         explanation_parts.append("While no specific key phrases were matched, the overall sentiment and context of the statement are considered to constitute hate speech.")

#     return " ".join(explanation_parts)

# def enhance_report(text: str, category: str) -> Dict:
#     """
#     Enhances the hate speech report by providing detailed analysis and explanations.

#     Args:
#         text: The original Arabic text.
#         category: The detected hate speech category.

#     Returns:
#         A dictionary containing the enhanced report details.
#     """
#     translation = translate_to_english(text)
#     transliteration = get_transliteration(text)
#     phrase_matches = identify_key_phrases(text, category)
#     targeted_group = extract_targeted_group(text, category)
#     explanation = generate_detailed_explanation(text, category, {"phrase_matches": phrase_matches, "targeted_group": targeted_group})

#     report = {
#         "original_text": text,
#         "translation": translation,
#         "transliteration": transliteration,
#         "category": category,
#         "targeted_group": targeted_group,
#         "key_phrases": phrase_matches,
#         "detailed_explanation": explanation
#     }
#     return report

# # Example usage:
# text = "المرأة ناقصه دين وعقل"
# category = "misogyny"
# enhanced_report = enhance_report(text, category)
# print(enhanced_report)

# text_racism = "هؤلاء العرب متخلفون جداً"
# category_racism = "racism"
# enhanced_report_racism = enhance_report(text_racism, category_racism)
# print(enhanced_report_racism)

# text_homophobia = "هذا الشاذ يجب أن يُعاقب"
# category_homophobia = "homophobia"
# enhanced_report_homophobia = enhance_report(text_homophobia, category_homophobia)
# print(enhanced_report_homophobia)



from typing import List, Dict, Optional
import re
import unicodedata
import requests
from googletrans import Translator
from deep_translator import GoogleTranslator


# Create a translator instance for translation functions
try:
    translator = GoogleTranslator(source='ar', target='en')
except Exception as e:
    translator = None
    print(f"Error initializing translator: {e}")

def translate_to_english(text: str) -> str:
    """
    Translate Arabic text to English using deep_translator library.
    Falls back to placeholder if translation fails.

    Args:
        text: Arabic text to translate

    Returns:
        English translation or placeholder message
    """
    try:
        if translator:
            translation = translator.translate(text)
            return translation
        else:
            return f"[Translation service not available]"
    except Exception as e:
        print(f"An error occurred during translation: {e}")
        return f"[Translation error: {text}]"

def get_transliteration(text: str) -> str:
    """
    Simple transliteration for Arabic text using character mapping.
    This is a basic implementation - for production, use a specialized library.

    Args:
        text: Arabic text to transliterate

    Returns:
        Transliterated text
    """
    # Basic mapping of Arabic characters to Latin equivalents
    ar_to_en = {
        'ا': 'a', 'أ': 'a', 'إ': 'i', 'آ': 'aa','ؤ': 'o',
    'ب': 'b', 'ت': 't', 'ث': 'th',
    'ج': 'j', 'ح': 'h', 'خ': 'kh',
    'د': 'd', 'ذ': 'dh', 'ر': 'r',
    'ز': 'z', 'س': 's', 'ش': 'sh',
    'ص': 's', 'ض': 'd', 'ط': 't',
    'ظ': 'dh', 'ع': '\'', 'غ': 'gh',
    'ف': 'f', 'ق': 'q', 'ك': 'k',
    'ل': 'l', 'م': 'm', 'ن': 'n',
    'ه': 'h', 'و': 'w', 'ي': 'y',
    'ى': 'aa',  # Often pronounced as a long 'a' sound at the end
    'ة': 'ah',  # Common transliteration for final 'ta marbuta'
    'ء': 'a',
    ' ': ' ', '،': ',', '.': '.',
    'ِ': 'i',   # Short 'i' (kasra)
    'ُ': 'u',   # Short 'u' (damma)
    'َ': 'a',   # Short 'a' (fatha)
    'ٍ': 'in',  # Tanwin kasra
    'ٌ': 'un',  # Tanwin damma
    'ً': 'an',  # Tanwin fatha
    'ّ': '',    # Shadda (doubling)
    'ْ': '',    # Sukun (no vowel)
    }

    # Fall back to this if character-by-character replacement fails
    try:
        result = ''
        for char in text:
            result += ar_to_en.get(char, char)
        return result
    except Exception as e:
        print(f"Transliteration error: {str(e)}")
        return f"[Transliteration unavailable]"

# Replace your current get_transliteration function with this

def identify_key_phrases(text: str, category: str) -> List[Dict]:
    """
    Identify key phrases in the text that indicate hate speech.
    Uses pattern matching to extract relevant phrases based on category.

    Args:
        text: The original Arabic text
        category: The detected hate speech category

    Returns:
        List of dictionaries containing phrase and explanation
    """
    # Define patterns and explanations for different categories
    category_patterns = {

        "misogyny": {
            r'مكانك\s+المطبخ': "Telling a woman her place is the kitchen",
            r'انتي\s+بس\s+اتجوزي\s+وسكتي': "Telling a woman to just get married and be quiet",
            r'ليش\s+بتشتغلي\s+\?': "Questioning why a woman works",
            r'البنات\s+ما\s+بينفعوا\s+للشغل': "Claiming women are unfit for work",
            r'المرأة\s+ناقصه\s+دين\s+وعقل': "Religious/cultural claim of women's inferiority",
            r'ما\s+في\s+بنت\s+تفهم\s+بالسياسة': "Saying women shouldn't be involved in politics",
            r'مش\s+لازم\s+تدرسي\s+أكتر\s+من\s+هيك': "Telling a woman she doesn't need to study more",
            r'تأدبك\s+ببيتك': "Suggesting that a woman's dignity is only preserved at home",
            r'المرأة\s+تتبهدل\s+لما\s+تشتغل': "Saying working women lose respect",
            r'ما\s+حدا\s+بياخد\s+البنت\s+اللي\s+بتطلع\s+كتير': "Shaming socially active women",
            r'البنت\s+لازم\s+تغطي\s+وتسكت': "Imposing silence and control over women's appearance",
            r'اللي\s+بتحكي\s+كثير\s+ما\s+بتتجوز': "Discouraging women from speaking out",
            r'ما\s+تفرجي\s+رأيك،\s+انتي\s+بنت': "Telling women they can't have opinions",
            r'الحرمة\s+بس\s+للولادة': "Reducing a woman's role to reproduction",
            r'ليش\s+ما\s+طبختي': "Criticizing women for not doing domestic chores",
            r'ما\s+تفكري،\s+انتي\s+بنت': "Discouraging women from thinking independently"
        },
        "racism": {
            r'عرب': "Potentially derogatory reference to Arabs",
            r'أجنبي': "Potentially derogatory reference to foreigners",
            r'أسود': "Potentially racist reference to skin color",
            r'زنجي': "Derogatory racial term",
            r'يهود': "Potentially antisemitic reference",
            r'غجر': "Derogatory reference to Roma people"
        },
        "violence": {
            r'اقتل': "Explicit call for killing",
            r'ضرب': "Reference to physical violence",
            r'دم': "Reference to blood or bloodshed",
            r'موت': "Reference to death or dying",
            r'سلاح': "Reference to weapons",
            r'تهديد': "Threat or intimidation"
        },
        "homophobia": {
            r'شاذ': "Derogatory term for LGBTQ+ individuals",
            r'مثلي': "Potentially derogatory reference to homosexuality",
            r'لوطي': "Derogatory term for gay men",
            r'مخنث': "Derogatory term for effeminate men",
            r'متحول': "Potentially derogatory reference to transgender individuals"
        },
        "offensive": {
            r'كلب': "Dehumanizing animal comparison",
            r'حمار': "Dehumanizing animal comparison",
            r'غبي': "Insulting intelligence",
            r'حقير': "Degrading personal attack",
            r'قذر': "Dehumanizing reference to uncleanliness"
        },
        "political": {
            r'خائن': "Accusation of treason",
            r'عميل': "Accusation of being an agent for foreign powers",
            r'تخريب': "Accusation of sabotage",
            r'إرهاب': "Association with terrorism",
            r'فاسد': "Accusation of corruption"
        }
    }

    # Get patterns for the specified category, with fallback to default patterns
    patterns = category_patterns.get(category, {})
    if not patterns:
        # Default patterns for when category is not recognized
        patterns = {
            r'[!؟]': "Use of strong punctuation indicating confrontational tone",
            r'انت': "Direct confrontation using second person",
            r'أنت': "Direct confrontation using second person"
        }

    # Find matches in the text
    matches = []
    for pattern, explanation in patterns.items():
        if re.search(pattern, text, re.IGNORECASE):
            # Extract the actual matched text
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                matched_text = match.group(0)
                matches.append({
                    "phrase": matched_text,
                    "explanation": explanation
                })

    # If no specific patterns matched, return the whole text as a phrase
    if not matches:
        return [{
            "phrase": text,
            "explanation": "This statement as a whole constitutes hate speech"
        }]

    return matches

def extract_targeted_group(text: str, category: str) -> str:
    """
    Attempt to extract the targeted group from the text.
    Uses pattern matching based on category to identify targeted groups.

    Args:
        text: The original Arabic text
        category: The detected hate speech category

    Returns:
        String describing the targeted group
    """
    # Define patterns to identify targeted groups based on category
    targeted_group_patterns = {
        "racism": {
            r'عرب': "Arabs",
            r'أفارقة': "Africans",
            r'سود': "Black individuals",
            r'أجانب': "Foreigners",
            r'مهاجرين': "Immigrants",
            r'يهود': "Jewish people",
            r'فلسطيني': "Palestinians",
            r'أمازيغ': "Amazigh people"
        },
        "misogyny": {
            r'نساء': "women",
            r'بنات': "women and girls",
            r'زوجات': "wives",
            r'أمهات': "mothers",
            r'غادة': "the woman mentioned (Ghada)",
            r'هي': "the woman referenced"
        },
        "homophobia": {
            r'مثلي': "LGBTQ+ individuals",
            r'مثليين': "LGBTQ+ individuals",
            r'شواذ': "LGBTQ+ individuals (derogatory)",
            r'متحولين': "transgender individuals"
        },
        "political": {
            r'حزب': "members of a political party",
            r'معارضة': "political opposition",
            r'حكومة': "government officials",
            r'رئيس': "leadership figures",
            r'سياسيين': "politicians"
        }
    }

    # Get patterns for the specified category
    patterns = targeted_group_patterns.get(category, {})

    # Check for matches
    for pattern, group in patterns.items():
        if re.search(pattern, text, re.IGNORECASE):
            return group

    # Default responses based on category if no specific match
    category_defaults = {
        "racism": "specific ethnic or racial groups",
        "misogyny": "women",
        "homophobia": "LGBTQ+ individuals",
        "violence": "targeted individuals or groups",
        "offensive": "the addressed individuals",
        "political": "political opponents"
    }

    return category_defaults.get(category, "the specified group")

def generate_detailed_explanation(text: str, category: str, analysis: Dict) -> str:
    """
    Generate a detailed explanation for why the text falls into a particular hate speech category.

    Args:
        text: The original Arabic text
        category: The detected hate speech category
        analysis: The detailed analysis dictionary containing:
            - 'phrase_matches': List of identified key phrases
            - 'targeted_group': Extracted group name

    Returns:
        A detailed explanation of why the text constitutes hate speech
    """
    phrase_matches = analysis.get("phrase_matches", [])
    targeted_group = analysis.get("targeted_group", "a group")
    translation = translate_to_english(text)

    explanation_parts = [f"The text, which translates to '\"{translation}\"', is categorized as {category} hate speech."]

    if targeted_group:
        explanation_parts.append(f"It specifically targets {targeted_group}.")

    if phrase_matches:
        phrase_explanations = []
        for item in phrase_matches:
            phrase = item.get("phrase", "")
            reason = item.get("explanation", "")
            phrase_explanations.append(f"The phrase '\"{phrase}\"' is indicative of hate speech because: {reason}.")
        explanation_parts.extend(phrase_explanations)
    else:
        explanation_parts.append("While no specific key phrases were matched, the overall sentiment and context of the statement are considered to constitute hate speech.")

    return " ".join(explanation_parts)

def enhance_report(text: str, category: str) -> Dict:
    """
    Enhances the hate speech report by providing detailed analysis and explanations.

    Args:
        text: The original Arabic text.
        category: The detected hate speech category.

    Returns:
        A dictionary containing the enhanced report details.
    """
    translation = translate_to_english(text)
    transliteration = get_transliteration(text)
    phrase_matches = identify_key_phrases(text, category)
    targeted_group = extract_targeted_group(text, category)
    explanation = generate_detailed_explanation(text, category, {"phrase_matches": phrase_matches, "targeted_group": targeted_group})

    report = {
        "original_text": text,
        "translation": translation,
        "transliteration": transliteration,
        "category": category,
        "targeted_group": targeted_group,
        "key_phrases": phrase_matches,
        "detailed_explanation": explanation
    }
    return report

def enlarge_report_output(report: Dict) -> str:
    """
    Creates a more detailed and larger hate speech report output.

    Args:
        report: A dictionary containing the hate speech report.

    Returns:
        A larger string representation of the report with more details.
    """
    original_text = report.get('original_text', 'N/A')
    translation = report.get('translation', 'N/A')
    transliteration = report.get('transliteration', 'N/A')
    category = report.get('category', 'N/A').capitalize()
    targeted_group = report.get('targeted_group', 'N/A')
    key_phrases = report.get('key_phrases', [])
    detailed_explanation = report.get('detailed_explanation', 'N/A')

    report_parts = [
        f"**Hate Speech Analysis Report**\n",
        f"**Original Text:** {original_text}\n",
        f"**Translation:** {translation}\n",
        f"**Transliteration:** {transliteration}\n",
        f"**Category of Hate Speech:** {category}\n",
        f"**Targeted Group:** {targeted_group}\n"
    ]

    if key_phrases:
        report_parts.append("\n**Key Indicative Phrases:**")
        for phrase_info in key_phrases:
            phrase = phrase_info.get('phrase', 'N/A')
            explanation = phrase_info.get('explanation', 'N/A')
            report_parts.append(f"\n  - **Phrase:** '{phrase}'")
            report_parts.append(f"    **Explanation:** {explanation}")
    else:
        report_parts.append("\n**Key Indicative Phrases:** None identified. The entire statement is considered hate speech.")

    report_parts.append(f"\n**Detailed Explanation:** {detailed_explanation}")

    return "\n".join(report_parts)
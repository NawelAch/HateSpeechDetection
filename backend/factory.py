# models/model_factory.py
from .arabic import ArabicHateSpeechModel
from .darija import DarijaHateSpeechModel

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
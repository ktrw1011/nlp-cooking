class LanguageDetect:
    def __init__(self, model_path):
        try:
            import fasttext
            self.model = fasttext.load_model(model_path)
        except:
            raise ImportError
    
    def __call__(self, text):
        label, prob = self.model.predict(text, 1)
        lang = list(zip([l.replace("__label__", "") for l in label], prob))[0][0]
        return lang
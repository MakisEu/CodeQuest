import google.generativeai as genai

class GeminiAI:


    def __init__(self,GOOGLE_API_KEY,modelName="gemini-1.5-flash"):

        genai.configure(api_key=GOOGLE_API_KEY)
        self.model = genai.GenerativeModel(modelName)
    
    def getResponse(self, promt):
        self.last_response = self.model.generate_content(promt)
        return self.last_response.text()

    

from awan_llm_api import AwanLLMClient, Role
from awan_llm_api.completions import Completions, ChatCompletions

class AwanLLM:
    
    def __init__(self,AWANLLM_API_KEY,model="Meta-Llama-3-8B-Instruct"):
        self.client = AwanLLMClient(AWANLLM_API_KEY)
        self.model = model
        self.chat = ChatCompletions(model)
        self.completion = None
        self.lastResponseText=None
        self.lastResponse=None

    def textCompletion(self,prompt):
        self.completion = Completions(self.model, prompt)
        self.lastResponse=self.client.completion(self.completion)
        try:
            self.lastResponseText=self.lastResponse["choices"][0]["text"]
        except KeyError:
            print ("KeyError in textCompletion!!! Received response:")
            print (self.lastResponse)
        return self.lastResponseText
    
    def chatCompletion(self,promt):
        self.chat.add_message(Role.USER, promt)
        self.lastResponse=self.client.chat_completion(self.chat)
        return self.lastResponse

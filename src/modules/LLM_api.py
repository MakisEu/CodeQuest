from LLMs.BardAI import GeminiAI
from LLMs.AwanLLm import AwanLLM
from utils import getAPIKey,printToLog

class LLM:

    def __init__(self,llmName,apiKey,model=None):
        models={"bard" : ["gemini-1.5-flash","gemini-1.5-pro","gemini-1.0-pro"], "awanllm" : ["Meta-Llama-3-8B-Instruct", "Awanllm-Llama-3-8B-Dolfin","Awanllm-Llama-3-8B-Cumulus","Meta-Llama-3-70B-Instruct", "WizardLM-2-8x22B"]}
        self.llmName = llmName
        self.lastResponse=None
        self.lastResponseText=""
        self.lastError=""
        if (llmName=="bard"):
            llmModel=None
            if model in models["bard"]:
                llmModel=model
            else:
                llmModel=models["bard"][0]
            self.model=llmModel
            try:
                self.LLM=GeminiAI(apiKey,llmModel)
            except Exception as ex:
                template = "An exception of type {0} occurred using BardAI. Arguments:\n{1!r}"
                message = template.format(type(ex).__name__, ex.args)
                printToLog(message)
                self.lastError=type(ex)

        elif (llmName=="awanllm"):
            llmModel=None
            if model in models["awanllm"]:
                llmModel=model
            else:
                llmModel=models["awanllm"][0]
            self.model=llmModel
            self.LLM=AwanLLM(apiKey,llmModel)
        
    def getResponse(self,prompt):
        if (self.llmName=="bard"):
            try:
                self.lastResponse=self.LLM.getResponse(prompt)
                self.lastResponseText=self.lastResponse.text
            except Exception as ex:
                template = "An exception of type {0} occurred using BardAI. Arguments:\n{1!r}"
                message = template.format(type(ex).__name__, ex.args)
                printToLog(message)
                self.lastError=type(ex)
                return message
        elif (self.llmName=="awanllm"):
            self.lastResponse=self.LLM.chatCompletion(prompt)
            try:
                self.lastResponseText=self.lastResponse["choices"][0]["message"]["content"]
            except KeyError:
                printToLog("(AwanLLM):Model"+self.model+". Error getting text from response:"+str(self.lastResponse))
                self.lastResponseText=""
        return self.lastResponseText



def test_llm(llmName,prompt,api_key=None,model=None):
    if (api_key==None):
        api_key=getAPIKey(llmName) 
    
    llm=LLM(llmName,api_key,model)

    try:
        cnt=30000
        while(True):
            print (cnt)
            p="a"*cnt
            llm.getResponse(p)
            cnt+=1000
    except:
        print (str(cnt)+" Character are over max size of post")
    print(llm.getResponse(prompt))

if (__name__=="__main__"):
    print ("Testing LLM APIs...")
    print ("BardAI/Gemini:\n")
    



    #test_llm("bard","Write me a story")
    
    print ("\nAwan LLM:\n")

    #with open("/home/makis/Documents/Github/CodeQuest/prompt.txt", 'r') as file:
    #    prompt=file.read()
    
    test_llm("awanllm",prompt="Write me a story")
    
    print ("\nFinished running tests")

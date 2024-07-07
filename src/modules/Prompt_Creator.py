
class PromtCreator:

    def __init__(self,content="",prefix="Based on the slides from a university course", suffix=". Design a programming assignment that incorporates the key concepts discussed in the course.", topic=None,constraints="Consider including practical application scenarios and code examples to demonstrate understanding"):
        self.maxCharactersOfPrompt=30000
        self.prefix=prefix
        self.suffix=suffix
        self.topic=" on "
        self.hasTopic=False

        if (topic is not None):
            self.topic+=topic
            self.hasTopic=True

        if (content!=""):
            content=", "+content
        
        self.content=content
        self.prompt=""
        self.constraints=constraints

    def generatePrompt(self,content=""):
        if (content!=""):
            self.content=", "+content
        
        prefix=self.prefix
        
        if (self.hasTopic):
            prefix+=self.topic
        self.prompt=prefix+"\n"+content+self.suffix+self.constraints
        
        return self.prompt
    
    def getLastPrompt(self):
        return self.prompt
if (__name__=="__main__"):
    PC=PromtCreator()
    content=""
    with open('PDF File **CHANGE ME**', 'r') as file:
        content=file.read()
        with open('prompt.txt', 'w') as file2:
            file2.write(PC.generatePrompt(content))

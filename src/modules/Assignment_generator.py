from TextExtraction.pdf_text_extreactor import PdfTextExtractor
from Prompt_Creator import PromtCreator
from LLM_api import LLM
from utils import getAPIKey
class AssignmentGenerator:

    def __init__(self,apiKey,charLimit=30000,slidesPerText=10, llmService="awanllm",model=None):
        self.charLimit=charLimit
        self.slidesPerText=slidesPerText
        self.llm=LLM(llmName=llmService,apiKey=apiKey,model=model)
        self.promptCreator=PromtCreator()
        self.lastChunks=[]
        self.lastPrompts=[]
        self.lastAssignments=[]
        self.promptsWithErrors=[]
    
    def splitPdfToTextChunks(self,file,charLimit=None,slidesPerText=None,pdfSlideHasFooter=False):
        if (charLimit is None):
            charLimit=self.charLimit
        if (slidesPerText is None):
            slidesPerText=self.slidesPerText
        slides=PdfTextExtractor(file).getTextFromAllPages(hasFooter=pdfSlideHasFooter)
        nSlides=len(slides)
        chunks=[]
        i=0
        while (i<nSlides):
            n=min(nSlides,i+slidesPerText)
            chunk=""
            while (i<n and len(chunk)<charLimit):
                chunk+=slides[i]
                i+=1
            chunks.append(chunk)
        self.lastChunks=chunks
        return self.lastChunks

    def createPromptFromText(self,content):
        return self.promptCreator.generatePrompt(content)

    def createPromptsFromChunks(self,chunks=None):
        if (chunks is None):
            chunks=self.lastChunks
        
        prompts=[]
        
        for chunk in chunks:
            prompts.append(self.createPromptFromText(chunk))
        
        self.lastPrompts=prompts

        return self.lastPrompts

    def generateAssignmentFromPrompt(self,prompt):
        return self.llm.getResponse(prompt)

    def generateAssignmentsFromPrompts(self,prompts=None):
        if (prompts is None):
            prompts=self.lastPrompts

        assignments=[]
        for prompt in prompts:
            assignments.append(self.generateAssignmentFromPrompt(prompt))
        self.lastAssignments=assignments
        
        return self.lastAssignments

    def generateAssignmentsFromPdf(self,file,pdfSlideHasFooter=False):
        self.splitPdfToTextChunks(file,pdfSlideHasFooter=pdfSlideHasFooter)
        print("Len chunks:",len(self.lastChunks))
        self.createPromptsFromChunks()
        print("Len prompts:",len(self.lastPrompts))
        self.generateAssignmentsFromPrompts()
        print("Len assignments:",len(self.lastAssignments))
        return self.lastAssignments

    def generateAssignmentsFromPdfGenerator(self,file,pdfSlideHasFooter=False):
        self.splitPdfToTextChunks(file,pdfSlideHasFooter=pdfSlideHasFooter)
        self.lastPrompts=[]
        self.lastAssignments=[]
        self.promptsWithErrors=[]
        for i in self.lastChunks:
            chunkPrompt=self.createPromptFromText(i)
            self.lastPrompts.append(chunkPrompt)
            chunkAssignment=None
            try:
                chunkAssignment=self.generateAssignmentFromPrompt(chunkPrompt)
                self.lastAssignments.append(chunkAssignment)
            except Exception as ex:
                template = "An exception of type {0} occurred. Arguments:\n{1!r}\n"
                message = template.format(type(ex).__name__, ex.args)
                chunkAssignment=message
                self.lastAssignments.append(chunkAssignment)
                self.promptsWithErrors.append(chunkPrompt)
            finally:
                yield (i,chunkPrompt,chunkAssignment)


            
if (__name__=="__main__"):
    apiKey=getAPIKey("awanllm")
    AG=AssignmentGenerator(apiKey,charLimit=15000,slidesPerText=9)
    file="PDF File **CHANGE ME**"
    with open('chunks_prompts_assignments.txt', 'w') as fileChucks:
        for chunk,prompt,assignment in AG.generateAssignmentsFromPdfGenerator(file):
            fileChucks.write(chunk)
            fileChucks.write("\n---------------------"*10+"\n")
            fileChucks.write(prompt)
            fileChucks.write("\n---------------------"*10+"\n")
            fileChucks.write(assignment)
            fileChucks.write("\n---------------------"*10+"\n")
            print ([chunk,prompt,assignment])
    print (AG.lastAssignments)

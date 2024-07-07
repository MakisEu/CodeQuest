from pathlib import Path

def getAPIKey(APIName):
    relativePath="../../"+APIName+"_secrets.txt"
    absolutePath=getAbsolutePath(relativePath)
    f=open(absolutePath,"r")
    apiKey=f.readline()
    f.close()
    return apiKey.strip()
    
def getAbsolutePath(relativePath):
    mod_path = Path(__file__).parent
    filename= (mod_path / relativePath).resolve()
    return filename

def printToLog(text):
    log_file = open("CodeQuest.log","a")
    log_file.write(text.strip()+"\n")
    log_file.close()

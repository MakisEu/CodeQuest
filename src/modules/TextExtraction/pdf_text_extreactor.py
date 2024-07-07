from pypdf import PdfReader

class PdfTextExtractor:

    def __init__(self,file):
        self.reader = PdfReader(file)
        self.numberOfPages = len(self.reader.pages)
    def getTextFromPage(self,pageNumber,hasFooter=False):
        if (pageNumber>self.numberOfPages or pageNumber<-self.numberOfPages):
            return None
        page = self.reader.pages[pageNumber]
        text = page.extract_text().strip()
        if (hasFooter):
            sentences=text.split("\n")
            text="\n".join(sentences[:-1])
        return text
    def getTextFromAllPages(self,hasFooter=False):
        texts=[]
        for i in range(self.numberOfPages):
            text=self.getTextFromPage(i,hasFooter=hasFooter)+"\n"
            texts.append(text)
        return texts

    def getTextFromAllPagesUniSlides_WIP(self,hasFooter=False):
        text=""
        lastSlide=""
        for i in range(self.numberOfPages):
            currentSlide = self.getTextFromPage(i,hasFooter=hasFooter)
            if lastSlide in currentSlide:
                lastSlide = currentSlide
            else:
                text += lastSlide + "\n"
                lastSlide = currentSlide
        text += lastSlide + "\n"
        return text.strip()


if (__name__=="__main__"):
    pdf=PdfTextExtractor("PDF File **CHANGE ME**")
    with open('allPages.txt', 'w') as file:
        texts=pdf.getTextFromAllPages(hasFooter=True)
        for i in texts:
            file.write("["+i+"]\n")
        print(len(texts))
        print(texts)
    print (pdf.numberOfPages)

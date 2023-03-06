import PyPDF2

# './Neih-Sahota---Key-Partnerships.pdf'

class PDFReader():
    def __init__(self,pdf_name):
        self.pdf_name = pdf_name
        self.reader = PyPDF2.PdfReader(self.pdf_name)
        self.pages = self.reader.pages
    
    def getLen(self):
        return len(self.pages)
    
    def getPage(self,index):
       return self.pages[index].extract_text()
    
    def getTranscript(self):
        return ''.join([self.getPage(i) for i in range(self.getLen())])

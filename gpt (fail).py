import os
import openai

from PDFReader import PDFReader

API_KEY = os.getenv("OPENAI_API_KEY")

# MAX_TOKENS = 4096

def query(messages):    
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=messages
    )

    return response.choices[0].message.content

class Summarizer:
    def __init__(self,pdf_name):
        self.pdf_name = pdf_name
        self.PDFReader = PDFReader(name)

        self.article_properties = ['be 500 words',
            'written in an inspirational lens',
            'targeted towards student entrepreneurs',
            'should begin by introducing the speaker',
            'should end by advising students to visit ANTrepreneur Center']

        self.behavior = f'''
You are a social media market manager.
Your job is to construct tailored articles for ANTrepreneur Center.
Each article should %s.
''' % (', '.join(self.article_properties))
        
        self.transcript_prompt = '''
Since you can’t take larger inputs of text, I will feed you the transcript in chunks. 
The transcript will start when I say “*BEGINNING*” and end when I say “*END*”.
        '''
    
    def parsePage(self,index):
        return {'role':'assistant','content':self.PDFReader.getPage(index)}
    
    def parsePages(self):
        return [self.parsePage(i) for i in range(self.PDFReader.getLen())]
    
    def summarize(self):
        messages = [
            {'role':'system','content':self.behavior},
            {'role':'assistant','content':self.transcript_prompt},
            {'role':'assistant','content':'*BEGINNING*'}            
        ]

        messages += self.parsePages()

        messages += [
            {'role':'assistant','content':'*END*'},
            {'role':'user','content':'Write an article about the transcript.'}
        ]

        return query(messages)
    
    def summarizeOneChunk(self,text):
        prompt = f'Write an article about the following text: "{text}"'

        messages = [
            {'role':'system','content':self.behavior},
            {'role':'user','content':prompt}
        ]

        return query(messages)

    def summarizePage(self,index):
        return self.summarizeOneChunk(self.PDFReader.getPage(index))

    def summarizeTranscript(self):
        return self.summarizeOneChunk(self.PDFReader.getTranscript())

if __name__=='__main__':
    name = './Neih-Sahota---Key-Partnerships.pdf'

    summarizer = Summarizer(name)
    # summary = summarizer.summarizePage(0)
    # summary = summarizer.summarizeTranscript()

    # summary = summarizer.parsePages()
    summary = summarizer.summarize()
    
    print(summary)
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
    
    def writeArticle(self,text):
        prompt = 'Write an article about the following text: %s' % text

        messages = [
            {'role':'system','content':self.behavior},
            {'role':'user','content':prompt}
        ]

        return query(messages)
    
    def getSummaries(self):
        return [summarizer.summarizePage(i) for i in range(4)]
        return [summarizer.summarizePage(i) for i in range(self.PDFReader.getLen())]
    
    def summarizePage(self,index):
        print('summarizing page %s'%str(index))

        text = self.PDFReader.getPage(index)

        # return str(index)

        prompt = 'Summarize the following text: %s' % text

        messages = [
            {'role':'user','content':prompt}
        ]

        return query(messages)

    def mergeTwo(self,summaries) -> str:

        # print('merging: %s'%summaries)

        # return str(sum([int(el) for el in summaries]))

        messages = [
            {'role':'assistant','content':'Part 1: %s'% summaries[0]},
            {'role':'assistant','content':'Part 2: %s'% summaries[1]},
            {'role':'user','content':'Combine parts 1 and 2 in 500 words'}
        ]

        return query(messages)
    
    def mergeAll(self,summaries):

        if len(summaries) == 1:
            return summaries[0]
        if len(summaries) == 2:
            return self.mergeTwo(summaries)
        else:
            print('MERGING: %s'%len(summaries))
            l = int(len(summaries)/2)
            return self.mergeTwo([
                self.mergeAll(summaries[0:l]),
                self.mergeAll(summaries[l:])
            ])

if __name__=='__main__':
    name = './Neih-Sahota---Key-Partnerships.pdf'

    summarizer = Summarizer(name)

    # summarize each page
    summaries = summarizer.getSummaries()

    # merge summaries
    summary = summarizer.mergeAll(summaries)

    # transform summary into article
    article = summarizer.writeArticle(summary)
    print(article)
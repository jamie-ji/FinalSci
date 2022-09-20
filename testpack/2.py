import sys
sys.path.append("preprocess\pdfminer")
from txtprocess import txtprocess

class summary():
    def __init__(self,origintxt):
        self.origintxt=origintxt

    def getsummary(self):

        TxTprocess=txtprocess(self.origintxt)
        
        refine=TxTprocess.first_process()
        summary=TxTprocess.title_extract()


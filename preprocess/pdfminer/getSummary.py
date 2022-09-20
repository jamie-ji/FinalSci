from txtprocess import txtprocess

class getSummary():
    def __init__(self,origintxt):
        self.origintxt=origintxt

    def getsummary(self):

        TxTprocess=txtprocess(self.origintxt)
        
        refine=TxTprocess.first_process()
        afterrefine=txtprocess(refine)
        
        summary,englishsummary=afterrefine.title_extract()
        
        return summary,englishsummary

    def getrawsummary(self):
        TxTprocess=txtprocess(self.origintxt)
        summary,englishsummary=TxTprocess.summary_rawtxt()
        return summary,englishsummary
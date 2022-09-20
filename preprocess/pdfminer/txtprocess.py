import re
import sys
sys.path.append("D:\discourse_code\code\summary")
from huggingface import facebook_bart

sys.path.append("preprocess")
import ydfanyi


class txtprocess():
    
    def __init__(self,origintxt):

        # self.rawpath=rawpath
        # #self.refinepath=refinepath
        # self.summarypath=summarypath
        self.origintxt=origintxt
        
        self.summarytxt=''
        self.englishsummarytext=''
        self.refinetxt=''

    
    #去掉多余符号，以及表格数据,和参考文献标注
    def first_process(self):
        
        # with open(self.rawpath,'r', encoding='UTF-8' ) as f:  
        #     lines=f.readlines()
        lines = self.origintxt.split('\n')

        for line in lines:
            #print(len(line))
                #等于1为空行情况
            if(len(line)==0):
                line=re.sub('\n','',line)
                #print(line)
                #2为页眉
            if(len(line)==1):
                #print(line)
                continue
                

            #开头数字或者带单位
            if re.findall('^[%.\d]+$|^[%.\d\s]+[a-zA-Z]{,2}$',line):
                #print(line)
                continue
            
            self.refinetxt=self.refinetxt+line+'\n'

        return self.refinetxt
        
    #提取标题，根据标题以及内容进行摘要
    #形成一个大字典，由标题作为key，内容作为value
    def title_extract(self):
        fanyi=ydfanyi.YouDaoFanyi('7a8e1e60f26f8514','rSZorXXlhX6tglvqvZsOXl2jQVn81MOI')
        # #按照标题来进行划分，每个标题根据长短来划分得到的摘要
        #         if re.findall('^[0-9]+[\.\s]*[A-Z][a-zA-Z\s\w\S]+\n$',line):
        #             print(line)

        article={}

        #标题标志 
        content=''
        biaoti=''

        # with open(self.rawpath,'r', encoding='UTF-8' ) as f:  
        #     lines=f.readlines()
        lines = self.origintxt.split('\n')
        
        for line in lines:
                
                #标题
                if re.findall('^[0-9]{1}[\.\s]+[A-Z][a-zA-Z\s\w\S]+$|^[0-9]{1}[\.\s]*[0-9]{1}[\.\s]+[A-Z][a-zA-Z\s\w\S]+$',line):
                    #把上一段内容送到摘要里
                    if biaoti=='':    #第一个标题
                        pass
                    else:              #有内容，将其送去摘要，得到返回值，再将其清空
                        # 标题保留，然后内容送去摘要完成后一起打包返回
                        # 1. 将其展示在网站上
                        # 2. 保存为txt，续在2.txt上
                        # 3. 生成pptx
                        

                        #print(biaoti)
                        #print(facebook_bart.summary(content))
                        
                        # with open(self.summarypath, "a",encoding='UTF-8') as file1:
                        #     #fanyi.translate(biaoti)
                        #     #print(biaoti)
                        #     file1.write('\n'+fanyi.translate(biaoti)+'\n')
                        #     file1.write(fanyi.translate(facebook_bart.summary(content))+'\n')
                        
                        print(biaoti+"biaoti")
                        self.summarytxt=self.summarytxt+fanyi.translate(biaoti)+'\n'+fanyi.translate(facebook_bart.summary(content))+'\n'
                        self.englishsummarytext=self.englishsummarytext+biaoti+'\n'+facebook_bart.summary(content)+'\n'

                        #print(content)

                        content=''    #清空
                    
                    biaoti=line
                
                #内容
                else: 
                    content=content+' '+line
                
        #最后一段内容
        if biaoti!='':
            #print(biaoti)
            #print(facebook_bart.summary(content))
            # with open(self.summarypath, "a",encoding='UTF-8') as file1:
            #     print(biaoti)
            #     file1.write('\n'+fanyi.translate(biaoti)+'\n')
            #     file1.write(fanyi.translate(facebook_bart.summary(content))+'\n')
            print(biaoti)
            self.summarytxt=self.summarytxt+fanyi.translate(biaoti)+'\n'+fanyi.translate(facebook_bart.summary(content))+'\n'
            self.englishsummarytext=self.englishsummarytext+biaoti+'\n'+facebook_bart.summary(content)+'\n'
            content=''

        return self.summarytxt,self.englishsummarytext



    def summary_rawtxt(self):
        fanyi=ydfanyi.YouDaoFanyi('7a8e1e60f26f8514','rSZorXXlhX6tglvqvZsOXl2jQVn81MOI')
        englishresult=facebook_bart.summary(self.origintxt)
        result=fanyi.translate(facebook_bart.summary(self.origintxt))
        return result,englishresult


if __name__=='__main__':

    rawpath=r'resource\txt\resnet\origin.txt'
    #refinepath=r'resource\txt\resnet\refine.txt'

    summarypath=r'resource\txt\resnet\summary.txt'

    a=txtprocess(rawpath,summarypath)
    #a.first_process()
    a.title_extract()
    #a.sentence()
    

    




     
   

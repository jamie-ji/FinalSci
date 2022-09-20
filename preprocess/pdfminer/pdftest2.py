from mailbox import linesep
import os
from pickle import TRUE
from quopri import decodestring
#from this import d
from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfdevice import PDFDevice
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal, LAParams,LTTextLineHorizontal,LTImage,LTRect,LTLine
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed
import re
import hashlib  #hash
import requests
import json
import time
import uuid
import sys
sys.path.append(r"D:\discourse_code\code\preprocess")
from ydfanyi import YouDaoFanyi


from transformers import LXMERT_PRETRAINED_CONFIG_ARCHIVE_MAP

class PDFprocess():
    def __init__(self,originpath):
        self.originpath=originpath
        # self.save_path=save_path  
        # self.extractresult=extractresult
        self.origintxt=''
        self.abstracttxt=''

    #获取文件夹的文件，限定只收录*pdf
    def getFileName(self,filepath):
        file_list = []
        for root,dirs,files in os.walk(filepath):
            for filespath in files:
                if 'pdf' in filespath.split('.')[1]:
                    file_list.append(os.path.join(root,filespath))
        return file_list

    def parse(self):

        #要解析PDF至少需要两个类：PDFParser 和 PDFDocument，PDFParser 从文件中提取数据，PDFDocument保存数据。
        #另外还需要PDFPageInterpreter去处理页面内容，PDFDevice将其转换为我们所需要的。
        #PDFResourceManager用于保存共享内容例如字体或图片。

        #用文件对象创建一个PDF文档分析器
        with open(self.originpath,'rb') as pdf_html:
            parser = PDFParser(pdf_html)
        #创建一个PDF文档
        doc = PDFDocument()
        #分析器和文档相互连接
        parser.set_document(doc)
        doc.set_parser(parser)

        #提供初始化密码，没有默认为空
        doc.initialize()
        #检查文档是否可以转成TXT，如果不可以就忽略
        if not doc.is_extractable:
            raise PDFTextExtractionNotAllowed
        else:
            #创建PDF资源管理器，来管理共享资源
            rsrcmagr = PDFResourceManager()
            #创建一个PDF设备对象
            laparams = LAParams()
            #将资源管理器和设备对象聚合
            device = PDFPageAggregator(rsrcmagr, laparams=laparams)
            
            #创建一个PDF解释器对象
            interpreter = PDFPageInterpreter(rsrcmagr, device)
            
            
            last_para = '' # 记录上一段文本
            count = 0 # 对文本块进行计数，方便后续查找标题和作者,多重循环的标记
            ab_count=True
            keycount=True
            author = '' # 记录作者
            #ab_count = 0 # 记录已识别的摘要的数量,多文件时需要
            
            fanyi=YouDaoFanyi('7a8e1e60f26f8514','rSZorXXlhX6tglvqvZsOXl2jQVn81MOI')
            #循环遍历列表，每次处理一个page内容
            #doc.get_pages()获取page列表
            for page in doc.get_pages():        
                interpreter.process_page(page)
                #接收该页面的LTPage对象
                layout = device.get_result()
                #这里的layout是一个LTPage对象 里面存放着page解析出来的各种对象
                #一般包括LTTextBox，LTFigure，LTImage，LTTextBoxHorizontal等等一些对像
                #想要获取文本就得获取对象的text属性
                
                for x in layout:   
                    try: 
                        if(isinstance(x, LTLine)):
                            #print(x)
                            continue

                        if(isinstance(x, LTTextBoxHorizontal)):
                            
                            result = x.get_text()          #行
                            
                            #过滤公式以及页脚，=放txt处理，一行只有=和其他的公式
                                         
                            if re.findall('[@∈∑#∉*∩∪⎤⎥⎦]|^fig\.|^tab\.|^figure\s\d|^table\s\d',result.lower())!=[] or '':
                                #print(result.lower())
                                continue

                            # #过滤表格里的多余数字
                            # if re.findall('^[0-9]+\.[0-9]+\s',result.lower())!=[] or '':
                            #     print(result.lower())
                            #     continue
                            # #过滤页边
                            # if re.findall('^[0-9a-zA-Z:\[\]]$',result.lower())!=[] or '':
                            #     #print(result.lower())
                            #     continue
                            # #过滤参考文献
                            # if re.findall('^\[[0-9]+]',result.lower().replace(' ', ''))!=[]:
                            #     #print(result.lower())
                            #     continue

                            #页眉过滤
                            # if re.findall('(^[0-9])|(^(research )?article)|(unclassified)|(www.)|(accepted (from|manuscript))|(proceedings of)|(vol.)|(volume \d)|(https?://)|(^ieee)|(sciencedirect)|(\d{4}\)$)|(\d{1,4} - \d{1,4}$)|(cid:)|(arxiv)',re.split('\s+$',result.lower())[0])!=[] or '':
                            #     #print('页眉信息:%s' % result.lower())
                            #     continue
                        
                            
                #输出第一份txt，为预处理后的原文，等待二次处理，分句
                            # else:  
                            #     #去掉文中的参考文献
                            #     result=re.sub('\[[\d\,\-\s]+\]',' ',result)
                            if ab_count == False:                          
                                result=re.sub('^[\w]?[\.]?[\w]?$','',result)
                                # with open('%s' % (self.save_path), 'a',encoding='utf-8') as f:
                                #     f.write(result)
                                self.origintxt=self.origintxt+result


                #输出第二份txt,为简单的摘要和关键词的集合，适用于多个文件
                            if count==0:
                                # 如果是researchgate的文章，直接翻页
                                if re.findall('^see discussions', result.lower())!=[]:                                
                                    break   #跳出外循环，直接跳一页
                                # 如果第一行是各种页眉等干扰信息，直接略过
                                if re.findall('(^[0-9])|(^(research )?article)|(unclassified)|(www.)|(accepted (from|manuscript))|(proceedings of)|(vol.)|(volume \d)|(https?://)|(^ieee)|(sciencedirect)|(\d{4}\)$)|(\d{1,4} - \d{1,4}$)|(cid:)|(arxiv)',re.split('\s+$',result.lower())[0])!=[] or '':
                                    #print('页眉信息:%s' % result.lower())
                                    count -= 1

                                else:
                                    # 将标题结果写入TXT
                                    # with open('%s' % (self.extractresult), 'a',encoding='utf-8') as ff:
                                    #     ff.write('\t\t\t\t标题为:'+result.lower()+'\n')
                                    self.abstracttxt=self.abstracttxt+'\t\t\t\t标题为:'+result.lower()+'\n'
                                        
                                    
                            # print(result)
                            #f.write(result)
                            # 提取作者
                            elif count==1:

                            
                                # 只取第一作者

                                author=result.split('\n')[0].split(',')[0].split(' and ')[0]                            
                                author = re.sub('by |[\s\d\*∗\/@†\(\&\)]+$', '', author)
                                # with open('%s' % (self.extractresult), 'a',encoding='utf-8') as ff:
                                #         ff.write('一作为:'+author+'\n')
                                self.abstracttxt=self.abstracttxt+'一作为:'+author+'\n'
                            
                            result=result.replace('\n', '')
                    
                            if ab_count:
                            #提取摘要，两种情况

                            # 转为小写，去掉空格，方便正则识别
                                last_para = last_para.lower().replace(' ', '')
                                
                                # 匹配Abstract和摘要内容分开的情况
                                if re.findall('abstract$', last_para)!=[]:
                                    # 去掉关键词
                                    oringin_result = re.split('(K|k)(eyword|EYWORD)[sS]?',result)[0]
                                    # 翻译
                                    trans_result = fanyi.translate(result)
                                    #print(trans_result)
                                    # with open('%s' % (self.extractresult), 'a',encoding='utf-8') as ff:
                                    #     ff.write('abstract：'+oringin_result+'\n')
                                    #     ff.write('\n摘要：'+trans_result+'\n')
                                    self.abstracttxt=self.abstracttxt+'abstract：'+oringin_result+'\n'
                                    self.abstracttxt=self.abstracttxt+'\n摘要：'+trans_result+'\n'
                                    ab_count=False
                            
                                # 匹配Abstract和摘要内容位于同一行的情况
                                elif re.findall('^abstract', result.lower().replace(' ', ''))!=[] and re.findall('abstract$', result.lower().replace(' ', ''))==[]:
                                    #if ab_count==0:
                                        # 去掉Abstract字眼及其后续的符号
                                        oringin_result = re.sub('(a|A)(bstract|BSTRACT)[- —.]?','', result)                                
                                        # 翻译
                                        trans_result = fanyi.translate(oringin_result)                                                                      
                                        #ab_count += 1
                                        # with open('%s' % (self.extractresult), 'a',encoding='utf-8') as ff:
                                        #     ff.write('\nabstract：'+oringin_result+'\n')
                                        #     ff.write('\n摘要：'+trans_result+'\n')
                                        self.abstracttxt=self.abstracttxt+'\nabstract：'+oringin_result+'\n'
                                        self.abstracttxt=self.abstracttxt+'\n摘要：'+trans_result+'\n'
                                        ab_count=False
                            if keycount:
                                # 匹配keywords和内容分开的情况
                                if re.findall('keywords$', last_para)!=[]:
                                    keywords_result = re.split('(K|k)(eyword|EYWORD)[sS]?',result)[0]
                                    # 翻译
                                    trans_result = fanyi.translate(keywords_result)                               
                                    #ab_count += 1                               
                                    # with open('%s' % (self.extractresult), 'a',encoding='utf-8') as ff:
                                    #     ff.write('\nkeywords：'+keywords_result+'\n')
                                    #     ff.write('\n关键词：'+trans_result+'\n')
                                    self.abstracttxt=self.abstracttxt+'\nkeywords：'+keywords_result+'\n'
                                    self.abstracttxt=self.abstracttxt+'\n关键词：'+trans_result+'\n'
                                    keycount=False

                                # 匹配keywords和内容位于同一行的情况
                                elif re.findall('^keywords', result.lower().replace(' ', ''))!=[] and re.findall('keywords$',result.lower().replace(' ', ''))==[]:
                                    #if ab_count==0:
                                        # 去掉keywords字眼及其后续的符号
                                        keywords_result = re.sub('(k|K)(eywords|EYWORDS)[- —.]?','', result)
                                        # 去掉关键词
                                        keywords_result = re.split('(K|k)(eyword|EYWORD)[sS]?',keywords_result)[0]
                                        # 翻译并转换人称
                                        trans_result = fanyi.translate(keywords_result)                                           
                                        #ab_count += 1                                                                        
                                        # with open('%s' % (self.extractresult), 'a',encoding='utf-8') as ff:
                                        #     ff.write('\nkeywords：'+keywords_result+'\n')
                                        #     ff.write('\n关键词：'+trans_result+'\n')    
                                        self.abstracttxt=self.abstracttxt+'\nkeywords：'+keywords_result+'\n'
                                        self.abstracttxt=self.abstracttxt+'\n关键词：'+trans_result+'\n' 
                                        keycount=False              
                            
                            last_para=result

                            count += 1
                            

                    except Exception as e:
                        print('out'+str(e))
                else:
                    continue
        return self.abstracttxt,self.origintxt


            
#单次调用，供开发使用
if __name__ == '__main__':
    #解析本地PDF文本，保存到本地TXT
    
    originpath=r'resource\pdf_dome\yolov4.pdf'
    # savepath=r'resource\txt\YOLOV4\1.txt'
    # extractresult=r'resource\txt\YOLOV4\2.txt'
    
    
    

    pdfprocess=PDFprocess(originpath)
    
    pdfprocess.parse()
    
    #processtxt(savepath)

#多次调用,界面


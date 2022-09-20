from nltk.tokenize import sent_tokenize
import re

sentences=[]
with open(r'pdf\raw.txt','r', encoding='UTF-8' ) as f:
    lines=f.readlines()
    for line in lines:
        strlist = re.sub('','',line)
        

for s in lines:
    sentences.append(sent_tokenize(s))

# sentences=[y for x in sentences for y in x]
print(sentences)
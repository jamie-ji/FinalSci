from datasets import load_from_disk
from transformers import BartTokenizer, BartForConditionalGeneration

# --------------------------------------------------------
# 数据集的load

checkpoint='model/facebook/'
tokenizer=BartTokenizer.from_pretrained(checkpoint)

dataset=load_from_disk("dataset/xsum/")

#dataset组成：'document': Value(dtype='string', id=None), 'summary': Value(dtype='string', id=None), 'id': Value(dtype='string', id=None)

#查看xsum的内容
#print(dataset)
#print(dataset['train'].features)
#print(dataset['train'][1]['document'])
#print(dataset['train'][1]['summary'])

#----------------------------------------------
# preprocess

#tokenizer全部的train数据集，204045个..(验证集11332个，测试集11334个)

test=tokenizer(dataset['train'][1]['document'],dataset['train'][1]['summary'],padding=True,truncation=True,)
print(test)



#train-body
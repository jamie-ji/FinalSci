from transformers import BartForConditionalGeneration,BartTokenizer
from transformers import AutoTokenizer,AutoModelForSequenceClassification,AdamW

import torch

#本地模型
tokenizer = AutoTokenizer.from_pretrained("model/bert-base-uncased/")
model =AutoModelForSequenceClassification .from_pretrained("model/bert-base-uncased/")

#model.save_pretrained('model/bert-base-uncased/')
#sequences = ["Using a Transformer network is simple","i am a super hero"]


#这些工作都在tokenizer里完成了
#tokens = tokenizer.tokenize(sequence)    #简单切token
#print(tokens)                            
#token转ids，对应tokennizer里的id
#ids = tokenizer.convert_tokens_to_ids(tokens)
#tokens = tokenizer(sequence)
#print(tokens)   #返回的是字典类型，有input_ids，token_type_ids,attention_mask

#input_ids = torch.tensor([ids])
#print("Input IDs:", input_ids)
#print(tokens)

#print(model(ids).logits)
#sequence=sequence[:max_sequence_length]
#print(tokens["input_ids"])

#----train

# batch = tokenizer(sequences, padding=True, truncation=True, return_tensors="pt")


# batch["labels"] = torch.tensor([1, 1])

# optimizer = AdamW(model.parameters())    #adam优化器
# loss = model(**batch).loss
# loss.backward()
# optimizer.step()


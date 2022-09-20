import torch
from transformers import BartForConditionalGeneration,BartTokenizer
tokenizer = BartTokenizer.from_pretrained(r"D:\discourse_code\model")
model = BartForConditionalGeneration.from_pretrained(r"D:\discourse_code\model",output_past=True)


articles = 'The tower is 324 metres (1,063 ft) tall, about the same height as an 81-storey building, and the tallest structure in Paris. Its base is square, measuring 125 metres (410 ft) on each side. During its construction, the Eiffel Tower surpassed the Washington Monument to become the tallest man-made structure in the world, a title it held for 41 years until the Chrysler Building in New York City was finished in 1930. It was the first structure to reach a height of 300 metres. Due to the addition of a broadcasting aerial at the top of the tower in 1957, it is now taller than the Chrysler Building by 5.2 metres (17 ft). Excluding transmitters, the Eiffel Tower is the second tallest free-standing structure in France after the Millau Viaduct.'  # put your articles here

length=len(articles.split())       #单词数

# 小于56的话，限定最长为本身，大于56，限定最短为0.2自身，最长为0.8自身

if length<56:
    maxl=56
    minl=10
else:
    maxl=int(0.8*length)
    minl=int(0.2*length)

inputs = tokenizer(articles, max_length=1024, return_tensors="pt",truncation=True)

summary_ids = model.generate(inputs["input_ids"], num_beams=2,max_length=maxl, min_length=minl)


print(tokenizer.batch_decode(summary_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0])
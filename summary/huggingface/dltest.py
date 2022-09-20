# from transformers import BartTokenizer, BartForConditionalGeneration

# model = BartForConditionalGeneration.from_pretrained("facebook/bart-large-cnn")
# tokenizer = BartTokenizer.from_pretrained("facebook/bart-large-cnn")

# model.save_pretrained("model/facebook/")
# tokenizer.save_pretrained("model/facebook/")

## huggingface
import torch
from transformers import BartForConditionalGeneration,BartTokenizer
tokenizer = BartTokenizer.from_pretrained("model/facebook/")
model = BartForConditionalGeneration.from_pretrained("model/facebook/",output_past=True)
articles = ['The tower is 324 metres (1,063 ft) tall, about the same hei·ght as an 81-storey building, and the tallest structure in Paris. Its base is square, measuring 125 metres (410 ft) on each side. During its construction, the Eiffel Tower surpassed the Washington Monument to become the tallest man-made structure in the world, a title it held for 41 years until the Chrysler Building in New York City was finished in 1930. It was the first structure to reach a height of 300 metres. Due to the addition of a broadcasting aerial at the top of the tower in 1957, it is now taller than the Chrysler Building by 5.2 metres (17 ft). Excluding transmitters, the Eiffel Tower is the second tallest free-standing structure in France after the Millau Viaduct.']  # put your articles here

#sentence=['what is wrong with you?','i love asoul']

#dct = tokenizer.batch_encode_plus(articles, max_length=1024, return_tensors="pt", pad_to_max_length=True)  # you can change max_length if you want

# #model_generate的参数？
# summaries = model.generate(
#     input_ids=dct["input_ids"],
#     attention_mask=dct["attention_mask"],
#     num_beams=4,
#     length_penalty=2.0,
#     max_length=142,  # +2 from original because we start at step=1 and stop before max_length
#     min_length=56,  # +1 from original because we start at step=1
#     no_repeat_ngram_size=3,
#     early_stopping=True,
#     do_sample=False,
# )  # change these arguments if you want

# dec = [tokenizer.decode(g, skip_special_tokens=True, clean_up_tokenization_spaces=False) for g in summaries]

# print(dec)
#print(tokenizer(sentence,padding=True,truncation=True, return_tensors="pt"))
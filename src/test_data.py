import os
import json
import nltk
import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm


nlp = en_core_web_sm.load()

data = None

ner_dict = {}

with open("../input/final_data.json",encoding="utf-8") as inpf:
    data = json.load(inpf)

ques_data = [x["text"] for x in data["rasa_nlu_data"]["common_examples"]]

for x in ques_data:
    text = nlp(x)
    for e in text.ents:
        label = e.label_
        word = e.text
        ner_dict[label] = ner_dict.get(label, [])
        if word not in ner_dict[label]:
            ner_dict[e.label_].append(word)



with open("../output/data.json","w",encoding="utf-8") as outf:
    json.dump(ner_dict,outf)
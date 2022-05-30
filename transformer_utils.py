from transformers import pipeline
from typing import List
import re

sentiment_analysis = pipeline("sentiment-analysis",model="siebert/sentiment-roberta-large-english")

# [{'label': 'POSITIVE', 'score': 0.9988656044006348}]

def get_sentiment(row):
    text = row.sent_msg
    if text is None:
        text = ''
    text = re.sub("<Media omitted>","",text)
    text = text.strip()
    if text == '':
        return None, None
    tokenizer_kwargs = {'padding':True,'truncation':True,'max_length':512}
    res = sentiment_analysis(text,**tokenizer_kwargs)[0]
    score = res['score']
    label = res['label']
    if label == 'NEGATIVE':
        score = score * -1
    return label, score

from transformers import AutoTokenizer, AutoModelForTokenClassification,TokenClassificationPipeline
ner_tokenizer = AutoTokenizer.from_pretrained("dslim/bert-base-NER")
ner_model = AutoModelForTokenClassification.from_pretrained("dslim/bert-base-NER")
nlp = pipeline("ner", model=ner_model, tokenizer=ner_tokenizer, aggregation_strategy="simple")

def get_locs(row):
    return get_entities(row, 'LOC')

def get_pers(row):
    return get_entities(row, 'PER')

def get_entities(row, entity_group):
    text = row.sent_msg
    if text is None or text.strip() == '':
        return [], []
    text = re.sub("<Media omitted>","",text)
    res = nlp(text)
    ents = [x['word'] for x in res if x['entity_group'] == entity_group and x['score'] > 0.9]
    scores = [x['score'] for x in res if x['entity_group'] == entity_group and x['score'] > 0.9 ]
    return ents, scores

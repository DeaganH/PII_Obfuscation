import numpy as np 

def predict_token_ids(text, tokenizer, model):
    
    tokenized = tokenizer([text], return_tensors="np")
    preds = model(tokenized).logits
    classes = np.argmax(preds, axis=-1)[0]
    
    word_index = {word_id:[] for word_id in tokenized.word_ids()}
    
    for word_id, input_id in zip(tokenized.word_ids(), tokenized['input_ids'][0]):
        word_index[word_id] += [input_id]
        
    word_index = {key:[tokenizer.decode(val)] for key, val in word_index.items()}
    
    identified = {word_id:model.config.id2label[id] 
                  for word_id, id in zip(tokenized.word_ids(), classes) 
                  if model.config.id2label[id] != 'O'}
    
    results = [
        {'entity': value,
        'index': key,
        'word': word_index[key][0],
        'start': tokenized.word_to_chars(key)[0],
        'end': tokenized.word_to_chars(key)[1]}
        for key, value in identified.items() if key != None        
    ]
    
    return results


def redact_text(text, PII_Entities):
    redacted_string = text

    for i in range(len(PII_Entities)):
        redacted_string = redacted_string[:PII_Entities[i]['start']] + '#'*(PII_Entities[i]['end']-PII_Entities[i]['start']) + redacted_string[PII_Entities[i]['end']:]
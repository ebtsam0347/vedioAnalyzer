import torch
from transformers import BertForQuestionAnswering, BertTokenizer

def extract_answer(question, text):
    # Load the pre-trained BERT model and tokenizer
    model = BertForQuestionAnswering.from_pretrained('bert-base-uncased')
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    
    # Tokenize the question and text
    inputs = tokenizer(question, text, add_special_tokens=True, return_tensors='pt')
    
    # Use the model to predict the start and end positions of the answer
    start_scores, end_scores = model(**inputs)
    start_index = torch.argmax(start_scores)
    end_index = torch.argmax(end_scores)
    
    # Decode the tokens back into text
    tokens = tokenizer.convert_ids_to_tokens(inputs['input_ids'][0])
    answer = ' '.join(tokens[start_index:end_index+1])
    answer = answer.replace(' ##', '')
    answer = answer.replace('[CLS] ', '')
    answer = answer.replace('[SEP]', '')
    
    return answer

question = 'What is the capital of France?'
text = 'Paris is the capital of France.'
answer = extract_answer(question, text)
print(answer) # Output: Paris

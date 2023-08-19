
#from transformers import BartTokenizer, BartForConditionalGeneration


def bart_summarize(article, max_length=100):
    # Load the pre-trained BART model and tokenizer
    model = BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn')
    tokenizer = BartTokenizer.from_pretrained('facebook/bart-large-cnn')
    
    # Tokenize the input article
    inputs = tokenizer([article], return_tensors='pt')
    
    # Generate a summary using the BART model
    summary_ids = model.generate(inputs['input_ids'], max_length=max_length, early_stopping=False)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    
    return summary
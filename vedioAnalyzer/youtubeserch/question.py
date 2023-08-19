'''from django.shortcuts import render
from django.http import JsonResponse
import torch
from transformers import BertTokenizer, BertForQuestionAnswering

tokenizer = BertTokenizer.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
model = BertForQuestionAnswering.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')

# Predefined text
context = "The COVID-19 pandemic, also known as the coronavirus pandemic, is an ongoing pandemic of coronavirus disease 2019 (COVID-19), caused by severe acute respiratory syndrome coronavirus 2 (SARS-CoV-2). The virus was first identified in December 2019 in Wuhan, China. The World Health Organization declared a Public Health Emergency of International Concern regarding COVID-19 on 30 January 2020, and later declared a pandemic on 11 March 2020. As of February 2023, more than 466 million cases have been confirmed, with more than 6 million deaths attributed to COVID-19, making it one of the deadliest pandemics in history."

def get_answer(request):
    if request.method == 'POST':
        question = request.POST.get('question', '')
        inputs = tokenizer.encode_plus(question, context, add_special_tokens=True, return_tensors="pt")
        input_ids = inputs["input_ids"].tolist()[0]
        start_scores, end_scores = model(inputs["input_ids"], token_type_ids=inputs["token_type_ids"])
        answer_start = torch.argmax(start_scores)
        answer_end = torch.argmax(end_scores) + 1
        answer = tokenizer.convert_tokens_to_string(tokenizer.convert_ids_to_tokens(input_ids[answer_start:answer_end]))
        return JsonResponse({'answer': answer})
    else:
        return render(request, 'qa.html')

from transformers import pipeline
import numpy

question_answer_pipeline = pipeline("question-answering")

context = r"""My name is Ebtsam. I am 14 years old."""

result = question_answer_pipeline(question="What is your name?", context=context)

print(f"Answer: '{result['answer']}', score: {round(result['score'], 4)}, start: {result['start']}")
'''
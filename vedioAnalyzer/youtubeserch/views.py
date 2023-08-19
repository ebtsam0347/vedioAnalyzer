from django.shortcuts import render
from django.http import HttpResponse
from .forms import *
from embed_video.fields import EmbedVideoField
from youtubesearchpython import VideosSearch
import pandas as pd
from pytube import YouTube
import os
import requests
from time import sleep
from urllib.parse import urlparse, parse_qs
from contextlib import suppress
from .pythonVedioIDPractice import get_yt_id 
from .assembly import*
from django.views.decorators.clickjacking import xframe_options_exempt
#from .summurization import bart_summarize
 

# Create your views here.

 



#temp
def index(request):
    return render(request, "youtubeserch/index.html")
    
def youtube(request):
    if request.method == "POST":
        form = youtubeForm(request.POST)
        text = request.POST['text']
        video = VideosSearch(text,limit =40)
        result_list = []
        for i in video.result()['result']:
            result_dict = {
                'input': text,
                'title': i['title'],
                'duration': i['duration'],
                'thumbnail': i['thumbnails'][0]['url'],
                'channel': i['channel']['name'],
                'link': i['link'],
                'views': i['viewCount']['short'],
                'published': i['publishedTime'],
                
            }
            desc = ' '
            if i['descriptionSnippet']:
                for j in i['descriptionSnippet']:
                    desc += j['text']
                result_dict['description'] = desc
                result_list.append(result_dict)
                contex = {
                    'form':form,
                    'results' : result_list
                }
        return render(request, "youtubeserch/youtube1.html",contex) 
    else:
        form = youtubeForm()
    contex = {'form':form}
    return render(request, "youtubeserch/youtube1.html",contex) 

# Search by  a youtube link
def youtubeLink(request):
    form = SearchForm(request.POST) 
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data["youtubeLink"]
        #url  = request.POST["youtubeLink"]
        

            print (url)
    return render(request, 'youtubeserch/youtubeLink.html', {
    "form":form,
      
    })
   
 
def searchLink(request,  link):
    form = SearchForm(request.POST)
    if form.is_valid():
            url = form.cleaned_data["youtubeLink"]

        #url  = request.POST["youtubeLink"]
            video_title, save_location, video_thumbnail = save_audio(url)
             # upload mp3 file to AssemblyAI
            audio_url = upload_to_AssemblyAI(save_location)
            # start analysis of the file
            polling_endpoint = start_analysis(audio_url)
            # receive the results
            results = get_analysis_results(polling_endpoint)

            
            text = results.json()['text']
            summary = results.json()['summary']
            topics = results.json()['iab_categories_result']['summary']
            sensitive_topics = results.json()['content_safety_labels']['summary']
            chapters = results.json()['chapters'] 
            auto_highlights = results.json()['auto_highlights_result'] 
            sentiment_analysis = results.json()['sentiment_analysis_results']

            #using bert model to summurize

            summurizetion = None#bart_summarize(text)
 
    
            #showing youtube video 
            link = url
            yid = get_yt_id(url)
            print(url.replace("watch?", "embed/"))
            print(get_yt_id(url)) 
            url = url.replace("watch?", "embed/")
            

            url = "https://www.youtube.com/embed/" + yid
        
        
    return render(request, "youtubeserch/main.html",{
      
     "url" : url,
     "link": link,
     "title":video_title,
     "file": save_location,
     "thumbnail": video_thumbnail,
     "summary": summary,
     "topics":topics,
     "sensitive_topics":sensitive_topics,
     "chapters":  chapters ,
     "auto_highlights": auto_highlights ,
     "sentiment_analysis":sentiment_analysis,
     "text":text,
     "summurizetion":summurizetion,


     })

#upload function
def upload(request):
    return render(request, "youtubeserch/upload.html",)
    
#upload vedio process
def uplodvideoprocess(request):
    file =  request.GET['file']
    return render (request,"youtubeserch/uplodvideoprocess.html",{
        "file" :file,
    })

#get function 
def videoprocess(request):
     
            url =  request.GET['link']

            video_title, save_location, video_thumbnail = save_audio(url)
            # upload mp3 file to AssemblyAI
            audio_url = upload_to_AssemblyAI(save_location)
             # start analysis of the file
            polling_endpoint = start_analysis(audio_url)
            # receive the results
            results = get_analysis_results(polling_endpoint)

            text = results.json()['text']
            summary = results.json()['summary']
            topics = results.json()['iab_categories_result']['summary']
            sensitive_topics = results.json()['content_safety_labels']['summary']
            chapters = results.json()['chapters'] 
            auto_highlights = results.json()['auto_highlights_result'] 
            sentiment_analysis = results.json()['sentiment_analysis_results']
            
            summarization = None#bart_summarize(text)
            #showing youtube video 
            link = url
            yid = get_yt_id(url)
            print(url.replace("watch?", "embed/"))
            print(get_yt_id(url)) 
            url = url.replace("watch?", "embed/")
            url = "https://www.youtube.com/embed/" + yid
       
            return render(request, "youtubeserch/youtubeserch.html",{

     "url" : url,
     "link": link,
     "title":video_title,
     "file": save_location,
     "thumbnail": video_thumbnail,
     "summary": summary,
     "topics":topics,
     "sensitive_topics":sensitive_topics,
     "chapters":  chapters ,
     "auto_highlights": auto_highlights ,
     "sentiment_analysis":sentiment_analysis,
     "text":text,
     "summurizetion":summarization,
    })


    # Predefined text
context = "The COVID-19 pandemic, also known as the coronavirus pandemic, is an ongoing pandemic of coronavirus disease 2019 (COVID-19), caused by severe acute respiratory syndrome coronavirus 2 (SARS-CoV-2). The virus was first identified in December 2019 in Wuhan, China. The World Health Organization declared a Public Health Emergency of International Concern regarding COVID-19 on 30 January 2020, and later declared a pandemic on 11 March 2020. As of February 2023, more than 466 million cases have been confirmed, with more than 6 million deaths attributed to COVID-19, making it one of the deadliest pandemics in history."

'''def get_answer(request):
    
    answereofq = {}  # define a default value for answereofq
    if request.method == 'POST':
        question = request.POST.get('question', '')
        inputs = tokenizer.encode_plus(question, context, add_special_tokens=True, return_tensors="pt")
        input_ids = torch.tensor(inputs['input_ids'])
        start_logits, end_logits = model(input_ids, token_type_ids=inputs["token_type_ids"])
        print(f'start_scores: {start_logits}')
        print(f'end_scores: {end_logits}')
        answer_start = torch.argmax(start_logits)
        answer_end = torch.argmax(end_logits) + 1
        answer = tokenizer.convert_tokens_to_string(tokenizer.convert_ids_to_tokens(input_ids[0][answer_start:answer_end]))
        answereofq = JsonResponse({'answer': answer})
        return answereofq
    else:
        answereofq = None
        return render(request, 'youtubeserch/qa.html',{
            "answereofq":answereofq,
        })'''

from django.http import JsonResponse
#from transformers import pipeline


def question_answer(request):
    if request.method == 'POST':
        question = request.POST['question']
        context = request.POST['context']

        # Run question answering pipeline
        question_answer_pipeline = pipeline("question-answering")
        result = question_answer_pipeline(question=question, context=context)

        # Return JSON response
        response_data = {
            'answer': result['answer'],
            'score': round(result['score'], 4),
            'start': result['start'],
        }
        return JsonResponse(response_data)

    context = {'default_context': 'My name is Ebtsam. I am 14 years old.'}
    return render(request, 'youtubeserch/qa.html', context=context)
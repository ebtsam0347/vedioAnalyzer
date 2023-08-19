from django.urls import path
from . import views

urlpatterns = [
    path ("",views.index,name = "index"),
    path ("youtube",views.youtube,name = "youtube"),
    path ("youtubeLink",views.youtubeLink,name = "youtubeLink"),
    path ("upload",views.upload,name = "upload"),
    path ("uplodvideoprocess",views.uplodvideoprocess, name = "uplodvideoprocess"),
    path ("videoprocess",views.videoprocess, name = "videoprocess"),
    path ("<str:link>",views.searchLink,name = "searchLink"),

    #temp
    #path('question_answer/', views.question_answer, name="question_answer"),


]

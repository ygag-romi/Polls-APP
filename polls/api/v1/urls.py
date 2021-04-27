from django.urls import path
from .views import ChoiceView, QuestionView, CommentView


urlpatterns = [
    path('questions/',
         QuestionView.as_view(), name='questionAPI-view'),

    path('choices/', ChoiceView.as_view(),
         name='choiceAPI-view'),

    path('comments/', CommentView.as_view(), name='commentAPI-view')
]
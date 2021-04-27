from django.urls import path
from .views import ChoiceView, QuestionView


urlpatterns = [
    path('questions/',
         QuestionView.as_view(), name='questionAPI-view'),

    path('choices/', ChoiceView.as_view(),
         name='choiceAPI-view'),
]
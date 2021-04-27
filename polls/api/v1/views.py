from rest_framework import generics as rest_generics
from .serializers import QuestionSerializer, ChoiceSerializer
from polls.models import Question, Choice


class QuestionView(rest_generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class ChoiceView(rest_generics.ListCreateAPIView):
    serializer_class = ChoiceSerializer
    queryset = Choice.objects.all()

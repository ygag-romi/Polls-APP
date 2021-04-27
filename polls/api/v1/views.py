from rest_framework import generics as rest_generics
from .serializers import QuestionSerializer, ChoiceSerializer, CommentSerializer
from polls.models import Question, Choice, Comment


class QuestionView(rest_generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class ChoiceView(rest_generics.ListCreateAPIView):
    serializer_class = ChoiceSerializer
    queryset = Choice.objects.all()


class CommentView(rest_generics.ListAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

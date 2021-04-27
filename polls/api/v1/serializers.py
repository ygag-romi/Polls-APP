from rest_framework import serializers
from polls.models import Question, Choice, Comment


class QuestionSerializer(serializers.ModelSerializer):
    pub_date = serializers.DateTimeField(format="%d-%b-%Y",
                                         input_formats=['%d-%b-%Y',
                                                        'iso-8601'])
    expiry = serializers.DateTimeField(format="%d-%b-%Y",
                                       input_formats=['%d-%b-%Y',
                                                      'iso-8601'])

    class Meta:
        fields = (
            'id',
            'question_text',
            'pub_date',
            'created_by',
            'expiry',
        )
        model = Question


class ChoiceSerializer(serializers.ModelSerializer):
    question_text = serializers.CharField(read_only=True,
                                          source='question.question_text')

    class Meta:
        model = Choice
        fields = (
            'id',
            'choice_text',
            'question',
            'question_text',
            'votes',
        )
        extra_kwargs = {
            'question': {'write_only': True}
        }


class CommentSerializer(serializers.ModelSerializer):
    question_text = serializers.CharField(read_only=True,
                                          source='question.question_text')

    class Meta:
        model = Comment
        fields = (
            'question_text',
            'question',
            'email',
            'body',
        )
        extra_kwargs = {
            'question': {'write_only': True}
        }

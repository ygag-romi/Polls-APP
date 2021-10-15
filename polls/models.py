from django.db import models
import datetime
from django.utils import timezone
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Tag(models.Model):
    """
    A model to add and save Tags associated with each Questions.
    """
    tag = models.CharField(max_length=200)

    def __str__(self):
        return self.tag


class Question(models.Model):
    """
    A model used to add and save new questions to the database,
    having multiple relationships with other models, to
    add choices, tags and comments to each poll.
    """
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    views = models.IntegerField(default=0)
    expiry = models.DateTimeField(null=True, default=None)
    priority = models.PositiveIntegerField(default=0, blank=True)
    question_tags = models.ManyToManyField(Tag, related_name='que_tags')
    closed = models.BooleanField(default=False,
                                 help_text="marks a poll as closed")
    # added 'closed' field later on to test django custom commands

    def __str__(self):
        return self.question_text

    def choices(self):
        no_of_choices = self.choice_set.all().count()
        return no_of_choices

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def is_expired(self):
        now = timezone.now()
        if self.expiry > now:
            return False
        else:
            return True


class Choice(models.Model):
    """
    A model used to add/save choices to each question.
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return str(self.choice_text)


class Comment(models.Model):
    """
    A model used to save comments associated with each
    question to the database.
    """
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name='comments')
    email = models.EmailField()
    created = models.DateTimeField(auto_now_add=True)
    body = models.TextField()
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return self.body

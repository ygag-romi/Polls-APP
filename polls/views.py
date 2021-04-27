from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from .models import Question, Choice, Comment
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.db.models import F
from .forms import CommentForm
from django.views.generic.edit import FormMixin, CreateView
from django.db.models import Sum


class IndexView(generic.ListView):
    """
    Displays the latest polls, ordered by a admin specified priority
    along with the most popular poll.
    """
    template_name = 'polls/index.html'

    def get(self, request):
        latest_question_list = Question.objects.order_by('priority')[:4]
        popular_polls = Question.objects.annotate(
            num_votes=Sum('choice__votes')).filter(
            num_votes__isnull=False).order_by('-num_votes')[0]

        return render(request, 'polls/index.html',
                      {'popular_polls': popular_polls,
                       'latest_question_list': latest_question_list})


class DetailView(FormMixin, generic.DetailView):
    """
    Once a user logs in, displays the selected poll and its tags, with an
    option to vote for one of the given choices. The user also has the
    option to view existing comments and to add new ones if required.
    """
    model = Question
    template_name = 'polls/details.html'
    form_class = CommentForm

    def get_queryset(self):
        """
        Excludes any questions that arent published yet
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

    def view_counter(self, request, question_id):
        Question.objects.filter(pk=question_id).update(views=F('views') + 1)

    def get(self, request, question_id):
        """
        Overrides the default 'get' method to check if the user selected
        question is expired, if so, redirects them to the results page of
        the poll.
        """
        question = get_object_or_404(Question, pk=question_id)
        if question.is_expired():
            return HttpResponseRedirect(
                reverse('polls:results', args=(question_id,)))
        else:
            self.view_counter(request, question_id)
            comments = Comment.objects.filter(question=question_id)
            form = CommentForm()
            return render(request, 'polls/details.html',
                          {'question': question, 'form': form,
                           'comments': comments})

    def post(self, request, question_id):
        return self.save_comment(request, question_id)

    def save_comment(self, request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        comment = None
        if request.method == 'POST':
            form = CommentForm(data=request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.question = question
                comment.save()

        else:
            form = CommentForm()

        context = {'question': question, 'comment': comment, 'form': form}
        return render(request, 'polls/details.html', context)


class ResultsView(generic.DetailView):
    """
    Displays the current results of a poll. Also provides the user an option
    to vote again
    """
    model = Question
    template_name = 'polls/results.html'


class VoteView(generic.ListView):
    """
    When a user votes in a question, this view checks whether the user actually
    selected a choice, if yes, it increases the selected choice by 1 and
    redirects the user to the results page of the question. Otherwise,
    the user is asked redirected to the same page again.
    """

    def post(self, request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        try:
            selected_choice = question.choice_set.get(
                pk=request.POST['choice'])

        except (KeyError, Choice.DoesNotExist):
            return render(request, 'polls/details.html', {
                'question': question,
                'error_message': "You did not select a choice",
            })
        else:
            selected_choice.votes += 1
            selected_choice.save()

            return HttpResponseRedirect(
                reverse('polls:results', args=(question_id,)))

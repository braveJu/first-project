from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from .models import Question, Choice
from django.urls import reverse
from django.views import generic


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'task/detail.html',
                      context={'question': question, 'error_message': "You didn't select a choice"})
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('task:results', args=(question.id,)))


class IndexView(generic.ListView):
    template_name = 'task/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'task/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'task/results.html'


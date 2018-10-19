# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .models import Choice, Question
from django.views.generic.edit import CreateView
from .forms import QuestionForm, ChoiceForm, ChoiceInlineFormSet
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from datetime import datetime


class QuestionChoiceCreate(CreateView):
    template_name = 'polls/question_form.html'
    form_class = QuestionForm
    success_url = reverse_lazy('polls:index')  
    def get_context_data(self, *args, **kwargs):
        context = super(QuestionChoiceCreate, self).get_context_data(*args,**kwargs)
        context['pub_date'] = datetime.now()
        if self.request.POST:
            context['questionchoices'] = ChoiceInlineFormSet(self.request.POST)
        else:
            context['questionchoices'] = ChoiceInlineFormSet()
        return context


    def form_valid(self, form):
        context = self.get_context_data()
        questionchoices = context['questionchoices']
        if questionchoices.is_valid():
            # self.object= form.save(commit=False)
            print(questionchoices)
            print(self.object)
            self.object = form.save()
            questionchoices.instance = self.object
            questionchoices.save()
            return redirect(self.success_url)
        else:
            return self.render_to_response(self.get_context_data(form=form))


class ChoicesCreate(CreateView):
    model = Choice
    form_class = ChoiceInlineFormSet
    success_url = reverse_lazy('polls:index')

    def get_context_data(self, **kwargs):
        data = super(ChoicesCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['choicequestions'] = ChoiceInlineFormSet(self.request.POST)
        else:
            data['choicequestions'] = ChoiceInlineFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        choicequestions = context['choicequestions']
        if choicequestions.is_valid():
            self.object = form.save()
            choicequestions.instance = self.object
            choicequestions.save()
            return HttpResponseRedirect(self.success_url)
        else:
            return self.render_to_response(self.get_context_data(form=form))


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

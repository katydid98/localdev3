# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .models import Choice, Question, Company
from django.views.generic.edit import CreateView
from django.core.urlresolvers import reverse_lazy
from polls.forms import QuestionForm, ChoiceInlineFormSet
import json


# I DON'T KNOW HOW TO USE THIS IN D3 YET.
# data to extract choices and votes into a dict list
# [{'choice_text': u'hello', 'votes': 5}, {'choice_text': u'there', 'votes': 1}, {'choice_text': u'u', 'votes': 1}]
def d3_voteData(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    choices_votes = question.choice_set.all().values('choice_text',
                                                     'votes')
    choices_list = list(choices_votes) # convert the QuerySet to a list object
    return JsonResponse(choices_list, safe=False)


def autocomplete_companyData(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        companies = Company.objects.filter(name__startswith=q)
        results = []
        for company in companies:
            company_json = {}
            company_json['id'] = company.pk
            company_json['label'] = company.name
            company_json['value'] = company.name
            results.append(company_json)
        data = json.dumps(results)
    else:
        data = 'why im i failing??'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


class QuestionCreate(CreateView):
    template_name = 'polls/question_form.html'
    model = Question
    form_class = QuestionForm
    success_url = reverse_lazy('polls:index')

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests. Instantiates blank versions of the form
        and its inline formsets.
        """
        self.object = None
        form = QuestionForm()
        choice_form = ChoiceInlineFormSet()
        return self.render_to_response(
            self.get_context_data(form=form, choice_form=choice_form))

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests. Instantiates a form instance and its inline
        formsets with the passed POST inputs, then checks for
        validity.
        """
        self.object = None
        form = QuestionForm(self.request.POST)
        choice_form = ChoiceInlineFormSet(self.request.POST)
        if (form.is_valid() and choice_form.is_valid()):
            return self.form_valid(form, choice_form)
        else:
            return self.form_invalid(form, choice_form)

    def form_valid(self, form, choice_form):
        """
        If form is valid, creates a Question instance along with
        associated Choices and redirects to index page.
        """
        self.object = form.save(commit=False)
        self.object.pub_date = timezone.now()
        self.object.save()
        choice_form.instance = self.object
        choice_form.save()
        return HttpResponseRedirect(self.success_url)

    def form_invalid(self, form, choice_form):
        """
        If form is invalid, re-renders the context data with the
        data-filled forms and errors.
        """
        return self.render_to_response(
            self.get_context_data(form=form, choice_form=choice_form))


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
        return HttpResponseRedirect(reverse('polls:results',
                                            args=(question.id,)))


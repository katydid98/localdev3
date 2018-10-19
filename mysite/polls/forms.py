from django import forms
from django.forms import ModelForm
from polls.models import Question, Choice
from django.forms.models import modelformset_factory, inlineformset_factory
from django.forms import BaseInlineFormSet


class QuestionForm(forms.ModelForm):

    class Meta:
        model = Question
        fields = ['question_text']
        labels = {
            'question_text': ('Question')
        }
        widgets = {
            'question_text': forms.TextInput(attrs={'placeholder': 'Enter Question'})
        }


class ChoiceForm(forms.ModelForm):

    class Meta:
        model = Choice
        fields = ['choice_text', 'question']
        labels = {
            'choice_text': ('Choice')
        }


ChoiceFormSet = modelformset_factory(
    Choice,
    form=ChoiceForm,
    extra=2,

)


ChoiceInlineFormSet = inlineformset_factory(
    Question,
    Choice,
    can_delete=False,
    extra=2,
    fields=['choice_text'],
    labels={
        'choice_text': ('Choice')
    },
    form=QuestionForm,
    formset=ChoiceFormSet,
    min_num=1,
        widgets = {
        'choice_text': forms.TextInput(attrs={'placeholder': 'enter choice'})
    }
)

# from django import forms
# from django.forms import ModelForm, inlineformset_factory

# from .models import Question, Choice


# class QuestionForm(forms.ModelForm):
#     class Meta:
#         model = Question
#         fields = ['question_text']
#         labels = {
#             'question_text': ('Question')
#         }
#         widgets = {
#             'question_text': forms.TextInput(attrs={'placeholder': 'Enter Question'})
#         }

# class ChoiceForm(forms.ModelForm):

#     class Meta:
#         model = Choice
#         fields = ['choice_text', 'question']
#         labels = {
#             'choice_text': ('Choice')
#         }

# # class ChoiceForm(forms.ModelForm):
# #     class Meta:
# #         model = Choice
# #         exclude = ()


# ChoiceInlineFormSet = inlineformset_factory(Question, Choice,
#                                             form=ChoiceForm, extra=1)

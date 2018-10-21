from django import forms
from polls.models import Question, Choice
from django.forms.models import inlineformset_factory


class QuestionForm(forms.ModelForm):

    class Meta:
        model = Question
        fields = ['question_text', 'company']
        labels = {
            'question_text': ('Question'),
            'company': ('Company')
        }
        widgets = {
            'question_text': forms.TextInput(attrs={'placeholder': 'Enter Question'}),
            'company': forms.TextInput(attrs={'id': 'companiesList'}),
        }


ChoiceInlineFormSet = inlineformset_factory(Question,
                                            Choice,
                                            fields=['question', 'choice_text'],
                                            exclude=[], can_delete=False)



from django import forms
from polls.models import Question, Choice
from django.forms.models import inlineformset_factory


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


ChoiceInlineFormSet = inlineformset_factory(Question,
                                            Choice,
                                            fields=['question', 'choice_text'],
                                            exclude=[], can_delete=False)


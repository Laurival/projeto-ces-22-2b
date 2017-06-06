from django import forms
from django.db import models
from .models import Question,Choice

class QuestionForm(forms.ModelForm):

    class Meta:
        model = Question
        fields = (
            'question_text',
            )

class ChoiceForm(forms.Form):
    choice_text = forms.CharField(max_length=200)
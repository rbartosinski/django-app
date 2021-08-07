from django import forms
from django.forms import SelectDateWidget


class QuestionForm(forms.Form):
    question_text = forms.CharField(label="Podaj pytanie", max_length=200)
    pub_date = forms.DateTimeField(label="Data publikacji")
    # pub_date = forms.DateTimeField(label="Data publikacji", widget=SelectDateWidget)

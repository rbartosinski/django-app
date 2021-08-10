from django import forms
from django.forms import SelectDateWidget

from .models import Question


class QuestionForm(forms.Form):
    question_text = forms.CharField(label="Podaj pytanie", max_length=200)
    pub_date = forms.DateTimeField(label="Data publikacji")
    # pub_date = forms.DateTimeField(label="Data publikacji", widget=SelectDateWidget)


class ChoiceForm(forms.Form):
    question = forms.ModelChoiceField(queryset=Question.objects.all())
    choice_text = forms.CharField(label="Podaj wybór", max_length=200)
    votes = forms.IntegerField(required=False)


class LoginForm(forms.Form):
    username = forms.CharField(label="Podaj nazwę użytkownika")
    password = forms.CharField(label="Hasło", widget=forms.PasswordInput)


class RegisterForm(forms.Form):
    username = forms.CharField(label='Your name')
    password = forms.CharField(widget=forms.PasswordInput, label='Password')
    password_confirmation = forms.CharField(widget=forms.PasswordInput, label='Password confirmation')
    email = forms.EmailField(label='Your email')

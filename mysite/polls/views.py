from django.contrib import messages
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views import generic, View

from .models import Question, Choice
from .forms import QuestionForm, ChoiceForm


class IndexView(View):

    def get(self, request):
        latest_question_list = Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')
        form = QuestionForm()
        context = {
            'form': form,
            'latest_question_list': latest_question_list,
        }
        return render(request, 'polls/index.html', context)

    def post(self, request):
        form = QuestionForm(request.POST)
        if form.is_valid():
            Question.objects.create(**form.cleaned_data)
        else:
            messages.error(request, 'Message: Form is not valid')
            return HttpResponseRedirect(reverse('polls:index'))
        return HttpResponseRedirect(reverse('polls:index'))


class DetailView(View):

    def get(self, request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        context = {
            'question': question,
        }
        return render(request, 'polls/detail.html', context)


class EditQuestionView(View):

    def get(self, request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        form = QuestionForm(initial={
            'question_text': question.question_text,
            'pub_date': question.pub_date,
        })
        context = {
            'form': form,
            'question': question,
        }
        return render(request, 'polls/edit.html', context)

    def post(self, request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        form = QuestionForm(request.POST)
        if form.is_valid():
            question.question_text = form.cleaned_data["question_text"]
            question.pub_date = form.cleaned_data["pub_date"]
            question.save()
        else:
            messages.error(request, 'Message: Form is not valid')
            return HttpResponseRedirect(reverse('polls:edit'))
        return HttpResponseRedirect(reverse('polls:detail', args=(question.id,)))


class DeleteQuestionView(View):

    def get(self, request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        question.delete()
        messages.info(request, 'Message: Question ID {} deleted'.format(question_id))
        return HttpResponseRedirect(reverse('polls:index'))


class AddChoiceView(View):

    def get(self, request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        form = ChoiceForm(initial={
            'question': question_id,
            'votes': 0,
        })
        context = {
            'form': form,
            'question': question,
        }
        return render(request, 'polls/add_choice.html', context)

    def post(self, request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        form = ChoiceForm(request.POST)
        if form.is_valid():
            Choice.objects.create(**form.cleaned_data)
        else:
            messages.error(request, 'Message: Form is not valid')
            return HttpResponseRedirect(reverse('polls:add_choice'))
        return HttpResponseRedirect(reverse('polls:detail', args=(question.id,)))


class EditChoiceView(View):

    def get(self, request, question_id, choice_id):
        question = get_object_or_404(Question, pk=question_id)
        choice = get_object_or_404(Choice, pk=choice_id)
        form = ChoiceForm(initial={
            'question': question_id,
            'choice_text': choice.choice_text,
            'votes': choice.votes,
        })
        context = {
            'form': form,
            'question': question,
            'choice': choice,
        }
        return render(request, 'polls/edit_choice.html', context)

    def post(self, request, question_id, choice_id):
        question = get_object_or_404(Question, pk=question_id)
        choice = get_object_or_404(Choice, pk=choice_id)
        form = ChoiceForm(request.POST)
        if form.is_valid():
            choice.question = form.cleaned_data["question"]
            choice.choice_text = form.cleaned_data["choice_text"]
            choice.votes = form.cleaned_data["votes"]
            choice.save()
        else:
            messages.error(request, 'Message: Form is not valid')
            return HttpResponseRedirect(reverse('polls:edit_choice'))
        return HttpResponseRedirect(reverse('polls:detail', args=(question.id,)))


class ResultsView(View):

    def get(self, request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        context = {
            'question': question,
        }
        return render(request, 'polls/results.html', context)


class VoteView(View):

    def post(self, request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        try:
            selected_choice = question.choice_set.get(pk=request.POST['choice'])
        except (KeyError, Choice.DoesNotExist):
            messages.error(request, 'Message: You didnt select a choice.')
            return HttpResponseRedirect(reverse('polls:detail', args=(question.id,)))
        else:
            try:
                selected_choice.votes += 1
            except TypeError:
                selected_choice.votes = 1
            selected_choice.save()
            return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


# class IndexView(generic.ListView):
#     template_name = 'polls/index.html'
#     context_object_name = 'latest_question_list'
#
#     def get_queryset(self):
#         return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')

# class ResultsView(generic.DetailView):
#     model = Question
#     template_name = 'polls/results.html'

# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     context = {
#         'latest_question_list': latest_question_list,
#         'if_test': "success",
#         'if_test1': "error",
#     }
#     return render(request, 'polls/index.html', context)
#
#
# def detail(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     context = {
#         'question': question,
#     }
#     return render(request, 'polls/detail.html', context)
#
#
# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     context = {
#         'question': question,
#     }
#     return render(request, 'polls/results.html', context)

# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')
#     form = QuestionForm()
#     context = {
#         'form': form,
#         'latest_question_list': latest_question_list,
#     }
#     return render(request, 'polls/index.html', context)


# def create_question(request):
#     prefix = "My object"
#     form_template = QuestionForm()
#     print("Form template: ", form_template)
#     print("Request POST data: ", request.POST)
#     form = QuestionForm(request.POST)
#     print("Form with request data: ", form)
#
#     # Question.objects.create(
#     #     question_text="{} - {}".format(prefix, request.POST["question_text"]),
#     #     pub_date=request.POST["pub_date"]
#     # )
#
#     if form.is_valid():
#         print("Form from cleaned data dict: ", form.cleaned_data)
#         # Question.objects.create(**form.cleaned_data)
#         Question.objects.create(
#             question_text="{} - {}".format(prefix, form.cleaned_data["question_text"]),
#             pub_date=form.cleaned_data["pub_date"]
#         )
#     else:
#         latest_question_list = Question.objects.order_by('-pub_date')[:5]
#         context = {
#             'form': form,
#             'latest_question_list': latest_question_list,
#             'error_message': "Form is not valid"
#         }
#         return render(request, 'polls/index.html', context)
#     return HttpResponseRedirect(reverse('polls:index'))

# def vote(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     print(question)
#     print("POST: ", request.POST)
#     try:
#         selected_choice = question.choice_set.get(pk=request.POST['choice'])
#         print("Choice nr: ", request.POST['choice'])
#     except (KeyError, Choice.DoesNotExist):
#         context = {
#             'question': question,
#             'error_message': "You didn't select a choice.",
#         }
#         return render(request, 'polls/detail.html', context)
#     else:
#         print("var - selected_choice: ", selected_choice)
#         print("var - selected_choice votes: ", selected_choice.votes)
#         selected_choice.votes += 1
#         # selected_choice.choice_text = "Słoń"
#         selected_choice.save()
#         print("var - selected_choice votes - after: ", selected_choice.votes)
#         return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
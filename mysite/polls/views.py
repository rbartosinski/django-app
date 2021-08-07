from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from .models import Question, Choice
from .forms import QuestionForm


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')
    form = QuestionForm()
    context = {
        'form': form,
        'latest_question_list': latest_question_list,
    }
    return render(request, 'polls/index.html', context)


def create_question(request):
    prefix = "My object"
    form_template = QuestionForm()
    print("Form template: ", form_template)
    print("Request POST data: ", request.POST)
    form = QuestionForm(request.POST)
    print("Form with request data: ", form)

    # Question.objects.create(
    #     question_text="{} - {}".format(prefix, request.POST["question_text"]),
    #     pub_date=request.POST["pub_date"]
    # )

    if form.is_valid():
        print("Form from cleaned data dict: ", form.cleaned_data)
        # Question.objects.create(**form.cleaned_data)
        Question.objects.create(
            question_text="{} - {}".format(prefix, form.cleaned_data["question_text"]),
            pub_date=form.cleaned_data["pub_date"]
        )
    else:
        latest_question_list = Question.objects.order_by('-pub_date')[:5]
        context = {
            'form': form,
            'latest_question_list': latest_question_list,
            'error_message': "Form is not valid"
        }
        return render(request, 'polls/index.html', context)
    return HttpResponseRedirect(reverse('polls:index'))


def edit_question(request, question_id):
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
    print(question)
    print("POST: ", request.POST)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
        print("Choice nr: ", request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        context = {
            'question': question,
            'error_message': "You didn't select a choice.",
        }
        return render(request, 'polls/detail.html', context)
    else:
        print("var - selected_choice: ", selected_choice)
        print("var - selected_choice votes: ", selected_choice.votes)
        selected_choice.votes += 1
        # selected_choice.choice_text = "Słoń"
        selected_choice.save()
        print("var - selected_choice votes - after: ", selected_choice.votes)
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


# class IndexView(generic.ListView):
#     template_name = 'polls/index.html'
#     context_object_name = 'latest_question_list'
#
#     def get_queryset(self):
#         return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

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

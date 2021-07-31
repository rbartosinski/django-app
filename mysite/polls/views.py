from django.http import HttpResponse


def index(request):
    return HttpResponse("String")


def my_new_view(request):
    return HttpResponse("NEW STATUS")

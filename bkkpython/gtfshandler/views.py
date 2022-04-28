from importlib import import_module
from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponse
from django.template import loader
from .models import Question, HevDeparture
from django.shortcuts import get_object_or_404, render
from . import gtfsparser

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'gtfshandler/index.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'gtfshandler/detail.html', {'question': question})

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)

def menetrend(request):
    departuresList = HevDeparture.objects.order_by('departureTime')#[:5]
    time = timezone.localtime(timezone.now())

    print('now')
    print(time)
    departuresListFiltered = departuresList.filter(departureTime__time__gte=time)
    print(departuresListFiltered)
    context = {'departuresList': departuresListFiltered}
    return render(request, 'gtfshandler/menetrend.html', context)
from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("Вы на странице index аккаунтов")
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse


def index(request):
    dados = {'mensagem': 'Olá'}
    return JsonResponse(dados)

def login(request):
    dados = {'mensagem':'tas a tentar fazer login ze'}
    return JsonResponse(dados)
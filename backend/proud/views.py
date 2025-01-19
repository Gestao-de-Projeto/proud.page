from django.shortcuts import render
from django.http import HttpResponse, JsonResponse


def index(request):
    dados = {'mensagem': 'Olá'}
    return JsonResponse(dados)

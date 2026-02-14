from django.http import JsonResponse
from django.shortcuts import render


def health(request):
    return JsonResponse({"status": "ok"})


def landing(request):
    return render(request, "landing.html")
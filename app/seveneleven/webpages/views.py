from django.shortcuts import render


def index(request):
    """ Render homepage"""
    return render(request, 'index.html')

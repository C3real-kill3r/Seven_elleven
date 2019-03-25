from django.shortcuts import render

# Create your views here.

def index(request):
    """ Render homepage"""
    return render(request, 'index.html')

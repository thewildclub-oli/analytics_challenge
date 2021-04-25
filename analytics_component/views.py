from django.shortcuts import render, redirect

# Create your views here.

def index(request):
    context = {}
    return render(request, 'analytics_component/index.html', context)

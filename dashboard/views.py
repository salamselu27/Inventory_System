from django.shortcuts import render

def index(request):
    return render(request, 'dashboard/index.html')

def coming_soon(request):
    return render(request, 'dashboard/coming_soon.html')

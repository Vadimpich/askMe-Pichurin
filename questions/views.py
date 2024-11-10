from django.shortcuts import render

def index(request):
    return render(request, 'questions/index.html')

def question(request, pk):
    return render(request, 'questions/question.html')

def tag(request, tag):
    return render(request, 'questions/tag.html')

def hot(request):
    return render(request, 'questions/hot.html')

def ask(request):
    return render(request, 'questions/ask.html')

def login(request):
    return render(request, 'users/login.html')

def register(request):
    return render(request, 'users/register.html')

def settigns(request):
    return render(request, 'users/settings.html')

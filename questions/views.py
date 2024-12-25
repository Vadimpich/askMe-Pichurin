from django.db.models import Count
from django.shortcuts import render

from questions.models import Question, Answer, Tag
from questions.utils import paginate


def index_view(request):
    questions = Question.objects.new_questions().add_likes()
    page_obj = paginate(request, questions, 10)
    return render(
        request,
        'questions/index.html',
        {'page_obj': page_obj}
    )


def question_detail_view(request, pk):
    answers = Answer.objects.filter(question_id=pk).annotate(
        likes_count=Count('answer_likes'))
    cur_question = Question.objects.annotate(
        likes_count=Count('question_likes')).get(pk=pk)
    page_obj = paginate(
        request,
        answers,
        5
    )
    return render(
        request,
        'questions/question.html',
        {
            'question': cur_question,
            'page_obj': page_obj
        }
    )


def tag_view(request, tag_name):
    tag = Tag.objects.get(name=tag_name)
    questions = tag.questions.all().add_likes()
    page_obj = paginate(
        request,
        questions,
        10
    )
    return render(
        request,
        'questions/tag.html',
        {
            'tag': tag_name,
            'page_obj': page_obj,
        }
    )


def hot_view(request):
    questions = Question.objects.hot_questions().add_likes()
    page_obj = paginate(
        request,
        questions,
        10
    )
    return render(
        request,
        'questions/hot.html',
        {'page_obj': page_obj}
    )


def ask(request):
    return render(request, 'questions/ask.html')


def login(request):
    return render(request, 'users/login.html')


def signup(request):
    return render(request, 'users/signup.html')


def settigns(request):
    return render(
        request,
        'users/settings.html'
    )

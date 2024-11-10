from django.shortcuts import render

from questions.utils import paginate

QUESTIONS = [{
    'id': i,
    'title': f'Вопрос №{i}',
    'text': f'Текст вопроса №{i}',
    'tag': 'Python' if (i % 2 == 0) else 'JavaScript',
} for i in range(1, 31)]

ANSWERS = [{
    'id': i,
    'question_id': i % 30 + 1,
    'text': f'Ответ {i} на вопрос {i % 30 + 1}\n'
            f'Попробуйте перезагрузить компьютер'
} for i in range(1, 151)]

USER = {
    'id': 1,
    'username': 'TestUser',
    'email': 'test@email.com'
}

def index(request):
    page_obj = paginate(request, QUESTIONS, 10)
    return render(
        request,
        'questions/index.html',
        {'page_obj': page_obj}
    )


def question(request, pk):
    page_obj = paginate(
        request,
        [ans for ans in ANSWERS if ans['question_id'] == pk],
        3
    )
    return render(
        request,
        'questions/question.html',
        {
            'question': QUESTIONS[pk - 1],
            'page_obj': page_obj
        }
    )


def tag(request, tag):
    page_obj = paginate(
        request,
        [q for q in QUESTIONS if q['tag'].lower() == tag.lower()],
        10
    )
    return render(
        request,
        'questions/tag.html',
        {
            'tag': tag,
            'page_obj': page_obj,
        }
    )


def hot(request):
    page_obj = paginate(
        request,
        list(reversed(QUESTIONS[:10])),
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
        'users/settings.html',
        {'user': USER}
    )

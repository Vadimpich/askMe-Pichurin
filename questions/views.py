from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404

from questions.models import Question, Answer, Tag
from questions.forms import QuestionForm, AnswerForm
from questions.utils import paginate


def index_view(request):
    questions = Question.objects.new_questions().add_likes().add_answers()
    page_obj = paginate(request, questions, 10)
    return render(
        request,
        'questions/index.html',
        {'page_obj': page_obj}
    )


def ask(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.save()
            form.save_m2m()
            return redirect('question', pk=question.pk)
    else:
        form = QuestionForm()

    return render(request, 'questions/ask.html', {'form': form})


def question_detail_view(request, pk):
    question = Question.objects.get(pk=pk)
    answers = question.answers.annotate(likes_count=Count('answer_likes'))

    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.question = question
            answer.save()
            return redirect('question', pk=question.pk)
    else:
        form = AnswerForm()

    page_obj = paginate(request, answers, 5)
    return render(request, 'questions/question.html', {
        'question': question,
        'page_obj': page_obj,
        'form': form,
    })


def add_answer(request, pk):
    question = get_object_or_404(Question, id=pk)

    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = question
            answer.author = request.user
            answer.save()
            return redirect('question', pk=question.id)
    else:
        form = AnswerForm()

    return render(request, 'questions/question.html',
                  {'question': question, 'form': form})


def tag_view(request, tag_name):
    tag = Tag.objects.get(name=tag_name)
    questions = tag.questions.all().add_likes().add_answers()
    page_obj = paginate(request, questions, 10)
    return render(
        request,
        'questions/tag.html',
        {
            'tag': tag_name,
            'page_obj': page_obj,
        }
    )


def hot_view(request):
    questions = Question.objects.hot_questions().add_likes().add_answers()
    page_obj = paginate(request, questions, 10)
    return render(
        request,
        'questions/hot.html',
        {'page_obj': page_obj}
    )

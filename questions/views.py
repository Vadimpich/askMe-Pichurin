from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from questions.models import Question, Answer, Tag, QuestionLike, AnswerLike
from questions.forms import QuestionForm, AnswerForm
from questions.utils import paginate


def index_view(request):
    questions = Question.objects.new_questions().add_likes()
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
    likes_count = QuestionLike.objects.filter(question=question).count()

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
        'likes_count': likes_count,
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
    questions = tag.questions.all().add_likes()
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
    questions = Question.objects.hot_questions().add_likes()
    page_obj = paginate(request, questions, 10)
    return render(
        request,
        'questions/hot.html',
        {'page_obj': page_obj}
    )


@login_required
def like_question(request):
    if request.method == 'POST':
        question_id = request.POST.get('question_id')
        try:
            question = Question.objects.get(id=question_id)
        except Question.DoesNotExist:
            return JsonResponse({'error': 'Вопрос не найден'}, status=400)

        existing_like = QuestionLike.objects.filter(question=question, user=request.user).first()
        if existing_like:
            existing_like.delete()
        else:
            QuestionLike.objects.create(question=question, user=request.user)

        likes_count = question.question_likes.count()
        return JsonResponse({'likes_count': likes_count})
    return JsonResponse({'error': 'Неверный метод запроса'}, status=400)


@login_required
def like_answer(request):
    if request.method == 'POST':
        answer_id = request.POST.get('answer_id')
        try:
            answer = Answer.objects.get(id=answer_id)
        except Answer.DoesNotExist:
            return JsonResponse({'error': 'Вопрос не найден'}, status=400)

        existing_like = AnswerLike.objects.filter(answer=answer, user=request.user).first()
        if existing_like:
            existing_like.delete()
        else:
            AnswerLike.objects.create(answer=answer, user=request.user)

        likes_count = answer.answer_likes.count()
        return JsonResponse({'likes_count': likes_count})
    return JsonResponse({'error': 'Неверный метод запроса'}, status=400)


@login_required
def mark_correct_answer(request):
    if request.method == 'POST':
        question_id = request.POST.get('question_id')
        answer_id = request.POST.get('answer_id')

        try:
            question = Question.objects.get(id=question_id)
            answer = Answer.objects.get(id=answer_id, question=question)
        except (Question.DoesNotExist, Answer.DoesNotExist):
            return JsonResponse({'error': 'Вопрос или ответ не найден'}, status=400)

        if question.author != request.user:
            return JsonResponse({'error': 'Вы не можете выбрать правильный ответ'}, status=403)

        answer.correct = not answer.correct
        answer.save()

        return JsonResponse({'message': 'Ответ помечен как правильный'})
    return JsonResponse({'error': 'Неверный метод запроса'}, status=400)

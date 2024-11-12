import random

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from questions.models import Question, Answer, Tag, QuestionLike


class Command(BaseCommand):
    help = 'Заполнение базы данных тестовыми данными'

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int)

    def handle(self, *args, **kwargs):
        ratio = kwargs['ratio']

        users = [
            User(username=f'User{i}', password='password')
            for i in range(ratio)
        ]
        User.objects.bulk_create(users, ignore_conflicts=True)
        users = User.objects.all()[:ratio]
        print(f'Создано {ratio} пользователей.')


        tags = [
            Tag(name=f'Тег{i}')
            for i in range(ratio)
        ]
        Tag.objects.bulk_create(tags, ignore_conflicts=True)
        tags = Tag.objects.all()[:ratio]
        print(f'Создано {ratio} тегов.')

        questions = [
            Question(
                title=f'Вопрос №{i}',
                author=random.choice(users),
                text=f'Текст вопроса №{i}',
            ) for i in range(ratio * 10)
        ]
        Question.objects.bulk_create(questions)
        questions = Question.objects.all()[
                    :ratio * 10]
        print(f'Создано {ratio * 10} вопросов.')

        for question in questions:
            question.tags.add(*random.sample(list(tags), min(3, len(tags))))

        answers = [
            Answer(
                question=random.choice(questions),
                author=random.choice(users),
                text=f'Текст ответа №{i}',
            ) for i in range(ratio * 100)
        ]
        Answer.objects.bulk_create(answers)
        print(f'Создано {ratio * 100} ответов.')

        question_likes = [
            QuestionLike(
                user=random.choice(users),
                question=random.choice(questions)
            ) for _ in range(ratio * 200)
        ]
        QuestionLike.objects.bulk_create(question_likes, ignore_conflicts=True)
        print(f'Создано {ratio * 200} лайков.')

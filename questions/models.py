from django.contrib.auth.models import User
from django.db import models
from django.db.models import Count


class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True,
                            verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class QuestionQuerySet(models.QuerySet):
    def add_likes(self):
        return self.annotate(likes_count=Count('likes'))


class QuestionManager(models.Manager):
    def get_queryset(self):
        return QuestionQuerySet(self.model, using=self._db)

    def hot_questions(self):
        return self.get_queryset().add_likes().order_by('-likes_count')

    def new_questions(self):
        return self.get_queryset().add_likes().order_by('-created_at')


class Question(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок вопроса')
    text = models.TextField(verbose_name='Текст вопроса')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               verbose_name='Автор')
    tags = models.ManyToManyField(Tag, related_name='questions',
                                  verbose_name='Теги')
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Дата создания')
    updated_at = models.DateTimeField(blank=True, null=True,
                                      verbose_name='Дата обновления')

    objects = QuestionManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE,
                                 related_name='answers',
                                 verbose_name='Вопрос')
    text = models.TextField(verbose_name='Текст ответа')
    correct = models.BooleanField(default=False, verbose_name='Верный')
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Дата ответа')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               verbose_name='Автор')

    def __str__(self):
        return f'Ответ к вопросу: {self.question.title}'

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'


class QuestionLike(models.Model):
    question = models.ForeignKey(Question, related_name='likes',
                                 on_delete=models.CASCADE,
                                 verbose_name='Вопрос')
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             verbose_name='Пользователь')

    class Meta:
        unique_together = ('question', 'user')
        verbose_name = 'Лайк на вопрос'
        verbose_name_plural = 'Лайки на вопрос'


class AnswerLike(models.Model):
    answer = models.ForeignKey(Answer, related_name='likes',
                               on_delete=models.CASCADE, verbose_name='Ответ')
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             verbose_name='Пользователь')

    class Meta:
        unique_together = ('answer', 'user')
        verbose_name = 'Лайк на ответ'
        verbose_name_plural = 'Лайки на ответы'

from django import forms
from questions.models import Question, Answer, Tag


class QuestionForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.SelectMultiple(attrs={
            'class': 'form-control',
        }),
        required=True,
        label="Теги",
        help_text="Выберите теги для вашего вопроса"
    )

    class Meta:
        model = Question
        fields = ['title', 'text', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'title',
                'placeholder': 'Введите заголовок вашего вопроса',
            }),
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'id': 'description',
                'placeholder': 'Подробно опишите ваш вопрос',
                'rows': 4,
            }),
        }


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Ваш ответ...'})
        }

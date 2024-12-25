from django.urls import path

from questions import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('question/<int:pk>/', views.question_detail_view, name='question'),
    path('question/<int:pk>//answer/', views.add_answer, name='add_answer'),
    path('tag/<str:tag_name>/', views.tag_view, name='tag'),
    path('ask/', views.ask, name='ask'),
    path('hot/', views.hot_view, name='hot'),
    path('like/question/', views.like_question, name='like_question'),
    path('like/answer/', views.like_answer, name='like_answer'),
    path('mark_correct/', views.mark_correct_answer,
         name='mark_correct_answer'),
]

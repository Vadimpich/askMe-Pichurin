from django.urls import path

from questions import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('question/<int:pk>/', views.question_detail_view, name='question'),
    path('question/<int:pk>//answer/', views.add_answer, name='add_answer'),
    path('tag/<str:tag_name>/', views.tag_view, name='tag'),
    path('ask/', views.ask, name='ask'),
    path('hot/', views.hot_view, name='hot'),
]

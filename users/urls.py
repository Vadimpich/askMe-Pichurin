from django.contrib.auth.views import LogoutView
from django.urls import path
from users import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('profile/edit/', views.edit_profile_view, name='edit_profile'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
]

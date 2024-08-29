from . import views
from django.urls import path

urlpatterns = [
    path('register/',views.RegisterView.as_view()),
    path('login/', views.LoginView.as_view()),
    path('todo/',views.TodoView.as_view()),
    path('todo/<int:pk>',views.TodoDetailView.as_view()),
]

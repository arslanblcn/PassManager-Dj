from django.urls import path
from django.urls.conf import re_path
from .views import CreatePasswordView, PasswordDeleteView, PasswordDetailView, PasswordUpdateView, SavePasswordView, search_password_view

urlpatterns = [
    path('create-password/', CreatePasswordView.as_view(), name="create-password"),
    path('save-password/', SavePasswordView.as_view(), name="save-password"),
    path('update/<pk>/', PasswordUpdateView.as_view(), name="update"),
    path('delete/<pk>/', PasswordDeleteView.as_view(), name="delete"),
    path('search/', search_password_view, name="search"),
    path('<pk>/', PasswordDetailView.as_view(), name="detail")
]
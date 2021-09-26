"""passApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls.conf import include
from .views import DashboardView
from accounts.views import RegisterView, UserLoginView, UserLogoutView
from django.contrib import admin
from django.urls import path


urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name="dashboard"),
    path('register/', RegisterView.as_view(), name="register"),
    path('', UserLoginView.as_view(), name="login"),
    path('logout/', UserLogoutView.as_view(), name="logout"),
    path('', include('manager.urls')),
    path('admin/', admin.site.urls),
]

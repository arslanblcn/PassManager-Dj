from django.contrib.auth.models import User
from django.core import exceptions
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views import View
from django.views.generic import RedirectView
from .forms import UserRegisterForm, UserAuthForm

# Create your views here.

class RegisterView(View):
    #if there is a get method
    def get(self, request):
        return render(request, "accounts/register.html", {'form' : UserRegisterForm()})

    #if there is an post method then make register process
    def post(self, request):
        form = UserRegisterForm(request.POST)
        #check is form valid and then save it and redirect
        if form.is_valid():
            form.save()
            messages.success(request, f"Account was created successfully")
        return render(request, "accounts/register.html", {'form' : form})


class UserLoginView(View):
    def get(self, request):
        return render(request, "accounts/login.html",{'form' : UserAuthForm()})
    
    def post(self, request):
        form = UserAuthForm(request , data = request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            remember_me = form.cleaned_data.get('remember_me')
            user = authenticate(username = username, password = password)

            #if remember me check set expiry time to 2 weeks
            if remember_me:
                self.request.session.set_expiry(1209600)
            if user is None:
                return render(request, "accounts/login.html", {'form' : form})
            
            try:
                form.confirm_login_allowed(user)
            except exceptions.ValidationError:
                return render(request, "accounts/login.html", {'form' : form})
            login(request, user)
            return redirect("dashboard")
        else:
            messages.warning(request, f"Invalid Username or Password!")
            return render(request, "accounts/login.html", {'form' : form})

class UserLogoutView(RedirectView):
    permanent = False
    query_string = True
    pattern_name = "login"

    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            logout(self.request,)
        return super(UserLogoutView, self).get_redirect_url(*args, **kwargs)

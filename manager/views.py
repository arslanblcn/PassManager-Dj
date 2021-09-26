from django.contrib.messages.api import success
from django.db.models.query_utils import Q
from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, DeleteView
from django.contrib import messages
from .forms import GeneratePasswordForm, CreatePasswordForm
from .models import CreatePasswordModel
import random, string
from django.utils import timezone
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
# Create your views here.

class CreatePasswordView(LoginRequiredMixin, TemplateView):
    login_url = "login"
    redirect_field_name = "login"
    template_name = "manager/create-password.html"
    def get(self, request):
        return render(request, "manager/create-password.html", {'form' : GeneratePasswordForm()})
    
    def post(self, request):
        lower_letters = string.ascii_lowercase
        mixed_case = string.ascii_letters
        symbols = string.punctuation
        numbers = string.digits
        form = GeneratePasswordForm(data=request.POST)
        if form.is_valid():
            password_length = int(form.cleaned_data.get('passwordLength'))
            has_letters = form.cleaned_data.get('has_letters')
            has_mixed_case = form.cleaned_data.get('has_mixed_case')
            has_panctuation = form.cleaned_data.get('has_panctuation')
            has_numbers = form.cleaned_data.get('has_numbers')
            characters = []
            if has_mixed_case:
                characters.extend(mixed_case)
            if has_panctuation:
                characters.extend(symbols)
            if has_numbers:
                characters.extend(numbers)
            if has_letters:
                characters.extend(lower_letters)
            temp = random.choices(characters, k = password_length)
            password = ''.join(temp)
        return render(request, "manager/create-password.html", {'form' : form, 'password' : password})
        #return render(request, "manager/create-password.html", {'form' : GeneratePasswordForm()})

    
class SavePasswordView(LoginRequiredMixin, TemplateView):
    login_url = "login"
    redirect_field_name = "login"
    template_name = "manager/save-password.html"

    def get(self, request):
        context = {}
        context['form'] = CreatePasswordForm()
        return render(request, "manager/save-password.html", context = context)
    
    def post(self, request):
        context = {}
        form = CreatePasswordForm(data=request.POST)
        passwd = request.POST.get('passwd')
        context['passwd'] = passwd
        if form.is_valid():
            #get fields
            password = form.cleaned_data.get('password')
            retired_date = form.cleaned_data.get('retired_date')
            used_for_website = form.cleaned_data.get('used_for_website')
            explanation = form.cleaned_data.get('explanation')

            #Check if there is a same password
            if CreatePasswordModel.objects.filter(password = password):
                messages.warning(request, f"The password is already used on a platform")
                context['form'] = CreatePasswordForm()
            else:
                # save them into database
                obj = CreatePasswordModel.objects.create(
                    password=password, 
                    created_date = timezone.now(),
                    retired_date=retired_date, 
                    used_for_website = used_for_website, 
                    explanation = explanation)
                messages.success(request, f"New password was created succesfully. The password will be retired on")
                context['form'] = CreatePasswordForm()
                context['object'] = obj
        else:
            context['form'] = CreatePasswordForm()
        return render(request, "manager/save-password.html", context = context)

@login_required(login_url="/")
def search_password_view(request, *args, **kwargs):
    context = {}
    query = request.GET.get('q')
    if not query:
        query = ""
    pass_obj = CreatePasswordModel.objects.filter(
            Q(used_for_website__icontains = query) |
            Q(explanation__icontains = query) |
            Q(password__icontains = query)).order_by("retired_date")
    p = Paginator(pass_obj, 8)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)

    context = {
        'page_obj' : page_obj,
    }
        
    return render(request, "manager/search-password.html", context = context)


class PasswordUpdateView(LoginRequiredMixin, UpdateView):
    login_url = "login"
    redirect_field_name = "login"
    model = CreatePasswordModel
    fields = [
        "password", "used_for_website", "retired_date", "explanation"
    ]
    template_name = "manager/update-password.html"
    success_url = reverse_lazy("dashboard")
    
    def form_valid(self, form):
        messages.success(self.request, f"The record was updated!!")
        return super(PasswordUpdateView, self).form_valid(form)

class PasswordDeleteView(LoginRequiredMixin, DeleteView):
    login_url = "login"
    redirect_field_name = "login"
    model = CreatePasswordModel
    template_name = "manager/delete-password.html"
    success_url = reverse_lazy("dashboard")
    success_message =  "The record was removed successfully!"

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        data = super(PasswordDeleteView, self).delete(request, *args, **kwargs)
        messages.warning(self.request, self.success_message % obj.__dict__)
        return data
    

class PasswordDetailView(LoginRequiredMixin, DetailView):
    login_url = "login"
    redirect_field_name = "login"
    model = CreatePasswordModel
    template_name = "manager/detail-password.html"

    def get_context_data(self, *args, **kwargs):
        context = super(PasswordDetailView, self).get_context_data(*args, **kwargs)
        return context

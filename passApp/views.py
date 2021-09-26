import datetime
from typing import Dict
from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from manager.models import CreatePasswordModel
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib.auth.decorators import login_required

class DashboardView(LoginRequiredMixin ,ListView):
    model = CreatePasswordModel
    login_url = "login"
    redirect_field_name = "login"
    template_name = "dashboard-view.html"

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        qs = CreatePasswordModel.objects.all().order_by('-id')
        p = Paginator(qs , 5)
        page_number = self.request.GET.get('page')
        try:
            page_obj = p.get_page(page_number)  # returns the desired page object
        except PageNotAnInteger:
            # if page_number is not an integer then assign the first page
            page_obj = p.page(1)
        except EmptyPage:
            # if page is empty then return last page
            page_obj = p.page(p.num_pages)
        now = timezone.now()
        end_date = now + datetime.timedelta(days = 15)
        closest_date = CreatePasswordModel.objects.filter(retired_date__gte = now).order_by('retired_date').first()
        notification_qs = CreatePasswordModel.objects.filter(retired_date__range=[now, end_date])
        #print(notification_qs)
        last_item = CreatePasswordModel.objects.last()
        context = {
            'last_item' : last_item,
            'closest_date' : closest_date,
            'records' : qs.count(),
            'page_obj': page_obj,
            'notification' : notification_qs,
            'notification_record': notification_qs.count(),
        }
        return context

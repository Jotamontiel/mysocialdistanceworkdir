from django.views.generic.list import ListView
from django.shortcuts import render
from .models import ServiceVideo, ServiceImage, Service, Employer

# Create your views here.
class ServicesListView(ListView):
    model = Service
    template_name = "services/services.html"

    def get_context_data(self, **kwargs):
        context = super(ServicesListView, self).get_context_data(**kwargs)
        context['employer_list'] = Employer.objects.all()
        context['employer_amount'] = len(Employer.objects.all())
        context['hidd'] = False
        if context['employer_list']:
            context['hidd'] = True
        else:
            context['hidd'] = False

        return context
from django.views.generic.base import TemplateView
from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_sameorigin
import random

class HomePageView(TemplateView):
    template_name = "core/home.html"

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['choice_song'] = random.randrange(2)

        return context

class InfoPageView(TemplateView):
    template_name = "core/info.html"

@xframe_options_sameorigin
def cmdDisplayView(request):
    return render(request, "core/cmd_display.html")

@xframe_options_sameorigin
def city3DDisplayView(request):
    return render(request, "core/city3D_display.html")

@xframe_options_sameorigin
def timeLineDisplayView(request):
    return render(request, "core/timeline_display.html")
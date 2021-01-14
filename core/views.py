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

class HomeMenuPageView(TemplateView):
    template_name = "core/menu_home.html"

class AboutMenuPageView(TemplateView):
    template_name = "core/menu_about.html"

class ProjectsMenuPageView(TemplateView):
    template_name = "core/menu_projects.html"

@xframe_options_sameorigin
def cmdDisplayView(request):
    return render(request, "core/displays/cmd_display.html")

@xframe_options_sameorigin
def city3DDisplayView(request):
    return render(request, "core/displays/city3D_display.html")

@xframe_options_sameorigin
def timeLineDisplayView(request):
    return render(request, "core/displays/timeline_display.html")

@xframe_options_sameorigin
def techTreeDisplayView(request):
    return render(request, "core/displays/techtree_display.html")

@xframe_options_sameorigin
def selectAboutDisplayView(request):
    return render(request, "core/displays/selectabout_display.html")
from django.views.generic.base import TemplateView
from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_sameorigin
from .models import Curriculum

class HomePageView(TemplateView):
    template_name = "core/home.html"

class InfoPageView(TemplateView):
    template_name = "core/info.html"

    def get_context_data(self, **kwargs):
        context = super(InfoPageView, self).get_context_data(**kwargs)
        context['curriculum_list'] = Curriculum.objects.all()
        return context

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
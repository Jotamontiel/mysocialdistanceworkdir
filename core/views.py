from django.views.generic.base import TemplateView
from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_sameorigin

class HomePageView(TemplateView):
    template_name = "core/home.html"

@xframe_options_sameorigin
def cmdDisplayView(request):
    return render(request, "core/cmd_display.html")

@xframe_options_sameorigin
def city3DDisplayView(request):
    return render(request, "core/city3D_display.html")
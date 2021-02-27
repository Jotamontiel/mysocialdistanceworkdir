from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.urls import reverse, reverse_lazy
from django.views.generic.base import TemplateView
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .models import Component
from .forms import ComponentForm
from registration.models import Profile
from registration.forms import ProfileForm
from django import forms

# Create your views here.
@method_decorator(login_required, name='dispatch')
class IotModuleDashboardView(TemplateView):
    template_name = "iot_module/display_dashboard/iotmodule_dashboard.html"

@method_decorator(login_required, name='dispatch')
class IotModuleProfileCreateAuxView(UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = "iot_module/display_profiles/profile_aux_form.html"
    success_url = reverse_lazy('iotmodule_dashboard_display')

    def get_object(self):
        # recuperar objeto que se va editar
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        return profile

@method_decorator(login_required, name='dispatch')
class IotModuleComponentListView(ListView):
    model = Component
    template_name = "iot_module/display_components/component_list.html"
    paginate_by = 5

@method_decorator(login_required, name='dispatch')
class IotModuleComponentDetailView(DetailView):
    model = Component
    template_name = "iot_module/display_components/component_detail.html"

@method_decorator(login_required, name='dispatch')
class IotModuleComponentUpdateView(UpdateView):
    model = Component
    form_class = ComponentForm
    template_name = "iot_module/display_components/component_update_form.html"

    def get_success_url(self):
        return reverse_lazy('iotmodule_componentlist_display') + '?okEdit'

@method_decorator(login_required, name='dispatch')
class IotModuleComponentDeleteView(DeleteView):
    model = Component
    template_name = "iot_module/display_components/component_confirm_delete.html"
    
    def get_success_url(self):
        return reverse_lazy('iotmodule_componentlist_display') + '?okDelete'

@method_decorator(login_required, name='dispatch')
class IotModuleComponentCreateView(CreateView):
    model = Component
    form_class = ComponentForm
    template_name = "iot_module/display_components/component_form.html"
    success_url = reverse_lazy('iotmodule_componentlist_display')

    # Search for profile instance
    def form_valid(self, form):
        form.instance.profile = Profile.objects.get(id=self.request.user.id)
        return super(IotModuleComponentCreateView, self).form_valid(form)
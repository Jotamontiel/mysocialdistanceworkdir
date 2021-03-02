from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.urls import reverse, reverse_lazy
from django.views.generic.base import TemplateView
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Component
from .forms import ComponentForm
from registration.models import Profile
from registration.forms import ProfileForm, ProfileAdminForm, ProfileUpdateForm, UserEmailUpdateForm
from django import forms

@method_decorator(login_required, name='dispatch')
class IotModuleDashboardView(TemplateView):
    template_name = "iot_module/display_dashboard/iotmodule_dashboard.html"

##############################################################################################
########## USER VIEWS: USER EMAIL UPDATE #####################################################
##############################################################################################
@method_decorator(login_required, name='dispatch')
class IotModuleUserEmailUpdateView(UpdateView):
    form_class = UserEmailUpdateForm
    template_name = 'iot_module/display_profiles/profile_email_form.html'

    def get_object(self):
        return User.objects.get(id=self.kwargs['pk'])
    
    def get_success_url(self):
        profileid=User.objects.get(id=self.kwargs['pk']).profile.id
        profileslug=User.objects.get(id=self.kwargs['pk']).profile.nickName
        if self.kwargs['flag'] == '1':
            url_path = 'iotmodule_profileupdate_display'
        elif self.kwargs['flag'] == '2':
            url_path = 'iotmodule_profileupdateaux_display'
        else:
            url_path = 'iotmodule_profileupdateaux_display'

        return reverse_lazy(url_path, kwargs={'pk': profileid, 'slug': profileslug}) + '?okUserEmailUpdate'

    def get_form(self, form_class=None):
        form = super(IotModuleUserEmailUpdateView, self).get_form()
        # Modificar en tiempo real
        form.fields['email'].widget = forms.EmailInput(attrs={'class':'form-control mb-2', 'placeholder':'Email', 'style': 'text-transform:none'})
        return form

##############################################################################################
########## PROFILE VIEWS: LIST, DETAIL, UPDATE, DELETE, CREATE ###############################
##############################################################################################
@method_decorator(login_required, name='dispatch')
class IotModuleProfileListView(ListView):
    model = Profile
    template_name = "iot_module/display_profiles/profile_list.html"
    paginate_by = 20

@method_decorator(login_required, name='dispatch')
class IotModuleProfileDetailView(DetailView):
    model = Profile
    template_name = "iot_module/display_profiles/profile_detail.html"

@method_decorator(login_required, name='dispatch')
class IotModuleProfileUpdateView(UpdateView):
    model = Profile
    form_class = ProfileUpdateForm
    template_name = "iot_module/display_profiles/profile_update_form.html"

    def get_success_url(self):
        return reverse_lazy('iotmodule_profilelist_display') + '?okEditProfile'

@method_decorator(login_required, name='dispatch')
class IotModuleProfileUpdateAuxView(UpdateView):
    model = Profile
    form_class = ProfileUpdateForm
    template_name = "iot_module/display_profiles/profile_aux_update_form.html"

    def get_success_url(self):
        return reverse_lazy('iotmodule_profileupdateaux_display', kwargs={'pk': self.kwargs['pk'], 'slug': self.kwargs['slug']}) + '?okEditProfile'

@method_decorator(login_required, name='dispatch')
class IotModuleProfileDeleteView(DeleteView):
    model = Profile
    template_name = "iot_module/display_profiles/profile_confirm_delete.html"
    
    def get_success_url(self):
        return reverse_lazy('iotmodule_profilelist_display') + '?okDeleteProfile'

@method_decorator(login_required, name='dispatch')
class IotModuleProfileDeleteAuxView(DeleteView):
    model = Profile
    template_name = "iot_module/display_profiles/profile_aux_confirm_delete.html"
    
    def get_success_url(self):
        return reverse_lazy('iotmodule_dashboard_display') + '?okDeleteProfile'

@method_decorator(login_required, name='dispatch')
class IotModuleProfileCreateView(CreateView):
    model = Profile
    form_class = ProfileAdminForm
    template_name = "iot_module/display_profiles/profile_form.html"

    def get_success_url(self):
        return reverse_lazy('iotmodule_profilelist_display') + '?okCreateProfile'

@method_decorator(login_required, name='dispatch')
class IotModuleProfileCreateAuxView(CreateView):
    model = Profile
    form_class = ProfileForm
    template_name = "iot_module/display_profiles/profile_aux_form.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(IotModuleProfileCreateAuxView, self).form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('iotmodule_dashboard_display') + '?okCreateProfile'

##############################################################################################
########## COMPONENT VIEWS: LIST, DETAIL, UPDATE, DELETE, CREATE #############################
##############################################################################################
@method_decorator(login_required, name='dispatch')
class IotModuleComponentListView(ListView):
    model = Component
    template_name = "iot_module/display_components/component_list.html"
    paginate_by = 10

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
        return reverse_lazy('iotmodule_componentlist_display') + '?okEditComponent'

@method_decorator(login_required, name='dispatch')
class IotModuleComponentDeleteView(DeleteView):
    model = Component
    template_name = "iot_module/display_components/component_confirm_delete.html"
    
    def get_success_url(self):
        return reverse_lazy('iotmodule_componentlist_display') + '?okDeleteComponent'

@method_decorator(login_required, name='dispatch')
class IotModuleComponentCreateView(CreateView):
    model = Component
    form_class = ComponentForm
    template_name = "iot_module/display_components/component_form.html"

    # Search for profile instance
    def form_valid(self, form):
        form.instance.profile = Profile.objects.get(user__id=self.request.user.id)
        return super(IotModuleComponentCreateView, self).form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('iotmodule_componentlist_display') + '?okCreateComponent'
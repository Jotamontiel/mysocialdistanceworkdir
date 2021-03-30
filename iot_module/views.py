from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.urls import reverse, reverse_lazy
from django.views.generic.base import TemplateView
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Company, ComponentType, Component, SensorType, Sensor
from .forms import CompanyForm, CompanyUpdateForm, CompanyEmailUpdateForm, ComponentTypeForm, ComponentForm, ComponentUpdateForm, SensorTypeForm, SensorForm, SensorUpdateForm
from registration.models import Profile
from registration.forms import ProfileForm, ProfileAdminForm, ProfileUpdateForm, UserCreationFormWithEmail, UserEmailUpdateForm
from django import forms
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.core.serializers import serialize
import json

##############################################################################################
########## DASHBOARD VIEWS ###################################################################
##############################################################################################
@method_decorator(login_required, name='dispatch')
class IotModuleDashboardView(TemplateView):
    template_name = "iot_module/display_dashboard/iotmodule_dashboard.html"

    def get_context_data(self, **kwargs):
        context = super(IotModuleDashboardView, self).get_context_data(**kwargs)
        if Profile.objects.filter(user=self.request.user):
            my_user = User.objects.filter(id=self.request.user.id)
            my_profile = Profile.objects.filter(id=self.request.user.profile.id)
            my_components = Component.objects.filter(profile=self.request.user.profile).order_by('alias')
            my_sensors = Sensor.objects.filter(component__profile=self.request.user.profile)
            context["user_info"] = my_user
            context["profile_info"] = my_profile
            context["component_list"] = my_components
            context["sensor_list"] = my_sensors
            context["user_info_json"] = json.dumps(serialize('json', my_user))
            context["profile_info_json"] = json.dumps(serialize('json', my_profile))
            context["component_list_json"] = json.dumps(serialize('json', my_components))
            context["sensor_list_json"] = json.dumps(serialize('json', my_sensors))
        else:
            my_user = User.objects.filter(id=self.request.user.id)
            context["user_info"] = my_user
            context["user_info_json"] = json.dumps(serialize('json', my_user))
        return context

##############################################################################################
########## USER VIEWS: USER EMAIL UPDATE, SIGN UP ############################################
##############################################################################################
class SignUpView(CreateView):
    form_class = UserCreationFormWithEmail
    template_name = 'registration/signup.html'

    def get_success_url(self):
        return reverse_lazy('login') + '?register'

    def get_form(self, form_class=None):
        form = super(SignUpView, self).get_form()
        # Modificar en tiempo real
        form.fields['username'].widget = forms.TextInput(attrs={'class':'md-input', 'placeholder':'Username', 'style': 'text-transform:none'})
        form.fields['email'].widget = forms.EmailInput(attrs={'class':'md-input', 'placeholder':'Email', 'style': 'text-transform:none'})
        form.fields['password1'].widget = forms.PasswordInput(attrs={'class':'md-input', 'placeholder':'Password', 'style': 'text-transform:none'})
        form.fields['password2'].widget = forms.PasswordInput(attrs={'class':'md-input', 'placeholder':'Repeat Password', 'style': 'text-transform:none'})
        return form

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
    paginate_by = 10

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
########## COMPANY VIEWS: LIST, DETAIL, UPDATE, DELETE, CREATE ###############################
##############################################################################################
@method_decorator(login_required, name='dispatch')
class IotModuleCompanyEmailUpdateView(UpdateView):
    form_class = CompanyEmailUpdateForm
    template_name = 'iot_module/display_companies/company_email_form.html'

    def get_object(self):
        return Company.objects.get(id=self.kwargs['pk'])
    
    def get_success_url(self):
        return reverse_lazy('iotmodule_companyupdate_display', kwargs={'pk': self.kwargs['pk'], 'slug': self.kwargs['slug']}) + '?okCompanyEmailUpdate'

    def get_form(self, form_class=None):
        form = super(IotModuleCompanyEmailUpdateView, self).get_form()
        # Modificar en tiempo real
        form.fields['email'].widget = forms.EmailInput(attrs={'class':'form-control mb-2', 'placeholder':'Email', 'style': 'text-transform:none'})
        return form

@method_decorator(login_required, name='dispatch')
class IotModuleCompanyListView(ListView):
    model = Company
    template_name = "iot_module/display_companies/company_list.html"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(IotModuleCompanyListView, self).get_context_data(**kwargs)
        if self.request.user.is_staff:
            context['company_list'] = Company.objects.all().order_by('profile')
        else:
            context['company_list'] = Company.objects.filter(profile=self.request.user.profile)

        paginator = Paginator(list(context['company_list']), self.paginate_by)
        page_number = self.request.GET.get('page')
        try:
            page_obj = paginator.get_page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.get_page(1)
        except EmptyPage:
            page_obj = paginator.get_page(paginator.num_pages)
        context['company_list'] = page_obj
        context['page_obj'] = page_obj
        
        return context

@method_decorator(login_required, name='dispatch')
class IotModuleCompanyDetailView(DetailView):
    model = Company
    template_name = "iot_module/display_companies/company_detail.html"

@method_decorator(login_required, name='dispatch')
class IotModuleCompanyUpdateView(UpdateView):
    model = Company
    form_class = CompanyUpdateForm
    template_name = "iot_module/display_companies/company_update_form.html"

    def get_success_url(self):
        return reverse_lazy('iotmodule_companylist_display') + '?okEditCompany'

@method_decorator(login_required, name='dispatch')
class IotModuleCompanyDeleteView(DeleteView):
    model = Company
    template_name = "iot_module/display_companies/company_confirm_delete.html"
    
    def get_success_url(self):
        return reverse_lazy('iotmodule_companylist_display') + '?okDeleteCompany'

@method_decorator(login_required, name='dispatch')
class IotModuleCompanyCreateView(CreateView):
    model = Company
    form_class = CompanyForm
    template_name = "iot_module/display_companies/company_form.html"

    def form_valid(self, form):
        form.instance.profile = self.request.user.profile
        return super(IotModuleCompanyCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('iotmodule_companylist_display') + '?okCreateCompany'

##############################################################################################
########## COMPONENT TYPES VIEWS: LIST, DETAIL, UPDATE, DELETE, CREATE #######################
##############################################################################################
@method_decorator(login_required, name='dispatch')
class IotModuleComponentTypeListView(ListView):
    model = ComponentType
    template_name = "iot_module/display_component_types/component_types_list.html"
    paginate_by = 10

@method_decorator(login_required, name='dispatch')
class IotModuleComponentTypeDetailView(DetailView):
    model = ComponentType
    template_name = "iot_module/display_component_types/component_types_detail.html"

@method_decorator(login_required, name='dispatch')
class IotModuleComponentTypeUpdateView(UpdateView):
    model = ComponentType
    form_class = ComponentTypeForm
    template_name = "iot_module/display_component_types/component_types_update_form.html"

    def get_success_url(self):
        return reverse_lazy('iotmodule_componenttypeslist_display') + '?okEditComponentType'

@method_decorator(login_required, name='dispatch')
class IotModuleComponentTypeDeleteView(DeleteView):
    model = ComponentType
    template_name = "iot_module/display_component_types/component_types_confirm_delete.html"
    
    def get_success_url(self):
        return reverse_lazy('iotmodule_componenttypeslist_display') + '?okDeleteComponentType'

@method_decorator(login_required, name='dispatch')
class IotModuleComponentTypeCreateView(CreateView):
    model = ComponentType
    form_class = ComponentTypeForm
    template_name = "iot_module/display_component_types/component_types_form.html"

    def get_success_url(self):
        return reverse_lazy('iotmodule_componenttypeslist_display') + '?okCreateComponentType'

##############################################################################################
########## COMPONENT VIEWS: LIST, DETAIL, UPDATE, DELETE, CREATE #############################
##############################################################################################
@method_decorator(login_required, name='dispatch')
class IotModuleComponentListView(ListView):
    model = Component
    template_name = "iot_module/display_components/component_list.html"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(IotModuleComponentListView, self).get_context_data(**kwargs)
        if self.request.user.is_staff:
            context['component_list'] = Component.objects.all().order_by('profile')
        else:
            context['component_list'] = Component.objects.filter(profile=self.request.user.profile)

        paginator = Paginator(list(context['component_list']), self.paginate_by)
        page_number = self.request.GET.get('page')
        try:
            page_obj = paginator.get_page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.get_page(1)
        except EmptyPage:
            page_obj = paginator.get_page(paginator.num_pages)
        context['component_list'] = page_obj
        context['page_obj'] = page_obj
        
        return context

@method_decorator(login_required, name='dispatch')
class IotModuleComponentDetailView(DetailView):
    model = Component
    template_name = "iot_module/display_components/component_detail.html"

@method_decorator(login_required, name='dispatch')
class IotModuleComponentUpdateView(UpdateView):
    model = Component
    form_class = ComponentUpdateForm
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
    
    def get_success_url(self):
        return reverse_lazy('iotmodule_componentlist_display') + '?okCreateComponent'

##############################################################################################
########## SENSOR TYPES VIEWS: LIST, DETAIL, UPDATE, DELETE, CREATE ##########################
##############################################################################################
@method_decorator(login_required, name='dispatch')
class IotModuleSensorTypeListView(ListView):
    model = SensorType
    template_name = "iot_module/display_sensor_types/sensor_types_list.html"
    paginate_by = 10

@method_decorator(login_required, name='dispatch')
class IotModuleSensorTypeDetailView(DetailView):
    model = SensorType
    template_name = "iot_module/display_sensor_types/sensor_types_detail.html"

@method_decorator(login_required, name='dispatch')
class IotModuleSensorTypeUpdateView(UpdateView):
    model = SensorType
    form_class = SensorTypeForm
    template_name = "iot_module/display_sensor_types/sensor_types_update_form.html"

    def get_success_url(self):
        return reverse_lazy('iotmodule_sensortypeslist_display') + '?okEditSensorType'

@method_decorator(login_required, name='dispatch')
class IotModuleSensorTypeDeleteView(DeleteView):
    model = SensorType
    template_name = "iot_module/display_sensor_types/sensor_types_confirm_delete.html"
    
    def get_success_url(self):
        return reverse_lazy('iotmodule_sensortypeslist_display') + '?okDeleteSensorType'

@method_decorator(login_required, name='dispatch')
class IotModuleSensorTypeCreateView(CreateView):
    model = SensorType
    form_class = SensorTypeForm
    template_name = "iot_module/display_sensor_types/sensor_types_form.html"

    def get_success_url(self):
        return reverse_lazy('iotmodule_sensortypeslist_display') + '?okCreateSensorType'

##############################################################################################
########## SENSOR VIEWS: LIST, DETAIL, UPDATE, DELETE, CREATE ################################
##############################################################################################
@method_decorator(login_required, name='dispatch')
class IotModuleSensorListView(ListView):
    model = Sensor
    template_name = "iot_module/display_sensors/sensor_list.html"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(IotModuleSensorListView, self).get_context_data(**kwargs)
        if self.request.user.is_staff:
            context['sensor_list'] = Sensor.objects.all().order_by('component')
        else:
            context['sensor_list'] = Sensor.objects.filter(component__profile=self.request.user.profile)

        paginator = Paginator(list(context['sensor_list']), self.paginate_by)
        page_number = self.request.GET.get('page')
        try:
            page_obj = paginator.get_page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.get_page(1)
        except EmptyPage:
            page_obj = paginator.get_page(paginator.num_pages)
        context['sensor_list'] = page_obj
        context['page_obj'] = page_obj
        
        return context

@method_decorator(login_required, name='dispatch')
class IotModuleSensorDetailView(DetailView):
    model = Sensor
    template_name = "iot_module/display_sensors/sensor_detail.html"

@method_decorator(login_required, name='dispatch')
class IotModuleSensorUpdateView(UpdateView):
    model = Sensor
    form_class = SensorUpdateForm
    template_name = "iot_module/display_sensors/sensor_update_form.html"

    def get_success_url(self):
        return reverse_lazy('iotmodule_sensorlist_display') + '?okEditSensor'

@method_decorator(login_required, name='dispatch')
class IotModuleSensorDeleteView(DeleteView):
    model = Sensor
    template_name = "iot_module/display_sensors/sensor_confirm_delete.html"
    
    def get_success_url(self):
        return reverse_lazy('iotmodule_sensorlist_display') + '?okDeleteSensor'

@method_decorator(login_required, name='dispatch')
class IotModuleSensorCreateView(CreateView):
    model = Sensor
    form_class = SensorForm
    template_name = "iot_module/display_sensors/sensor_form.html"
    
    def get_success_url(self):
        return reverse_lazy('iotmodule_sensorlist_display') + '?okCreateSensor'
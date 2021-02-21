from django.db import models
from registration.models import Profile

# Create your models here.
class Company(models.Model):
    businessName = models.CharField(verbose_name="Business Name", max_length=500, null=False, blank=False)
    rut = models.CharField(verbose_name="Rut", max_length=50, null=False, blank=False, unique=True)
    logoLink = models.ImageField(verbose_name="Logo (400x300 px)", upload_to="iot_module/companies", blank=True)
    street =  models.CharField(verbose_name="Street", max_length=200, null=True, blank=True)
    number = models.CharField(verbose_name="Number", max_length=100, null=True, blank=True)
    office = models.CharField(verbose_name="Office", max_length=200, null=True, blank=True)
    city = models.CharField(verbose_name="City", max_length=200, null=False, blank=False)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    postalCode = models.CharField(verbose_name="Postal Code", max_length=200, null=True, blank=True)
    phone = models.CharField(verbose_name="Phone", max_length=200, null=True, blank=True)
    email = models.EmailField(verbose_name="Email", max_length=300, null=True, blank=True, unique=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Creation Date")
    updated = models.DateTimeField(auto_now=True, verbose_name="Update Date")

    class Meta:
        verbose_name = "company"
        verbose_name_plural = "companies"
        ordering = ['businessName']

    def __str__(self):
        return self.businessName

class ComponentType(models.Model):
    name = models.CharField(verbose_name="Component Type Name", max_length=300, null=False, blank=False)
    initials = models.CharField(verbose_name="Component Type Initials", max_length=200, null=False, blank=False)
    description = models.TextField(verbose_name="Component Type Description", null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Creation Date")
    updated = models.DateTimeField(auto_now=True, verbose_name="Update Date")

    class Meta:
        verbose_name = "component type"
        verbose_name_plural = "component types"
        ordering = ['name']

    def __str__(self):
        return self.name

class Component(models.Model):
    alias = models.CharField(verbose_name="Component Alias", max_length=200, null=False, blank=False)
    serialCode = models.CharField(verbose_name="Component Serial Code", max_length=500, null=False, blank=False)
    description = models.TextField(verbose_name="Component Description", null=True, blank=True)
    imeiRecord = models.CharField(verbose_name="Component IMEI Record", max_length=300, null=True, blank=True)
    componentType = models.ForeignKey(ComponentType, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    connectionType = models.CharField(verbose_name="Component Connection Type", max_length=300, null=True, blank=True)
    supplyType = models.CharField(verbose_name="Component Supply Type", max_length=300, null=True, blank=True)
    latitude = models.FloatField(verbose_name="Component Latitude", null=True, blank=True)
    longitude = models.FloatField(verbose_name="Component Longitude", null=True, blank=True)
    isEnabled = models.BooleanField(verbose_name="Component Status", default=False, null=False, blank=False)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Creation Date")
    updated = models.DateTimeField(auto_now=True, verbose_name="Update Date")

    class Meta:
        verbose_name = "component"
        verbose_name_plural = "components"
        ordering = ['alias']

    def __str__(self):
        return self.alias

class SensorType(models.Model):
    name = models.CharField(verbose_name="Sensor Type Name", max_length=300, null=False, blank=False)
    initials = models.CharField(verbose_name="Sensor Type Initials", max_length=200, null=False, blank=False)
    measurementUnit = models.CharField(verbose_name="Sensor Type Measurement Unit", max_length=100, null=True, blank=True)
    description = models.TextField(verbose_name="Sensor Type Description", null=True, blank=True)
    isGraphical = models.BooleanField(verbose_name="Is Graphical", default=False, null=False, blank=False)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Creation Date")
    updated = models.DateTimeField(auto_now=True, verbose_name="Update Date")

    class Meta:
        verbose_name = "sensor type"
        verbose_name_plural = "sensor types"
        ordering = ['name']

    def __str__(self):
        return self.name

class Sensor(models.Model):
    alias = models.CharField(verbose_name="Sensor Alias", max_length=200, null=False, blank=False)
    serialCode = models.CharField(verbose_name="Sensor Serial Code", max_length=500, null=False, blank=False)
    measurementUnit = models.CharField(verbose_name="Sensor Measurement Unit", max_length=100, null=True, blank=True)
    description = models.TextField(verbose_name="Sensor Description", null=True, blank=True)
    sensorType = models.ForeignKey(SensorType, on_delete=models.CASCADE)
    component = models.ForeignKey(Component, on_delete=models.CASCADE)
    brand = models.CharField(verbose_name="Sensor Brand", max_length=200, null=True, blank=True)
    isEnabled = models.BooleanField(verbose_name="Sensor Status", default=False, null=False, blank=False)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Creation Date")
    updated = models.DateTimeField(auto_now=True, verbose_name="Update Date")

    class Meta:
        verbose_name = "sensor"
        verbose_name_plural = "sensors"
        ordering = ['alias']

    def __str__(self):
        return self.alias

class SensorData(models.Model):
    value = models.CharField(verbose_name="Sensor Data Value", max_length=100, null=True, blank=True)
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Creation Date")
    updated = models.DateTimeField(auto_now=True, verbose_name="Update Date")

    class Meta:
        verbose_name = "sensor data"
        verbose_name_plural = "sensor data"
        ordering = ['id']
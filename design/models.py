import os
from django.conf import settings
from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator, FileExtensionValidator
from models.Main_HEPU import main

# Functions
def makehours():
    hours = []
    for i in range(24):
        hours.append(("{}:00".format(i),"{}:00".format(i)))
    return hours

def custom_upload_to(instance,filename):
    if Design.objects.filter(pk=instance.pk).exists():
        old_instance = Design.objects.get(pk=instance.pk)
        if os.path.isfile(old_instance.o_s_gen.path):
            os.remove(old_instance.o_s_gen.path)
    return '{0}/{1}/{2}'.format(instance.user.username,instance.project_name,filename)

# quitar luego
def custom_image_upload_to(instance,filename):
    if Results.objects.filter(pk=instance.pk).exists():
        old_instance = Results.objects.get(pk=instance.pk)
        old_instance.image1.delete()
        old_instance.image2.delete()
        old_instance.image3.delete()
    return 'results/{0}/{1}-{2}/{3}'.format(instance.design.user.username,instance.design.pk,instance.design.project_name,filename)

# Models
class Design(models.Model):
    # Variables
    hours = makehours()
    energy_input = [
        ('PPA','PPA'),
        ('On-site', 'User-defined generation vector'),
    ]
    if_ppa = [
        ('24/7','24/7'),
        ('Custom','Customized'),
    ]
    if_onsite = [
        ('TMY','TMY'),
        ('TMY_SAM','TMY_SAM'),
        ('TMY_PVsol','TMY_PVsol'),
        ('PVSyst','PVSyst'),
    ]
    electrolyzer_choices = [
        ('PEM','PEM'),
        ('ALK','ALK'),
        ('SOEC','SOEC'),
    ]
    water_type_choices = [
        ('Tap','Tap Water'),
        ('demi','Deionized-demi Water'),
    ]
    message = "Value must be on range between 1 and 100"

    # Atributes
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    # General
    project_name = models.CharField(verbose_name="Project name", max_length=30, default="Project")
    location = models.CharField(verbose_name="Location", max_length=30)
    cod = models.IntegerField(verbose_name="Start of production", default=2025, validators=[MinValueValidator(limit_value=2000, message="Value must be greater than 2000")])
    horizon = models.IntegerField(verbose_name="Years of operation", default=20, validators=[MinValueValidator(limit_value=1, message="Value must be greater than 1")])
    # Energy supply
    op_type = models.CharField(verbose_name="Energy input", max_length=30, choices=energy_input, default="PPA")
    #   If ppa
    ppa_type = models.CharField(verbose_name="PPA type", max_length=30, choices=if_ppa, default="24/7", blank=True)
    nom_power = models.IntegerField(verbose_name="PPA nominal power [MW]", default=10, blank=True, validators=[MinValueValidator(limit_value=1, message="Value must be greater than 1")])
    #   If customized
    customized_from = models.CharField(verbose_name="From", max_length=5, choices=hours, default="8:00", blank=True)
    customized_to = models.CharField(verbose_name="To", max_length=5, choices=hours, default="18:00", blank=True)
    #   If on-site generation
    file_type = models.CharField(verbose_name="Type", max_length=20, choices=if_onsite, default="TMY", blank=True)
    o_s_gen = models.FileField(verbose_name="Input File", upload_to=custom_upload_to, null=True, blank=True, validators=[FileExtensionValidator(allowed_extensions=['csv'], message="Only csv files are allowed")])
    # Electrolysis
    elec_type = models.CharField(verbose_name="Electrolyzer type", max_length=30, choices=electrolyzer_choices, default="PEM")
    elec_size = models.IntegerField(verbose_name="Electrolyzer nominal power [MW]", default=10, validators=[MinValueValidator(limit_value=1, message="Value must be greater than 1")])
    eff_replacement = models.FloatField(verbose_name="Min. electrolyzer efficiency before replacement [%]", default=80, validators=[MinValueValidator(limit_value=0, message="Value must be greater than 0")])
    water_type = models.CharField(verbose_name="Water supply", max_length=30, choices=water_type_choices, default="tap")
    sp_footprint = models.IntegerField(verbose_name="System footprint [m²/MW]", default=600, validators=[MinValueValidator(limit_value=1, message="Value must be greater than 1")])
    # CAPEX
    elec_cost = models.FloatField(verbose_name="Specific Electrolyzer and BoP cost [USD/kW]", default=1200, validators=[MinValueValidator(limit_value=1, message="Value must be greater than 1")])
    develop_cost = models.FloatField(verbose_name="Specific Development cost [USD/kW]", validators=[MinValueValidator(limit_value=1, message="Value must be greater than 1")])
    installation_cost = models.FloatField(verbose_name="Installation cost [USD/kW]", default=180 ,validators=[MinValueValidator(limit_value=1, message="Value must be greater than 1")])
    indirect_cost = models.FloatField(verbose_name="Indirect costs [USD/project]",default=1000000, validators=[MinValueValidator(limit_value=1, message="Value must be greater than 1")])
    land_cost = models.FloatField(verbose_name="Land cost [USD/ha/year]", validators=[MinValueValidator(limit_value=0, message="Value must be gratter than 0")], default=6000)
    # OPEX 
    energy_cost = models.FloatField(verbose_name="Energy cost [USD/MWh]", default=50, validators=[MinValueValidator(limit_value=1, message="Value must be greater than 1")])
    om = models.FloatField(verbose_name="O&M [USD/kW/year]", validators=[MinValueValidator(limit_value=0, message="Value must be gratter than 0")], default=50)
    water_cost = models.FloatField(verbose_name="Water cost [USD/m3]", default=3, validators=[MinValueValidator(limit_value=1, message="Value must be greater than 1")])
    # Finance
    equity_discount_rate = models.FloatField(verbose_name="Equity discount rate [%]", validators=[MinValueValidator(limit_value=0, message="Value must be greater than 0"),MaxValueValidator(limit_value=100, message="Value must be lower than 100")], default=12)
    debt = models.FloatField(verbose_name="Debt [%]", validators=[MinValueValidator(limit_value=0, message="Value must be greater than 0"),MaxValueValidator(limit_value=100, message="Value must be lower than 100")], default=60)
    debt_term = models.IntegerField(verbose_name="Debt term [years]", default=0)
    interest_rate = models.FloatField(verbose_name="Interest Rate [%]", validators=[MinValueValidator(limit_value=0, message="Value must be greater than 0"),MaxValueValidator(limit_value=100, message="Value must be lower than 100")], default=6)
    first_category_tax = models.FloatField(verbose_name="First category Tax [%]", validators=[MinValueValidator(limit_value=0, message="Value must be greater than 0"),MaxValueValidator(limit_value=100, message="Value must be lower than 100")], default=25)
    # Metadata
    created = models.DateTimeField(verbose_name="Creation date", auto_now_add=True)
    updated = models.DateTimeField(verbose_name="Update date", auto_now=True)
    
    class Meta:
        verbose_name = "design"
        verbose_name_plural = "designs"
        ordering = ["-created"]

    def __str__(self):
        return self.project_name

class Results(models.Model):
    # Design data
    design = models.OneToOneField(to=Design,on_delete=models.CASCADE)
    # Technical results
    hydrogen_production = models.FloatField(verbose_name="Hydrogen production [tons/year]", default=0.0)
    oxigen_production = models.FloatField(verbose_name="Oxigen production [tons/year]", default=0.0)
    energy_consumption = models.FloatField(verbose_name="Energy consumption [GWh/year]", default=0.0)
    load_factor = models.FloatField(verbose_name="Electrolyzer load factor [%]", default=0.0)
    average_energy_consumption = models.FloatField(verbose_name="Average energy consumption [kWh/kgH2]", default=0.0)
    water_consumption = models.FloatField(verbose_name="Water consumption Y1 [m3/year]", default=0.0)
    curtailed_energy = models.FloatField(verbose_name="Energy curtailed [GWh/year]", default=0.0)
    energy_cost = models.FloatField(verbose_name="Energy cost [USD/year]", default=0.0)
    water_cost = models.FloatField(verbose_name="Water cost [USD/year]", default=0.0)
    # Economic results
    total_capex = models.FloatField(verbose_name="Total CAPEX [USD]", default=0.0)
    nvp_energy_cost = models.FloatField(verbose_name="Present Cost of energy for life cycle [USD]", default=0.0)
    nvp_om = models.FloatField(verbose_name="Present Cost of O&M for life cycle [USD]", default=0.0)
    nvp_water = models.FloatField(verbose_name="Present Cost of water for life cycle [USD]", default=0.0)
    nvp_land = models.FloatField(verbose_name="Present Cost of land for life cycle [USD]", default=0.0)
    present_stack_replacements = models.FloatField(verbose_name="Present cost of stack replacements [USD]", default=0.0)
    present_total_cost = models.FloatField(verbose_name="Total present cost for life cycle [USD]", default=0.0)
    stack_replacements = models.IntegerField(verbose_name="Stack replacements", default=0)
    year_of_replacements = models.TextField(verbose_name="Year of replacements", default="0")
    wacc = models.FloatField(verbose_name="WACC", default=0.0)
    lcoh = models.FloatField(verbose_name="LCOH [USD/kgH2]", default=0.0)
    # Images Data
    monthly_plot_data = models.TextField(verbose_name="monthly_plot_data", null=True, blank=True)
    energy_plot_data = models.TextField(verbose_name="energy_plot_data", null=True, blank=True)
    yearly_plot_data = models.TextField(verbose_name="yearly_plot_data", null=True, blank=True)
    lcoh_data = models.TextField(verbose_name="LCOH_data", null=True, blank=True)
    # Download Data
    h2_annual = models.TextField(verbose_name="H2 Annual", null=True, blank=True)
    water_consumption_data = models.TextField(verbose_name="Water Consumption", null=True, blank=True)
    npc_data = models.TextField(verbose_name="Project annual costs", null=True, blank=True)
    lcoh_down_data = models.TextField(verbose_name="LCOH Data", null=True, blank=True)
    capex_breakdown = models.TextField(verbose_name="Capex Breakdown data", null=True, blank=True)
    capex_tot = models.FloatField(verbose_name="Total capex", null=True, blank=True)
    opex_breakdown = models.TextField(verbose_name="Opex Breakdown data", null=True, blank=True)
    opex_tot = models.FloatField(verbose_name="Total capex", null=True, blank=True)
    # # Metadata
    created = models.DateTimeField(verbose_name="Creation date", auto_now_add=True)
    updated = models.DateTimeField(verbose_name="Update date", auto_now=True)
    
    class Meta:
        verbose_name = "result"
        ordering = ["-created"]

    def __str__(self):
        return "{0} - results".format(self.design.project_name)

# Triggers
@receiver(models.signals.post_delete, sender=Design)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.o_s_gen:
        if os.path.isfile(instance.o_s_gen.path):
            os.remove(instance.o_s_gen.path)

@receiver(models.signals.post_save, sender=Design)
def fill_results(sender, instance, **kwargs):
    data = main(instance)
    obj, created = Results.objects.update_or_create(design=instance,defaults=data)
    if settings.DEBUG:
        if created:
            print("Creado")
        else:
            print("Actualizado")
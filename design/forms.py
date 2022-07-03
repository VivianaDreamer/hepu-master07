from django import forms
from .models import Design

class DesignForm(forms.ModelForm):
    class Meta:
        model = Design
        fields = [
            'project_name', 
            'location', 
            'cod', 
            'horizon', 
            'op_type',
            'ppa_type',
            'nom_power',
            'customized_from',
            'customized_to',
            'file_type',
            'o_s_gen',
            'elec_type',
            'elec_size',
            'eff_replacement',
            'water_type',
            'sp_footprint',
            'elec_cost',
            'develop_cost',
            'installation_cost',
            'indirect_cost',
            'land_cost',
            'energy_cost',
            'om',
            'water_cost',
            'equity_discount_rate',
            'debt',
            'debt_term',
            'interest_rate',
            'first_category_tax',
        ]
        widgets = {
            'project_name':forms.TextInput(attrs={'class':'form-control'}), 
            'location':forms.TextInput(attrs={'class':'form-control'}), 
            'cod':forms.NumberInput(attrs={'class':'form-control'}), 
            'horizon':forms.NumberInput(attrs={'class':'form-control','id':'horizon'}), 
            'op_type':forms.RadioSelect(attrs={'class':'custom-radio','id':'op_type'}),
            'ppa_type':forms.Select(attrs={'class':'form-control', 'id':'ppa_type'}),
            'nom_power':forms.NumberInput(attrs={'class':'form-control'}),
            'customized_from':forms.Select(attrs={'class':'form-control'}),
            'customized_to':forms.Select(attrs={'class':'form-control'}),
            'file_type':forms.Select(attrs={'class':'form-control'}),
            'o_s_gen':forms.FileInput(attrs={'class':'form-control', 'accept':'.csv', 'value':'Upload'}),
            'elec_type':forms.Select(attrs={'class':'form-control', 'id':'elec_type'}),
            'elec_size':forms.NumberInput(attrs={'class':'form-control', 'id':'elec_size'}),
            'eff_replacement':forms.NumberInput(attrs={'class':'form-control'}),
            'water_type':forms.Select(attrs={'class':'form-control'}),
            'sp_footprint':forms.NumberInput(attrs={'class':'form-control'}),
            'elec_cost':forms.NumberInput(attrs={"class":"form-control",'id':'elect'}),
            'develop_cost':forms.NumberInput(attrs={"class":"form-control",'id':'develop'}),
            'installation_cost':forms.NumberInput(attrs={"class":"form-control",'id':'instalation'}),
            'indirect_cost':forms.NumberInput(attrs={"class":"form-control",'id':'indirect'}),
            'land_cost':forms.NumberInput(attrs={'class':'form-control'}),
            'energy_cost':forms.NumberInput(attrs={'class':'form-control'}),
            'om':forms.NumberInput(attrs={'class':'form-control'}),
            'water_cost':forms.NumberInput(attrs={"class":"form-control"}),
            'equity_discount_rate':forms.NumberInput(attrs={'class':'form-control'}),
            'debt':forms.NumberInput(attrs={'class':'form-control'}),
            'debt_term':forms.NumberInput(attrs={'class':'form-control','id':'debt_term'}),
            'interest_rate':forms.NumberInput(attrs={'class':'form-control'}),
            'first_category_tax':forms.NumberInput(attrs={'class':'form-control'})
        }
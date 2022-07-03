from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView, View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ViewDoesNotExist

from models.Main_HEPU import deg_outputs_h2hourly, energy_input_download, cost_data

from .downloads import render_dict_to_csv, render_dataframe_to_csv, render_dataframe_to_excel, render_dict_to_excel, render_to_csv, render_to_excel, render_to_pdf
from .CreatePDF import render_pdf
from .models import Design
from .forms import DesignForm

@method_decorator(login_required(login_url="/login/"), name='dispatch')
class ResumeResultsPdf(View):
    def get(self, request, *args, **kwargs):
        object = Design.objects.get(pk=kwargs['pk'])
        if object.user != request.user:
            raise ViewDoesNotExist()
        return render_pdf(object)

@method_decorator(login_required(login_url="/login/"), name='dispatch')
class DesignListView(ListView):
    model = Design

    def get_queryset(self):
        return Design.objects.filter(user=self.request.user)

@method_decorator(login_required(login_url="/login/"), name='dispatch')
class DesignDetailView(DetailView):
    model = Design

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.user != self.request.user:
            raise ViewDoesNotExist()
        return obj

@method_decorator(login_required(login_url="/login/"), name='dispatch')
class DesignCreate(CreateView):
    model = Design
    form_class = DesignForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('design:detail', kwargs={'pk':self.object.pk})

    def get_form_kwargs(self, *args, **kwargs):
        return super(DesignCreate,self).get_form_kwargs(*args, **kwargs)

@method_decorator(login_required(login_url="/login/"), name='dispatch')
class DesignUpdate(UpdateView):
    model = Design
    form_class = DesignForm
    template_name_suffix = '_update_form'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.user == self.request.user:
            return obj
        raise ViewDoesNotExist()

    def get_success_url(self):
        return reverse('design:detail', kwargs={'pk':self.object.pk})

    def get_form_kwargs(self, *args, **kwargs):
        return super(DesignUpdate,self).get_form_kwargs(*args, **kwargs)

@method_decorator(login_required(login_url="/login/"), name='dispatch')
class DesignDelete(DeleteView):
    model = Design
    success_url = reverse_lazy('design:results')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.user == self.request.user:
            return obj
        raise ViewDoesNotExist()

@method_decorator(login_required(login_url="/login/"), name='dispatch')
class H2annualDownload(View):
    def get(self, request, *args, **kwargs):
        object = Design.objects.get(pk=kwargs['pk'])
        if object.user != request.user:
            raise ViewDoesNotExist()
        data = eval(object.results.h2_annual)[0]
        if kwargs['type'] == 'csv':
            return render_to_csv(data=data,filename="h2_annual.csv")
        elif kwargs['type'] == 'excel':
            return render_to_excel(data=data,filename="h2_annual.xlsx")
        else:
            raise ViewDoesNotExist()

@method_decorator(login_required(login_url="/login/"), name='dispatch')
class H2hourlyDownload(View):
    def get(self, request, *args, **kwargs):
        object = Design.objects.get(pk=kwargs['pk'])
        if object.user != request.user:
            raise ViewDoesNotExist()
        h2_hourly = deg_outputs_h2hourly(object)
        if kwargs['type'] == 'csv':
            return render_dataframe_to_csv(data=h2_hourly,filename="h2_hourly.csv")
        elif kwargs['type'] == 'excel':
            return render_dataframe_to_excel(data=h2_hourly,filename="h2_hourly.xlsx")
        else:
            raise ViewDoesNotExist()

@method_decorator(login_required(login_url="/login/"), name='dispatch')
class energyInputDownload(View):
    def get(self, request, *args, **kwargs):
        object = Design.objects.get(pk=kwargs['pk'])
        if object.user != request.user:
            raise ViewDoesNotExist()
        energy_input = energy_input_download(object)
        if kwargs['type'] == 'csv':
            return render_dataframe_to_csv(data=energy_input,filename="energy_input.csv")
        elif kwargs['type'] == 'excel':
            return render_dataframe_to_excel(data=energy_input,filename="energy_input.xlsx")
        else:
            raise ViewDoesNotExist()

@method_decorator(login_required(login_url="/login/"), name='dispatch')
class waterAnnualDownload(View):
    def get(self, request, *args, **kwargs):
        object = Design.objects.get(pk=kwargs['pk'])
        if object.user != request.user:
            raise ViewDoesNotExist()
        data = eval(object.results.water_consumption_data)[0]
        if kwargs['type'] == 'csv':
            return render_to_csv(data=data,filename="water_annual.csv")
        elif kwargs['type'] == 'excel':
            return render_to_excel(data=data,filename="water_annual.xlsx")
        else:
            raise ViewDoesNotExist()

@method_decorator(login_required(login_url="/login/"), name='dispatch')
class pacDownload(View):
    def get(self, request, *args, **kwargs):
        object = Design.objects.get(pk=kwargs['pk'])
        if object.user != request.user:
            raise ViewDoesNotExist()
        data = cost_data(object)
        if kwargs['type'] == 'csv':
            return render_dataframe_to_csv(data=data,filename="pac.csv")
        elif kwargs['type'] == 'excel':
            return render_dataframe_to_excel(data=data,filename="pac.xlsx")
        else:
            raise ViewDoesNotExist()

@method_decorator(login_required(login_url="/login/"), name='dispatch')
class lcohDownload(View):
    def get(self, request, *args, **kwargs):
        object = Design.objects.get(pk=kwargs['pk'])
        if object.user != request.user:
            raise ViewDoesNotExist()
        data = eval(object.results.lcoh_down_data)
        if kwargs['type'] == 'csv':
            return render_dict_to_csv(data=data,filename="lcoh.csv")
        elif kwargs['type'] == 'excel':
            return render_dict_to_excel(data=data,filename="lcoh.xlsx")
        else:
            raise ViewDoesNotExist()
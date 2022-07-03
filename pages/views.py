from django.views.generic.list import ListView
from .models import Pages, Patch

# Create your views here.
class TermsListView(ListView):
    model = Pages
    template_name = "pages/terms.html"

    def get_context_data(self, **kwargs):
        context = super(TermsListView,self).get_context_data(**kwargs)
        context['pages'] = Pages.objects.all()
        context['patch'] = Patch.objects.all()
        return context
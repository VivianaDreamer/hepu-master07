from django.urls import path
from .views import TermsListView

pages_patterns = ([
    path('', TermsListView.as_view(), name="terms"),
],'pages')
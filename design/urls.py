from django.urls import path
from .views import DesignCreate, DesignListView, DesignDetailView, DesignUpdate, DesignDelete, ResumeResultsPdf, H2annualDownload, H2hourlyDownload, energyInputDownload, waterAnnualDownload, pacDownload, lcohDownload

design_patterns = ([
    path("results/", DesignListView.as_view(), name="results"),
    path("results/<int:pk>/",DesignDetailView.as_view(), name="detail"),
    path("resume/<int:pk>/",ResumeResultsPdf.as_view(), name="resume"),
    path("h2annual/<int:pk>/<slug:type>/",H2annualDownload.as_view(),name="h2_annual_download"),
    path("h2hourly/<int:pk>/<slug:type>/",H2hourlyDownload.as_view(),name="h2_hourly_download"),
    path("energyinput/<int:pk>/<slug:type>/",energyInputDownload.as_view(),name="energy_input_download"),
    path("waterannual/<int:pk>/<slug:type>/",waterAnnualDownload.as_view(),name="water_annual_download"),
    path("pac/<int:pk>/<slug:type>/",pacDownload.as_view(),name="pac_download"),
    path("lcoh/<int:pk>/<slug:type>/",lcohDownload.as_view(),name="lcoh_down_data"),
    path("new/", DesignCreate.as_view() , name="create"),
    path("update/<int:pk>/",DesignUpdate.as_view(),name="update"),
    path("delete/<int:pk>/",DesignDelete.as_view(),name="delete"),
],'design')
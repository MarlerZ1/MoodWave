from django.contrib import admin
from django.urls import path, include

from charts.views import ChartsView

app_name = "charts"

urlpatterns = [
    path('chart_list/', ChartsView.as_view(), name="chart_list"),
]

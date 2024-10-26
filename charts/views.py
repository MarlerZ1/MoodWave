from django.shortcuts import render
from django.views.generic import TemplateView


# Create your views here.

class ChartsView(TemplateView):
    template_name = 'charts/chart_list.html'
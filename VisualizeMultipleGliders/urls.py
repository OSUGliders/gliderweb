from django.urls import path
from .views import glider_map_view, plot_glider_data, glider_data_to_display, home_page, people, projects,data_products, deployments,documentation, statistics, publications

urlpatterns = [
     path('', home_page, name='home_page'), 
     path('map/', glider_map_view, name='glider_map'),
     path('plots/', plot_glider_data, name='plots'),
     path('gliderdata/',glider_data_to_display, name='glider_data_to_display'),
     path('people/', people, name='people'),
     path('projects/', projects, name='projects'),
     path('deployments/', deployments, name='deployments'),
     path('data-products/', data_products, name='data_products'),
     path('documentation/', documentation, name='documentation'),
     path('statistics/', statistics, name='statistics'),
     path('publications/', publications, name='publications'),
]
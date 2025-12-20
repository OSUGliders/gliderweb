from django.urls import path
from .views import glider_map_view, plot_glider_data, glider_data_to_display,home_page

urlpatterns = [
     path('', home_page, name='home_page'), 
     path('map/', glider_map_view, name='glider_map'),
     path('plots/', plot_glider_data, name='plots'),
     path('gliderdata/',glider_data_to_display, name='glider_data_to_display'),
     
]
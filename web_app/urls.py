from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home_url'),
    path('about', views.about, name='about_url'),
    path('run', views.run, name='run_url'),
    path('real_time', views.real_time, name='real_time_url')
]

from django.urls import path
from tgenerator import views

app_name = 'tgenerator'

urlpatterns = [
    path('', views.home, name='home'),
    path('<str:lang>', views.changelanguage, name='changelanguage')
]

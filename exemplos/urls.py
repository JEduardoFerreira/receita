#from django.contrib import admin
from django.urls import path, include
from . import views
import receita


urlpatterns = [
    #path('admin/', admin.site.urls),
    path('', views.index),
    path('consulta_cnpj', views.consulta_cnpj),
    path('consulta_cpf', views.consulta_cpf),
    path('', include('receita.urls')),
]

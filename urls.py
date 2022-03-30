from django.urls import path
#import receita.views as views
from . import views

urlpatterns = [
    path('obter_captcha_cnpj', views.obter_captcha_cnpj, name='obter_captcha_cnpj'),
    path('consultar_cnpj_sefaz', views.consultar_cnpj_sefaz, name='consultar_cnpj_sefaz'),
    path('obter_captcha_cpf', views.obter_captcha_cpf, name='obter_captcha_cpf'),
    path('consultar_cpf_sefaz', views.consultar_cpf_sefaz, name='consultar_cpf_sefaz'),
]

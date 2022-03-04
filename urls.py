from django.urls import path
import receita.views as views

urlpatterns = [
    path('obter_captcha_cnpj', views.obter_captcha_cnpj, name='obter_captcha_cnpj'),
    path('consultar_cnpj_sefaz', views.consultar_cnpj_sefaz, name='consultar_cnpj_sefaz'),
]

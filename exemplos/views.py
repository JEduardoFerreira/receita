from django.shortcuts import render

def index(request):
    return render(request, 'html/demo.html', context={})

def consulta_cnpj(request):
    return render(request, 'html/consulta_cnpj.html', context={})

def consulta_cpf(request):
    return render(request, 'html/consulta_cpf.html', context={})
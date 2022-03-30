import simplejson, re
from receita.situacao.cnpj import cnpj
from receita.situacao.cpf import cpf
from django.http import HttpResponse
from django.views.decorators.gzip import gzip_page
from django.views.decorators.http import require_http_methods


@gzip_page
@require_http_methods(['GET'])
def obter_captcha_cnpj(request):
    try:
        _request, _session = cnpj.init_session()        
        validate_captcha = "#".join(_request.cookies.get_dict().popitem())
        #validate_captcha = "#".join(_request.headers['Set-Cookie'].split(';')[0].split('='))
        status, msg, captcha = cnpj.get_cnpj_image_captcha(_session)
        _session.close() #http.client only
        
        return HttpResponse(
            simplejson.dumps({
                'status': status, 
                'msg': msg, 
                'hash': captcha, 
                'session': validate_captcha,
            })
        )
    except:
        return HttpResponse(
            simplejson.dumps({
                'status': '500', 
                'msg': 'Erro Interno do Servidor.', 
                'hash': '', 
                'session': '',
            })
        )


@gzip_page
@require_http_methods(['GET'])
def consultar_cnpj_sefaz(request):
    try:
        cnpj_info = re.sub("(\.|\/|-)", "", request.GET['cnpj'])
        captcha_info = request.GET['captcha']
        validate_captcha = request.GET['session_key']

        response = cnpj.validate_cnpj_sefaz(validate_captcha, captcha_info, cnpj_info)

        return HttpResponse(simplejson.dumps(response))
    except:
        return HttpResponse(
            simplejson.dumps({
                'status': '500', 
                'msg': 'Erro Interno do Servidor.', 
            })
        )


@gzip_page
@require_http_methods(['GET'])
def obter_captcha_cpf(request):
    try:
        _request, _session = cpf.init_session()

        #validate_captcha = "#".join(_request.cookies.get_dict().popitem())
        validate_captcha = "#".join(_request.headers['Set-Cookie'].split(';')[0].split('='))
        #print(_request.headers.get('Set-Cookie'))
        #_request.headers['Set-Cookie']
        status, msg, captcha = cpf.get_cpf_image_captcha(_session)
        
        return HttpResponse(
            simplejson.dumps({
                'status': status, 
                'msg': msg, 
                'hash': captcha, 
                'session': validate_captcha,
            })
        )
    except:
        return HttpResponse(
            simplejson.dumps({
                'status': '500', 
                'msg': 'Erro Interno do Servidor.', 
                'hash': '', 
                'session': '',
            })
        )


@gzip_page
@require_http_methods(['GET'])
def consultar_cpf_sefaz(request):
    try:
        cnpj_info = re.sub("(\.|\/|-)", "", request.GET['cnpj'])
        captcha_info = request.GET['captcha']
        validate_captcha = request.GET['session_key']

        response = cnpj.validate_cnpj_sefaz(validate_captcha, captcha_info, cnpj_info)

        return HttpResponse(simplejson.dumps(response))
    except:
        return HttpResponse(
            simplejson.dumps({
                'status': '500', 
                'msg': 'Erro Interno do Servidor.', 
            })
        )
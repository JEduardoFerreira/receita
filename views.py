import simplejson, re
from receita.situacao.cnpj import cnpj
from django.http import HttpResponse
from django.views.decorators.gzip import gzip_page
from django.views.decorators.http import require_http_methods


@gzip_page
@require_http_methods(['GET'])
def obter_captcha_cnpj(request):
    try:
        _request, _session = cnpj.init_session()
        validate_captcha = "#".join(_request.cookies.get_dict().popitem())
        status, msg, captcha = cnpj.get_cnpj_image_captcha(_session)
        
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
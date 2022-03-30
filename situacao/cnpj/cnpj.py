from receita.settings import URL_BASE_CNPJ, URL_SOLICITACAO_CNPJ, URL_CAPTCHA_CNPJ, URL_VALIDA_CNPJ
from receita.situacao.cnpj.crawler import dadosEmpresa
from receita.situacao.cnpj.error import dadosErro
import requests, base64, re, http.client


def init_session(ssl=True, timeout=30):
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:97.0) Gecko/20072614 Firefox/97.0'}
    ###### Início Implementação requests ######
    _session = requests.Session()
    _request = _session.get(url=URL_SOLICITACAO_CNPJ, headers=headers)
    return _request, _session
    ###### Fim Implementação requests ######

    ###### Início Implementação urllib3 ######
    # import urllib3
    # _session = urllib3.PoolManager()
    # _request = _session.request('GET', URL_SOLICITACAO_CNPJ)
    # _content = _request.data

    # return _request, _session
    ###### Fim Implementação urllib3 ######

    ###### Início Implementação http.client ######
    # if not ssl:
    #     url = URL_SOLICITACAO_CNPJ.replace("https://", "http://")
    # else:
    #     url = URL_SOLICITACAO_CNPJ
        
    # protocolo, servidor, porta, caminho = separar_endereco(url)

    # if protocolo == 'https' and ssl == True:
    #     _session = http.client.HTTPSConnection(servidor, porta, timeout = timeout)
    # else:
    #     _session = http.client.HTTPConnection(servidor, porta, timeout = timeout)
    
    # _session.request('GET', caminho)    
    # _request = _session.getresponse()
    # _content = _request.read()

    # return _request, _session
    ###### Fim Implementação http.client ######


def get_cnpj_image_captcha(session):
    try:
        ###### Início Implementação requests ######
        request_captcha = session.get(url=URL_CAPTCHA_CNPJ, stream=True, timeout=15)
        status = request_captcha.status_code
        msg = request_captcha.reason
        captcha = request_captcha.raw.read()
        if status == 200:
            captcha = base64.b64encode(captcha)

        return status, msg, captcha
        ###### Fim Implementação requests ######

        ###### Início Implementação http.client ######
        # session.request('GET', separar_endereco(URL_CAPTCHA_CNPJ)[3])
        # request_captcha = session.getresponse()
        # status = request_captcha.status
        # msg = request_captcha.reason
        # captcha = request_captcha.read()
        
        # if status == 200:
        #     captcha = base64.b64encode(captcha)

        # return status, msg, captcha
        ###### Fim Implementação http.client ######
        
        ###### Início Implementação urllib3 ######
        # _request = session.request('GET', URL_CAPTCHA_CNPJ)

        # status = _request.status
        # msg = _request.reason
        # captcha = _request.data
        
        # if status == 200:
        #     captcha = base64.b64encode(captcha)

        # return status, msg, captcha
        ###### Fim Implementação urllib3 ######
    except Exception as e:
        erro = str(e)
        if "timed out" in erro:
            return '408', 'Sefaz não respondeu no tempo esperado!', ''
        else:
            return '500', 'Erro Interno', ''


def validate_cnpj_sefaz(validate_captcha, captcha, cnpj):
    ###### Início Implementação requests ######
    _request, _session = init_session()
    _session.cookies.set("flag","1")
    name, value = validate_captcha.split("#")
    _session.cookies.set(name, value)
    data = {
        "origem":"comprovante",
        "cnpj": re.sub("(\.|\/|-)", "", cnpj),
        "txtTexto_captcha_serpro_gov_br": captcha,
        "submit1":"Consultar",
        "search_type": "cnpj"
    }
    request = _session.post(url=URL_VALIDA_CNPJ, data=data)
    html = request.text

    if request.url.endswith("Cnpjreva_Comprovante.asp"):
        return {
            'status': '200',
            'dados': dadosEmpresa(html).json()
        }
    else:
        return {
            'status': '400',
            'dados': dadosErro(html, URL_BASE_CNPJ).json()
        }
    ###### Fim Implementação requests ######

    ###### Início Implementação http.client - Não Funciona ######
    # session_key = f'{name}={value}; flag=1;'
    # headers = {
    #     "Content-type": "application/x-www-form-urlencoded", 
    #     'Accept-Encoding': 'gzip, deflate', 
    #     'Accept': '*/*', 
    #     'Connection': 'keep-alive', 
    #     'Cookie': session_key,
    # }

    # params = {
    #     "@origem": "comprovante", 
    #     "@cnpj": re.sub("(\.|\/|-)", "", cnpj),
    #     "@txtTexto_captcha_serpro_gov_br": captcha, 
    #     "@submit1": "Consultar", 
    #     "@search_type": "cnpj", 
    # }

    # _request, _session = init_session(ssl=False)
    # _session.request("POST", separar_endereco(URL_VALIDA_CNPJ)[3], params, headers)
    # _request = _session.getresponse()
    # _context = _request.read()
    # _session.close()
    ###### Fim Implementação http.client ######

    ###### Início Implementação urllib3 - Não Funciona ######
    # import urllib3
    # from urllib.parse import urlencode
    # name, value = validate_captcha.split("#")    
    # session_key = f'{name}={value}; flag=1;'
    # encoded_data = urlencode({
    #     "origem": "comprovante", 
    #     "cnpj": re.sub("(\.|\/|-)", "", cnpj),
    #     "txtTexto_captcha_serpro_gov_br": captcha, 
    #     "submit1": "Consultar", 
    #     "search_type": "cnpj"
    # })
    # _session = urllib3.PoolManager()
    # request = _session.request('GET', URL_SOLICITACAO_CNPJ)
    # _content = request.data
    # new_cookie = request.getheader('Set-Cookie')
    # new_cookie = f'{name}={value}{new_cookie[new_cookie.index(";"):len(new_cookie)]}'
    # encoded_url = URL_VALIDA_CNPJ + '?' + encoded_data
    # request = _session.request(
    #     'POST', 
    #     #URL_VALIDA_CNPJ, 
    #     encoded_url, 
    #     fields={
    #         "origem": "comprovante", 
    #         "cnpj": re.sub("(\.|\/|-)", "", cnpj),
    #         "txtTexto_captcha_serpro_gov_br": captcha, 
    #         "submit1": "Consultar", 
    #         "search_type": "cnpj"
    #     }, 
    #     headers={
    #     'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:97.0) Gecko/20072614 Firefox/97.0',
    #     'Cookie': new_cookie
    #     #'Cookie': session_key
    #     }
    # )
    # html = request.data
    ###### Fim Implementação urllib3 ######


def separar_endereco(endereco, porta = -1, protocolo = ''):
    if '://' in endereco[:15]:
        protocolo, resto = endereco.split('://', 1)
    else:
        resto = endereco
    protocolo = protocolo.lower()

    if '/' in resto:
        serv_port, resto = resto.split('/', 1)
        caminho = '/' + resto
    else:
        serv_port = resto
        caminho = '/'

    if ':' in serv_port:
        servidor, porta = serv_port.split(':', 1)
    else:
        servidor = serv_port

    if not protocolo:
        protocolo = 'https' if porta == 443 else 'http'
    elif protocolo not in ('http', 'https'):
        raise Exception('Protocolo "%s" inválido!' % protocolo)

    if porta == -1:
        porta = 443 if protocolo == 'https' else 80
    if not isinstance(porta, int) or 1 > porta > 65535:
        raise Exception('Porta "%s" inválida!' % str(porta))

    return protocolo, servidor, porta, caminho
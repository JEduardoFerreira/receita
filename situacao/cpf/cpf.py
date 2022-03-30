from receita.settings import URL_BASE_CPF, URL_SOLICITACAO_CPF, URL_CAPTCHA_CPF, URL_VALIDA_CPF
from receita.situacao.cpf.crawler import dadosEmpresa
from receita.situacao.cpf.error import dadosErro
import requests, base64, re
import http as conexao

def init_session():
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:97.0) Gecko/20072614 Firefox/97.0'}
    timeout = 60
    protocolo, servidor, porta, caminho = separar_endereco(URL_SOLICITACAO_CPF)
    if protocolo == 'https':
        _session = conexao.client.HTTPSConnection(servidor, porta, timeout = timeout)
    else:
        _session = conexao.client.HTTPConnection(servidor, porta, timeout = timeout)
    _session.protocolo = protocolo
    _session.servidor = servidor
    _session.porta = porta
    _session.caminho = caminho
    _session.timeout = timeout
    _session.cabecalhos = headers
    _session.cabecalhos['Host'] = _session.servidor
    _session.cookies = {}
    _session.request("GET", "/")
    _request = _session.getresponse()

    return _request, _session


def get_cpf_image_captcha(session):
    #try:
    session.request('GET', URL_CAPTCHA_CPF) 
    request_captcha = session.getresponse()
    status = request_captcha.status
    msg = request_captcha.reason
    captcha = request_captcha.read()
    if status == 200:
        captcha = base64.b64encode(captcha)

    return status, msg, captcha    
    # except Exception as e:
    #     erro = str(e)
    #     if "timed out" in erro:
    #         return '408', 'Sefaz não respondeu no tempo esperado!', ''
    #     else:
    #         return '500', 'Erro Interno', ''
    
    


def validate_cpf_sefaz(validate_captcha, captcha, cnpj):
    _request, _session = init_session()
    _session.cookies.set("flag","1")
    name, value = validate_captcha.split("#")
    _session.cookies.set(name, value)
    data = {"origem":"comprovante",
            "cnpj": re.sub("(\.|\/|-)", "", cnpj),
            "txtTexto_captcha_serpro_gov_br": captcha,
            "submit1":"Consultar",
            "search_type": "cnpj"}
    request = _session.post(url=URL_VALIDA_CPF, data=data)
    html = request.text

    if request.url.endswith("Cnpjreva_Comprovante.asp"):
        return {
            'status': '200',
            'dados': dadosEmpresa(html).json()
        }
    else:
        return {
            'status': '400',
            'dados': dadosErro(html, URL_BASE_CPF).json()
        }


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
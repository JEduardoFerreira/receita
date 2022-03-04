from receita.settings import URL_BASE, URL_SOLICITACAO, URL_CAPTCHA, URL_VALIDA
from receita.situacao.cnpj.crawler import dadosEmpresa
from receita.situacao.cnpj.error import dadosErro
import requests, base64, re


def init_session():
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:97.0) Gecko/20072614 Firefox/97.0'}
    _session = requests.Session()
    _request = _session.get(url=URL_SOLICITACAO, headers=headers)
    return _request, _session


def get_cnpj_image_captcha(session):
    try:
        request_captcha = session.get(url=URL_CAPTCHA, stream=True, timeout=15)
        status = request_captcha.status_code
        msg = request_captcha.reason
        captcha = request_captcha.raw.read()
        if status == 200:
            captcha = base64.b64encode(captcha)

        return status, msg, captcha    
    except Exception as e:
        erro = str(e)
        if "timed out" in erro:
            return '408', 'Sefaz não respondeu no tempo esperado!', ''
        else:
            return '500', 'Erro Interno', ''
    
    


def validate_cnpj_sefaz(validate_captcha, captcha, cnpj):
    _request, _session = init_session()
    _session.cookies.set("flag","1")
    name, value = validate_captcha.split("#")
    _session.cookies.set(name, value)
    data = {"origem":"comprovante",
            "cnpj": re.sub("(\.|\/|-)", "", cnpj),
            "txtTexto_captcha_serpro_gov_br": captcha,
            "submit1":"Consultar",
            "search_type": "cnpj"}
    request = _session.post(url=URL_VALIDA, data=data)
    html = request.text

    if request.url.endswith("Cnpjreva_Comprovante.asp"):
        return {
            'status': '200',
            'dados': dadosEmpresa(html).json()
        }
    else:
        return {
            'status': '400',
            'dados': dadosErro(html, URL_BASE).json()
        }
        
    
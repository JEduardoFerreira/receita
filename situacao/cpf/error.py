from bs4 import BeautifulSoup
import re


class dadosErro:
    def __init__(self, html, URL_BASE):
        self.url_base = URL_BASE
        self._soup = BeautifulSoup(html, "html.parser")
        self._dados_erro = self._soup.find(id="msgTxtErroCaptcha")

    @property
    def msg_erro(self):
        dados = self._dados_erro.b
        return dados.get_text().strip()
    
    @property
    def ajuda_erro(self):
        dados = self._dados_erro.a
        dados["href"] = f'{self.url_base}{dados["href"]}'
        dados["target"] = 'new_blank'
        dados.string = 'Possíveis Causas.'
        return  str(dados)
    
    def json(self):
        return {info: getattr(self, info) for info in dir(self)
                if not re.match("^(_|json)", info)}
from bs4 import BeautifulSoup
import re

class dadosEmpresa:
    def __init__(self, html):
        self._soup = BeautifulSoup(html, "html.parser")
        self._soup.find(id="principal")
        table_principal = self._soup.find("table")
        self._dados_empresa = table_principal.findChild("tr").findChild("td").findAll("table")

    @property
    def numero_inscricao(self):
        dados = self._dados_empresa[1].findAll("font", limit=5)[0:2]
        return (dados[0].get_text().strip(), dados[1].get_text().strip())
    
    @property
    def data_de_abertura(self):
        dados = self._dados_empresa[1].findAll("font", limit=5)[3:5]
        return (dados[0].get_text().strip(), dados[1].get_text().strip())

    @property
    def razao_social(self):
        dados = self._dados_empresa[2].findAll("font", limit=2)
        return (dados[0].get_text().strip(), dados[1].get_text().strip())

    @property
    def nome_fantasia(self):
        dados = self._dados_empresa[3].findAll("font", limit=4)[0:2]
        return (dados[0].get_text().strip(), dados[1].get_text().strip())

    @property
    def porte(self):
        dados = self._dados_empresa[3].findAll("font", limit=4)[2:4]
        return (dados[0].get_text().strip(), dados[1].get_text().strip())
    
    @property
    def atividade_economica_principal(self):
        dados = self._dados_empresa[4].findAll("font", limit=2)
        return (dados[0].get_text().strip(), dados[1].get_text().strip())
    
    @property
    def atividades_economicas_secundarias(self):
        dados = self._dados_empresa[5].findAll("font")
        atividades = []
        if len(dados) > 1:
            dados[1] = dados[1:len(dados)]
            for dado in dados[1]:
                atividades.append(dado.get_text().strip())
            dados[1] = atividades

        return (dados[0].get_text().strip(), dados[1])

    @property
    def natureza_juridica(self):
        dados = self._dados_empresa[6].findAll("font", limit=2)
        return (dados[0].get_text().strip(), dados[1].get_text().strip())
    
    @property
    def logradouro(self):
        dados = self._dados_empresa[7].findAll("font", limit=6)[0:2]
        return (dados[0].get_text().strip(), dados[1].get_text().strip())

    @property
    def numero(self):
        dados = self._dados_empresa[7].findAll("font", limit=6)[2:4]
        return (dados[0].get_text().strip(), dados[1].get_text().strip())

    @property
    def complemento(self):
        dados = self._dados_empresa[7].findAll("font", limit=6)[4:6]
        return (dados[0].get_text().strip(), dados[1].get_text().strip())

    @property
    def cep(self):
        dados = self._dados_empresa[8].findAll("font", limit=8)[0:2]
        return (dados[0].get_text().strip(), dados[1].get_text().strip())

    @property
    def bairro(self):
        dados = self._dados_empresa[8].findAll("font", limit=8)[2:4]
        return (dados[0].get_text().strip(), dados[1].get_text().strip())

    @property
    def municipio(self):
        dados = self._dados_empresa[8].findAll("font", limit=8)[4:6]
        return (dados[0].get_text().strip(), dados[1].get_text().strip())

    @property
    def uf(self):
        dados = self._dados_empresa[8].findAll("font", limit=8)[6:8]
        return (dados[0].get_text().strip(), dados[1].get_text().strip())
    
    @property
    def email(self):
        dados = self._dados_empresa[9].findAll("font", limit=4)[0:2]
        return (dados[0].get_text().strip(), dados[1].get_text().strip())
    
    @property
    def telefone(self):
        dados = self._dados_empresa[9].findAll("font", limit=4)[2:4]
        return (dados[0].get_text().strip(), dados[1].get_text().strip())

    @property
    def efr(self):
        dados = self._dados_empresa[10].findAll("font", limit=2)
        return (dados[0].get_text().strip(), dados[1].get_text().strip())
    
    @property
    def situacao_cadastral(self):
        dados = self._dados_empresa[11].findAll("font", limit=4)[0:2]
        return (dados[0].get_text().strip(), dados[1].get_text().strip())
    
    @property
    def data_situacao_cadastral(self):
        dados = self._dados_empresa[11].findAll("font", limit=4)[2:4]
        return (dados[0].get_text().strip(), dados[1].get_text().strip())
    
    @property
    def motivo_situacao_cadastral(self):
        dados = self._dados_empresa[12].findAll("font", limit=2)
        return (dados[0].get_text().strip(), dados[1].get_text().strip())
    
    @property
    def situacao_especial(self):
        dados = self._dados_empresa[11].findAll("font", limit=4)[0:2]
        return (dados[0].get_text().strip(), dados[1].get_text().strip())
    
    @property
    def data_situacao_especial(self):
        dados = self._dados_empresa[11].findAll("font", limit=4)[2:4]
        return (dados[0].get_text().strip(), dados[1].get_text().strip())

    def json(self):
        return {info: getattr(self, info) for info in dir(self)
                if not re.match("^(_|json)", info)}
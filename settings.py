# -*- coding: utf-8 -*-

# URL Base da Pagina de Consulta CNPJ da Receita Federal.
URL_BASE = 'http://servicos.receita.fazenda.gov.br/Servicos/cnpjreva/'

# URL da Pagina de Consulta CNPJ da Receita Federal.
URL_SOLICITACAO = f'{URL_BASE}Cnpjreva_Solicitacao_CS.asp'

# URL para Geração do Captcha da Consulta CNPJ da Receita Federal.
URL_CAPTCHA = f'{URL_BASE}captcha/gerarCaptcha.asp'

# URL de Validação da Consulta CNPJ da Receita Federal.
URL_VALIDA = f'{URL_BASE}valida.asp'
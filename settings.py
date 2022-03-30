# -*- coding: utf-8 -*-

# URL Base da Pagina de Serviços da Receita Federal.
URL_BASE = 'servicos.receita.fazenda.gov.br/Servicos/'

# URL Base dos Serviços de Consulta CNPJ.
URL_BASE_CNPJ = f'http://{URL_BASE}cnpjreva/'

# URL da Pagina de Consulta CNPJ.
URL_SOLICITACAO_CNPJ = f'{URL_BASE_CNPJ}Cnpjreva_Solicitacao_CS.asp'

# URL para Geração do Captcha da Consulta CNPJ.
URL_CAPTCHA_CNPJ = f'{URL_BASE_CNPJ}captcha/gerarCaptcha.asp'

# URL de Validação da Consulta CNPJ.
URL_VALIDA_CNPJ = f'{URL_BASE_CNPJ}valida.asp'



# URL Base dos Serviços de Consulta CPF.
URL_BASE_CPF = f'https://{URL_BASE}CPF/'

# URL da Pagina de Consulta CPF.
URL_SOLICITACAO_CPF = f'{URL_BASE_CPF}ConsultaSituacao/ConsultaPublicaSonoro.asp'

# URL para Geração do Captcha da Consulta CPF.
URL_CAPTCHA_CPF = f'{URL_BASE_CPF}captcha/gerarCaptcha.asp'

# URL de Validação da Consulta CPF.
URL_VALIDA_CPF = f'{URL_BASE_CPF}valida.asp'

# 'ConsultaPublicaExibir.asp'
if (document.getElementById('consultar_cnpj') !== null){
    document.getElementById('cnpj').focus();
    document.getElementById('consultar_cnpj').onclick = function(event){
        event.preventDefault();
        let cnpj = document.getElementById('cnpj').value;
        if (cnpj != ('', undefined) && isCNPJ(cnpj)){
            consultarCnpj(cnpj);
        }
    }
}

if (document.getElementById('consultar_cpf') !== null){
    document.getElementById('cpf').focus();
    document.getElementById('consultar_cpf').onclick = function(event){
        event.preventDefault();
        let cpf = document.getElementById('cpf').value;
        if (cpf != ('', undefined) && isCPF(cpf)){
            consultarCpf(cpf);
        }
    }
}
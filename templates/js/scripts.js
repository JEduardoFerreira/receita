const masks = {'cpf': '999.999.999-99', 'cnpj': '99.999.999/9999-99'}
const erCNPJ = /[0-9]{2}\.?[0-9]{3}\.?[0-9]{3}\/?[0-9]{4}\-?[0-9]{2}/;
const erCPF = /[0-9]{3}\.?[0-9]{3}\.?[0-9]{3}\-?[0-9]{2}/;
const erPont = /\W/igm; // Somente Pontuações/Simbolos.
let hash_ima;
let session_key;
let callback_request;
let recaptcha;


function consultarCnpj(cnpj, callback){
    callback_request = callback;
    if (document.querySelector('*[modal-receita]') == null){
        construirModal(cnpj);
    }
    recarregarCaptcha();
}

function construirModal(cnpj){
    let html = `
        <div id="fundo_modal" modal-receita>
            <div id="container_modal">
                <div class="container_campos">
                    <input type="text" id="texto_cnpj" name="texto_cnpj" mask="cnpj" placeholder=" " value="${applyMask(cnpj, "cnpj")}"/>
                    <span>CNPJ informado</span>
                </div>
                <div id="container_captcha">
                    <img id="imagem_captcha"/>
                </div>
                <div class="container_campos">
                    <input id="texto_captcha" name="texto_captcha" type="text" placeholder=" "/>
                    <span>Forneça os caracteres da imagem acima</span>
                </div>
                <div id="container_mensagens">
                    <span id="request_status"></span>
                </div>
                <div id="container_controles">
                    <button type="button" id="bt_ok_captcha">
                        Confirmar
                    </button>
                    <button type="button" id="bt_recarregar_captcha">
                        Recarregar
                    </button>
                    <button type="button" id="bt_cancel_captcha">
                        Voltar
                    </button>
                </div>
            </div>
        </div>`;
        document.querySelector('body').innerHTML += html;
}

function exibirResultadoConsulta(dados){
    let html = '';
    html += '<div id="fundo_modal_resultado" modal-receita>';
    html += '    <button id="fechar_modal_resultado"><i>x</i></button>';
    html += '    <div id="container_modal">';
    html += '        <ul id="lista_dados_empresa">';
    for (d in dados){
        html += '<li>';
        html += `   <h6 class="">${dados[d][0]}</h6>`;
        if (typeof(dados[d][1]) === 'object'){
            let itens = dados[d][1];
            for (i in itens){
                html += `   <p class="">${itens[i]}</p>`;
            }
        }else{
            html += `   <p class="">${dados[d][1]}</p>`;
        }
        html += '</li>';
    }
    html += '        </ul>';
    html += '    </div>';
    html += '</div>';
    document.querySelector('body').innerHTML += html;
}

function recarregarCaptcha(){
    obterCaptcha();
    clearTimeout(recaptcha);
    recaptcha = setTimeout(()=>{recarregarCaptcha();}, 60000); //timeout 1 minuto.
    document.getElementById('texto_captcha').value = '';
    document.getElementById('texto_captcha').focus();
}

function obterCaptcha(){
    $.ajax({
        type: "GET",
        data: {},
        url: "/obter_captcha_cnpj",
        async: false,
        dataType: "json",
        success: function(result){
            if (result.status == '200'){
                hash_ima  = result.hash;
                session_key = result.session;
                let captchaUrl = gerarURI(hash_ima);
                document.querySelector('#imagem_captcha').src = captchaUrl;
            }else{
                document.getElementById('request_status').innerText = `${result.status} - ${result.msg}`;
            }
        },
        error: function(result){
            document.getElementById('request_status').innerText = `${result.status} - ${result.msg}`;
        }
    });
}

function enviarConsulta(cnpj, captcha){
    let cnpjSemMascara = cnpj.replace(erPont, '');
    let cnpj_valido = verificarCnpj(cnpjSemMascara);
    if(cnpj_valido && captcha != ""){
        $.ajax({
            type: "GET",
            data: {
                cnpj: cnpj, 
                captcha: captcha, 
                session_key: session_key,
            }, 
            url: "/consultar_cnpj_sefaz",
            async: false,
            dataType: "json",
            success: function(result){
                if (result.status === '200'){
                    clearTimeout(recaptcha);
                    document.getElementById('fundo_modal').remove();
                    if (callback_request !== (undefined, null) && typeof callback_request === 'function'){
                        callback_request.call(this, result.dados);
                    }else{
                        exibirResultadoConsulta(result.dados);
                    }
                }else if (result.status === '400'){
                    document.getElementById('request_status').innerHTML= `${result.dados.msg_erro} - ${result.dados.ajuda_erro}`;
                    document.getElementById('texto_captcha').focus();
                }else{
                    recarregarCaptcha();
                    document.getElementById('request_status').innerText = `${result.status} - ${result.msg}`;
                }
            }
        });
    }else{
        if (!cnpj_valido){
            document.getElementById('request_status').innerText = 'CNPJ inválido!'
        }else if(captcha == ''){
            document.getElementById('request_status').innerText = 'Capctha não foi informado!'
        }
        document.getElementById('texto_captcha').focus();
    }
}

function gerarURI(base64str, type='jpg'){
    // decode base64 string, remove space for IE compatibility
    var binary = atob(base64str.replace(/\s/g, ''));
    var len = binary.length;
    var buffer = new ArrayBuffer(len);
    var view = new Uint8Array(buffer);
    for (var i = 0; i < len; i++) {
        view[i] = binary.charCodeAt(i);
    }
    // create the blob object with content-type "application/pdf"               
    var blob = new Blob( [view], { type: type });
    var url = URL.createObjectURL(blob);
    return url;
}

function isCNPJ(value){
    if (!value) return false;
    erCNPJ.lastIndex = 0;
    return erCNPJ.test(value);
}

function isCPF(value){
    if (!value) return false;
    erCPF.lastIndex = 0;
    return erCPF.test(value);
}

function verificarCnpj(cnpj){
    var numeros, digitos, soma, i, resultado, pos, tamanho, digitos_iguais;
    digitos_iguais = 1;
    if (cnpj.length < 14 && cnpj.length < 15)
        return false;
    if(cnpj != "00000000000000"){
        for (i = 0; i < cnpj.length - 1; i++){
            if (cnpj.charAt(i) != cnpj.charAt(i + 1)){
                digitos_iguais = 0;
                break;
            }
        }
        if (!digitos_iguais){
            tamanho = cnpj.length - 2
            numeros = cnpj.substring(0,tamanho);
            digitos = cnpj.substring(tamanho);
            soma = 0;
            pos = tamanho - 7;
            for (i = tamanho; i >= 1; i--){
                soma += numeros.charAt(tamanho - i) * pos--;
                if (pos < 2)
                    pos = 9;
            }
            resultado = soma % 11 < 2 ? 0 : 11 - soma % 11;
            if (resultado != digitos.charAt(0))
                return false;
            tamanho = tamanho + 1;
            numeros = cnpj.substring(0,tamanho);
            soma = 0;
            pos = tamanho - 7;
            for (i = tamanho; i >= 1; i--){
                soma += numeros.charAt(tamanho - i) * pos--;
                if (pos < 2)
                    pos = 9;
            }
            resultado = soma % 11 < 2 ? 0 : 11 - soma % 11;
            if (resultado != digitos.charAt(1))
                return false;
            return true;
        }else{
            return false;
        }
    }else{
        return true;
    }
}

$('body').on('click', '#bt_ok_captcha, #bt_recarregar_captcha, #bt_cancel_captcha, #fechar_modal_resultado', function(event){
    event.preventDefault();
    if (this.id == 'bt_ok_captcha'){
        enviarConsulta(document.getElementById('texto_cnpj').value, document.getElementById('texto_captcha').value);
    }else if (this.id == 'bt_recarregar_captcha'){
        recarregarCaptcha();
    }else if (this.id == 'bt_cancel_captcha'){
        clearTimeout(recaptcha);
        document.getElementById('fundo_modal').remove();
    } if(this.id == 'fechar_modal_resultado'){
        document.getElementById('fundo_modal_resultado').remove();
    }
});

$("body").on("keydown", "#texto_captcha", function(event){
    let tecla = ( window.event ) ? event.keyCode : event.which;
    if (tecla == 13 || tecla == 9){
        document.getElementById('bt_ok_captcha').click();
    }
});

$("body").on("keypress", "input[mask]", (event)=>{
    let type  = $(this).attr("mask");
    let tecla = ( window.event ) ? event.keyCode : event.which;
    let v = String.fromCharCode(tecla);
    if (type == 'string'){
        var er = /[^a-z\u00C0-\u00FF]/ig; // (A-Z).
    }else{
        var er = /[^0-9]/ig; // Somente (0-9).
    }
    if ((v.match(er) != null) && (tecla != 8 ) && (tecla != 0)){
        event.preventDefault(event);
    }
});

$("body").on("keyup", "input[mask]", function(event){
    let tecla = ( window.event ) ? event.keyCode : event.which;
    let string  = $(this).val();
    if (tecla == 13 || tecla == 9){
        return;
    }
    if ((tecla != 16) && (tecla < 37 || tecla > 40)){
        let len = $(this).attr("maxlength");
        if (tecla == 8 && string.length < len-1){
            return;
        }else{
            evalueMask(this);
        }
    }
});

function evalueMask(obj, tecla){
    var type    = $(obj).attr("mask"); // Tipo de mascara que sera aplicada.
    var posCur  = obj.selectionStart + 1; // Captura Posição do cursor no Objeto.
    var string  = $(obj).val(); // texto atual do campo.
    var mascara = ""; // Mascara que será aplicada.
    var tamanho = 0; // Tamanho máximo do campo.
    if (string != ''){
       // Define Tamanho do campo
       if (type == "cpf/cnpj" || type == "cpf" || type == "cnpj"){
            if (type == "cpf" || type == "cnpj"){
                tamanho = masks[type].length;
            }else{
                if (string.length <= 14){ //CPF Formatado ou CNPJ sem Mascára.
                    if ((string.length == 14) && (string.match(/[^0-9]/ig) == null)){ // CNPJ
                        type = 'cnpj';
                    }else{ // CPF
                        type = 'cpf';
                    }
                }else{ // CNPJ
                    type = 'cnpj';
                }
                tamanho = masks[type].length+1;
            }
        }else{
            if (type != "string"){
                tamanho = masks[type].length;
            }
        }
        if (type == "string"){ // Texto.
            $(obj).removeAttr("maxlength");
            return;
        }
        $(obj).attr("maxlength", tamanho);
        $(obj).val(applyMask(string, type, tecla));
        if (posCur <= string.length ){posCur--}else{
            if ($(obj).val().length > posCur){posCur++;}
        }
        obj.selectionStart = posCur;
        obj.selectionEnd = posCur;
    }
}

function applyMask(string, type, tecla=undefined){
    let pattern = masks[type];
    let txt = string.replace(/\W/g, '');
    let opc1 = pattern.replace(/[?]/g, '9');
    let opc2 = pattern.replace(/[?]/g, '');
    let mascara = [];
    let cont = 0;
    let resp = '';

    if (opc2 && string.match(/[0-9a-z]/ig) != null){
        if (string.match(/[0-9a-z]/ig).length <= opc2.match(/[9]/ig).length){
            newPattern = opc2;
        }else{
            newPattern = opc1;
        }
    }else{
        newPattern = opc1;
    }    
    for (i=0; i < newPattern.length; i++){
        if (newPattern[i] != '9'){
            mascara[i] = newPattern[i];
        }else{
            mascara[i] = ' ';
        }
    }
    
    for (i=0; i < mascara.length; i++){
        if (mascara[i] == ' '){
            if (txt[cont]){
                mascara[i] = txt[cont];
            }else{
                mascara[i] = ' ';
            }
            cont++;
        }
    }
    
    for (i=0; i < mascara.length; i++){
        if (mascara[i] == ' '){break;}
        resp += mascara[i];
    }
    //resp = resp.replace("!", " ");
    resp = resp.replace(/[!]/g, ' ');
    return resp;
}
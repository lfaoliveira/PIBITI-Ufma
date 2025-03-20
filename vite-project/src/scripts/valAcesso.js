class Validator{
    constructor(){
        this.regexEspaco= /[\s]+/;
        this.emailRegex = /^[\w]+@[\w]+\.[\w]+$/;
        this.senhaRegex = /[]/;
        this.nomeRegex = /[]/;
        this.crmRegex = /[]/;

    }
    login(email=String,senha=String) {
        //TODO: INSERIR LOGICA DE CONSULTA AO BANCO DE DADOS

    }
    cadastro(email=String, senha=String, nome=String, crm=String, checks=Boolean){
        email = email.replace(this.regexEspaco);
        if(!this.emailRegex.test(strEmail)){
            return ["Insira um email válido!", null];
        }
        if(!this.senhaRegex.test(senha)){
            //TODO: Aqui tem que  ter bullet list com campos de senha
            return ["adaddawdadwdwadwd", null];
        }
        if(!this.nomeRegex.test(nome)){
        return ["Nome contem números!", null];
        }
        if(!this.crmRegex.test(crm)){
            return ["Insira um CRM válido!", null];
        }

    }
}


export default Validator;
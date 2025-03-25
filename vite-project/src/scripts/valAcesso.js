/**
 * Class responsible for handling validation logic for user authentication and registration
 * @class Validator
 * @description Validates user credentials and registration information using regex patterns
 */
class Validator{
    constructor(){

    }

    /**
     * Validates user login credentials
     * @param {string} email - User's email address
     * @param {string} senha - User's password
     * @returns {void}
     */
    login(email=String,senha=String) {
        //TODO: INSERIR LOGICA DE CONSULTA AO BANCO DE DADOS
    }

    /**
     * Validates and processes user registration information
     * @param {string} email - User's email address
     * @param {string} senha - User's password
     * @param {string} nome - User's name
     * @param {string} crm - User's CRM (Medical Registration Number)
     * @returns {Array} Array containing [error message, null] if validation fails
     */
    cadastro(email=String, senha=String, nome=String, crm=String){
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
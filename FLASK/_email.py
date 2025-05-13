from bs4 import BeautifulSoup
from flask_mail import Mail, Message
from typing import Literal

SOURCE_HTML = "FLASK\\assets\\template-email.html"
# TODO: MUDAR TITULO DO APLICATIVO!!!!!!!!!!!!!
TITULO_APP = "<<TITULO DO APP>>"


class MailHandler:
    def __init__(self, flask_mail):
        self.mailer = flask_mail

    def format_html(self, class_value_mapper: dict):
        with open(SOURCE_HTML, 'r', encoding='utf-8') as file:
            html_content = file.read()
        parser = BeautifulSoup(html_content, 'html.parser')
        # substitui valores no HTML
        for classe, valor in class_value_mapper.items():
            elements = parser.find_all(class_=classe)
            for element in elements:
                if element.name.lower() == "img":
                    element['src'] = valor
                    continue
                # Remove existing content.
                element.clear()
                element.append(str(valor))
        # Return the modified HTML as a string.
        return str(parser)

    def enviar_email_usuario(self, tipo: Literal['recuperar', 'cadastroOK', 'cadastroInvalido']):

        texto1 = ""
        texto2 = ""
        texto_botao = ""

        if tipo == 'recuperar':
            texto1 = "Clique no link abaixo para recuperar sua senha."
            texto2 = "Se não foi você, por favor não clique no link e nos avise por meio deste email: "
            texto_botao = "Recuperar Senha"

        elif tipo == 'cadastroOK':
            texto1 = "Seu cadastro foi validado com sucesso!"
            texto2 = "Agora você pode salvar seus diagnósticos em nosso site "
            texto_botao = "Link do site"
        elif tipo == 'cadastroInvalido':
            texto1 = "Seu cadastro estava inválido!"
            texto2 = "Verifique se seu nome ou CRM estavam corretos e tente novamente."
            texto_botao = "Link do suporte"
        else:
            raise ValueError(f"TIPO: {tipo} NAO EXISTE!")

    def enviar_email_admin(self, email_med, nome_med, crm):
        texto_cad = "Novo cadastro:"
        texto_email = f"Email: {email_med}"
        texto_nome = f"Nome: {nome_med}"
        texto_crm = f"CRM: {crm}"

    def enviar_email(self, class_value_mapper: dict, destino, assunto):
        try:
            html = self.format_html(class_value_mapper)
            msg = Message(
                subject=assunto,
                recipients=[destino],  # List of recipients
                html=html
            )
            self.mailer.send(msg)
            return True
        except Exception as e:
            return False

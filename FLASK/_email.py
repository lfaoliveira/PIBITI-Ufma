from bs4 import BeautifulSoup
from flask_mail import Mail, Message
from typing import Literal

SOURCE_HTML = "FLASK\\assets\\template-email.html"
# TODO: MUDAR TITULO DO APLICATIVO!!!!!!!!!!!!!
TITULO_APP = "<<TITULO DO APP>>"

CORPO = "corpo-texto"
BOTOES = "botoes"


class MailHandler:
    def __init__(self, flask_mail):
        self.mailer = flask_mail
        with open(SOURCE_HTML, 'r', encoding='utf-8') as file:
            html_content = file.read()
        self.parser = BeautifulSoup(html_content, 'html.parser')

    def reset_parser(self):
        with open(SOURCE_HTML, 'r', encoding='utf-8') as file:
            html_content = file.read()
        self.parser = BeautifulSoup(html_content, 'html.parser')

    def format_html(self, class_value_mapper: dict):
        # substitui valores no HTML
        for classe, valor in class_value_mapper.items():
            elements = self.parser.find_all(class_=classe)
            for element in elements:
                # Remove existing content.
                element.clear()
                element.append(str(valor))
        # Return the modified HTML as a string.
        return str(self.parser)

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

    def add_h2(self, lista_texto):

        corpo = self.parser.find_all(class_=CORPO)[0]
        for texto in lista_texto:
            h2_tag = self.parser.new_tag("h2")
            h2_tag.string = texto
            corpo.append(h2_tag)
        return str(self.parser)

    def add_botao(self, dict_link: dict[str, str]):
        """
        dict_link: dict[str, str] key=texto, value=url
        """
        botoes = self.parser.find_all(class_=BOTOES)[0]
        for texto, link in dict_link.items():
            td_tag = self.parser.new_tag("td")
            td_tag.string = texto
            botoes.append(td_tag)
            button_tag = self.parser.new_tag("button")
            button_tag.string = texto
            button_tag['onclick'] = f"location.href='{link}'"
            td_tag.append(button_tag)

        return str(self.parser)

    def add_table(self, entries: list[str]):
        """
        Adiciona ao corpo do texto table e entradas(texto)
        """
        corpo = self.parser.find_all(class_=CORPO)[0]
        table = self.parser.new_tag("table")
        for entry in entries:
            table_row = self.parser.new_tag("tr")
            td_tag = self.parser.new_tag("td")
            td_tag.text = entry
            td_tag['style'] = "margin: 5px;"
            table_row.append(td_tag)
            table.append(table_row)

        corpo.append(table)
        return str(self.parser)

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

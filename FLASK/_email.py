from bs4 import BeautifulSoup
from flask_mail import Mail, Message
from typing import Literal
import time

SOURCE_HTML = "./static/template-email.html"  # MUDAR COM BASE EM LINUX OU WINDOWS!!!!
# TODO: MUDAR TITULO DO APLICATIVO!!!!!!!!!!!!!
TITULO_APP = "NeurOptic"
EMAIL_APP = "viplab.psno@nca.ufma.br"

CORPO = "corpo-texto"
BOTOES = "botoes"
URL_RECUP_SENHA = ""
URL_HOMEPAGE = ""
URL_SUPORTE = ""


class MailHandler:
    def __init__(self, flask_mail):
        self.mailer = flask_mail
        with open(SOURCE_HTML, "r", encoding="utf-8") as file:
            html_content = file.read()
        self.parser = BeautifulSoup(html_content, "html.parser")

    def reset_parser(self):
        with open(SOURCE_HTML, "r", encoding="utf-8") as file:
            html_content = file.read()
        self.parser = BeautifulSoup(html_content, "html.parser")

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

    def add_h2(self, lista_texto):

        corpo = self.parser.find_all(class_=CORPO)[0]
        for texto in lista_texto:
            h2_tag = self.parser.new_tag("h2")
            h2_tag.string = texto
            corpo.append(h2_tag)
        return

    def add_anchor(self, dict_link: dict[str, str]):
        """
        dict_link: dict[str, str] key=texto, value=url
        """
        i = 0
        botoes = self.parser.find_all(class_=BOTOES)[0]
        for texto, link in dict_link.items():
            td_tag = self.parser.new_tag("td")
            anchor_tag = self.parser.new_tag("a", href=link)
            anchor_tag.string = texto
            if i == 0:
                # background roxo
                background = "hsl(267, 81%, 37%)"
            else:
                background = "#000000"
            td_tag["style"] = "width: 20ch"
            anchor_tag["style"] = (
                f"color: #ffffff; text-align: center; margin-right:10px; padding: 2% 0.5%; background: {background}; border-radius: 17%;"
            )
            td_tag.append(anchor_tag)

            botoes.append(td_tag)
        return

    def add_table(self, entries: list[str]):
        """
        Adiciona ao corpo do texto table e entradas(texto)
        """
        corpo = self.parser.find_all(class_=CORPO)[0]
        table = self.parser.new_tag("table")
        for entry in entries:
            table_row = self.parser.new_tag("tr")
            td_tag = self.parser.new_tag("td")
            td_tag.string = str(entry)
            td_tag["style"] = "margin: 5px;"
            table_row.append(td_tag)
            table.append(table_row)

        corpo.append(table)
        return

    def enviar_email_usuario(
        self,
        tipo: Literal["recuperar", "cadastroOK", "cadastroInvalido"],
        email_destino,
        assunto,
        url,
    ):
        try:
            texto1 = ""
            texto2 = ""
            texto_botao = ""
            link = url

            if tipo == "recuperar":
                texto1 = "Clique no link para recuperar sua senha."
                texto2 = f"Se não foi você, por favor não clique no link e nos avise por meio deste email: {EMAIL_APP}"
                texto_botao = "Recuperar Senha"

            elif tipo == "cadastroOK":
                texto1 = "Seu cadastro foi validado com sucesso!"
                texto2 = "Agora você pode salvar seus diagnósticos em nosso site."
                texto_botao = "Link do site"

            elif tipo == "cadastroInvalido":
                texto1 = "Seu cadastro estava inválido!"
                texto2 = (
                    "Verifique se seu nome e CRM estavam corretos e tente novamente."
                )
                texto_botao = "Link do suporte"
            else:
                raise ValueError(f"TIPO: {tipo} NAO EXISTE!")

            self.add_h2([texto1, texto2])
            self.add_anchor({texto_botao: link})

            self.enviar_email(str(self.parser), email_destino, assunto)

            with open("last_email_rendered.html", "w", encoding="utf-8") as f:
                f.write(str(self.parser))

            self.reset_parser()
            return True

        except Exception as e:
            print(e)
            time.sleep(2)
            return self.enviar_email_usuario(tipo, email_destino, assunto, url)

    def enviar_email_admin(self, email_med, nome_med, crm, urlAceita, urlRecusa):
        try:

            texto_cad = "Novo cadastro:"
            texto_email = f"Email: {email_med}"
            texto_nome = f"Nome: {nome_med}"
            texto_crm = f"CRM: {crm}"
            # TODO: CRIAR URL de aceitacao e recusa de cadastro
            self.add_table([texto_cad, texto_email, texto_nome, texto_crm])
            self.add_anchor({"Aceitar": urlAceita, "Recusar": urlRecusa})
            self.enviar_email(str(self.parser), EMAIL_APP, "NOVO CADASTRO")
            self.reset_parser()

            with open("last_email_rendered.html", "w", encoding="utf-8") as f:
                f.write(str(self.parser))

            return True

        except Exception as e:
            print(e)
            time.sleep(2)
            return self.enviar_email_admin(email_med, nome_med, crm)

    def enviar_email(self, html, destino, assunto):
        try:
            # html = self.format_html(class_value_mapper)
            msg = Message(
                subject=assunto, recipients=[destino], html=html  # List of recipients
            )
            self.mailer.send(msg)
            return True
        except Exception as e:
            return False

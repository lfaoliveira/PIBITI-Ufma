from bs4 import BeautifulSoup
from weasyprint import HTML, CSS
import os


class Converter:
    def __init__(self):
        pass

    def convert_html_to_pdf(self, source_html, source_css, output_filename):
        try:
            # Create HTML and CSS objects from input strings
            html = HTML(string=source_html)
            css = CSS(filename=source_css)
            # Write PDF to the specified output file using the CSS stylesheet
            html.write_pdf(output_filename, stylesheets=[css])
            return True
        except Exception as e:
            return False

    def insert_text_by_class(self, html_file_path, class_value_mapping):
        """
        Function that takes HTML, parses it with bs4 and uses a mapping of values to populate the HTML.
        """
        # Open and read the input HTML file.
        with open(html_file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()

        # Parse the HTML content.
        soup = BeautifulSoup(html_content, 'html.parser')

        # Iterate over each class and its associated text to insert.
        for class_name, value in class_value_mapping.items():
            # Find all elements that have the given class.
            elements = soup.find_all(class_=class_name)
            for element in elements:
                if element.name.lower() == "img":
                    element['src'] = value
                    continue
                # Clear existing contents.
                element.clear()
                # Insert the given text value.
                element.append(str(value))

        # Return the modified HTML as a string.
        return str(soup)


# Example HTML string
print("HOME: ", os.getcwd())
# Create an instance of Converter.

# Convert the HTML to PDF.
# Note: A CSS file is expected. Replace 'style.css' with the appropriate CSS file.
try:
    converter = Converter()
    mapeamento = {'logo': "../vite-project/src/assets/logo ufma.png", "nome-medico": "AB do Caralho D", "crm": 12345,
                  "data": "11/09/2001", "nome-paciente": "Arrombado da Silva", "diag-auto": "Paralisia", "diag-medico": "Paralisia",
                  "vel-esq": "3mm/s", "vel-dir": "3mm/s", "dif-vel": "3%",
                  "img-grafico": "../vite-project/src/assets/sexto-nervo.png", "logo-vip": "../vite-project/src/assets/logo_VIP_Lab.png",
                  "logo-ufma": "../vite-project/src/assets/logo ufma.png",
                  "logo-nca": "../vite-project/src/assets/LogoNCAFundBranco2000_2021.png"}

    html_content = converter.insert_text_by_class(
        './FLASK/template-pdf.html', mapeamento)
    if converter.convert_html_to_pdf(html_content, "./FLASK/template-pdf.css", "./FLASK/output.pdf"):
        print("PDF created successfully!")
except:
    print("An error occurred during PDF creation.")

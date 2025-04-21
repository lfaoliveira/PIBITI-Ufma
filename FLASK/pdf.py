from bs4 import BeautifulSoup
from weasyprint import HTML, CSS
import os

HTML_FILEPATH = './template-pdf.html'
CSS_FILEPATH = './template-pdf.css'


class Converter:
    def __init__(self):
        pass

    def convert_html_to_pdf(self, source_html, output_filename, base_url):
        try:
            # Create HTML and CSS objects from the input strings
            html = HTML(string=source_html, base_url=base_url)
            css = CSS(filename=CSS_FILEPATH)
            # Write PDF to the specified output file using the CSS stylesheet
            print("Escrevendo pdf...")
            html.write_pdf(output_filename, stylesheets=[css])
            return True, None

        except Exception as e:
            print("Error creating PDF:", e)
            return False, e

    def insert_text_by_class(self, class_value_mapping):
        """
        Parse the HTML template (specified by HTML_FILEPATH) with BeautifulSoup and
        update elements based on the mapping of class names to text or image paths.
        """
        # Open and read the input HTML file.
        with open(HTML_FILEPATH, 'r', encoding='utf-8') as file:
            html_content = file.read()

        # Parse the HTML content.
        soup = BeautifulSoup(html_content, 'html.parser')
        print("Parsing html...")
        # Iterate over each class and its associated value to insert.
        for class_name, value in class_value_mapping.items():
            # Find all elements that have the given class.
            elements = soup.find_all(class_=class_name)
            for element in elements:
                if element.name.lower() == "img":
                    element['src'] = value
                    continue
                # Remove existing content.
                element.clear()
                # Insert the new value.
                element.append(str(value))
        # Return the modified HTML as a string.
        return str(soup)


"""  if __name__ == '__main__':
     # Create an instance of Converter.
     converter = Converter()
     # Define a test mapping for HTML elements.
     mapping = {
         'logo': "path/to/logo.png",
         'nome-medico': "Dr. Test",
         'crm': "123456",
         'data': "01/01/2021",
         'nome-paciente': "John Doe",
         'diag-auto': "Teste Diagnóstico",
         'diag-medico': "Teste Diagnóstico Médico",
         'vel-esq': "3mm/s",
         'vel-dir': "3mm/s",
         'dif-vel': "0%",
         'img-grafico': "path/to/grafico.png",
         'logo-vip': "path/to/logo_vip.png",
         'logo-ufma': "path/to/logo_ufma.png",
         'logo-nca': "path/to/logo_nca.png"
     }
     HTML_FILEPATH = './FLASK/template-pdf.html'
     CSS_FILEPATH = './FLASK/template-pdf.css'
     # Update the HTML template with test values.
     modified_html = converter.insert_text_by_class(mapping)
     # Use the modified HTML to create a test PDF.
     output_file = "test.pdf"
     if converter.convert_html_to_pdf(modified_html, output_file):
         print("PDF creation successful:", output_file)
     else:
         print("PDF creation failed.") """

import logging
from bs4 import BeautifulSoup
from weasyprint import HTML, CSS
import sys
import os
import shutil
import json

HTML_FILEPATH = './template.html'
CSS_FILEPATH = './template.css'

# Configure logging
logging.basicConfig(
    filename='pdf.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


class Converter:
    def __init__(self):
        pass

    def convert_html_to_pdf(self, source_html, output_filename, base_url):
        """
        base_url: caminho para folder estatico da applicacao para achar mais facil assets
        """
        try:
            # Create HTML and CSS objects from the input strings
            html = HTML(string=source_html, base_url=base_url)
            css = CSS(filename=CSS_FILEPATH)
            # Write PDF to the specified output file using the CSS stylesheet
            logging.info("Escrevendo pdf...")
            html.write_pdf(output_filename, stylesheets=[css])
            return True, None

        except Exception as e:
            logging.error("Error creating PDF: %s", e)
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
        logging.info("Parsing html...")
        # Iterate over each class and its associated value to insert.
        for class_name, value in class_value_mapping.items():
            # Find all elements that have the given class.
            elements = soup.find_all(class_=class_name)
            for element in elements:
                if element.name.lower() == "img":
                    element['src'] = value
                    continue
                # caso da lista de velocidade
                elif element.name.lower() == "li":
                    if class_name == "vel-esq":
                        value = f"Olho Esquerdo:\t{value}"
                    if class_name == "vel-dir":
                        value = f"Olho Direito:\t{value}"
                    if class_name == "dif-vel":
                        value = f"Diferença entre os olhos:\t{value}"

                # Remove existing content.
                element.clear()
                # Insert the new value.
                element.append(str(value))
        # Return the modified HTML as a string.
        return str(soup)


if __name__ == '__main__':
    # Create an instance of Converter.
    converter = Converter()
    # Define a test mapping for HTML elements.
    dict_mapping = json.loads(sys.argv[1])

    path_output = sys.argv[2]
    base_url = sys.argv[3]
    string_html = converter.insert_text_by_class(dict_mapping)
    filename = os.path.basename(path_output)

    pdfOK, erro = converter.convert_html_to_pdf(
        string_html, filename, base_url)
    if pdfOK:
        logging.info("PDF created successfully. Base URL: %s", base_url)
        if os.path.exists(path_output):
            os.remove(path_output)

        shutil.move(filename, path_output)
        sys.exit(0)
    else:
        logging.error("PDF creation failed. Error: %s", erro)
        sys.exit(-1)

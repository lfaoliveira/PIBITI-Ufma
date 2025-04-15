from bs4 import BeautifulSoup
from weasyprint import HTML, CSS


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
                element.append(value)

        # Return the modified HTML as a string.
        return str(soup)


# Example HTML string
html_content = """
<html>
  <head>
    <meta charset="utf-8">
    <title>xhtml2pdf Example</title>
  </head>
  <body>
    <h1>Hello, World!</h1>
    <p>This PDF was generated from an HTML string using xhtml2pdf.</p>
  </body>
</html>
"""

# Create an instance of Converter.
converter = Converter()

# Convert the HTML to PDF.
# Note: A CSS file is expected. Replace 'style.css' with the appropriate CSS file.
if converter.convert_html_to_pdf(html_content, "template-pdf.css", "output.pdf"):
    print("PDF created successfully!")
else:
    print("An error occurred during PDF creation.")

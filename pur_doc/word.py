import os
from docxtpl import DocxTemplate
from pur_doc import sql, constant

TEMPLATE_PATH = constant.TEMPLATE_PATH

def generate_nl(inject_data):

    template_file_path = TEMPLATE_PATH + 'nl.docx'
    output_file_path = './output/nl_output.docx'

    if os.path.exists(output_file_path):
        os.remove(output_file_path)
    else:
        pass

    doc = DocxTemplate(template_file_path)

    doc.render(inject_data)

    doc.save(output_file_path)
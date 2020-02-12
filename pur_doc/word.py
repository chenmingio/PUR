import os

from docxtpl import DocxTemplate

from pur_doc import constant, sql

TEMPLATE_PATH = constant.TEMPLATE_PATH


def generate_nl(project, vendor, part_list):
    inject_data = sql.assemble_nl_info(project, vendor, part_list)
    inject_nl(inject_data)


def inject_nl(inject_data):

    template_file_path = TEMPLATE_PATH + 'nl.docx'
    output_file_path = './output/nl_output.docx'

    if os.path.exists(output_file_path):
        os.remove(output_file_path)

    doc = DocxTemplate(template_file_path)

    doc.render(inject_data)

    doc.save(output_file_path)


def generate_nl_pcb(inject_data):

    template_file_path = TEMPLATE_PATH + 'nl_pcb.docx'
    output_file_path = './output/nl_pcb_output.docx'

    if os.path.exists(output_file_path):
        os.remove(output_file_path)
    else:
        pass

    doc = DocxTemplate(template_file_path)

    doc.render(inject_data)

    doc.save(output_file_path)

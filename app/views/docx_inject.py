import os
from pprint import pprint
from docxtpl import DocxTemplate

from app.models.assemble_dict import assemble_nl_info
from config import TEMPLATE_FOLDER, DOWNLOAD_FOLDER


def generate_nl(project, vendor, part_list):
    inject_data = assemble_nl_info(project, vendor, part_list)
    pprint(f"[generate nl] inject data: {inject_data}")

    filename = f"Nomination_Letter_{project}_{vendor}.docx"
    template_path = os.path.join(TEMPLATE_FOLDER, 'nl.docx')
    output_path = os.path.join(DOWNLOAD_FOLDER, filename)

    doc = DocxTemplate(template_path)
    doc.render(inject_data)
    doc.save(output_path)

    return filename


def generate_nl_pcb(inject_data):
    template_file_path = TEMPLATE_FOLDER + 'nl_pcb.docx'
    output_file_path = './downloads/nl_pcb_output.docx'

    if os.path.exists(output_file_path):
        os.remove(output_file_path)
    else:
        pass

    doc = DocxTemplate(template_file_path)

    doc.render(inject_data)

    doc.save(output_file_path)

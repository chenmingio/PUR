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

def generate_mm(project):
    '''generate mm for all parts under this project'''

    # prepare the data
    part_list = sql.get_project_part_list(project)

    # create folder
    template_file_path = TEMPLATE_PATH + 'sds_mm.docx'
    output_folder_path = './output/mm_output'

    if os.path.exists(output_folder_path):
        pass

    for part in part_list:
        output_file_path = './output/mm_' + project + '/mm_' + part + '.docx'
        rc = sql.assemble_project(project, [part])

        doc = DocxTemplate(template_file_path)
        doc.render(rc)
        doc.save(output_file_path)

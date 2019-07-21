import os
from docxtpl import DocxTemplate


def generate_nl(context):

    filePath = "./NL_generated.docx"

    if os.path.exists(filePath):
        os.remove(filePath)
        print("nl generated")
    else:
        print("no generated nl yet")

    doc = DocxTemplate("NL.docx")

    doc.render(context)

    doc.save("NL_g.docx")


if __name__=="__main__":
    generate_nl()

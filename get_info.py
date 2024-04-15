from pypdf import PdfReader
import logging
import docx2txt
import re

logger = logging.getLogger("pypdf")
logger.setLevel(logging.ERROR)


def get_pdf_text(pdf_file):
    reader = PdfReader(pdf_file)
    text = ''
    for page in reader.pages:
        text += page.extract_text(extraction_mode="layout", layout_mode_space_vertically=False,  layout_mode_scale_weight=1.0, layout_mode_strip_rotated=False)
    return text

# text = get_pdf_text(f"static/pdf/AarushiRohatgi.pdf")
# print(text)


def  get_word_text(word_file):
    doc = docx2txt.process(word_file)
    doc.encode("utf-8")
    doc = doc.replace('\n', "")
    return doc

def get_gmail(text: str):
    gmail = []
    pattern = re.compile(r'[a-zA-Z0-9-\.]+@[a-zA-Z-\.]*\.(com|edu|net|ac.in)')
    matches = pattern.finditer(text)
    for match in matches:
        gmail.append(match.group(0))

    return gmail



def get_phone(text: str):
    numbers = []
    pattern = re.compile(r'\b\d{10}\b')
    matches = pattern.finditer(text)
    for match in matches:
        numbers.append(match.group(0))
    return numbers

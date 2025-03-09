import PyPDF2

def get_number_of_pages(pdf_path):
    with open(pdf_path, "rb") as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        return len(pdf_reader.pages)

# Příklad použití
pdf_path = "dnd_character_sheet.pdf"
num_pages = get_number_of_pages(pdf_path)
print(f"PDF dokument má {num_pages} stránek.")
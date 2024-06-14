# Scrapes pdf data from the website https://www.visitportugal.com/en/search/site?regioes=285&context=485&localidades=300
# the output is a file, where each chunk is separated by a new line
import fitz  # PyMuPDF
from langchain.docstore.document import Document
from langchain_text_splitters import CharacterTextSplitter
from dbs.db import get_top_n_chunks, add_chunks_to_db
import sys

#pdf_path = "./beaches.pdf"
pdf_path = sys.argv[1]
entity_type = sys.argv[2]
print("pdf_path: " + pdf_path + ", entity_type: " + entity_type)

# rough coordinates for the columns
left_column_coords = fitz.Rect(0, 0, 306, 792)  # x0, y0, x1, y1 for the left column
right_column_coords = fitz.Rect(306, 0, 612, 792)  # x0, y0, x1, y1 for the right column

title_font_size = 9
text_font_size = 8

"""
Receives param side
side can be 'left' or 'right'. By default it's left
"""
def extract_blocks_by_font_size(column_coords):
    pdf_document = fitz.open(pdf_path)
    blocks = []
    current_block = []
    # font size of the title of each block is 9
    for page in pdf_document:
        text_blocks = page.get_text("dict", clip=column_coords)["blocks"]
        for block in text_blocks:
            if block['type'] == 0:
                for line in block["lines"]:
                    current_line = ""
                    for span in line["spans"]:
                        if span['size'] == title_font_size:
                            if len(current_block) > 0:
                                blocks.append("\n".join(current_block))
                            current_line += span['text']
                            current_block = []
                        elif span['size'] == text_font_size:
                            current_line += span['text']
                    current_block.append(current_line)

    # add last block
    if current_block:
        blocks.append("\n".join(current_block))

    pdf_document.close()
    return blocks

if __name__ == "__main__":
    # gets blocks on the left side of the pdf
    blocks_left = extract_blocks_by_font_size(left_column_coords)
    # gets blocks on the right side of the pdf
    blocks_right = extract_blocks_by_font_size(right_column_coords)
    # concatenates all the blocks
    blocks = blocks_left + blocks_right
    
    text_splitter = CharacterTextSplitter(
        separator="\n\n",
        chunk_size=10,
        chunk_overlap=0,
        length_function=len,
        is_separator_regex=False,
    )
    
    documents = text_splitter.create_documents(texts = blocks)
    add_chunks_to_db(documents, entity_type=entity_type)
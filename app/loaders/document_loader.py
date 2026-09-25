from pathlib import Path

from app.loaders.pdf_loader import load_pdf
from app.loaders.docx_loader import load_docx
from app.loaders.txt_loader import load_txt
from app.loaders.csv_loader import load_csv
from app.loaders.json_loader import load_json


def load_document(file_path: str):

    extension = Path(file_path).suffix.lower()


    if extension == ".pdf":

        return load_pdf(file_path)


    elif extension == ".docx":

        return load_docx(file_path)


    elif extension == ".txt":

        return load_txt(file_path)


    elif extension == ".csv":

        return load_csv(file_path)


    elif extension == ".json":

        return load_json(file_path)


    else:

        raise ValueError(
            f"Unsupported file type: {extension}"
        )
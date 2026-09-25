from langchain_community.document_loaders import CSVLoader


def load_csv(file_path: str):

    loader = CSVLoader(file_path)

    documents = loader.load()

    return documents
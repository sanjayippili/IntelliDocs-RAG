import json

from langchain_core.documents import Document


def load_json(file_path: str):

    with open(file_path, "r", encoding="utf-8") as file:

        data = json.load(file)


    documents = []


    if isinstance(data, list):

        for i, item in enumerate(data):

            documents.append(
                Document(
                    page_content=json.dumps(item, indent=2),
                    metadata={
                        "source": file_path,
                        "record": i
                    }
                )
            )


    else:

        documents.append(
            Document(
                page_content=json.dumps(data, indent=2),
                metadata={
                    "source": file_path
                }
            )
        )


    return documents
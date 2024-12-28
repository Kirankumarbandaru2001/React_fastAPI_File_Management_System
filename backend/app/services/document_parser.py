from unstructured.partition.auto import partition

def parse_document(file_url):
    elements = partition(filename=file_url)
    metadata = {"content": "".join([element.text for element in elements])}
    return metadata

from app.services.nlp_processing import process_query

def query_documents(query: str):
    return process_query(query)

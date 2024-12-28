from langchain.chains import RetrievalQA
# from langchain_community.vectorstores import ElasticVectorSearch
from langchain_elasticsearch import ElasticsearchStore
from langchain_openai import OpenAIEmbeddings

from app.core.config import settings

# Initialize embedding model
embeddings = OpenAIEmbeddings(openai_api_key=settings.OPENAI_API_KEY)

#  Initialize the vectorstore with the required embedding
vectorstore = ElasticsearchStore(
    embedding=embeddings,
    es_url="http://localhost:9200", index_name="documents"
)

# creating qa chain
qa_chain = RetrievalQA.from_chain_type(
    retriever=vectorstore.as_retriever(), chain_type="stuff"
)

def handle_query(query: str):
    return qa_chain.run(query)

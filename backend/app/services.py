import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()
import boto3
import uuid
from sentence_transformers import SentenceTransformer, util
from haystack.document_stores import FAISSDocumentStore
from haystack.nodes import DensePassageRetriever, FARMReader
from haystack.pipelines import ExtractiveQAPipeline
from haystack.schema import Document
from unstructured.partition.auto import partition
from typing import List, Optional
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import TextLoader
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.agents import initialize_agent, AgentType
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME"),
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID"),
AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
from .database import SessionLocal
from .models import Document
import openai
import logging

# Initialize S3 client for AWS S3 storage
s3_client = boto3.client(
    "s3", aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY
)


# Helper function to process document upload
def process_document(file) -> str:
    """Handles document upload, stores it in S3, and returns the file URL."""
    try:
        # Generate a unique filename
        file_extension = file.filename.split('.')[-1]
        file_name = f"{uuid.uuid4()}.{file_extension}"

        # Upload to S3
        s3_client.upload_fileobj(
            file.file, S3_BUCKET_NAME, file_name, ExtraArgs={'ACL': 'public-read'}
        )

        file_url = f"https://{S3_BUCKET_NAME}.s3.amazonaws.com/{file_name}"
        return file_url
    except Exception as e:
        logging.error(f"Error uploading file to S3: {str(e)}")
        raise Exception(f"Error uploading file: {str(e)}")


# Helper function to extract text from documents using unstructured.io
def extract_text_from_url(file_url: str) -> str:
    """Extracts text from a document URL using unstructured.io."""
    try:
        # Download the document from S3
        response = s3_client.get_object(Bucket=S3_BUCKET_NAME, Key=file_url.split('/')[-1])
        file_content = response['Body'].read()

        # Use unstructured.io to parse the document
        document = partition(file_content)
        text_content = "\n".join([doc.text for doc in document])
        return text_content
    except Exception as e:
        logging.error(f"Error extracting text from URL: {str(e)}")
        raise Exception(f"Error extracting text: {str(e)}")


# Function to query the document using a RAG Agent (Retrieve and Generate)
def query_with_qa_model(query: str, document_text: str) -> str:
    """Uses free models and Haystack for querying document contents."""
    try:
        # Split the document into chunks (you can tweak the chunk size as needed)
        chunk_size = 1000
        texts = [document_text[i:i + chunk_size] for i in range(0, len(document_text), chunk_size)]

        # Convert chunks to Haystack Document format
        documents = [Document(content=chunk) for chunk in texts]

        # Initialize FAISS document store
        document_store = FAISSDocumentStore(embedding_dim=768)
        document_store.write_documents(documents)

        # Initialize SentenceTransformer model for embeddings
        retriever = DensePassageRetriever(
            document_store=document_store,
            query_embedding_model="facebook/dpr-question_encoder-single-nq-base",
            passage_embedding_model="facebook/dpr-ctx_encoder-single-nq-base",
            use_gpu=False
        )
        document_store.update_embeddings(retriever)

        # Initialize a reader model for generating answers
        reader = FARMReader(model_name_or_path="deepset/roberta-base-squad2")

        # Set up the pipeline
        pipeline = ExtractiveQAPipeline(reader, retriever)

        # Query the pipeline
        results = pipeline.run(query=query, params={"Retriever": {"top_k": 5}, "Reader": {"top_k": 1}})

        # Extract the best answer
        if results["answers"]:
            return results["answers"][0].answer
        else:
            return "No answer found in the document."

    except Exception as e:
        logging.error(f"Error querying with free model: {str(e)}")
        raise Exception(f"Error querying with free model: {str(e)}")



# Helper function to initialize the RAG agent (for more complex querying)
def initialize_rag_agent(document_text: str) -> object:
    """Initializes the RAG Agent for query handling."""
    try:
        # Create a document loader to load the document content into a format that LangChain can understand
        loader = TextLoader(document_text, encoding='utf-8')
        documents = loader.load()

        # Initialize vector store for efficient querying
        embeddings = OpenAIEmbeddings()
        vectorstore = FAISS.from_documents(documents, embeddings)

        # Initialize RAG agent
        agent = initialize_agent(
            tools=[vectorstore.as_tool()],
            agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            llm=OpenAI(model="gpt-3.5-turbo"),
            verbose=True
        )
        return agent
    except Exception as e:
        logging.error(f"Error initializing RAG agent: {str(e)}")
        raise Exception(f"Error initializing RAG agent: {str(e)}")


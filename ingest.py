import os
from dotenv import load_dotenv

from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore

from pinecone import Pinecone

# Load environment variables
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX = os.getenv("PINECONE_INDEX")

# Initialize Pinecone
pc = Pinecone(
    api_key=PINECONE_API_KEY
)

# Load PDFs
loader = DirectoryLoader(
    "knowledge_base",
    glob="*.pdf"
)

documents = loader.load()

# Split documents
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

texts = text_splitter.split_documents(documents)

# Create embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Upload to Pinecone
vectorstore = PineconeVectorStore.from_documents(
    texts,
    embeddings,
    index_name=PINECONE_INDEX
)

print("PDFs successfully uploaded to Pinecone")
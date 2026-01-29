
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

CHROMA_PATH = "data/chroma"

# pages we actually need
URLS = [
    "https://www.sunmarke.com/",
    "https://www.sunmarke.com/admissions/",
    "https://www.sunmarke.com/curriculum/",
    "https://www.sunmarke.com/learning/",
    "https://www.sunmarke.com/activities/",
    "https://www.sunmarke.com/facilities/"
]

print("Loading website pages...")

loader = WebBaseLoader(URLS)
docs = loader.load()

print("RAW WEB PAGES:", len(docs))

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=700,
    chunk_overlap=150
)

documents = text_splitter.split_documents(docs)
print("CHUNKS CREATED:", len(documents))

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

db = Chroma.from_documents(
    documents,
    embeddings,
    persist_directory=CHROMA_PATH
)

db.persist()

print("✅ WEBSITE INGEST COMPLETE")

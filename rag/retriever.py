
import os
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# -----------------------------
# ABSOLUTE PATH FIX
# -----------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CHROMA_PATH = os.path.abspath(
    os.path.join(BASE_DIR, "..", "data", "chroma")
)

print("CHROMA PATH:", CHROMA_PATH)

if os.path.exists(CHROMA_PATH):
    print("FILES:", os.listdir(CHROMA_PATH))
else:
    print("❌ CHROMA FOLDER NOT FOUND")

def get_retriever():
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    db = Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=embeddings
    )

    return db.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 5}
    )


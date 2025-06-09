import os
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from dotenv import load_dotenv

# Load OpenAI key
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
# openai_api_key = st.secrets["OPENAI_API_KEY"]

def process_and_store_pdf(pdf_path: str, persist_dir: str = "chroma_db"):
    loader = PyPDFLoader(pdf_path)
    pages = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = splitter.split_documents(pages)

    embedding_model = OpenAIEmbeddings(openai_api_key=openai_api_key)
    vectorstore = Chroma.from_documents(documents=docs, embedding=embedding_model, persist_directory=persist_dir)

    vectorstore.persist()
    print(f"Chroma vector store saved to: {persist_dir}")

if __name__ == "__main__":
    process_and_store_pdf("POET_Everyday_Instructions.pdf")

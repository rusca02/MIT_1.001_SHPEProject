# 02_index_documents.py
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.docstore.document import Document

def split_text(text, chunk_size=500, overlap=50):
    """
    Splits a long text into smaller chunks.

    Args:
        text (str): Text to be split.
        chunk_size (int): Maximum number of characters per chunk.
        overlap (int): Number of characters to overlap between consecutive chunks.

    Returns:
        List[str]: A list of text chunks.
    """
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap  # Overlap for context continuity.
    return chunks

def build_index(documents):
    """
    Splits documents into chunks and builds a FAISS index.

    Args:
        documents (list): List of dictionaries with keys 'filename' and 'text'.

    Returns:
        FAISS: A FAISS vector store built from text chunks.
    """
    doc_chunks = []
    # Process each document by splitting text and wrapping in a Document.
    for doc in documents:
        chunks = split_text(doc["text"])
        for idx, chunk in enumerate(chunks):
            doc_chunks.append(Document(
                page_content=chunk,
                metadata={"source": doc["filename"], "chunk": idx}
            ))
    # Use the community Hugging Face embedding model.
    embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    # Create the FAISS index from the chunk Documents.
    vectorstore = FAISS.from_documents(doc_chunks, embedding_model)
    return vectorstore

def save_index(vectorstore, path="faiss_index"):
    """
    Saves the FAISS vector store locally.

    Args:
        vectorstore (FAISS): The vector store.
        path (str): Directory path to save the index.
    """
    vectorstore.save_local(path)

if __name__ == "__main__":
    from ingest import load_documents

    # Load raw documents from your data source.
    docs = load_documents()
    # Build the FAISS index using document chunks.
    vs = build_index(docs)
    # Save the FAISS index for later reuse.
    save_index(vs)
    print("Index built and saved.")

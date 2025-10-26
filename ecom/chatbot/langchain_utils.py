# import os
# from typing import List, Optional
# from pathlib import Path

# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.docstore.document import Document
# from langchain.embeddings.openai import OpenAIEmbeddings
# from langchain.vectorstores import Chroma
# from langchain.chat_models import ChatOpenAI
# from langchain.chains import RetrievalQA

# # Persisted chroma directory (inside the chatbot app)
# VSTORE_DIR = Path(__file__).resolve().parent.joinpath("chroma_db")

# def get_embeddings():
#     # """Return an embeddings instance (uses OPENAI_API_KEY)."""
#     return OpenAIEmbeddings()

# def build_vectorstore_from_texts(texts: List[str], persist: bool = True) -> Chroma:
#     # """
#     # Build a Chroma vectorstore from a list of text strings.
#     # Save to disk if persist=True.
#     # """
#     if not texts:
#         raise ValueError("No texts provided to build the vectorstore")

#     splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
#     docs = []
#     for t in texts:
#         chunks = splitter.split_text(t)
#         docs.extend([Document(page_content=chunk) for chunk in chunks])

#     embeddings = get_embeddings()
#     # Create Chroma vectorstore persisted to VSTORE_DIR
#     vectordb = Chroma.from_documents(documents=docs, embedding=embeddings, persist_directory=str(VSTORE_DIR))
#     if persist:
#         vectordb.persist()
#     return vectordb

# def load_vectorstore() -> Optional[Chroma]:
#     # """Load existing persisted Chroma vectorstore if present."""
#     if VSTORE_DIR.exists() and any(VSTORE_DIR.iterdir()):
#         embeddings = get_embeddings()
#         return Chroma(persist_directory=str(VSTORE_DIR), embedding_function=embeddings)
#     return None

# def get_rag_chain(vectorstore: Chroma, model_name: Optional[str] = None, temperature: float = 0.0, k: int = 4):
#     # """
#     # Build and return a RetrievalQA chain using ChatOpenAI and the given vectorstore.
#     # """
#     retriever = vectorstore.as_retriever(search_kwargs={"k": k})
#     model_name = model_name or os.getenv("OPENAI_LLM_MODEL", "gpt-4o-mini")
#     llm = ChatOpenAI(model_name=model_name, temperature=temperature)
#     chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)
#     return chain

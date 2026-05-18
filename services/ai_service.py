import os
from langchain_community.vectorstores import FAISS
from langchain_core.embeddings import FakeEmbeddings
from langchain.text_splitter import CharacterTextSplitter

# Using fake embeddings for the mock to avoid needing an OpenAI key
embeddings = FakeEmbeddings(size=1536)

# Global in-memory vector store for simplicity
vector_store = None

def index_document(content: str):
    global vector_store
    text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    texts = text_splitter.split_text(content)
    
    if not texts:
        return
        
    if vector_store is None:
        vector_store = FAISS.from_texts(texts, embeddings)
    else:
        vector_store.add_texts(texts)

def generate_feedback(draft_content: str):
    global vector_store
    
    context = ""
    if vector_store is not None:
        # Simulate retrieval
        try:
            docs = vector_store.similarity_search(draft_content, k=2)
            context = "\n".join([doc.page_content for doc in docs])
        except Exception as e:
            print(f"Vector store search failed: {e}")
        
    # Mock AI Feedback generation
    feedback_text = (
        "### AI Review Feedback\n\n"
        "**Clarity & Completeness:**\n"
        "- The proposal structure is decent, but the introduction could be more compelling.\n"
        "- Consider expanding on the specific methodologies to be used.\n\n"
        "**Missing Sections:**\n"
        "- A detailed budget estimation section appears to be missing.\n"
        "- Project timeline and milestones should be explicitly outlined.\n\n"
    )
    
    if context:
        feedback_text += "**Relevant Context from Past Proposals (RAG):**\n"
        short_context = context[:200] + "..." if len(context) > 200 else context
        feedback_text += f"> {short_context}\n\n"
        feedback_text += "Consider aligning your phrasing with these past successful proposals."
    else:
        feedback_text += "*(No past documents found for context. Try uploading reference proposals.)*"
        
    return feedback_text

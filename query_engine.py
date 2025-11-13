from pathlib import Path
import streamlit as st
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from rag_builder import load_notion_docs, chunk_documents, build_vector_store

load_dotenv()

# ------------------------------------------------
# Ensure the vector DB exists
# ------------------------------------------------
def ensure_vector_db():
    db_path = Path("db")
    if not db_path.exists() or not any(db_path.iterdir()):
        st.info("No database found. Initializing from Notion...")
        notion_docs = load_notion_docs()
        chunks = chunk_documents(notion_docs)
        build_vector_store(chunks)
        st.success("Vector database initialized successfully!")


# ------------------------------------------------
# Load the Chroma DB and model
# ------------------------------------------------
def get_vectordb():
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    vectordb = Chroma(
        persist_directory="db",
        embedding_function=embeddings,
        collection_name="company_docs"
    )
    return vectordb


def get_answer(query: str, k: int = 4):
    vectordb = get_vectordb()
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    docs = vectordb.similarity_search(query, k=k)

    context = "\n\n---\n\n".join(
        [f"[Source: {d.metadata.get('source', 'Unknown')}]\n{d.page_content}" for d in docs]
    )

    prompt = f"""
                You are a company assistant bot.
                Answer the user's question clearly and with good structure using the context below.
                If the context does not contain enough information, say you don't know.
                Do not make up answers. Always use the context provided. Assume you dont know anything else outside the context.

                Context:
                {context}

                Question:
                {query}

                Answer (structured, concise):
            """
    
    response = llm.invoke(prompt)
    sources = {d.metadata.get("source", "Unknown") for d in docs}
    return response.content, sources


# ------------------------------------------------
# Streamlit UI
# ------------------------------------------------
st.set_page_config(page_title="Company Knowledge Assistant", page_icon="💼", layout="wide")
st.title("💼 Company Knowledge Assistant")

# 🧠 Initialize vector DB if needed
ensure_vector_db()

st.markdown("Ask questions about your company policies, onboarding, or documents directly from Notion!")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

query = st.chat_input("Ask a company-related question...")

if query:
    with st.spinner("Fetching answer..."):
        answer, sources = get_answer(query)
        st.session_state["messages"].append({"role": "user", "content": query})
        st.session_state["messages"].append({
            "role": "assistant",
            "content": answer,
            "sources": ", ".join(sources)
        })

for msg in st.session_state["messages"]:
    if msg["role"] == "user":
        st.chat_message("user").markdown(msg["content"])
    else:
        st.chat_message("assistant").markdown(msg["content"])
        if msg.get("sources"):
            st.markdown(f"**📚 Sources:** {msg['sources']}")

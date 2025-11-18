from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from notion_utils import get_all_child_pages, get_page_text, ROOT_PAGE_ID

load_dotenv()


# 1. Load all Notion pages
def load_notion_docs():
    docs = []
    for title, pid in get_all_child_pages(ROOT_PAGE_ID):
        text = get_page_text(pid)
        docs.append({"title": title, "content": text})
    print(f" Loaded {len(docs)} Notion pages")
    return docs


# 2. Split text into chunks
def chunk_documents(documents):
    splitter = RecursiveCharacterTextSplitter(chunk_size=1200, chunk_overlap=200)
    all_chunks = []
    for d in documents:
        chunks = splitter.split_text(d["content"])
        for chunk in chunks:
            all_chunks.append({
                "text": chunk,
                "metadata": {"source": d["title"]}
            })
    print(f" Created {len(all_chunks)} text chunks")
    return all_chunks


# 3. Build vector store
def build_vector_store(chunks, persist_dir="db"):
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    texts = [c["text"] for c in chunks]
    metadatas = [c["metadata"] for c in chunks]

    vectordb = Chroma.from_texts(
        texts=texts,
        embedding=embeddings,
        metadatas=metadatas,
        persist_directory=persist_dir,
        collection_name="company_docs"
    )

    vectordb.persist()
    print(f"Vector store built and saved at {persist_dir}")


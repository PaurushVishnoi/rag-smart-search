🗃 ChromaDB — Core Operations (With Descriptive Steps)

This section walks you step-by-step through how vector databases operate inside a RAG pipeline.
Each operation includes:

🔍 What the step does

🎯 Why it matters for RAG

🧩 Where it fits in the pipeline

💻 A code example

1️⃣ Creating a Collection
🔍 What happens in this step?

A collection is like a folder inside the vector database.
It stores:

the text chunks

the metadata

the embeddings

🎯 Why this matters

Every RAG system needs a consistent place to store vector representations of your documents.

🧩 Where it fits

This is part of the indexing stage — creating the vector store before queries can be done.

# Choose an embedding model for vectorizing text
embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

# Initialize Chroma client
client = chromadb.Client()

# Create a collection to store all company policies
collection = client.create_collection(
    name="company_documents",
    metadata={"description": "Internal company policies and guidelines"},
    configuration={
        "embedding_function": embedding_fn
    }
)

2️⃣ Connecting to an Existing Collection
🔍 What happens?

If your collection already exists, you don’t recreate it — you simply connect to it.

🎯 Why this matters

During app runtime (e.g., inside Streamlit), you must load the stored database to run queries.

🧩 Where it fits

This is used during inference (when answering questions).
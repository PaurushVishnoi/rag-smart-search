# Vector Databases in RAG

A complete guide to understanding vector databases and how they power Retrieval-Augmented Generation systems.

## 📘 Table of Contents
- [ Chapter 1 — Role of Vector Databases in RAG](#-chapter-1--role-of-vector-databases-in-rag)
- [ Chapter 2 — What Is a Vector Database?](#-chapter-2--what-is-a-vector-database)
- [ Chapter 3 — Why Vector Databases Matter](#-chapter-3--why-vector-databases-matter)
- [ Chapter 4 — Common Pitfalls to Avoid](#-chapter-4--common-pitfalls-to-avoid)
- [ Chapter 5 — ChromaDB Fundamentals](#-chapter-5--chromadb-fundamentals)
  - [Creating a Collection](#creating-a-collection)
  - [Connecting to a Collection](#connecting-to-a-collection)
  - [Modifying a Collection](#modifying-a-collection)
  - [Adding Documents](#adding-documents)
  - [Retrieving Documents](#retrieving-documents)
  - [Updating Documents](#updating-documents)
  - [Deleting Documents](#deleting-documents)
- [ Chapter 6 — Metadata Filtering](#-chapter-6--metadata-filtering)
- [ Chapter 7 — Document Filtering](#-chapter-7--document-filtering)
- [ Chapter 8 — Distance Metrics](#-chapter-8--distance-metrics)
- [ Chapter 9 — What Vector Databases Do NOT Do](#-chapter-9--what-vector-databases-do-not-do)

## Chapter 1 — Role of Vector Databases in RAG


In a Retrieval-Augmented Generation (RAG) system, the vector database serves as the **long-term memory**. It stores document embeddings and retrieves the most relevant information for the LLM to use during generation.

A vector database in a RAG pipeline typically handles:

- Embedding source documents  
- Embedding user queries  
- Storing vectors efficiently  
- Performing fast semantic search  
- Returning relevant matches for prompt augmentation  

Some pipelines compute embeddings outside the database, but most modern vector databases — including **Chroma** — support built-in embedding functions.

## Chapter 2 — What Is a Vector Database?

A **vector database** stores text as numerical embeddings — vectors that represent the semantic meaning of content.  
Unlike traditional keyword search, **vector search retrieves information based on meaning**, even when the exact words don’t match.

Vector databases rely on **embeddings**, which are numerical representations of meaning.  
Both documents and user queries are converted into vectors so that similarity can be computed mathematically.

When you insert documents into a vector database, each document is passed through an **embedding model** (such as OpenAI, SentenceTransformers, etc.).

Example documents:

```python
documents = [
    'Bugs introduced by the intern had to be fix by the developer.',
    'Bugs found by the quality assurance engineer were difficult.',
    'Bugs are common in summers, according to the entomologist.',
    'Bugs, are extensively studied by arachnologists.'
]
```

An embedding model converts each sentence into a vector, such as:

`[0.12, -0.88, 0.51, ..., 0.04]` → *Lead developer sentence*
`[0.48, -0.33, 0.29, ..., 0.77]` → *QA sentence*
`[0.03, 0.91, -0.22, ..., 0.15]` → *Summer months (insect) sentence*
`[0.99, 0.12, -0.45, ..., 0.52]` → *Spiders (biology) sentence*



Embeddings capture **semantic meaning**, not exact wording.

For example:

- **“bugs” in a coding context** → close to vectors about software errors  
- **“bugs” in a biology context** → close to vectors about insects or spiders  

This is what enables a vector database to understand **context automatically**.

---


### Query:
**Who is responsible for a coding project and fixing others' mistakes?**

The same embedding model converts this query into a vector.  
That vector will be close to embeddings representing:

- lead developers  
- debugging  
- fixing code issues  
- software responsibilities  

And **far** from vectors about insects or bugs in nature.

---



The vector database performs a **similarity search** using cosine, L2, or inner product distance.

It compares the query vector to all document vectors and finds the closest ones.

### Conceptual Matching Example

| Document | Meaning | Similarity | Match? |
|----------|---------|------------|--------|
| “Bugs introduced by the intern had to be squashed by the lead developer.” | Software bugs, fixing mistakes | 🔥 High | ✅ Very relevant |
| “Bugs found by the quality assurance engineer…” | Software debugging | 🔥 High | ✅ Relevant |
| “Bugs are common in summer months…” | Literal insects | ❄️ Low | ❌ Not relevant |
| “Bugs, spiders, arachnologists…” | Biology | ❄️ Low | ❌ Not relevant |



## Chapter 3 — Why Vector Databases Matter

Vector databases make RAG systems:

### More Reliable  
They prevent common issues such as mismatched embedding models, missing metadata, or inconsistent document storage.

### Faster to Develop  
You don’t need to implement your own indexing, search algorithms, or metadata filtering — the database handles all of it for you.

### High-Performance  
Vector databases use optimized ANN (Approximate Nearest Neighbor) techniques — such as **HNSW** — to return results quickly, even when storing millions of vectors.

## Chapter 5 — ChromaDB Fundamentals

**ChromaDB** is a lightweight, high-performance vector database designed for both local development and production environments.

---

## 🗂️ Creating a Collection

A **collection** is similar to a table — it stores vectors, documents, and metadata.

```python
import chromadb
import chromadb.utils.embedding_functions as embedding_functions

# Choose an embedding model
embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

# Create client
client = chromadb.Client()

# Create a new collection
collection = client.create_collection(
    name="company_docs",
    metadata={"description": "Internal knowledge base"},
    configuration={
        "embedding_function": embedding_fn
    }
)
```

### Connecting to a Collection

```python
collection = client.get_collection(name="company_docs")
✏️ Modifying a Collection
python
Copy code
collection.modify(
    name="company_docs_v2",
    metadata={"updated_by": "admin"}
)
```
### Modifying a Collection

```python
collection.modify(
    name="company_docs_v2",
    metadata={"updated_by": "admin"}
)
```



**HNSW** : You cannot change the embedding model or distance metric of an existing collection — these are fixed at creation time.


### Adding Documents

Every document you add must include:

- the **raw text**
- **metadata**
- a **unique ID**

```python
collection.add(
    documents=[
        "The cafeteria operates from 8am to 6pm on weekdays.",
        "New hires must complete cybersecurity training within 30 days."
    ],
    metadatas=[
        {"source": "handbook", "tag": "facilities"},
        {"source": "training_manual", "tag": "onboarding"}
    ],
    ids=["cafeteria_hours", "cybersecurity_training"]
)
```

## Chapter 6 — Metadata Filtering

Metadata filtering allows you to refine results using structured metadata fields.

It can be used in:

- `.get()`
- `.query()`
- `.delete()`

### ✔️ Basic Filter

```python
collection.get(where={"tag": "facilities"})
```

## Chapter 7 - Document Filtering

Document filtering evaluates the **content of the document itself**, rather than its metadata.

### ✔️ Contains Text

```python
collection.get(
    where_document={"$contains": "training"}
)
```

### 🔀 Combined Filters

```python
collection.get(
    where_document={
        "$and": [
            {"$contains": "policy"},
            {"$not_contains": "outdated"}
        ]
    }
)
Copy code
```

## Chapter 8 — Distance Metrics

ChromaDB supports multiple similarity metrics:

| Metric | Description |
|--------|-------------|
| **l2** | Euclidean distance (default) |
| **cosine** | Angular similarity — recommended for transformer embeddings |
| **ip** | Inner product (dot-product–based similarity) |

### 🔧 Specify a Distance Metric

```python
collection = client.create_collection(
    name="company_docs",
    configuration={
        "embedding_function": embedding_fn,
        "hnsw": {"space": "cosine"}
    }
)
```

## Chapter 9 — What Vector Databases **Do NOT** Do

Vector databases handle **storage** and **semantic search**, but they are *not* responsible for the full RAG pipeline.

They do **not**:

- Chunk your documents  
- Build prompts for the LLM  
- Re-rank results using external scoring  
- Query the LLM directly  
- Generate answers  

These responsibilities must be implemented in your **application logic** or **RAG framework**.

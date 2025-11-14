<div align="center">

# 💼 Vector Search with RAG

A lightweight RAG system that pulls content from Notion, builds a vector database with Chroma, and answers questions using GPT.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![OpenAI](https://img.shields.io/badge/OpenAI-API-412991)
![Chroma](https://img.shields.io/badge/ChromaDB-Vector%20Search-green)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red)
![Notion](https://img.shields.io/badge/Notion-API-black)



</div>

#  Vector Search with RAG

A lightweight tool that connects to Notion, pulls in your company docs—like Onboarding Process, Meeting Policy, or Work-From-Home Guidelines—and transforms them into a searchable vector database using Chroma.

Employees can then ask questions in a friendly Streamlit chat interface:

“How do I request vacation time?”
“What’s our meeting-free Friday policy?”
“Where do I find the onboarding checklist?”
"Can you please code function of the new functionality for Impressions on Budget page ?"

The system understands natural language and instantly surfaces the right information from your internal guides and policies—no more digging through your comopany's confluence pages, github repos or Notion tabs.

---

## 📘 Table of Contents
- [ Chapter 1 — What Is RAG?](#-chapter-1--what-is-rag)
- [ Chapter 2 — What Is a Vector Database?](#-chapter-2--what-is-a-vector-database)
- [ Chapter 3 — What This Project Does](#-chapter-4--what-this-project-does)
- [ Chapter 4 — How It Works (Sequence Diagram)](#-chapter-5--how-it-works-sequence-diagram)
- [ Chapter 5 — Setting Up Notion](#-chapter-6--setting-up-notion)
- [ Chapter 6 — The Streamlit App](#-chapter-8--the-streamlit-app)
- [ Chapter 7 — Architecture](#-chapter-9--architecture)
- [ Chapter 8 — Setup](#️-chapter-10--setup)
- [ Chapter 9 — Example Queries](#-chapter-11--example-queries)
- [ Chapter 10 — Deployment](#-chapter-12--deployment)

---


# Chapter 1 — What Is RAG?

**RAG (Retrieval-Augmented Generation)** is a method where an AI model like GPT:

- **Retrieves** information from your own documents  
- **Generates** an answer based on that information  

This makes answers accurate, up-to-date, and grounded in your real data.

###  Example

**Without RAG:**  
“What's our leave policy?”  
→ GPT may guess or hallucinate because it has no idea what exact conext you are talking about.

**With RAG:**  
GPT finds the right text from your company documents and answers based on that.

![RAG Concept](./docs/images/RAG_pipeline.png)

Here is the detailed concept for RAG : [RAG and its concepts](./docs/03_RAG_concept.md)

---

# Chapter 2 — What Is a Vector Database?

A vector database stores text as **embeddings** — mathematical representations of meaning.  
This allows the system to search by *meaning*, not keywords.


### Simple Example

```python
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
texts = ["21 days annual leave", "Smoking is not allowed indoors"]

db = Chroma.from_texts(texts, embeddings)
results = db.similarity_search("What is the smoking rule?")
print(results[0].page_content)
```

![Vector Concept](./docs/images/Vectors.png)


Here is the detailed concept for Vecotr database : [Vector databases and Metadata filtering](./docs/02_vector_database.md)

---

# Chapter 3 — What This Project Does

This project connects directly to your Notion pages (such as **Company Policy** or **Onboarding Process**) using the Notion API.  
It then generates embeddings, stores them in a vector database, and provides an interactive **Streamlit chat interface** for querying your knowledge base.

---

##  Features

- Connects to live Notion content via API  
- Automatically builds and updates a vector database  
- Produces structured, well-formatted answers using GPT  
- Clean and intuitive Streamlit chat interface  
- Easy to deploy — runs with a single command

## Project Architecture


<div style="font-family: Arial, sans-serif;">

  <div style="
      padding: 10px 20px;
      border: 2px solid #4a90e2;
      border-radius: 8px;
      display: inline-block;
      margin-bottom: 6px;
      font-weight: bold;
  ">
    User
  </div>

  <div style="font-size: 20px; text-align: center;">↓</div>

  <div style="
      padding: 10px 20px;
      border: 2px solid #4a90e2;
      border-radius: 8px;
      display: inline-block;
      margin-bottom: 6px;
      font-weight: bold;
  ">
    Streamlit App (query_engine.py)
  </div>

  <div style="font-size: 20px; text-align: center;">↓</div>

  <div style="
      padding: 10px 20px;
      border: 2px solid #4a90e2;
      border-radius: 8px;
      display: inline-block;
      margin-bottom: 6px;
      font-weight: bold;
  ">
    Vector DB (Chroma)
  </div>

  <div style="font-size: 20px; text-align: center;">↓</div>

  <div style="
      padding: 10px 20px;
      border: 2px solid #4a90e2;
      border-radius: 8px;
      display: inline-block;
      margin-bottom: 6px;
      font-weight: bold;
  ">
    LLM (GPT-4 / GPT-5)
  </div>

  <div style="font-size: 20px; text-align: center;">↓</div>

  <div style="
      padding: 10px 20px;
      border: 2px solid #4a90e2;
      border-radius: 8px;
      display: inline-block;
      margin-bottom: 6px;
      font-weight: bold;
  ">
    Structured, Sourced Answer
  </div>

</div>




<div align="center">

# 💼 Vector Search with RAG

A lightweight RAG system that pulls content from Notion, builds a vector database with Chroma, and answers questions using GPT.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red)
![Chroma](https://img.shields.io/badge/ChromaDB-Vector%20Search-green)
![Notion](https://img.shields.io/badge/Notion-API-black)
![License](https://img.shields.io/badge/License-MIT-yellow)

</div>

#  Vector Search with RAG

A simple tool that connects to Notion, turns your company documents into a searchable vector database using Chroma, and lets you ask questions through a Streamlit chat interface. Employees can quickly find information from policies and internal guides using natural language.

---

## 📘 Table of Contents
- [ Vector Search with RAG](#-vector-search-with-rag)
- [ Chapter 1 — What Is RAG?](#-chapter-1--what-is-rag)
- [ Chapter 2 — What Is a Vector Database?](#-chapter-2--what-is-a-vector-database)
- [ Chapter 3 — Why Use RAG?](#-chapter-3--why-use-rag)
- [ Chapter 4 — What This Project Does](#-chapter-4--what-this-project-does)
- [ Chapter 5 — How It Works (Sequence Diagram)](#-chapter-5--how-it-works-sequence-diagram)
- [ Chapter 6 — Setting Up Notion](#-chapter-6--setting-up-notion)
- [ Chapter 7 — How ChromaDB Works](#-chapter-7--how-chromadb-works)
- [ Chapter 8 — The Streamlit App](#-chapter-8--the-streamlit-app)
- [ Chapter 9 — Architecture](#-chapter-9--architecture)
- [ Chapter 10 — Setup](#️-chapter-10--setup)
- [ Chapter 11 — Example Queries](#-chapter-11--example-queries)
- [ Chapter 12 — Deployment](#-chapter-12--deployment)

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

Here is the detailed concepts for RAG [RAG and its concepts](./docs/xys_app.md)
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
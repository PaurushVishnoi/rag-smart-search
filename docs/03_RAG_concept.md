# Retrieval-Augmented Generation (RAG) — Concepts

## What is RAG?
RAG stands for **Retrieval-Augmented Generation**.

It is a technique where a generative AI model (like an LLM) is given the ability to look up extra information from an external data source before answering a question.

### How it normally works:
- A regular LLM uses only:
  - What it learned during training  
  - What you type in the prompt  

### How RAG improves this:
With RAG, the model can also **search a knowledge base**, find relevant information, and use it while generating an answer.

---

## Why is RAG Needed?

Without RAG, a language model might:
- Give **wrong information**
- Give **outdated information**
- **Invent details** (hallucinations)
- Provide answers with **no source** or reference

### RAG fixes this by:
- Retrieving **real text** from stored documents  
- Combining it with the user’s question  
- Producing answers that are:
  - ✔ More accurate  
  - ✔ More current  
  - ✔ Easier to verify  

---

## But Aren’t Modern LLMs Able to Handle Long Prompts?
Yes — today’s models can handle **128,000+ tokens** (around 96,000 words).  
However, there are still major limitations:

### Problems with depending only on long context:
1. **The user must provide the information**  
   The model cannot access external documents by itself.

2. **Some documents are still too large**  
   Example: *War and Peace* has over 560,000 words — far beyond the context limit.

3. **Too much text makes it harder for the model to focus**  
   Important details can get buried.

4. **Long prompts take more processing time**

5. **More tokens = more money**

---

## ✔ How RAG Helps
RAG solves these problems by:

- Automatically finding the needed information  
- Retrieving only **small, relevant chunks**  
- Keeping the prompt short and focused  
- Reducing cost and processing time  
- Helping the model avoid hallucinations  

---

## How RAG Works (Simple Steps)

The following diagram illustrates the RAG process for a basic RAG system. This diagram represents the core concept well, as all variations of RAG rely on the same main idea shown here:

![RAG Concept](./images/RAG_pipeline.png)

### **1. Collect your information**
Gather documents like:
- PDFs  
- Manuals  
- Policies  
- Notes  
- Any data you want the system to use  

---

### **2. Split and embed the information**
- Large documents are **broken into smaller chunks**
- Each chunk is converted into a **vector**  
  (a list of numbers representing the meaning of the text)

---

### **3. Store the vectors**
- All vectors are saved in a **vector database**
  - Examples: FAISS, ChromaDB, Milvus

---

### **4. Get the user’s question**
- The user enters a prompt or question.

---

### **5. Embed the question**
- The question is also converted into a vector using the **same embedding model** used for the documents.

---

### **6. Retrieve matching information**
- The system compares the question vector with stored vectors.
- It finds the **most similar** and **most relevant** chunks.

---

### **7. Build an augmented prompt**
The system combines:
- The user’s question  
- The retrieved text  

This creates the **augmented prompt** used by the LLM.

---

### **8. Generate the final answer**
The LLM reads the augmented prompt and produces a response using:
- Its own internal knowledge  
- The retrieved external information  

This results in **more accurate and trustworthy answers**.

---

## Summary
RAG improves AI responses by giving models access to external information.  
It helps reduce errors, avoid hallucinations, lower costs, and ensure answers are backed by real data.


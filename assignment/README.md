# 🎭 PersonaForge: Your Digital Footprint as Persona

> “Reconstruct real Reddit personas with explainable AI – powered by embeddings, vector search, and local language models.”


![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![FAISS](https://img.shields.io/badge/FAISS-VectorSearch-orange)
![SentenceTransformers](https://img.shields.io/badge/SentenceTransformer-Embeddings-purple)
![Ollama](https://img.shields.io/badge/Ollama-Mistral_7B-black)
![RAG](https://img.shields.io/badge/Architecture-RAG-brightgreen)
![Reddit](https://img.shields.io/badge/API-Reddit-blueviolet)
![Contributions Welcome](https://img.shields.io/badge/Contributions-Welcome-yellowgreen)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)
---
---

## 📊 How It Works: Workflow Explained

Here’s how the system works from start to finish:
     ┌──────────────────────┐
     │  Reddit Username /   │
     │   Profile URL        │
     └────────┬─────────────┘
              │
              ▼
     ╔════════════════╗
     ║  PRAW          ║  ← Reddit API fetches posts/comments
     ╚════════════════╝
              │
              ▼
     ╔═════════════════════════╗
     ║ SentenceTransformer     ║ ← Embeds each post/comment into a vector
     ║ (MiniLM-L6-v2)          ║
     ╚═════════════════════════╝
              │
              ▼
     ╔═════════════════════════╗
     ║      FAISS Index        ║ ← Stores all semantic vectors
     ╚═════════════════════════╝
              │
     ┌────────▼────────┐
     │  RAG Retrieval  │ ← For each persona field (habits, goals, etc.)
     └────────┬────────┘
              │
    Uses Top-N Most Relevant Reddit Snippets
              │
              ▼
     ╔═════════════════════════╗
     ║    Local LLM (Mistral)  ║ ← Via Ollama
     ╚═════════════════════════╝
              │
   Returns rich persona text with source links
              ▼
     ╔═════════════════════╗
     ║ persona_report.txt  ║ ← Output is saved with link-backed citations
     ╚═════════════════════╝
****

---

## 📦 Core Technologies & Axioms

| 🔧 Component         | 💬 Description |
|----------------------|-----------------|
| ![PRAW](https://img.shields.io/badge/Reddit%20API-PRAW-red) | Fetches public posts/comments for any Reddit user |
| ![Embedding](https://img.shields.io/badge/NLP-Embeddings-purple) | `all-MiniLM-L6-v2` from SentenceTransformer to convert posts into vectors |
| ![FAISS](https://img.shields.io/badge/VectorStore-FAISS-orange) | Fast Approximate Nearest Neighbor Search (for retrieving similar posts/comments) |
| ![Ollama](https://img.shields.io/badge/LLM-Mistral_7B-lightgrey) | Local language model run via Ollama for natural language reasoning |
| ![RAG](https://img.shields.io/badge/Methodology-RAG-green) | Retrieval-Augmented Generation → respiration via vector search |
| ![Output](https://img.shields.io/badge/Output-Readable%20Persona-yellow) | Generates `.txt` report with cited evidence for all claims |

---

## 🚩 Why RAG?

**RAG (Retrieval-Augmented Generation)** combines two ideas:
- 📚 **Retrieval:** Before asking a question (e.g. "What are the user’s motivations?"), it retrieves the most semantically relevant Reddit posts from the user's history.
- 🤖 **Generation:** Then it passes those to a local LLM (Mistral) to **generate** the answer using only that evidence.

### 🔐 Benefits:
- **Grounded in real content**
- **Citations are traceable with Reddit permalink links**
- **Works offline** — No OpenAI API, No cloud LLMs
- **User privacy respected**

---

## 🎯 What Makes PersonaForge Special?

✅ Local-first Privacy  
✅ Fully Explainable Personas  
✅ Cites real Reddit links for every claim  
✅ Modular + Extensible (drop in new LLM, fields, custom template)

---

## ▶️ Example Persona Output
=== MOTIVATION ===
The user is motivated by seeking ways to stretch their money (Snippet [1], Link: https://reddit.com/r/Frugal/comments/15szxcx/how_do_you_decide_what_to_buy_and_not_buy/), learning about the experiences of H1B holders in the US (Snippets [4], [6]), and expressing gratitude for the opportunities they've found in the US as an H1B holder (Snippet [7], Link: https://reddit.com/r/AskReddit/comments/1hnx8j0/h1b_holders_what_are_your_thoughts_on_the/m4560kx/). They also seem interested in discussing the topic of exploitation of H1B holders (Snippets [4], [6]).

Citations:
- https://reddit.com/r/Frugal/comments/15szxcx/how_do_you_decide_what_to_buy_and_not_buy/
- https://reddit.com/r/AskReddit/comments/1hnx7lj/h1b_holders_do_you_feel_exploited_or_see_it_as_an/
- https://reddit.com/r/AskReddit/comments/1hnx8j0/h1b_holders_what_are_your_thoughts_on_the/


---



---



---
## 🚀 Quick Start

### 1️⃣ Prerequisites

- **Python 3.8+**
- **Git**

---

### 2️⃣ Ollama & Mistral Setup (Local LLM)

1. **Install Ollama**  
   - Go to [https://ollama.com/download](https://ollama.com/download)  
   - Download and install for your OS (Windows, macOS, or Linux)
2. **Pull the Mistral model for local inference**  
   Open a terminal and run:
   ollama pull mistral

---

### 3️⃣ Install Python Requirements

1. **Clone this repo:**
git clone https://github.com/yourusername/PersonaForge.git
cd PersonaForge

2. **Install dependencies:**
pip install -r requirements.txt

---

### 4️⃣ Install SentenceTransformer Model Locally

This project requires the embedding model  
`sentence-transformers/all-MiniLM-L6-v2`  
to be downloaded and stored locally for private and fast processing.

#### Run this setup script in your terminal or Python shell:
from sentence_transformers import SentenceTransformer
SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

This will **download the model to your cache** (`~/.cache/torch/sentence_transformers/` by default).  
No extra step is needed if you’ve done this once—future runs will use the local copy!

*If you want model files in a custom folder, use:*
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2', cache_folder='your/model/path')

Then point `EMBEDDING_MODEL_PATH` in the config to that directory.

---

### 5️⃣ Reddit API Credentials

1. Go to [https://www.reddit.com/prefs/apps](https://www.reddit.com/prefs/apps)
2. Create an app ("script" type)
3. Add your `client_id`, `client_secret`, and set a `user_agent`  
   Example is shown in `reddit_persona.py`

---

### 6️⃣ Run the Pipeline

In terminal:
python assignment/pyscript final code.py
(remember to change the paths in the code)

To see Full implementation with explanation look at the assigment.ipynb

- The persona profile and all evidence will be saved in `assignment/persona_report.txt`

---

## 🛠️ Folder Structure
assignment/

├── requirements.txt

├── README.md

└── assignment.ipynb

└── pyscript final code.py

├── persona_report-1.txt

├── persona_report-2.txt

└── reddit_user_data-1.json

└── reddit_user_data-2.json

---

## ⚡ requirements.txt

praw==7.7.1
sentence-transformers==2.2.2
faiss-cpu==1.7.4
numpy==1.24.3
*Ollama and your embedding model are managed outside pip.*

---

## ⭐ Features

- 📨 Scrapes Reddit posts/comments by username or URL.
- 🧮 Embeds content semantically with **MiniLM L6**.
- 🔍 RAG with **local FAISS** vector DB for efficient evidence retrieval.
- 🤖 Local inference with **Mistral LLM via Ollama**.
- 🔗 Evidence-rich persona profiles with direct Reddit links.
- 🛡️ 100% offline/private model execution, no cloud LLM needed.

---


---

## 🤝 Need Help?

- [Ollama Support](https://ollama.com/)
- [Sentence-Transformers Docs](https://www.sbert.net/)
- [Reddit/PRAW Documentation](https://praw.readthedocs.io/)

---
## To contact me 
email: velamalapavankrishna@gmail.com
insta: pavankrishna_v

Thank you! 🧠✨



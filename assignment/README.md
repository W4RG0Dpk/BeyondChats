# 🎭 PersonaForge: Reddit User Persona Generator

Turn real Reddit conversations into richly-cited, AI-generated user personas.  
Built on local semantic search, Retrieval-Augmented Generation (RAG), and private LLM inference—**no data leaves your device.**

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



import praw
import re
import json
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import subprocess
import os

# Your Reddit API credentials
REDDIT_CREDENTIALS = {
    "client_id": "Ze0l8Tb5iILjJLTDxKRflA",
    "client_secret": "PcqO8CtAQO7pIoGuotuNeb_qPWrAMQ",
    "user_agent": "my_reddit_scraper"
}

# Path to your local SentenceTransformer model folder
EMBEDDING_MODEL_PATH = r"C:\amrita_uni\Projects\BeyondChats\model"

# Persona fields to extract
PERSONA_FIELDS = [
    "gender", "age", "build", "hair", "skin tone", "clothing", "setting", "posture",
    "overall impression", "fashion sense", "lifestyle cues", "frustrations", "behaviors",
    "habits", "goals and needs", "motivation", "personality", "persona quote"
]

def extract_username(url):
    match = re.search(r'reddit\.com/user/([^/?]+)', url)
    return match.group(1) if match else url


def fetch_and_save_reddit_user_data(reddit, profile_url, save_path='reddit_user_data.json', limit=100):
    username = extract_username(profile_url)
    user = reddit.redditor(username)
    data = []
    for post in user.submissions.new(limit=limit):
        data.append({
            'type': 'post',
            'title': post.title,
            'body': post.selftext,
            'permalink': f'https://reddit.com{post.permalink}',
            'subreddit': str(post.subreddit)
        })
    for comment in user.comments.new(limit=limit):
        data.append({
            'type': 'comment',
            'body': comment.body,
            'permalink': f'https://reddit.com{comment.permalink}',
            'subreddit': str(comment.subreddit)
        })
    with open(save_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f" Saved {len(data)} posts/comments to {save_path}")


def load_reddit_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def build_faiss_index(docs, embedding_model_path):
    model = SentenceTransformer(embedding_model_path)
    print(" Embedding documents...")
    texts = [
        f"Title: {doc['title']}\nBody: {doc['body']}" if doc['type'] == 'post' else doc['body']
        for doc in docs
    ]
    embeddings = model.encode(texts, convert_to_numpy=True, show_progress_bar=True)
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)
    return index, docs, model


def retrieve_docs(query, index, docs, model, k=7):
    emb = model.encode([query], convert_to_numpy=True)
    D, I = index.search(emb, k)
    return [docs[i] for i in I[0]]

def build_prompt_for_field(field, docs):
    prompt = (f"Based on these numbered Reddit snippets, describe the user's {field}."
              f"\n- Every factual claim must cite the snippet number *and* the link as (Snippet [N], Link: ...)."
              f"\n- At the end, write 'Citations:' and list all links you cited (not unreferenced ones)."
              "\nExample:\n"
              '"The user lives in NYC (Snippet [2], Link: https://reddit.com/r/nyc/comments/xyz123/NYC_life/)".\n\n'
              "Snippets:\n")
    for i, doc in enumerate(docs, 1):
        text = (f"{doc.get('title', '')} {doc.get('body', '')}" if doc['type'] == 'post' else doc.get('body', ''))
        text = text.replace('\n', ' ').strip()
        snippet = text[:240]
        prompt += f"[{i}] \"{snippet}\" (Link: {doc['permalink']})\n"
    prompt += "\nYour answer:"
    return prompt




def run_ollama_mistral(prompt):
    result = subprocess.run(
        ['ollama', 'run', 'mistral'],
        input=prompt,
        text=True,
        capture_output=True,
        encoding='utf-8'
    )
    return result.stdout


def persona_pipeline(profile_url, persona_fields, reddit_credentials, embedding_model_path, docs_limit=70, output_path='persona_output.txt'):
    # Reddit setup
    reddit = praw.Reddit(
        client_id=reddit_credentials['client_id'],
        client_secret=reddit_credentials['client_secret'],
        user_agent=reddit_credentials['user_agent']
    )
    
    # Step 1: Fetch and save posts/comments
    fetch_and_save_reddit_user_data(reddit, profile_url, 'reddit_user_data.json', limit=docs_limit)
    
    # Step 2: Load data and build FAISS index
    docs = load_reddit_data('reddit_user_data.json')
    index, meta, embed_model = build_faiss_index(docs, embedding_model_path)
    
    # Step 3: Generate persona field-by-field
    results = {}
    with open(output_path, 'w', encoding='utf-8') as f_out:
        f_out.write(f" Persona Report for Reddit User: {extract_username(profile_url)}\n\n")
        for field in persona_fields:
            print(f" Generating {field}...")
            context = retrieve_docs(field, index, meta, embed_model, k=7)
            prompt = build_prompt_for_field(field, context)
            answer = run_ollama_mistral(prompt)
            results[field] = answer.strip()
            f_out.write(f"\n=== {field.upper()} ===\n{answer.strip()}\n")
    
    print(f"\nPersona report saved to: {output_path}")
    return results


if __name__ == "__main__":

    reddit_user_url = "https://www.reddit.com/user/Hungry-Move-6603/"  

    persona_output = persona_pipeline(
        profile_url=reddit_user_url,
        persona_fields=PERSONA_FIELDS,
        reddit_credentials=REDDIT_CREDENTIALS,
        embedding_model_path=EMBEDDING_MODEL_PATH,
        docs_limit=70,
        
        output_path='persona_report-2.txt'
    )


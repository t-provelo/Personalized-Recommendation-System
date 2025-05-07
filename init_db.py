import sqlite3
import pandas as pd
import numpy as np
from transformers import AutoTokenizer, AutoModel
import faiss
import torch

# Load model and tokenizer
model_name = "distilbert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

# Create SQLite database
conn = sqlite3.connect("movies.db")
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS movies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        genre TEXT,
        description TEXT
    )
""")

# Load CSV into SQLite
df = pd.read_csv("data/movies.csv")
for _, row in df.iterrows():
    cursor.execute(
        "INSERT INTO movies (title, genre, description) VALUES (?, ?, ?)",
        (row["title"], row["genre"], row["description"])
    )
conn.commit()

# Generate embeddings for descriptions
embeddings = []
for desc in df["description"]:
    inputs = tokenizer(desc, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
    embeddings.append(outputs.last_hidden_state.mean(dim=1).squeeze().numpy())
embeddings = np.array(embeddings)

# Create FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)
faiss.write_index(index, "movies_index.faiss")

conn.close()
print("Database and FAISS index created successfully!")
import streamlit as st
import sqlite3
import numpy as np
import faiss
from transformers import AutoTokenizer, AutoModel, AutoModelForCausalLM
from langchain.prompts import PromptTemplate
from langchain.llms import HuggingFacePipeline
from langchain.chains import LLMChain
import torch

# Initialize models for embeddings
embedding_model_name = "distilbert-base-uncased"
embedding_tokenizer = AutoTokenizer.from_pretrained(embedding_model_name)
embedding_model = AutoModel.from_pretrained(embedding_model_name)

# Load FAISS index
index = faiss.read_index("movies_index.faiss")

# Connect to SQLite
conn = sqlite3.connect("movies.db")
cursor = conn.cursor()

# Function to get recommendations
def get_recommendations(query, k=2):
    inputs = embedding_tokenizer(query, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = embedding_model(**inputs)
    query_embedding = outputs.last_hidden_state.mean(dim=1).squeeze().numpy()
    distances, indices = index.search(np.array([query_embedding]), k)
    recommendations = []
    for idx in indices[0]:
        cursor.execute("SELECT title, genre, description FROM movies WHERE id=?", (idx + 1,))
        recommendations.append(cursor.fetchone())
    return recommendations

# Set up LangChain for response generation
prompt_template = PromptTemplate(
    input_variables=["query", "recommendations"],
    template="User asked: {query}\nBased on this, recommend movies:\n{recommendations}\nProvide a friendly, concise explanation."
)
llm = HuggingFacePipeline.from_model_id(
    model_id="gpt2",
    task="text-generation",
    pipeline_kwargs={"max_length": 200}
)
chain = LLMChain(llm=llm, prompt=prompt_template)

# Streamlit UI
st.title("Personalized Recommendation System")
st.write("Enter your preferences (e.g., 'I like sci-fi movies with strong female leads')")
user_query = st.text_input("Your preferences:")
if st.button("Get Recommendations"):
    if user_query:
        recommendations = get_recommendations(user_query)
        rec_text = "\n".join([f"- {r[0]} ({r[1]}): {r[2]}" for r in recommendations])
        response = chain.run(query=user_query, recommendations=rec_text)
        st.write("### Recommendations")
        st.write(response)
    else:
        st.write("Please enter a query.")

conn.close()
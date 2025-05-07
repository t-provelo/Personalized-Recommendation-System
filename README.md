Personalized Recommendation System     ===============================     A natural language-based recommendation system that generates personalized suggestions (e.g., movies, books) using LLMs and vector search.
 ## Features
 - Interprets user queries with `distilbert-base-uncased` and LangChain.
 - Retrieves relevant items using FAISS and SQLite.
 - Provides a user-friendly Streamlit web interface.
 - Deployed on AWS EC2 with Docker for scalability.

 ## Installation
 ```bash
 git clone https://github.com/<your-username>/personalized-recommendation-system
 cd personalized-recommendation-system
 python3 -m venv venv
 source venv/bin/activate
 pip install -r requirements.txt
 python3 init_db.py
 streamlit run app.py
 ```

 ## Usage
 - Run locally and access at `http://localhost:8501`.
 - Enter preferences (e.g., "I like sci-fi movies") to get recommendations.

 ## Deployment
 - Containerized with Docker.
 - Deployed on AWS EC2 (see `Dockerfile`).

 ## Future Enhancements
 - User profiles for long-term personalization.
 - Integration with external APIs (e.g., IMDb).
 - Fine-tuning on domain-specific datasets.

 ## Tech Stack
 - Python, Streamlit, LangChain, Hugging Face Transformers
 - FAISS, SQLite, Docker, AWS EC2


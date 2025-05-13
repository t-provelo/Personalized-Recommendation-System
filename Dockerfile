# Use Python 3.12 slim base image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies for faiss-cpu, pandas, Rust, and build tools
RUN apt-get update && apt-get install -y \
    libatlas-base-dev \
    gfortran \
    libopenblas-dev \
    liblapack-dev \
    curl \
    swig \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Rust
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

# Install setuptools, wheel, and numpy binary
RUN pip install --no-cache-dir setuptools==74.1.2 wheel==0.44.0 numpy==1.24.3

# Copy requirements.txt
COPY requirements.txt .

# Install remaining Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY app.py init_db.py test_deps.py ./
COPY data/ data/

# Initialize database and FAISS index
RUN python3 init_db.py

# Expose Streamlit port
EXPOSE 8501

# Run Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
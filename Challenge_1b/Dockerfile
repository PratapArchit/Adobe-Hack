# Base image
FROM python:3.10-slim

# Set working directory inside the container
WORKDIR /app

# Install system dependencies required for PyMuPDF and NLP
RUN apt-get update && apt-get install -y \
    build-essential \
    libpoppler-cpp-dev \
    gcc \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements.txt to container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Download NLTK resources offline
RUN python -m nltk.downloader -d /app/nltk_data punkt stopwords averaged_perceptron_tagger wordnet

# Download and cache SentenceTransformer model for offline use
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2').save('/app/models/all-MiniLM-L6-v2')"

# Copy project files into container
COPY . .

# Set environment variables for NLTK and model path
ENV NLTK_DATA=/app/nltk_data
ENV MODEL_PATH=/app/models/all-MiniLM-L6-v2

# Default command to run the program
CMD ["python", "main.py", "--input", "input.json"]

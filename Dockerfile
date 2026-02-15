FROM python:3.11-slim

WORKDIR /app

# Install system dependencies if any (none obvious, but good practice to keep in mind)
# RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Download spaCy model
RUN python -m spacy download en_core_web_sm

COPY . .

# Create directories for upload and output
RUN mkdir -p uploads outputs

EXPOSE 8080

CMD ["python", "app.py"]

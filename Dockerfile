FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV AGENT_ID=p2pclaw-crypto-agent \
    AGENT_NAME="P2PCLAW Crypto Agent" \
    P2P_API_BASE=https://api-production-ff1b.up.railway.app \
    NVIDIA_MODEL=nvidia/llama-3.3-nemotron-70b-instruct \
    NVIDIA_MODEL_FAST=nvidia/llama-3.1-nemotron-70b-instruct
CMD ["python", "agent.py"]

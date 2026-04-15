FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y --no-install-recommends \
    nodejs npm \
    && npm install -g @anthropic-ai/claude-code@2.1.104 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=app
ENV FLASK_ENV=development
ENV PYTHONPATH=/app

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000", "--reload"]

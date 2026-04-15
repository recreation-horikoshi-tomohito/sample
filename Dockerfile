FROM python:3.12

WORKDIR /app

RUN apt-get update && apt-get install -y \
    git \
    nodejs npm \
    && npm install -g @anthropic-ai/claude-code@2.1.104 \
    && rm -rf /var/lib/apt/lists/*

# uv導入
RUN pip install --upgrade pip && pip install uv

# spec-kit CLI
RUN uv tool install specify-cli --from git+https://github.com/github/spec-kit.git

# PATH通す（超重要）
ENV PATH="/root/.local/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=app
ENV FLASK_ENV=development
ENV PYTHONPATH=/app

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000", "--reload"]

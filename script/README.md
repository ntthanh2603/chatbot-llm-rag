### Đăng nhập hugkingface, chạy lệnh này trong cmd và dán token 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

```bash
huggingface-cli login

```

### Windown

```bash
python -m venv venv

.\venv\Scripts\Activate.ps1

pip install -r script/requirements.txt
```

### Linux

```bash
python3 -m venv venv

source script/venv/bin/activate

pip install -r script/requirements.txt
```

### Use container ChromaDb

```bash
# Check version docker
docker -v

# Create container
docker compose up -d

# Delete container and volumn
docker compose down -v
```

### Run file python with model default is google/gemma-3-4b-it

```bash
# Run in CPU
python -m script.main

# Run in GPU
python -m script.main --gpu

# Run in GPU  4 bit
python -m script.main --gpu --4bit

# Model other
python -m script.main --model "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

# Not use RAG
python -m script.main --no-rag
```

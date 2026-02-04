# 🎮 OMEGA GPU Setup Guide

> *"Harness the power of Ada Lovelace for the Pantheon."*

## 🔱 Overview

OMEGA uses GPU acceleration for:
- **Embedding Generation** (embedding_accel) - Semantic vector embeddings for Chronicle memory
- **Audio Transcription** (whisper_transcriber) - Speech-to-text using OpenAI Whisper

This guide covers setup for **NVIDIA RTX 3500 Ada Generation** and similar GPUs.

---

## 🖥️ Hardware Requirements

### Minimum Requirements
- **GPU**: NVIDIA GPU with CUDA Compute Capability 8.0+
- **VRAM**: 4GB minimum (8GB recommended)
- **Driver**: NVIDIA Driver 525.60.13 or newer

### Tested Hardware
- ✅ **NVIDIA RTX 3500 Ada Generation** (5,120 CUDA cores, 8GB VRAM)
- ✅ NVIDIA RTX 3060/3070/3080/3090 (Ampere)
- ✅ NVIDIA RTX 4060/4070/4080/4090 (Ada Lovelace)

---

## 🔧 Prerequisites

### Windows (WSL2)

1. **Install WSL2**
   ```powershell
   wsl --install
   wsl --set-default-version 2
   ```

2. **Install NVIDIA Drivers** (on Windows, NOT in WSL)
   - Download from: https://www.nvidia.com/Download/index.aspx
   - Version 525.60.13 or newer

3. **Install Docker Desktop**
   - Download from: https://www.docker.com/products/docker-desktop
   - Enable WSL2 backend in settings
   - Enable GPU support in Docker Desktop settings

4. **Verify GPU Access**
   ```powershell
   # In PowerShell
   nvidia-smi
   
   # In WSL2
   wsl
   nvidia-smi
   ```

### Linux

1. **Install NVIDIA Drivers**
   ```bash
   sudo apt-get update
   sudo apt-get install -y nvidia-driver-525
   ```

2. **Install nvidia-container-toolkit**
   ```bash
   distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
   curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
   curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | \
       sudo tee /etc/apt/sources.list.d/nvidia-docker.list
   
   sudo apt-get update
   sudo apt-get install -y nvidia-container-toolkit
   sudo systemctl restart docker
   ```

3. **Verify GPU Access**
   ```bash
   nvidia-smi
   docker run --rm --gpus all nvidia/cuda:12.2.0-base-ubuntu22.04 nvidia-smi
   ```

---

## 🏗️ Building GPU Services

### Quick Start

**Windows (PowerShell):**
```powershell
cd D:\Repos\OMEGA\omega-core
.\scripts\build_gpu_services.ps1
```

**Linux/WSL2 (Bash):**
```bash
cd /path/to/omega-core
chmod +x scripts/build_gpu_services.sh
./scripts/build_gpu_services.sh
```

### Manual Build

```bash
# 1. Build base GPU image
docker build -f Dockerfile.omega-base-gpu -t omega-base-gpu:latest .

# 2. Build embedding accelerator
docker build -f Dockerfile.embedding_accelerator -t omega/embedding-accel:latest .

# 3. Build whisper transcriber (optional)
docker build -f Dockerfile.whisper_transcriber -t omega/whisper-transcriber:latest .
```

---

## 🚀 Running GPU Services

### Start Chronicle Integration (with GPU)

```bash
docker-compose up -d \
  mongodb \
  redis \
  qdrant \
  chronicle \
  embedding_accel \
  federation_core \
  context_server \
  chronicle_memory_sharding
```

### Verify GPU Usage

```bash
# Check if CUDA is available in container
docker exec embedding_accel python3 -c "import torch; print(f'CUDA Available: {torch.cuda.is_available()}'); print(f'GPU Name: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else \"N/A\"}')"

# Monitor GPU usage in real-time
nvidia-smi -l 1  # Linux/WSL2
# or
nvidia-smi  # Windows PowerShell (run repeatedly)
```

Expected output:
```
CUDA Available: True
GPU Name: NVIDIA GeForce RTX 3500 Ada Generation Laptop GPU
```

---

## 📊 GPU Monitoring

### Real-Time Monitoring

**Linux/WSL2:**
```bash
watch -n 1 nvidia-smi
```

**Windows PowerShell:**
```powershell
while ($true) { cls; nvidia-smi; Start-Sleep -Seconds 1 }
```

### Check GPU Memory Usage

```bash
nvidia-smi --query-gpu=name,memory.used,memory.total,utilization.gpu --format=csv
```

### Docker Container GPU Stats

```bash
docker stats embedding_accel
```

---

## 🔍 Troubleshooting

### Issue: "CUDA not available" in container

**Solution:**
```bash
# Verify Docker GPU support
docker run --rm --gpus all nvidia/cuda:12.2.0-base-ubuntu22.04 nvidia-smi

# If this fails, reinstall nvidia-container-toolkit (Linux)
sudo apt-get install --reinstall nvidia-container-toolkit
sudo systemctl restart docker

# For Windows, ensure Docker Desktop GPU support is enabled
```

### Issue: "nvidia/cuda:12.2.0-cudnn8-runtime-ubuntu22.04: not found"

**Solution:**
```bash
# Pull the base image manually
docker pull nvidia/cuda:12.2.0-cudnn8-runtime-ubuntu22.04

# Then rebuild
docker build -f Dockerfile.omega-base-gpu -t omega-base-gpu:latest .
```

### Issue: Out of GPU memory

**Solution:**
```bash
# Reduce batch size in embedding_accelerator_tool.py
# Or use a smaller model

# Check current GPU memory
nvidia-smi --query-gpu=memory.used,memory.total --format=csv
```

### Issue: Slow embedding generation

**Possible causes:**
1. GPU not being used (check with `nvidia-smi`)
2. Model not loaded on GPU
3. CPU fallback mode

**Solution:**
```bash
# Verify GPU is being used
docker exec embedding_accel python3 -c "
import torch
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')
print(f'Model device: {model.device}')
print(f'CUDA available: {torch.cuda.is_available()}')
"
```

---

## 🎯 Performance Benchmarks

### RTX 3500 Ada Generation (5,120 CUDA cores, 8GB VRAM)

| Task | Batch Size | Throughput | GPU Utilization |
|------|-----------|------------|-----------------|
| Embedding Generation (384-dim) | 32 | ~500 texts/sec | 60-80% |
| Whisper Transcription (base) | 1 | ~10x realtime | 40-60% |

### Expected GPU Memory Usage

| Service | Model | VRAM Usage |
|---------|-------|------------|
| embedding_accel | all-MiniLM-L6-v2 | ~500MB |
| whisper_transcriber | whisper-base | ~1GB |
| whisper_transcriber | whisper-large | ~3GB |

---

## 🔱 Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    NVIDIA RTX 3500 Ada                       │
│                  (5,120 CUDA cores, 8GB VRAM)                │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                  CUDA 12.2 + cuDNN 8                         │
│              (nvidia/cuda:12.2.0-cudnn8-runtime)             │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                  OMEGA Base GPU Image                        │
│         (Python 3.10 + PyTorch 2.1.2 + CUDA 12.1)            │
└────────────────────────┬────────────────────────────────────┘
                         │
         ┌───────────────┴───────────────┐
         ▼                               ▼
┌──────────────────┐          ┌──────────────────┐
│ embedding_accel  │          │whisper_transcriber│
│   (Port 9219)    │          │   (Port 9221)     │
│                  │          │                   │
│ • Sentence       │          │ • OpenAI Whisper  │
│   Transformers   │          │ • Audio → Text    │
│ • 384-dim vectors│          │ • Multi-language  │
└──────────────────┘          └──────────────────┘
```

---

## 📚 References

- [NVIDIA CUDA Documentation](https://docs.nvidia.com/cuda/)
- [PyTorch CUDA Support](https://pytorch.org/get-started/locally/)
- [Docker GPU Support](https://docs.docker.com/config/containers/resource_constraints/#gpu)
- [Sentence Transformers](https://www.sbert.net/)
- [OpenAI Whisper](https://github.com/openai/whisper)

---

## 🔱 The GPU Awakens

**Your RTX 3500 Ada is ready to serve the Pantheon.**
**Family is forever. This is the way.** ⚔️


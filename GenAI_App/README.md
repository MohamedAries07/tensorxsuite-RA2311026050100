# RA100 TensorX Suite 🩺⚡

**RA100 TensorX** is a cutting-edge Explainable AI (XAI) suite that bridges high-performance model serving with Generative AI insights. It leverages the speed of NVIDIA TensorRT and the intelligence of Large Language Models (LLMs) to provide transparent, human-readable diagnostic analysis.

## 🚀 Key Features
- **Inference Optimization**: Simulated high-performance engine based on **NVIDIA TensorRT v8.6**.
- **Explainable AI (XAI)**: Integrated with **Groq (Llama-3.3-70b)** to translate technical tensor data into plain-English insights.
- **Dynamic Input**: Supports natural language descriptions for symptom analysis and system monitoring.
- **Markdown Reporting**: Beautifully formatted, interactive reports with headers, bold text, and bullet points.
- **Containerized Architecture**: Fully Dockerized for seamless deployment.

## 🛠️ Built With
- **Frontend**: HTML5, Vanilla CSS, JavaScript (ES6), Marked.js
- **Backend**: Python (Flask)
- **AI Engine**: Groq SDK (Llama-3.3-70b-versatile)
- **Serving**: NVIDIA TensorRT (Inference Logic)
- **Deployment**: Docker, Gunicorn

## 📦 Quick Start (Docker)
You can run the application directly from the public DockerHub image:
```bash
docker pull ra2311026050077/ra100-tensorx
docker run -p 5000:5000 --env-file .env ra2311026050077/ra100-tensorx
```

## 📜 Credits & Acknowledgments
This project is built upon and inspired by the industry-standard high-performance inference libraries.
- **Core Technology**: [NVIDIA TensorRT](https://github.com/NVIDIA/TensorRT)
- **XAI Engine**: Powered by Groq Cloud Inference.
- **Research Framework**: Part of the RA100 Research Initiative.

---
*Special thanks to the NVIDIA team for providing the foundational TensorRT libraries that make high-speed inference possible.*

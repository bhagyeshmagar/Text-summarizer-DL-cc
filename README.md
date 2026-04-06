# Deep Learning & Cloud Computing Mini Project: Text Summarization

A full-stack, decoupled text summarization web application. Built as a comprehensive **Deep Learning and Cloud Computing mini project**, this application extracts the most meaningful sentences from any text payload using a suite of statistical, NLP, and Deep Learning algorithms, and is designed specifically to be deployed to scalable cloud infrastructure.

Originally developed in Streamlit, this architecture has been completely rewritten and upgraded into a modern decoupled stack to demonstrate industry-standard deployment practices.

---

## 🧠 Deep Learning & Architecture

### ⚡ Backend API (FastAPI / Python)
- **FastAPI:** High-performance async REST framework serving the API on `http://localhost:8000`.
- **Deep Learning & NLP Models:** Incorporates HuggingFace-compatible transformer models (via `transformers_based_summary.py`), classical statistical summarizations (Lex Rank, Text Rank, LSA via `sumy`), and core Python tokenization based on frequency logic.
- **NLTK Processing:** Implements natural language toolkits for robust stopwords processing and word ranking.

### 🎨 Frontend UI (React / Vite)
- **React.js & Vite:** A blazing fast frontend ecosystem.
- **Custom UI System:** A bespoke, zero-dependency CSS architecture inspired by the bold contrast of NothingOS and the smooth, organic rounded cards of OneUI.

---

## ☁️ Cloud Computing & AWS Deployment

This project serves as a practical demonstration of Cloud Computing principles, illustrating how to deploy decoupled microservice-like architectures to the cloud. 

We have compiled a rigorous, step-by-step guide explaining how to deploy this exact full-stack application safely and performantly using an **AWS EC2 instance**, **Nginx** (Reverse Proxy), and **Gunicorn/Uvicorn** (Process Managers).

👉 **[Read the AWS Deployment Guide Here](./aws_deployment_guide.md)**

---

## 🚀 Running the Application Locally

The application comprises two separate processes. Both need to be running for the app to function.

### 1. Start the Backend API
Open a terminal in the root directory:
```bash
# Create and activate your virtual environment (if not already done)
python3 -m venv venv_linux
source venv_linux/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the FastAPI server (auto-reloads on code changes)
uvicorn app:app --port 8000 --reload
```
*The API is now running and accepting connections on `http://127.0.0.1:8000`*

### 2. Start the Frontend UI
In a **new** terminal window:
```bash
# Navigate to the frontend directory
cd frontend

# Install Node modules
npm install

# Start the Vite development server
npm run dev
```
*You can now view the app in your browser at `http://localhost:5173`*

---
*Developed by Bhagyesh Magar.*

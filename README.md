
<div align="center">
  <br />
  <a href="https://YOUR-STREAMLIT-APP-URL.streamlit.app/" target="_blank">
    <img src="https://i.imgur.com/g8RnjtU.png" alt="Project Banner">
  </a>
  <br />

  <div>
    <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" />
    <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
    <img src="https://img.shields.io/badge/LangChain-LangGraph-yellow?style=for-the-badge" />
  </div>

  <h3 align="center">🌐 TravelBot - AI-Powered Travel Agent</h3>

  <div align="center">
    An intelligent, conversational AI agent designed to be your personal travel assistant. Plan trips, find information, and get instant answers to all your travel queries with confidence.
  </div>
</div>

---

📋 <a name="table">**Table of Contents**</a>  
- [✨ Introduction](#introduction)  
- [⚙️ Tech Stack](#tech-stack)  
- [🔋 Features](#features)  
- [🤸 Quick Start](#quick-start)  
- [☁️ Deployment](#deployment)  
- [👨‍💻 Developer](#developer)

---

<a name="introduction">✨ **Introduction**</a>  
TravelBot is not just a chatbot; it's a sophisticated AI agent built using the powerful **LangGraph** framework. It's designed to handle complex, multi-step travel queries and utilize a suite of tools to provide accurate, real-time travel information.

From planning full itineraries to finding the cheapest flights or checking weather forecasts, TravelBot's got you covered — all inside a clean, interactive Streamlit interface.

<div align="center">
  <a href="https://YOUR-STREAMLIT-APP-URL.streamlit.app/" target="_blank">
    <img src="https://i.imgur.com/g8RnjtU.png" alt="TravelBot Demo Screenshot">
  </a>
</div>

---

<a name="tech-stack">⚙️ **Tech Stack**</a>

- **LangChain & LangGraph** – Core agent workflow and state management  
- **Groq API (Llama 3)** – Fast, intelligent language model responses  
- **Tavily Search API** – For real-time, accurate search results  
- **Streamlit** – Sleek, interactive web application  
- **Python** – Main programming language  
- **GitHub + Streamlit Cloud** – Version control & deployment

---

<a name="features">🔋 **Features**</a>

- 👉 **Smart Travel Assistant** – Understands travel-focused chat context & follow-ups  
- 👉 **Multi-Tool Integration** – Search, Weather, and Calculator all built-in  
- 👉 **Multilingual** – Talks to you in English, বাংলা (Bengali), and more  
- 👉 **Domain-Focused** – Politely avoids non-travel topics  
- 👉 **Modern UI/UX** – Clean interface with chat history & restart options  
- 👉 **Real-time Streaming** – Word-by-word bot replies, just like ChatGPT

---

<a name="quick-start">🤸 **Quick Start**</a>

### 🔧 Prerequisites
Make sure you have:
- Git  
- Python 3.8+  
- pip

### 📥 Clone the Repo
```bash
git clone https://github.com/rownokstar/Eg-Travel-Agent.git
cd Eg-Travel-Agent
```

### 🧪 Set Up Environment
```bash
python -m venv venv
# For Windows:
venv\Scripts\activate
# For Mac/Linux:
source venv/bin/activate
pip install -r requirements.txt
```

### 🔑 Add API Keys
Create `.streamlit/secrets.toml`:
```toml
[api_keys]
GROQ_API_KEY = "YOUR_GROQ_API_KEY"
TAVILY_API_KEY = "YOUR_TAVILY_API_KEY"
```

### 🚀 Run the App
```bash
streamlit run app.py
```
Open [http://localhost:8501](http://localhost:8501) in your browser.

---

<a name="deployment">☁️ **Deployment on Streamlit Cloud**</a>

1. Push the entire project to a **public GitHub repo**  
2. Sign in at [share.streamlit.io](https://share.streamlit.io)  
3. Click **New app**, select your repo  
4. In **"Secrets"**, paste the same config as `secrets.toml`  
5. Click **Deploy!**

---

<a name="developer">👨‍💻 **Developer**</a>

> **DM Shahriar Hossain**  
> Passionate about building intelligent apps with clean UI, blazing-fast APIs, and meaningful user experiences.

---

📄 **License**  
This project is licensed under the [MIT License](LICENSE).

---
```

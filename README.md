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

📋 <a name="table">Table of Contents</a>
✨ Introduction

⚙️ Tech Stack

🔋 Features

🤸 Quick Start

☁️ Deployment

👨‍💻 Developer

<a name="introduction">✨ Introduction</a>
TravelBot is not just a chatbot; it's a sophisticated AI agent built using the powerful LangGraph framework. It's designed to understand complex, multi-step travel queries and use a suite of tools to provide accurate, real-time information. Whether you need a full itinerary for a family vacation, the cheapest flight options, or weather forecasts for your destination, TravelBot is here to help.

The entire application is wrapped in a beautiful and interactive user interface created with Streamlit, making trip planning a seamless and enjoyable experience.

<div align="center">
<a href="https://YOUR-STREAMLIT-APP-URL.streamlit.app/" target="_blank">
<img src="https://i.imgur.com/g8RnjtU.png" alt="TravelBot Demo Screenshot">
</a>
</div>

<a name="tech-stack">⚙️ Tech Stack</a>
LangChain & LangGraph: For building the core agentic workflow and state management.

Groq API (Llama 3): Powers the core language model for fast and intelligent responses.

Tavily Search API: For a powerful and accurate search tool.

Streamlit: For creating and deploying the interactive web application.

Python: The core programming language for the backend logic.

GitHub: For version control and CI/CD with Streamlit Cloud.

<a name="features">🔋 Features</a>
👉 Intelligent Conversational Agent: Understands context and follows up on conversations, providing a natural chat experience.

👉 Multi-Tool Capability: Utilizes multiple tools to gather information: Web Search, Weather Forecast, and a Calculator.

👉 Multilingual Support: Capable of understanding and responding in multiple languages, including English and Bengali.

👉 Domain-Specific: Politely refuses to answer queries that are not related to travel, keeping the conversation focused.

👉 Modern UI/UX: A clean, responsive, and user-friendly interface with features like persistent chat history and new chat functionality.

👉 Real-time Streaming: Responses are streamed word-by-word, similar to modern chatbots like ChatGPT, for an engaging user experience.

<a name="quick-start">🤸 Quick Start</a>
Follow these steps to set up the project locally on your machine.

Prerequisites

Make sure you have the following installed on your machine:

Git

Python 3.8+

pip (Python Package Installer)

Cloning the Repository

git clone https://github.com/rownokstar/Eg-Travel-Agent.git
cd Eg-Travel-Agent

Installation

It's recommended to use a virtual environment.

python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
pip install -r requirements.txt

Set Up API Keys

Create a file named secrets.toml inside a .streamlit folder (.streamlit/secrets.toml). Add your API keys in the following format:

[api_keys]
GROQ_API_KEY = "YOUR_GROQ_API_KEY"
TAVILY_API_KEY = "YOUR_TAVILY_API_KEY"

Running the Project

streamlit run app.py

Open http://localhost:8501 in your browser to view the project.

<a name="deployment">☁️ Deployment on Streamlit Cloud</a>
This app is deployed on Streamlit Community Cloud. The process is straightforward:

Push the entire project folder (containing app.py and requirements.txt) to a public GitHub repository.

Sign in to share.streamlit.io with your GitHub account.

Click "New app" and choose the repository you just created.

In the "Secrets" section, add your API keys in the same format as the secrets.toml file.

Click "Deploy!".

<a name="developer">👨‍💻 Developed By</a>
DM Shahriar Hossain

📄 License
This project is licensed under the MIT License.

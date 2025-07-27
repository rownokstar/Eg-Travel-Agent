🌐 TravelBot - AI-Powered Travel Agent
An intelligent, conversational AI agent designed to be your personal travel assistant. Plan trips, find information, and get instant answers to all your travel queries with confidence.

✨ View Live Demo
(Note: Replace YOUR-STREAMLIT-APP-URL with your actual Streamlit app link after deploying.)

(How to update screenshot: Take a nice screenshot of your app, upload it to a site like Imgur, and replace the link above with your new image link.)

🚀 Project Overview
TravelBot is not just a chatbot; it's a sophisticated AI agent built using the powerful LangGraph framework. It's designed to understand complex, multi-step travel queries and use a suite of tools to provide accurate, real-time information. Whether you need a full itinerary for a family vacation, the cheapest flight options, or weather forecasts for your destination, TravelBot is here to help.

The entire application is wrapped in a beautiful and interactive user interface created with Streamlit, making trip planning a seamless and enjoyable experience.

🔑 Key Features
🤖 Intelligent Conversational Agent: Understands context and follows up on conversations, providing a natural chat experience.

🛠️ Multi-Tool Capability: Utilizes multiple tools to gather information:

🌐 Web Search: For real-time flight, hotel, and general travel information using Tavily Search.

☁️ Weather Forecast: Provides weather updates for any destination.

🧮 Calculator: For quick budget and cost calculations.

🗣️ Multilingual Support: Capable of understanding and responding in multiple languages, including English and Bengali.

🔒 Domain-Specific: Politely refuses to answer queries that are not related to travel, keeping the conversation focused and professional.

✨ Modern UI/UX: A clean, responsive, and user-friendly interface with features like a persistent chat history, new chat functionality, and a professional blue-themed design.

💨 Real-time Streaming: Responses are streamed word-by-word, similar to modern chatbots like ChatGPT, for an engaging user experience.

🛠️ Tech Stack & Architecture
Backend & Logic:

LangChain & LangGraph: For building the core agentic workflow and state management.

Groq API (Llama 3): Powers the core language model for fast and intelligent responses.

Tavily Search API: For a powerful and accurate search tool.

Frontend:

Streamlit: For creating and deploying the interactive web application.

Deployment:

Streamlit Community Cloud: For free, permanent hosting.

GitHub: For version control and CI/CD with Streamlit Cloud.

⚙️ Setup and Installation (Local)
To run this project on your local machine, follow these steps:

1. Clone the Repository:

git clone https://github.com/rownokstar/Eg-Travel-Agent.git
cd Eg-Travel-Agent

2. Install Dependencies:
It's recommended to use a virtual environment.

python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
pip install -r requirements.txt

3. Set Up API Keys:
Create a file named secrets.toml inside a .streamlit folder (.streamlit/secrets.toml). Add your API keys in the following format:

[api_keys]
GROQ_API_KEY = "YOUR_GROQ_API_KEY"
TAVILY_API_KEY = "YOUR_TAVILY_API_KEY"

4. Run the Streamlit App:

streamlit run app.py

The application should now be running on your local machine.

☁️ Deployment on Streamlit Cloud
This app is deployed on Streamlit Community Cloud. The process is straightforward:

Push the entire project folder (containing app.py and requirements.txt) to a public GitHub repository.

Sign in to share.streamlit.io with your GitHub account.

Click "New app" and choose the repository you just created.

In the "Secrets" section (under advanced settings), add your API keys in the same format as the secrets.toml file.

Click "Deploy!".

👨‍💻 Developed By
DM Shahriar Hossain

📄 License
This project is licensed under the MIT License. See the LICENSE file for details.

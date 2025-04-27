# PantherBot - GSU Smart Program Assistant 🎓🤖

## Project Overview
PantherBot is an AI-powered chatbot developed to assist students in exploring undergraduate and graduate programs at Georgia State University (GSU).  
By integrating OpenAI's LLM capabilities with real-time data from GSU's program listings, PantherBot offers quick, intelligent, and contextually relevant responses to help students find the right program based on their interests. The chatbot leverages multi-turn memory to maintain the flow of conversation and enhance the user experience.

This project was created as part of the MSA 8700 course, focusing on designing, developing, and deploying a practical AI business solution using large language models (LLMs) in real-world scenarios.

---

## Business Problem Addressed
Choosing the right academic program can be overwhelming for students due to the lack of easily accessible, summarized, and personalized information across hundreds of programs. Traditional websites often present fragmented details, causing confusion and delays in decision-making.

PantherBot solves this problem by providing a conversational interface that fetches and presents key program information instantly, personalizes recommendations based on user queries, and ensures the information is easily digestible in a human-like conversation format.

---

## Solution Architecture
- **Frontend**: Developed using Streamlit to offer a seamless and responsive web-based interface.
- **AI Backend**: Powered by OpenAI's GPT-4 Turbo model through OpenAI API, integrated with customized prompt chaining and multi-turn memory.
- **Data Sources**: Two structured Excel datasets containing information about GSU Graduate and Undergraduate programs.
- **External Search**: Google search fallback through Serper.dev API for real-time information retrieval when internal datasets are insufficient.
- **Hosting**: Deployed on Streamlit Community Cloud, ensuring easy public access without setup barriers.

---

## Key Features
- Intelligent program search for undergraduate and graduate offerings.
- Real-time retrieval of program-specific tuition, faculty, outcomes, and curriculum information.
- Dynamic fallback to Google Search when program data is incomplete.
- Clean, intuitive, mobile-friendly Streamlit user interface.
- Multi-turn conversation memory maintaining context across multiple questions.
- Avatars and fade-in animation for a modern, professional chat experience.
- Live feedback form integrated post-chat to capture user satisfaction and improvement ideas.
- Fully offline-capable chatbot when integrated with local Ollama deployments (future ready).

---

## Live Application Access
You can try PantherBot live here:

👉 [Click Here to Open PantherBot App](https://pantherbot.streamlit.app/)

✅ The app is accessible to all students, faculty, and instructors for project demo, feedback collection, and real-world evaluation.

---

## How to Set Up and Run the Application Locally
1. Clone this repository to your local machine:
   ```bash
   git clone https://github.com/Harshalk2002/GENAI_003_PROJECT_02.git
   cd GENAI_003_PROJECT_02
   ```
2. Install all required Python packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Ensure your `.env` file or system environment variables are configured for OpenAI and Serper API keys.
4. Run the Streamlit application:
   ```bash
   streamlit run Panther_bot.py
   ```
5. Open your browser and interact with PantherBot!

---

## 🧑‍🤝‍🧑 Team Roles & Responsibilities

| Team Member | Role | Responsibilities |
|:------------|:-----|:------------------|
| **Harshal Kamble** | Project Lead / LLM Engineer | Designed and developed the chatbot logic using OpenAI's GPT-4 Turbo model, integrated Ollama API for future offline capabilities, managed backend conversation memory, configured interaction logging, oversaw GitHub repo and documentation. |
| **Vishnu Sankhyan** | Full Stack Developer | Designed and built the user-friendly Streamlit frontend, developed program selection and chat interfaces, ensured cross-device responsiveness, deployed the app on Streamlit Community Cloud, and managed continuous integration pipelines. |
| **Abhay Prabhakar** | UX / Feedback & Testing Lead | Designed chatbot conversation flows, conducted extensive user testing sessions, analyzed user feedback, identified interaction improvement areas, and proposed UX optimizations for enhanced engagement and usability. |

The team held weekly meetings, documented development milestones collaboratively, and ensured transparent communication to stay aligned with project goals.

---

## ⚙️ Challenges Faced
- **Performance Optimization**: Integrating multi-turn memory without sacrificing real-time response speed was critical. Various optimizations were made to balance conversational context depth and system resource usage.
- **Session State Management**: Designing a dynamic yet stable session management system that tracks user inputs, selected programs, and feedback across multiple conversation stages.
- **Local LLM Integration**: Preparing the application architecture to work not only with OpenAI’s hosted models but also supporting future offline deployments with Ollama APIs, ensuring greater accessibility and data privacy.
- **Deployment Scalability**: Managing a smooth deployment on Streamlit Community Cloud while ensuring the app remains responsive and fault-tolerant under multiple concurrent users.

---


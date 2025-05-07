# PantherBot - GSU Smart Program Assistant 🎓🤖

## Project Overview
PantherBot is an AI-powered chatbot I developed to assist students in exploring undergraduate and graduate programs at Georgia State University (GSU).  
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
   git clone https://github.com/Harshalk2002/Chat_bot.git
   cd Chat_bot
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

<img width="592" alt="Screenshot 2025-05-01 at 5 18 23 PM" src="https://github.com/user-attachments/assets/0ee9b7f1-4cfa-4d43-9483-9fdbd52827de" />
<img width="872" alt="Screenshot 2025-05-01 at 5 18 32 PM" src="https://github.com/user-attachments/assets/43ce2a04-c744-4185-838a-2773c30de9e8" />
<img width="895" alt="Screenshot 2025-05-01 at 5 18 45 PM" src="https://github.com/user-attachments/assets/c2445e03-6fc3-4576-9890-fb8d8d5de67b" />

---

## Role & Responsibilities

As the sole developer and project owner, I handled:

- **Project Design**: Identified the business problem, designed the solution architecture, and outlined the technical scope.
- **LLM Engineering**: Built and tuned the chatbot logic using GPT-4 Turbo with multi-turn memory and fallback strategies.
- **Frontend Development**: Designed and built the user interface using Streamlit, ensuring responsiveness and user-centric navigation.
- **Integration & Deployment**: Managed API integrations, session state handling, local and remote hosting configurations, and deployment on Streamlit Community Cloud.
- **Testing & Optimization**: Conducted extensive user testing, improved UX based on feedback, and optimized system performance and stability.

---

## ⚙️ Challenges Faced
- **Performance Optimization**: Balancing multi-turn memory with fast response times required careful prompt tuning and caching strategies.
- **Session State Management**: Building a stable yet dynamic session flow that tracks user progress across multi-step conversations.
- **Local LLM Integration**: Architected the backend to support future offline deployment using Ollama APIs for privacy-focused use cases.
- **Scalability**: Ensured the application could handle multiple users simultaneously with minimal lag or crashes.

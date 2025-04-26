# PantherBot - GSU Smart Program Assistant 🎓🤖

## Project Overview
PantherBot is an AI-powered chatbot developed to assist students in exploring undergraduate and graduate programs at Georgia State University (GSU).  
By integrating OpenAI's LLM capabilities with real-time data from GSU's program listings, PantherBot offers quick, intelligent responses to help students find the right program based on their interests.

This project was created as part of the MSA 8700 course, focusing on designing, developing, and deploying an AI business solution using large language models (LLMs).

---

## Business Problem Addressed
Choosing the right academic program can be overwhelming for students due to the lack of easily accessible, summarized information.  
PantherBot solves this problem by providing a conversational interface that fetches and presents key program information instantly, enhancing the decision-making experience.

---

## Solution Architecture
- **Frontend**: Streamlit (Web-based interface)
- **AI Backend**: OpenAI's GPT-4 Turbo (via OpenAI API)
- **Data Sources**: Excel sheets for GSU Graduate and Undergraduate programs
- **External Search**: Integrated Google search API via Serper.dev
- **Hosting**: Streamlit Community Cloud

---

## Key Features
- Search GSU undergraduate and graduate programs intelligently.
- Retrieve key program details from structured data files.
- Real-time web search fallback if internal data isn't sufficient.
- Clean, user-friendly Streamlit interface.

---

## Live Application Access
You can try PantherBot live here:

👉 [Click Here to Open PantherBot App](https://genai003project02.streamlit.app/)

✅ Accessible to all students and instructors for project demo and evaluation.

---

## How to Set Up and Run the Application Locally
1. Clone this repository:
   ```bash
   git clone https://github.com/Harshalk2002/GENAI_003_PROJECT_02.git
   cd GENAI_003_PROJECT_02

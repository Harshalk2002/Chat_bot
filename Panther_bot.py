# app.py - GSU PantherBot with University Info
import streamlit as st
import pandas as pd
import requests
import json
import re
import random
from openai import OpenAI
from pathlib import Path
from datetime import datetime
from streamlit.components.v1 import html

def select_program(program):
    st.session_state.app["selected_program"] = program
    st.session_state.app["current_program_data"] = st.session_state.app["programs"][st.session_state.app["program_type"]].loc[
        st.session_state.app["programs"][st.session_state.app["program_type"]]['Program Name'] == program
    ].iloc[0].to_dict()
    st.session_state.app["stage"] = "chat_interface"
    st.rerun()

# Add this to your main() function before the stage handlers:
if 'select_program' in st.query_params:
    select_program(st.query_params['select_program'])
# ===== CONFIGURATION =====
DATA_DIR = Path("data")
USER_DATA_PATH = DATA_DIR / "user_submissions.xlsx"
LOGO_PATH = Path("assets/gsu_logo.png")
UNIVERSITY_IMAGE_PATH = Path("assets/gsu_image.jpg")  # Added university image path

# Initialize APIs (replace with your actual keys)
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
SERPER_API_KEY = st.secrets["SERPER_API_KEY"]

# ===== UI CONFIGURATION =====
st.set_page_config(
    page_title="GSU PantherBot",
    page_icon="🎓",
    layout="wide"
)

# Modern styling
st.markdown("""
<style>
    [data-testid="stChatMessage"] {
        padding: 16px;
        border-radius: 12px;
        margin-bottom: 12px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    [data-testid="stChatMessage"] [data-testid="user"] {
        background-color: #003366;
        color: white;
        margin-left: auto;
        max-width: 85%;
    }
    [data-testid="stChatMessage"] [data-testid="assistant"] {
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
        max-width: 90%;
    }
    .program-card {
        border: 1px solid #dee2e6;
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 16px;
        background-color: white;
        transition: all 0.2s ease;
    }
    .program-card:hover {
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        transform: translateY(-2px);
    }
    .program-title {
        color: #003366;
        margin-top: 0;
        margin-bottom: 8px;
    }
    .stButton>button {
        background-color: #003366;
        color: white;
        border-radius: 8px;
        padding: 8px 16px;
        width: 100%;
    }
    .university-card {
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 20px;
        background: #f9f9f9;
        margin: 10px 0;
    }
    .compact-list {
        display: flex;
        flex-direction: column;
        gap: 8px;
    }
</style>
""", unsafe_allow_html=True)

# ===== SESSION STATE =====
if "app" not in st.session_state:
    st.session_state.app = {
        "stage": "get_name",
        "user_data": {},
        "program_type": None,
        "selected_program": None,
        "current_program_data": None,
        "chat_history": [],
        "programs": None,
        "search_cache": {}
    }

# ===== DATA LOADING =====
@st.cache_data
def load_programs():
    try:
        undergrad = pd.read_excel(DATA_DIR / "GSU_Undergrad.xlsx").fillna("Not available")
        grad = pd.read_excel(DATA_DIR / "GSU_graduate.xlsx").fillna("Not available")
        
        # Standardize column names
        undergrad = undergrad.rename(columns={
            "Financial Aid Email": "Contact Email",
            "Program Advisor Email": "Contact Email"
        })
        
        return {"undergrad": undergrad, "grad": grad}
    except Exception as e:
        st.error(f"❌ Failed to load program data: {str(e)}")
        st.stop()

# ===== CORE FUNCTIONS =====
def google_search(query):
    """Perform Google search via Serper API"""
    if query in st.session_state.app["search_cache"]:
        return st.session_state.app["search_cache"][query]
    
    url = "https://google.serper.dev/search"
    headers = {
        'X-API-KEY': SERPER_API_KEY,
        'Content-Type': 'application/json'
    }
    params = {
        "q": f"site:gsu.edu {query}",
        "num": 3
    }
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(params))
        results = response.json().get('organic', [])
        st.session_state.app["search_cache"][query] = results
        return results
    except Exception as e:
        st.error(f"🔍 Search error: {str(e)}")
        return []

def is_greeting(prompt: str) -> bool:
    patterns = [
        r"\b(hi|hello|hey|greetings|sup|what's up)\b",
        r"how('s| are) you( doing)?\??",
        r"good (morning|afternoon|evening)"
    ]
    return any(re.search(p, prompt.lower()) for p in patterns)

def is_thanks(prompt: str) -> bool:
    return bool(re.search(r"\b(thanks|thank you|appreciate|thx)\b", prompt.lower()))

def is_faculty_query(prompt: str) -> bool:
    return bool(re.search(r"\b(professor|faculty|teacher|instructor|lecturer|staff)\b", prompt.lower()))

def is_about_university_query(prompt: str) -> bool:
    return bool(re.search(r"\b(about this uni|about the university|about gsu|about robinson college)\b", prompt.lower()))

def generate_university_response():
    """Returns formatted university information with local image"""
    if not UNIVERSITY_IMAGE_PATH.exists():
        return "⚠️ University image not found in assets folder"
    
    # Create columns for image and text
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.image(str(UNIVERSITY_IMAGE_PATH), use_container_width=True)
    
    with col2:
        st.markdown("""
        <div class="university-card">
            <h3 style="color: #003366; margin-top: 0;">🏫 J. Mack Robinson College of Business</h3>
            
            <p>The J. Mack Robinson College of Business at Georgia State University in Atlanta is a leading business school offering a wide range of undergraduate, graduate, and doctoral programs. Established in 1913, the college is accredited by AACSB International and is known for its innovative curriculum and strong industry connections.</p>
            
            <h4 style="color: #003366;">Academic Programs</h4>
            <ul>
                <li><strong>Undergraduate Degrees:</strong> B.B.A. in Accounting, Finance, Marketing, Management, CIS, and more</li>
                <li><strong>Graduate Programs:</strong> M.S. in Finance, Information Systems, Health Administration, and customizable MBA</li>
                <li><strong>Doctoral Programs:</strong> Ph.D. programs focusing on research excellence</li>
            </ul>
            
            <h4 style="color: #003366;">Key Features</h4>
            <ul>
                <li>"Robinson Anywhere" platform for global synchronous learning</li>
                <li>Research centers like Center for Economic Analysis of Risk</li>
                <li>Ranked programs (e.g., #4 Risk Management, #10 MIS)</li>
                <li>Prime downtown Atlanta location near Fortune 500 companies</li>
            </ul>
            
            <a href="https://robinson.gsu.edu" style="
                display: inline-block;
                background: #003366;
                color: white;
                padding: 8px 15px;
                border-radius: 5px;
                text-decoration: none;
                margin-top: 10px;
            ">Visit Official Website</a>
        </div>
        """, unsafe_allow_html=True)
    
    return ""  # Empty string since we're rendering directly

def generate_tuition_response(program_data: dict) -> str:
    """Humanized tuition cost explanation"""
    def format_cost(value):
        if isinstance(value, (int, float)):
            return f"${value:,.2f}"
        if isinstance(value, str) and "-" in value:
            low, high = value.split("-")
            return f"${low.strip()}-${high.strip()}"
        return str(value)
    
    in_state = program_data.get("In-State Tuition Estimate", "Not available")
    out_state = program_data.get("Out-of-State Tuition Estimate", "Not available")
    financial_aid = program_data.get("Financial Aid Email", "rcbfinancialaid@gsu.edu")
    
    response = [
        f"📚 **Tuition Information for {program_data['Program Name']}**",
        "",
        f"• **Georgia Residents**: {format_cost(in_state)} per year",
        f"• **Out-of-State Students**: {format_cost(out_state)} per year",
        "",
        "💡 *Financial aid and scholarships are available*",
        f"• Contact: {financial_aid}",
        f"• Phone: {program_data.get('Phone Number', '404-413-2600')}",
        "",
        f"🔗 [View payment plans and detailed costs]({program_data.get('Program URL', 'https://robinson.gsu.edu')})"
    ]
    
    return "\n".join(response)

def generate_response(prompt: str) -> str:
    """Generate context-aware responses"""
    # 1. Handle university info queries
    if is_about_university_query(prompt):
        generate_university_response()  # This renders directly
        return ""  # Return empty string since we rendered components directly

    program_data = st.session_state.app["current_program_data"]

    # 2. Handle greetings
    if is_greeting(prompt):
        return random.choice([
            "🎓 Hello! How can I assist you with GSU programs today?",
            "👋 Hi there! Ready to explore degree programs?"
        ])

    # 3. Handle thanks
    if is_thanks(prompt):
        return random.choice([
            "🙏 You're welcome! Let me know if you have other questions.",
            "😊 Happy to help! What else can I assist with?"
        ])

    # 4. Special handling for tuition queries
    if any(word in prompt.lower() for word in ["tuition", "fee", "cost", "price"]):
        return generate_tuition_response(program_data)

    # 5. Handle faculty queries
    if is_faculty_query(prompt):
        faculty = program_data.get("Faculty", "Not available")
        if faculty != "Not available":
            return f"👨‍🏫 **Faculty Members**:\n\n" + "\n".join(f"- {name.strip()}" for name in faculty.split(","))
        return f"⚠️ Faculty information not found. Check the [program website]({program_data.get('Program URL', '#')})"

    # 6. Default AI response
    search_results = google_search(f"{program_data['Program Name']} {prompt}")
    web_context = "\n".join(f"{res.get('title')}: {res.get('snippet')}" for res in search_results)

    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{
                "role": "system",
                "content": f"Answer using: {program_data}\nWeb results: {web_context}\nRules: Be concise, friendly, and professional"
            }, {
                "role": "user",
                "content": prompt
            }],
            temperature=0.4
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

# ===== UI HANDLERS =====
def handle_name():
    st.title("🎓 Welcome to GSU PantherBot!")
    name = st.text_input("What's your name?")
    
    if st.button("Continue"):
        if name.strip():
            st.session_state.app["user_data"]["name"] = name.strip()
            st.session_state.app["stage"] = "get_email"
            st.rerun()
        else:
            st.warning("Please enter your name")

def handle_email():
    st.title("📧 Contact Information")
    st.write(f"Hello {st.session_state.app['user_data']['name']}! Please provide your email address.")
    email = st.text_input("Email Address")
    
    if st.button("Continue"):
        if re.match(r"[^@]+@[^@]+\.[^@]+", email):
            st.session_state.app["user_data"]["email"] = email
            st.session_state.app["stage"] = "get_phone"
            st.rerun()
        else:
            st.warning("Please enter a valid email address")

def handle_phone():
    st.title("📞 Contact Information")
    st.write("Almost done! Please provide your phone number (optional).")
    phone = st.text_input("Phone Number (optional)")
    
    if st.button("Continue"):
        st.session_state.app["user_data"]["phone"] = phone if phone else "Not provided"
        st.session_state.app["stage"] = "select_program_type"
        st.rerun()

def handle_program_type():
    st.title("🎓 Program Selection")
    st.write("Are you interested in undergraduate or graduate programs?")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Undergraduate Programs"):
            st.session_state.app["program_type"] = "undergrad"
            st.session_state.app["stage"] = "select_program"
            st.rerun()
    
    with col2:
        if st.button("Graduate Programs"):
            st.session_state.app["program_type"] = "grad"
            st.session_state.app["stage"] = "select_program"
            st.rerun()

    
   
def handle_program_selection():
    if st.session_state.app["programs"] is None:
        st.session_state.app["programs"] = load_programs()
    
    program_type = st.session_state.app["program_type"]
    programs = st.session_state.app["programs"][program_type]
    
    st.title(f"📚 {program_type.capitalize()} Programs")
    st.subheader("Browse our academic offerings", divider='blue')
    
    # Custom CSS for styling
    st.markdown("""
    <style>
        .program-card {
            border: 1px solid #e0e0e0;
            border-radius: 12px;
            padding: 18px;
            margin-bottom: 20px;
            background: white;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            transition: all 0.3s ease;
        }
        .program-card:hover {
            box-shadow: 0 4px 12px rgba(0,0,0,0.12);
            transform: translateY(-4px);
        }
        .program-title {
            color: #003366 !important;
            margin-top: 0;
            margin-bottom: 12px;
            font-size: 1.1rem;
            font-weight: 600;
        }
        .program-desc {
            color: #555;
            font-size: 0.92em;
            margin-bottom: 16px;
            line-height: 1.5;
        }
        .explore-btn-container {
            margin-top: auto;
        }
        div[data-testid="stButton"] > button {
            background: linear-gradient(to right, #003366, #004080) !important;
            border: none !important;
            border-radius: 20px !important;
            width: 100% !important;
            color: white !important;
            font-weight: 500;
            transition: opacity 0.2s ease !important;
        }
        div[data-testid="stButton"] > button:hover {
            opacity: 0.85 !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Create a grid of program cards
    cols = st.columns(3)
    col_index = 0
    
    for _, row in programs.iterrows():
        with cols[col_index]:
            # Create the card container
            st.markdown(f"""
            <div class="program-card">
                <div class="program-title">{row["Program Name"]}</div>
                <div class="program-desc">{row.get("Overview", "Explore this degree program")[:120]}...</div>
                <div class="explore-btn-container">
            </div>
            """, unsafe_allow_html=True)
            
            # Add the explore button inside the card
            if st.button(
                "Explore Program",
                key=f"explore_{row['Program Name']}",
            ):
                st.session_state.app["selected_program"] = row['Program Name']
                st.session_state.app["current_program_data"] = row.to_dict()
                st.session_state.app["stage"] = "chat_interface"
                st.rerun()
        
        col_index = (col_index + 1) % 3
    
    if st.button("← Back to Program Type Selection", type="secondary"):
        st.session_state.app["stage"] = "select_program_type"
        st.rerun()

def handle_chat_interface():
    program = st.session_state.app["selected_program"]

    left_col, right_col = st.columns([1, 3])

    with left_col:
        if LOGO_PATH.exists():
            st.image(str(LOGO_PATH), use_container_width=True)

        st.subheader(program)
        if "Program URL" in st.session_state.app["current_program_data"]:
            st.markdown(f"[🔗 Program Website]({st.session_state.app['current_program_data']['Program URL']})")

        if st.button("← Back to Programs"):
            st.session_state.app["stage"] = "select_program_type"
            st.rerun()

    with right_col:
        st.header(f"{program} Advisor")

        for msg in st.session_state.app["chat_history"]:
            avatar = "👤" if msg["role"] == "user" else "🎓"
            with st.chat_message(msg["role"], avatar=avatar):
                if msg["role"] == "assistant" and is_about_university_query(msg["content"]):
                    generate_university_response()
                else:
                    st.markdown(msg["content"], unsafe_allow_html=True)

        if prompt := st.chat_input(f"Ask about {program}..."):
            with st.spinner("Researching..."):
                response = generate_response(prompt)

            st.session_state.app["chat_history"].extend([
                {"role": "user", "content": prompt},
                {"role": "assistant", "content": response if response else "about_uni_response"}
            ])
            st.rerun()

# ===== MAIN APP =====
def main():
    stages = {
        "get_name": handle_name,
        "get_email": handle_email,
        "get_phone": handle_phone,
        "select_program_type": handle_program_type,
        "select_program": handle_program_selection,
        "chat_interface": handle_chat_interface
    }
    
    current_stage = st.session_state.app["stage"]
    if current_stage in stages:
        stages[current_stage]()
    else:
        st.error("Invalid state")
        st.session_state.app["stage"] = "get_name"
        st.rerun()

if __name__ == "__main__":
    main()

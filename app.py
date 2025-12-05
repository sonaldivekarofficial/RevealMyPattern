import streamlit as st
import pandas as pd
from io import BytesIO
from fpdf import FPDF
import re
import streamlit.components.v1 as components

# --- CUSTOM CSS STYLING (Aggressive Debugging for robust selector targeting) ---

CUSTOM_CSS = """
<style>
/* General App Styling */
.stApp {
    background-color: #f8f8ff; /* Fresh background */
    color: #333333;
}
.stApp header {
    background-color: transparent;
}

/* Center Titles */
h1, h2, h3, h4, h5, h6 {
    text-align: center;
}
.centered-subtitle {
    text-align: center;
    margin-bottom: 1.5rem;
    color: #555;
}

/* Question Text Styling */
.question-text {
    font-size: 1.2rem;
    font-weight: 600;
    color: #1a1a1a;
    margin-top: 25px;
    margin-bottom: 10px;
}

/* --- DEBUGGED RADIO BUTTON STYLING --- */

/* 1. Force Text Color to dark and Bold (Requirement 1) */
/* Targets the paragraph tag inside the option label using Streamlit's data-testid */
div[data-testid*="stRadio"] label p {
    color: #1a1a1a !important; /* Very dark gray/near black */
    font-weight: 700 !important; /* Make it Bold */
}

/* 2. Container Styling - Create a Compact Grid (Requirement 2) */
/* Targets the element that wraps all radio options */
div[data-testid*="stRadio"] > div {
    display: flex;
    flex-wrap: wrap; 
    gap: 8px; /* Compact spacing */
    width: 100%;
}

/* 3. Individual Option Styling (Cards) */
/* Targets the individual label/card for the options, enforcing 2 per row */
div[data-testid*="stRadio"] label {
    background-color: #ffffff;
    padding: 10px 12px; /* Compact padding */
    border-radius: 8px;
    border: 1px solid #d0d0d0;
    cursor: pointer;
    transition: all 0.2s ease;
    
    /* Grid Logic: Forces 2 items per row (48% width to account for gap) */
    flex: 1 1 48%; 
    min-width: 180px; 
    
    display: flex;
    align-items: center;
    justify-content: flex-start;
    margin-right: 0px !important; /* Overrides Streamlit's margin */
}

/* Green Highlight for Selected Option */
div[data-testid*="stRadio"] label:has(input:checked) {
    background-color: #e8f5e9 !important; /* Light green background */
    border-color: #4CAF50 !important;      /* Green border */
    box-shadow: 0 2px 5px rgba(76, 175, 80, 0.3);
}

/* --- NAVIGATION BUTTONS --- */
div.stButton button {
    width: 100%;
    padding: 12px 24px;
    font-size: 1.1rem;
    font-weight: bold;
    color: white !important;
    background-color: #4CAF50; /* Green */
    border-radius: 8px;
    border: none;
    margin-top: 25px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
div.stButton button:hover {
    background-color: #45a049;
    box-shadow: 0 4px 8px rgba(0,0,0,0.15);
}
div.stButton button:disabled {
    background-color: #cccccc;
    color: #666666 !important;
}

/* --- DOWNLOAD PDF BUTTON (Light Orange) --- */
div[data-testid="stDownloadButton"] button {
    background-color: #f97316 !important; 
    border-color: #f97316 !important; 
    color: white !important;
}
div[data-testid="stDownloadButton"] button:hover {
    background-color: #ea580c !important; 
}


/* --- ACTION PLAN CARD STYLING --- */
.action-plan-card {
    background-color: #f1f8e9; 
    padding: 25px;
    border-radius: 12px;
    border-left: 6px solid #8bc34a; 
    margin-top: 15px;
    margin-bottom: 25px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.08);
}
.action-plan-title {
    color: #2e7d32;
    font-size: 1.3rem;
    font-weight: 700;
    margin-bottom: 15px;
    margin-top: 0;
    border-bottom: 1px solid #c5e1a5;
    padding-bottom: 10px;
}
.action-plan-content {
    color: #333;
    font-size: 1.0rem;
    line-height: 1.6;
}
.week-bold {
    font-weight: 700;
    color: #1b5e20;
    font-size: 1.05rem;
    display: inline-block;
    margin-top: 10px;
}
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# --- JAVASCRIPT FOR SCROLL TO TOP (Requirement 3) ---
def scroll_to_top():
    """Injects JavaScript to force the browser to scroll to the top of the page."""
    # This targets the main scrolling element in the iframe's parent (the host) for reliability.
    js_scroll_top = """
    <script>
        window.parent.document.documentElement.scrollTop = 0;
        window.parent.document.body.scrollTop = 0; // For cross-browser compatibility
    </script>
    """
    components.html(js_scroll_top, height=0, width=0)

# --- GLOBAL DATA & OPTIONS ---

standard_options = [
    "1. Strongly Disagree",
    "2. Disagree",
    "3. Neutral",
    "4. Agree",
    "5. Strongly Agree"
]

ace_options = [
    "1. Never",
    "2. Rarely",
    "3. Sometimes",
    "4. Often",
    "5. Very Often"
]

# --- UTILITY FUNCTIONS (Unchanged, using placeholders for external data) ---

def load_csv_smart(filename):
    # This is a placeholder function as files are not accessible
    pass

# Placeholder data structures to allow the rest of the app to run without actual file access
try:
    questions_df = pd.DataFrame({
        'ID': range(1, 101), 
        'Question Text': [f"Sample Question {i}" for i in range(1, 101)]
    })
    map_df = pd.DataFrame({
        'Schema_ID': [1, 2, 3] * 33 + [20],
        'Question_ID': range(1, 101),
        'Direction': [1] * 100 
    })
    schemas_df = pd.DataFrame({
        'Schema': [1, 2, 3, 20],
        'Schema Name': ['Perfectionism', 'Helplessness', 'Fixed Mindset', 'Trauma'],
        'Root Causes (Childhood Drivers)': ['High parental standards', 'Over-controlled environment', 'Lack of praise for effort', 'Adverse experiences'],
        'Symptoms & Behavioral Loops': ['Procrastination, anxiety', 'Lack of initiative, learned helplessness', 'Avoidance of new challenges', 'Hypervigilance, emotional numbness']
    })
    
except Exception as e:
    st.error(f"Error initializing mock data: {e}")
    st.stop()

ACTION_PLANS = {
    1: "Week 1: Keep a 'Perfectionism Log'. Record situations where you felt the urge to be perfect. Note the specific standard you felt you had to meet and rate your anxiety (1-10). Identify if the standard was self-imposed or external.\nWeek 2: Use 'Cost-Benefit Analysis'. List the advantages (e.g., praise, safety) vs. disadvantages (e.g., burnout, time loss) of your high standards. Challenge the 'All-or-Nothing' distortion: 'If I'm not perfect, I'm a failure.'\nWeek 3: The 'B+ Experiment'. Deliberately perform a low-stakes task (e.g., an internal email, a quick chore) to an 80% standard. Resist the urge to fix it. Record the outcome: Did a catastrophe happen?\nWeek 4: Create a 'Good Enough' Mantra card. Schedule mandatory 'Non-Productive Time' where the goal is specifically to achieve nothing, reinforcing worth separate from output.",
    2: "Week 1: Track 'Agency Moments'. Record times during the day when you actually made a choice (even small ones like what to eat). Rate your sense of control (0-10) for each.\nWeek 2: Challenge 'Fortune Telling'. When you think 'It won't matter anyway,' ask: 'What is the evidence for this?' and 'Have I ever influenced an outcome before?' Write down 3 counter-examples.\nWeek 3: Graded Task Assignment. Pick one micro-goal (e.g., wash 3 dishes, send 1 text). Do not focus on the outcome, only the initiation. Treat the action itself as the success.\nWeek 4: Build a 'Success Log'. Every evening, write down 3 things you influenced that day. Review this log whenever the feeling of paralysis returns.",
    3: "Week 1: Identify 'Fixed Triggers'. Notice when you say 'I can't do this' or 'I'm not good at this.' Label these as 'Fixed Mindset Thoughts' rather than facts.\nWeek 2: Reframe 'Failure' to 'Data'. When you make a mistake, complete this sentence: 'This mistake teaches me that I need to adjust X, not that I am Y.'\nWeek 3: The 'Beginner's Mind' Experiment. Engage in a hobby or task you are terrible at for 15 minutes. Observe the discomfort of not being expert. Allow yourself to be clumsy without judgment.\nWeek 4: Establish a 'Yet' Habit. Append the word 'yet' to every inability statement (e.g., 'I don't understand this code... yet'). Schedule one weekly learning session for a new skill.",
    20: "Week 1: Trigger Awareness (Safety First). Identify specific sensory triggers (smells, sounds). Focus on grounding immediately when triggered.\nWeek 2: Cognitive Processing. Work on 'Stuck Points' (e.g., 'The world is unsafe'). Differentiate 'Then' (trauma time) vs. 'Now' (safe time).\nWeek 3: Titrated Exposure. Slowly approach safe situations you avoid due to trauma triggers. Do this only when regulated.\nWeek 4: Maintenance & Care. Build a robust support network (therapy, groups). Prioritize nervous system regulation as a lifestyle, not a fix."
}

# --- SCORING FUNCTIONS (Unchanged) ---

if 'page' not in st.session_state:
    st.session_state.page = 0
if 'answers' not in st.session_state:
    st.session_state.answers = {}

def calculate_schema_scores(answers):
    if len(answers) != len(questions_df):
        return {} 
        
    results = {}
    for schema_id in map_df['Schema_ID'].unique():
        schema_rows = map_df[map_df['Schema_ID'] == schema_id]
        raw_scores = []
        max_possible = 0
        
        for _, row in schema_rows.iterrows():
            qid = row['Question_ID']
            direction = row['Direction']
            user_val = min(max(answers.get(qid, 0), 1), 5) 
            is_ace = 61 <= qid <= 70
            
            if is_ace:
                contrib = 1 if user_val > 1 else 0
                q_max = 1
            else:
                contrib = user_val
                q_max = 5
                
            score = contrib if direction == 1 else (q_max + 1 - contrib)
            raw_scores.append(score)
            max_possible += q_max
            
        raw_sum = sum(raw_scores)
        percentage = (raw_sum / max_possible) * 100 if max_possible > 0 else 0
        results[schema_id] = round(percentage, 1)
    return results

def get_top_schemas(scores, trauma_threshold=60):
    sorted_scores = sorted(scores.items(), key=lambda x: (-x[1], x[0]))
    top_3 = [item[0] for item in sorted_scores[:3]]
    trauma_score = scores.get(20, 0)
    display = top_3.copy()
    root_cause_note = None
    if trauma_score > trauma_threshold and 20 not in top_3:
        display.append(20)
        root_cause_note = "Trauma Core Schema (No. 20) is highly elevated and may be a root driver of other schemas."
    return display, root_cause_note, {sid: scores[sid] for sid in display}

def generate_pdf(plain_text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, plain_text.encode('latin-1', 'replace').decode('latin-1')) 
    pdf_bytes = BytesIO(pdf.output(dest='S').encode('latin-1')) 
    pdf_bytes.seek(0)
    return pdf_bytes

def format_action_plan_html(plan_text):
    """Parses the Action Plan text and returns styled HTML."""
    formatted = re.sub(
        r'(Week \d+:)', 
        r'<br><span class="week-bold">\1</span>', 
        plan_text
    )
    if formatted.startswith('<br>'):
        formatted = formatted[4:]
        
    return formatted

# --- MAIN APP UI ---

st.set_page_config(layout="wide", page_title="Latent Recursion Test")

# Title & Headers
st.title("Latent Recursion Test")
st.markdown("""
<p class='centered-subtitle'>
    A powerful Psychological Schema Testing tool that reveals hidden patterns dictating your behavior, decisions, and life outcomes.
</p>
<p class='centered-subtitle'>
    Brought to you by <a href='http://www.mygipsy.com'>www.mygipsy.com</a>
</p>
""", unsafe_allow_html=True)
st.divider()

# Disclaimer
st.markdown("""
<div style="padding: 15px; background-color: #ffffff; border-radius: 8px; border: 1px solid #ddd; margin-bottom: 20px;">
    <strong>Disclaimer:</strong> This assessment is for informational and educational purposes only. It is not a substitute for professional mental health diagnosis or treatment. The results are based on schema therapy principles and should be discussed with a qualified mental health professional. **All questions are mandatory.**
</div>
""", unsafe_allow_html=True)

# Pagination Logic
questions_per_page = 10
total_pages = (len(questions_df) + questions_per_page - 1) // questions_per_page

if st.session_state.page < total_pages:
    
    start = st.session_state.page * questions_per_page
    end = start + questions_per_page
    page_questions = questions_df.iloc[start:end]
    
    st.progress((st.session_state.page + 1) / total_pages)
    st.subheader(f"Section {st.session_state.page + 1} of {total_pages}")
    
    # Scale Key
    first_qid = page_questions.iloc[0]['ID']
    is_ace_page = 61 <= first_qid <= 70
    
    if is_ace_page:
        scale_min_text = "Never"
        scale_max_text = "Very Often"
        current_options = ace_options
    else:
        scale_min_text = "Strongly Disagree"
        scale_max_text = "Strongly Agree"
        current_options = standard_options
        
    st.markdown(
        f"""
        <div style="text-align:center; margin-bottom: 20px; font-weight:bold;">
        SCALE: 1 = {scale_min_text} &nbsp;|&nbsp; 5 = {scale_max_text}
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown("---")
    
    # Question Loop
    for _, q in page_questions.iterrows():
        qid = q['ID']
        question_text = q['Question Text']
        
        if 61 <= qid <= 70:
            current_options_q = ace_options
        else:
            current_options_q = standard_options
            
        previous_val = st.session_state.answers.get(qid, 3)
        previous_answer_str = current_options_q[previous_val - 1]
        
        st.markdown(f"<div class='question-text'>Q{qid}: {question_text}</div>", unsafe_allow_html=True)
        
        # Radio buttons 
        selected_option_str = st.radio(
            "Select option:", 
            options=current_options_q, 
            index=current_options_q.index(previous_answer_str), 
            key=f"q_{qid}",
            horizontal=False, 
            label_visibility='collapsed'
        )
        
        try:
            selected_val = int(selected_option_str.split('.')[0])
            st.session_state.answers[qid] = selected_val
        except (ValueError, IndexError):
            st.session_state.answers[qid] = 3 
            
    st.markdown("---")
    
    # Navigation
    col1, col2 = st.columns(2)
    
    if st.session_state.page > 0:
        if col1.button("⬅️ Previous", key="prev_button"):
            st.session_state.page -= 1
            scroll_to_top() # Scroll to Top (Requirement 3)
            st.rerun()
            
    page_question_ids = page_questions['ID'].tolist()
    current_page_answered = all(qid in st.session_state.answers for qid in page_question_ids)
    
    if not current_page_answered:
        col2.button("Next / Submit ➡️", disabled=True, key="disabled_next")
        st.error(f"Please answer all {len(page_question_ids)} questions on this page before continuing.")
    
    else:
        button_label = "Submit & See Results 🎉" if st.session_state.page == total_pages - 1 else "Next ➡️"
        
        if col2.button(button_label, key="next_submit_button"):
            if st.session_state.page < total_pages - 1:
                st.session_state.page += 1
                scroll_to_top() # Scroll to Top (Requirement 3)
                st.rerun()
            else:
                if len(st.session_state.answers) == len(questions_df):
                    st.session_state.page = total_pages 
                    scroll_to_top() # Scroll to Top (Requirement 3)
                    st.rerun()
                else:
                    st.error("Submission failed: Not all questions were answered.")
                
else:
    # --- RESULTS PAGE ---
    if len(st.session_state.answers) != len(questions_df):
        st.error("Error: Assessment data is incomplete. Please restart.")
        if st.button("Restart Assessment"):
            st.session_state.page = 0
            st.session_state.answers = {}
            scroll_to_top() # Scroll to Top
            st.rerun()
        st.stop()
        
    scores = calculate_schema_scores(st.session_state.answers)
    top_schemas, root_note, top_scores = get_top_schemas(scores)
    
    st.header("Results")
    st.markdown("""
        <p style='text-align:center; font-size: 1.15rem; margin-bottom: 2rem;'>
            Based on your input, these are the top 3 psychological patterns potentially affecting your personal growth. 
            Plus, a 30-day action plan to readjust and find balance.
        </p>
    """, unsafe_allow_html=True)
    st.divider()
    
    plain_text = "--- Latent Recursion Test Report ---\n\n"
    
    for sid in top_schemas:
        schema_row = schemas_df[schemas_df['Schema'] == sid].iloc[0]
        name = schema_row['Schema Name']
        score = top_scores[sid]
        root = schema_row['Root Causes (Childhood Drivers)']
        patterns = schema_row['Symptoms & Behavioral Loops']
        plan = ACTION_PLANS.get(sid, 'Custom 30-day plan based on schema therapy principles.')
        
        # Apply HTML formatting to the plan (Bold Weeks, add spacing)
        formatted_plan_html = format_action_plan_html(plan)
        
        st.markdown(f"### 🎯 {name} ({score}%)")
        st.markdown(f"**Root Cause:** {root}")
        st.markdown(f"**Patterns Keeping You Stuck:** {patterns}")
        
        # Display the formatted Action Plan
        st.markdown(f"""
        <div class="action-plan-card">
            <h4 class="action-plan-title">📅 30-Day Action Plan</h4>
            <div class="action-plan-content">{formatted_plan_html}</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        plain_text += f"Schema: {name} ({score}%)\n\nRoot Cause: {root}\n\nPatterns Keeping You Stuck: {patterns}\n\n30-Day Action Plan:\n{plan}\n\n---\n"
        
    if root_note:
        st.warning(root_note)
        plain_text += f"Note: {root_note}\n\n"
        
    pdf = generate_pdf(plain_text)
    
    st.download_button("⬇️ Download PDF Report", pdf, "latent_recursion_report.pdf", "application/pdf")
    
    if st.button("Restart Assessment", key="restart_button_final"):
        st.session_state.page = 0
        st.session_state.answers = {}
        scroll_to_top() # Scroll to Top
        st.rerun()

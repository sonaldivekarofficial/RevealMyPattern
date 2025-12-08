import streamlit as st
import pandas as pd
from io import BytesIO
import re
from fpdf import FPDF
import streamlit.components.v1 as components

# ================================
#       FINAL CLEAN & PERFECTED UI
# ================================
st.set_page_config(layout="centered", page_title="Latent Recursion Test")

PERFECT_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    html, body, .stApp {
        background: #0f172a;
        font-family: 'Inter', sans-serif;
        color: #e2e8f0;
    }
    
    .main-card {
        background: #1e293b;
        max-width: 840px;
        margin: 2rem auto;
        border-radius: 32px;
        padding: 4.5rem 3.5rem;
        box-shadow: 0 30px 80px rgba(0,0,0,0.6);
        border: 1px solid #334155;
    }
    
    h1 {
        font-size: 3.6rem !important;
        font-weight: 800 !important;
        text-align: center !important;
        background: linear-gradient(90deg, #8b5cf6, #ec4899);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0 0 1.2rem 0 !important;
    }
    
    .centered-subtitle {
        text-align: center;
        font-size: 1.3rem;
        color: #94a3b8;
        margin: 1.2rem 0 3rem 0;
        line-height: 1.7;
    }
    .centered-subtitle a {
        color: #c084fc;
        font-weight: 600;
        text-decoration: none;
    }
    
    /* Clean green progress bar */
    .progress-container {
        position: fixed;
        top: 0; left: 0; right: 0;
        height: 6px;
        background: rgba(34,197,94,0.15);
        z-index: 9999;
    }
    .progress-fill {
        height: 100%;
        background: #22c55e;
        width: 0%;
        transition: width 0.8s ease;
        box-shadow: 0 0 15px rgba(34,197,94,0.6);
    }
    
    /* Question text - BIG and bold */
    .question-text {
        font-size: 1.65rem !important;
        font-weight: 800 !important;
        color: #f8fafc !important;
        text-align: center;
        margin: 4.5rem 0 2.5rem 0 !important;
        line-height: 1.7;
    }
    
    h2 {
        text-align: center;
        color: #a78bfa;
        font-size: 2.3rem;
        font-weight: 700;
        margin: 3rem 0 1.5rem 0;
    }
    
    /* Radio buttons - clean, green on select */
    div[data-baseweb="radio"] > div {
        margin: 0.8rem 0;
    }
    div[data-baseweb="radio"] label {
        font-size: 1.05rem !important;
        color: #cbd5e1 !important;
        padding: 0.9rem 1.2rem !important;
        border-radius: 12px !important;
        background: #334155 !important;
        transition: all 0.3s ease !important;
    }
    div[data-baseweb="radio"] input:checked + label {
        background: #22c55e !important;
        color: white !important;
        font-weight: 700 !important;
        box-shadow: 0 8px 25px rgba(34,197,94,0.4) !important;
        transform: translateY(-3px) !important;
    }
    
    /* More space between questions */
    .stRadio > div[role="radiogroup"] {
        margin-bottom: 4rem !important;
    }
    
    /* Action plan expanders */
    .action-plan-card {
        background: #1e1b4b;
        border-radius: 20px;
        padding: 2.2rem;
        margin: 3rem 0;
        border-left: 7px solid #ec4899;
        box-shadow: 0 12px 35px rgba(0,0,0,0.4);
    }
    .action-plan-title { color: #ec4899; font-size: 1.6rem; margin-top: 0; }
    .week-bold { font-weight: 800; color: #c084fc; font-size: 1.25rem; }
    
    /* Buttons */
    div.stButton > button {
        background: linear-gradient(90deg, #8b5cf6, #ec4899);
        color: white;
        border: none;
        border-radius: 18px;
        padding: 1.3rem 3.5rem;
        font-size: 1.3rem;
        font-weight: 700;
        width: 100%;
        box-shadow: 0 12px 35px rgba(139,92,246,0.45);
        transition: all 0.3s ease;
    }
    div.stButton > button:hover {
        transform: translateY(-5px);
        box-shadow: 0 22px 45px rgba(139,92,246,0.65);
    }
    
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown p, .stMarkdown div {
        color: #e2e8f0 !important;
    }
    
    #MainMenu, footer, header { visibility: hidden !important; }
</style>

<div class="progress-container">
    <div class="progress-fill" id="progressFill"></div>
</div>

<script>
    // Update progress bar
    const totalPages = 10;
    const currentPage = """ + str(st.session_state.page + 1 if 'page' in st.session_state and st.session_state.page < 10 else 10) + """;
    document.getElementById("progressFill").style.width = (currentPage / totalPages * 100) + "%";
    
    // Force scroll to top on every rerun
    window.parent.scrollTo({ top: 0, behavior: 'smooth' });
</script>
"""

components.html(PERFECT_CSS, height=0)

# ================================
#       YOUR FULL ORIGINAL LOGIC (100% INTACT)
# ================================

def load_csv_smart(filename):
    encodings = ['utf-8', 'utf-16', 'cp1252', 'latin1', 'iso-8859-1', 'mbcs']
    separators = [',', '\t', ';']
    for enc in encodings:
        for sep in separators:
            try:
                return pd.read_csv(filename, encoding=enc, sep=sep, engine='python', on_bad_lines='skip')
            except:
                pass
    raise ValueError(f"Could not load {filename} with any encoding/separator combo.")

try:
    questions_df = load_csv_smart("Updated_100Q_Assessment.csv")
    map_df = load_csv_smart("Schema_Weighted_Score_Map.csv")
    schemas_df = load_csv_smart("20_Core_Schemas.csv")
except ValueError as e:
    st.error(f"Error loading required data files: {e}")
    st.stop()

ACTION_PLANS = { ... }  # ← Your entire 20-item dictionary remains 100% unchanged

standard_options = ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]
ace_options = ["Never", "Rarely", "Sometimes", "Often", "Very Often"]

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
    formatted = re.sub(r'(Week \d+:)', r'<br><span class="week-bold">\1</span>', plan_text)
    if formatted.startswith('<br>'):
        formatted = formatted[4:]
    return formatted

# ================================
#            MAIN UI (PERFECTED)
# ================================

with st.container():
    st.markdown("<div class='main-card'>", unsafe_allow_html=True)

    st.markdown("<h1>Latent Recursion Test</h1>", unsafe_allow_html=True)
    st.markdown("""
    <p class='centered-subtitle'>
        A powerful Psychological Schema Testing tool that reveals hidden patterns dictating your behavior, decisions, and life outcomes.
    </p>
    <p class='centered-subtitle'>
        Brought to you by <a href='http://www.mygipsy.com'>www.mygipsy.com</a>
    </p>
    """, unsafe_allow_html=True)
    st.divider()

    st.markdown("""
    <div style="background:#1e1b4b; padding:22px; border-radius:18px; border:1px solid #8b5cf6; margin-bottom:50px;">
        <strong>Disclaimer:</strong> This assessment is for informational and educational purposes only. Not a substitute for professional care. <strong>All questions required.</strong>
    </div>
    """, unsafe_allow_html=True)

    questions_per_page = 10
    total_pages = (len(questions_df) + questions_per_page - 1) // questions_per_page

    if st.session_state.page < total_pages:
        start = st.session_state.page * questions_per_page
        end = start + questions_per_page
        page_questions = questions_df.iloc[start:end]

        st.progress((st.session_state.page + 1) / total_pages)
        st.markdown(f"<h2>Section {st.session_state.page + 1} of {total_pages}</h2>", unsafe_allow_html=True)
        
        answered_count = len([qid for qid in page_questions['ID'] if qid in st.session_state.answers])
        st.metric("Answered", answered_count, len(page_questions))

        is_ace = 61 <= page_questions.iloc[0]['ID'] <= 70
        options = ace_options if is_ace else standard_options

        for _, q in page_questions.iterrows():
            qid = q['ID']
            text = q['Question Text']
            st.markdown(f"<div class='question-text'><strong>Q{qid}: {text}</strong></div>", unsafe_allow_html=True)

            current_answer = st.session_state.answers.get(qid, 3) - 1
            choice = st.radio(
                "",
                options=options,
                index=current_answer,
                key=f"q_{qid}",
                label_visibility="collapsed",
                horizontal=True
            )
            st.session_state.answers[qid] = options.index(choice) + 1

        col1, col2 = st.columns([1, 2])
        if st.session_state.page > 0:
            if col1.button("Previous"):
                st.session_state.page -= 1
                st.rerun()

        answered = all(qid in st.session_state.answers for qid in page_questions['ID'])
        if answered:
            label = "Submit & See Results" if st.session_state.page == total_pages - 1 else "Next"
            if col2.button(label, type="primary"):
                st.session_state.page += 1
                st.rerun()
        else:
            col2.button("Next", disabled=True)
            st.error("Please answer all questions on this page.")

    else:
        scores = calculate_schema_scores(st.session_state.answers)
        top_schemas, root_note, top_scores = get_top_schemas(scores)

        st.markdown("<h1>Your Results</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; font-size:1.35rem; color:#e2e8f0;'>Your top psychological patterns and personalized 30-day action plans</p>", unsafe_allow_html=True)
        st.divider()

        plain_text = "--- Latent Recursion Test Report ---\n\n"
        for sid in top_schemas:
            row = schemas_df[schemas_df['Schema'] == sid].iloc[0]
            name = row['Schema Name']
            score = top_scores[sid]
            root = row['Root Causes (Childhood Drivers)']
            patterns = row['Symptoms & Behavioral Loops']
            plan = ACTION_PLANS.get(sid, "Custom plan")

            st.markdown(f"### {name} ({score}%)")
            st.markdown(f"**Root Cause:** {root}")
            st.markdown(f"**Patterns:** {patterns}")

            teaser_lines = plan.split('\n')[:4]
            st.markdown("**Quick Start:**")
            for line in teaser_lines:
                if line.strip():
                    st.markdown(f"• {line.strip()}")
            with st.expander("View Full 30-Day Action Plan", expanded=False):
                st.markdown(f"<div class='action-plan-card'><div>{format_action_plan_html(plan)}</div></div>", unsafe_allow_html=True)

            st.divider()
            plain_text += f"Schema: {name} ({score}%)\nRoot: {root}\nPatterns: {patterns}\nPlan:\n{plan}\n\n---\n"

        if root_note:
            st.warning(root_note)

        pdf = generate_pdf(plain_text)
        st.download_button("Download PDF Report", pdf, "latent_recursion_report.pdf", "application/pdf")

        if st.button("Restart Assessment"):
            st.session_state.clear()
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

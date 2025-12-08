import streamlit as st
import pandas as pd
from io import BytesIO
import re
import streamlit.components.v1 as components
from fpdf import FPDF

# ================================
#         MODERN CSS + JS
# ================================
st.set_page_config(page_title="Latent Recursion Test", layout="centered")

MODERN_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    body { font-family: 'Inter', sans-serif; }
    .stApp { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }

    /* Centered white card */
    .main > div { max-width: 720px; margin: 0 auto; padding-top: 2rem; }
    .card {
        background: white;
        border-radius: 24px;
        box-shadow: 0 25px 50px rgba(0,0,0,0.22);
        padding: 3rem 2.5rem;
        margin: 2rem auto;
        animation: fadein 1s;
    }
    @keyframes fadein { from {opacity:0; transform:translateY(20px);} to {opacity:1; transform:none;} }

    h1 {
        font-size: 3rem;
        background: linear-gradient(90deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .centered-subtitle { text-align:center; font-size:1.15rem; color:#555; margin:0.8rem 0; }
    .centered-subtitle a { color:#764ba2; font-weight:600; }

    /* Progress bar */
    .progress-container {
        position: fixed;
        top: 0; left: 0; right: 0;
        height: 7px;
        background: rgba(255,255,255,0.2);
        z-index: 9999;
    }
    .progress-bar {
        height: 100%;
        background: #fff;
        width: 0%;
        transition: width 0.6s ease;
        box-shadow: 0 0 15px rgba(255,255,255,0.6);
    }

    /* Beautiful star rating */
    .rating {
        display: flex;
        flex-direction: row-reverse;
        justify-content: center;
        gap: 1.2rem;
        margin: 1.8rem 0;
    }
    .rating input { display: none; }
    .rating label {
        font-size: 2.8rem;
        cursor: pointer;
        transition: all 0.25s ease;
    }
    .rating label:hover,
    .rating input:checked ~ label,
    .rating label:hover ~ label {
        transform: scale(1.25);
    }
    .rating input:checked ~ label {
        animation: bounce 0.5s;
    }
    @keyframes bounce {
        0%,100%{transform:scale(1)} 50%{transform:scale(1.5)}
    }

    /* Question styling */
    .question-text {
        font-size: 1.28rem;
        font-weight: 600;
        color: #333;
        text-align: center;
        margin: 2.2rem 0 0.8rem;
    }

    /* Action plan cards */
    .action-plan-card {
        background: #f8f5ff;
        border-radius: 16px;
        padding: 1.8rem;
        margin: 2rem 0;
        border-left: 6px solid #764ba2;
    }
    .action-plan-title { margin-top:0; color:#764ba2; }
    .week-bold { font-weight:800; color:#764ba2; font-size:1.15rem; }

    /* Buttons */
    div.stButton > button {
        background: linear-gradient(90deg, #667eea, #764ba2);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.8rem 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        box-shadow: 0 8px 20px rgba(118,75,162,0.4);
        transition: all 0.3s;
    }
    div.stButton > button:hover {
        transform: translateY(-4px);
        box-shadow: 0 15px 30px rgba(118,75,162,0.5);
    }

    /* Hide Streamlit junk */
    #MainMenu, footer { visibility: hidden; }
    header { visibility: hidden; }
</style>

<div class="progress-container"><div class="progress-bar" id="progressBar"></div></div>

<script>
    // Update progress bar
    const total = """ + str(total_pages) + """;
    const current = """ + str(st.session_state.page + 1 if st.session_state.page < total_pages else total_pages) + """;
    const percent = (current / total) * 100;
    document.getElementById("progressBar").style.width = percent + "%";
</script>
"""

# Inject everything
components.html(MODERN_CSS, height=0)

# ================================
#         YOUR ORIGINAL CODE (cleaned & improved)
# ================================

# Load data safely
@st.cache_data
def load_csv_smart(filename):
    encodings = ['utf-8', 'utf-16', 'cp1252', 'latin1']
    for enc in encodings:
        for sep in [',', '\t', ';']:
            try:
                return pd.read_csv(filename, encoding=enc, sep=sep, engine='python', on_bad_lines='skip')
            except:
                continue
    raise ValueError(f"Could not load {filename}")

try:
    questions_df = load_csv_smart("Updated_100Q_Assessment.csv")
    map_df = load_csv_smart("Schema_Weighted_Score_Map.csv")
    schemas_df = load_csv_smart("20_Core_Schemas.csv")
except Exception as e:
    st.error(f"Error loading data files: {e}")
    st.stop()

# Session state
if 'page' not in st.session_state: st.session_state.page = 0
if 'answers' not in st.session_state: st.session_state.answers = {}

questions_per_page = 10
total_pages = (len(questions_df) + questions_per_page - 1) // questions_per_page

# ================================
#         ACTION PLANS (unchanged)
# ================================
ACTION_PLANS = { ... }  # ← keep your huge dictionary exactly as it was

# ================================
#         SCORING FUNCTIONS (unchanged)
# ================================
def calculate_schema_scores(answers): ...  # keep exactly as you had
def get_top_schemas(scores, trauma_threshold=60): ...  # keep exactly

def generate_pdf(plain_text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, plain_text.encode('latin-1', 'replace').decode('latin-1'))
    return BytesIO(pdf.output(dest='S').encode('latin-1'))

def format_action_plan_html(plan_text):
    return re.sub(r'(Week \d+:)', r'<br><span class="week-bold">\1</span>', plan_text)

# ================================
#             MAIN UI
# ================================

with st.container():
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    st.title("Latent Recursion Test")
    st.markdown("""
        <p class='centered-subtitle'>A powerful Psychological Schema Testing tool that reveals hidden patterns dictating your behavior, decisions, and life outcomes.</p>
        <p class='centered-subtitle'>Brought to you by <a href='http://www.mygipsy.com'>www.mygipsy.com</a></p>
    """, unsafe_allow_html=True)
    st.divider()

    st.markdown("""
        <div style="background:#fff8f0; padding:20px; border-radius:12px; border:1px solid #ffd7ba; margin-bottom:30px;">
            <strong>Disclaimer:</strong> This assessment is for informational and educational purposes only.
            Not a substitute for professional mental health care. <strong>All questions are mandatory.</strong>
        </div>
    """, unsafe_allow_html=True)

    # ------------------ QUESTIONS ------------------
    if st.session_state.page < total_pages:
        start = st.session_state.page * questions_per_page
        end = start + questions_per_page
        page_questions = questions_df.iloc[start:end]

        progress = (st.session_state.page + 1) / total_pages
        st.progress(progress)
        st.markdown(f"<h2 style='text-align:center; color:#764ba2;'>Section {st.session_state.page+1} of {total_pages}</h2>", unsafe_allow_html=True)

        # Scale label
        is_ace = 61 <= page_questions.iloc[0]['ID'] <= 70
        scale_text = "Never → Very Often" if is_ace else "Strongly Disagree → Strongly Agree"
        st.markdown(f"<p style='text-align:center; color:#555; font-weight:600;'>{scale_text}</p>", unsafe_allow_html=True)

        for _, q in page_questions.iterrows():
            qid = q['ID']
            text = q['Question Text']

            st.markdown(f"<div class='question-text'>Q{qid}: {text}</div>", unsafe_allow_html=True)

            # STAR RATING instead of radio
            cols = st.columns(5)
            selected = st.session_state.answers.get(qid, 3)
            for idx, col in enumerate(cols, 1):
                label = "★" if idx <= selected else "☆"
                if col.button(label, key=f"star_{qid}_{idx}", help=str(idx)):
                    st.session_state.answers[qid] = idx
                    st.rerun()

            st.markdown("<br>", unsafe_allow_html=True)

        col1, col2 = st.columns([1,2])
        if st.session_state.page > 0:
            if col1.button("Previous", use_container_width=True):
                st.session_state.page -= 1
                st.rerun()

        answered = all(qid in st.session_state.answers for qid in page_questions['ID'])
        if answered:
            btn_text = "Submit & See Results" if st.session_state.page == total_pages-1 else "Next"
            if col2.button(btn_text, type="primary", use_container_width=True):
                if st.session_state.page == total_pages-1:
                    st.session_state.page = total_pages
                else:
                    st.session_state.page += 1
                st.rerun()
        else:
            col2.button("Next / Submit", disabled=True, use_container_width=True)
            st.error("Please answer all questions on this page.")

    # ------------------ RESULTS PAGE
    else:
        scores = calculate_schema_scores(st.session_state.answers)
        top_schemas, root_note, top_scores = get_top_schemas(scores)

        st.header("Your Results")
        st.markdown("<p style='text-align:center; font-size:1.2rem;'>These are the top psychological patterns most influencing you right now — plus a 30-day action plan.</p>", unsafe_allow_html=True)
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
            st.markdown(f"**Root:** {root}")
            st.markdown(f"**Stuck Patterns:** {patterns}")

            st.markdown(f"""
                <div class='action-plan-card'>
                    <h4 class='action-plan-title'>30-Day Action Plan</h4>
                    <div class='action-plan-content'>{format_action_plan_html(plan)}</div>
                </div>
            """, unsafe_allow_html=True)

            plain_text += f"Schema: {name} ({score}%)\nRoot: {root}\nPatterns: {patterns}\nPlan:\n{plan}\n\n"
            st.divider()

        if root_note:
            st.warning(root_note)

        pdf = generate_pdf(plain_text)
        st.download_button("Download PDF Report", pdf, "latent_recursion_report.pdf", "application/pdf")

        if st.button("Restart Assessment", type="secondary"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)  # close card

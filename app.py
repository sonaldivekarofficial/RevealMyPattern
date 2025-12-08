import streamlit as st
import pandas as pd
from io import BytesIO
import re
import streamlit.components.v1 as components
from fpdf import FPDF

# ==============================
#  MODERN PREMIUM CSS + JS
# ==============================
PREMIUM_CSS_JS = """
<style>
/* Import Google Font */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    font-family: 'Inter', sans-serif;
}

/* Hide Streamlit junk */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Centered Card */
.css-1d391kg, .stApp {
    background: transparent;
}
.main-card {
    background: white;
    max-width: 780px;
    margin: 2rem auto;
    border-radius: 24px;
    box-shadow: 0 25px 50px rgba(0,0,0,0.18);
    padding: 3rem 2.5rem;
    min-height: 80vh;
}

/* Titles */
h1 {
    font-size: 3rem;
    font-weight: 800;
    background: linear-gradient(90deg, #667eea, #764ba2);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
    margin-bottom: 0.5rem;
}
h2 { 
    color: #764ba2; 
    text-align: center; 
    font-weight: 600;
}

/* Progress Bar */
.progress-container {
    position: fixed;
    top: 0; left: 0; right: 0;
    height: 8px;
    background: rgba(255,255,255,0.2);
    z-index: 9999;
}
.progress-bar {
    height: 100%;
    background: #fff;
    width: 0%;
    transition: width 0.6s cubic-bezier(0.65, 0, 0.35, 1);
    box-shadow: 0 0 15px rgba(255,255,255,0.6);
}

/* Beautiful Star Rating */
.rating {
    display: flex;
    flex-direction: row-reverse;
    justify-content: center;
    gap: 1.5rem;
    margin: 2rem 0;
    padding: 1rem;
}
.rating input {
    display: none;
}
.rating label {
    font-size: 3.2rem;
    cursor: pointer;
    transition: all 0.3s ease;
    filter: grayscale(100%);
}
.rating label:hover,
.rating label:hover ~ label,
.rating input:checked ~ label {
    filter: grayscale(0%);
    transform: scale(1.15);
}
.rating input:checked ~ label {
    animation: bounce 0.5s;
}

/* Question text */
.question-text {
    font-size: 1.35rem;
    font-weight: 600;
    text-align: center;
    color: #1a1a1a;
    margin: 2.5rem 0 1rem;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    font-weight: 700;
    font-size: 1.1rem;
    padding: 0.9rem 2rem;
    border-radius: 50px;
    border: none;
    box-shadow: 0 8px 20px rgba(118,75,162,0.4);
    transition: all 0.3s;
    width: 100%;
    margin-top: 2rem;
}
.stButton > button:hover {
    transform: translateY(-4px);
    box-shadow: 0 15px 30px rgba(118,75,162,0.5);
}

/* Action Plan Card */
.action-plan-card {
    background: linear-gradient(135deg, #f0fff4, #e8f5e9);
    border-left: 6px solid #4CAF50;
    border-radius: 16px;
    padding: 2rem;
    margin: 2rem 0;
    box-shadow: 0 8px 25px rgba(0,0,0,0.1);
}
.week-bold {
    font-weight: 800;
    color: #1b5e20;
    font-size: 1.15rem;
}

/* Animations */
@keyframes bounce {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.4); }
}

/* Mobile adjustments */
@media (max-width: 640px) {
    .rating label { font-size: 2.5rem; }
    .main-card { margin: 1rem; padding: 2rem 1.5rem; border-radius: 18px; }
    h1 { font-size: 2.4rem; }
}
</style>

<!-- Progress Bar Update -->
<script>
    const progress = parent.document.querySelector('.progress-bar');
    if (progress) {
        progress.style.width = `${{(st.session_state.page + 1) / st.session_state.get('total_pages', 1) * 100}}%`;
    }
    // Scroll to top on page change
    window.parent.document.body.scrollTop = 0;
    window.parent.document.documentElement.scrollTop = 0;
</script>
"""

st.markdown(PREMIUM_CSS_JS, unsafe_allow_html=True)
st.markdown('<div class="progress-container"><div class="progress-bar"></div></div>', unsafe_allow_html=True)

# ==============================
#  YOUR ORIGINAL LOGIC (cleaned & enhanced)
# ==============================
def load_csv_smart(filename):
    # ... (your existing function unchanged)
    encodings = ['utf-8', 'utf-16', 'cp1252', 'latin1']
    for enc in encodings:
        try: return pd.read_csv(filename, encoding=enc, engine='python', on_bad_lines='skip')
        except: pass
    raise ValueError(f"Could not load {filename}")

try:
    questions_df = load_csv_smart("Updated_100Q_Assessment.csv")
    map_df = load_csv_smart("Schema_Weighted_Score_Map.csv")
    schemas_df = load_csv_smart("20_Core_Schemas.csv")
except Exception as e:
    st.error(f"Missing data files: {e}")
    st.stop()

# Session state
if 'page' not in st.session_state: st.session_state.page = 0
if 'answers' not in st.session_state: st.session_state.answers = {}
if 'total_pages' not in st.session_state:
    st.session_state.total_pages = -(-len(questions_df) // 10)  # ceiling division

# Action plans (unchanged – you had them perfect)
ACTION_PLANS = {1: "Week 1: Keep a ...", 2: "Week 1: Track ...", ...}  # ← paste your full dict here

# Scoring functions (unchanged – they work great)
def calculate_schema_scores(answers): ...   # keep yours
def get_top_schemas(scores, trauma_threshold=60): ...  # keep yours

# ==============================
#  MAIN UI
# ==============================
st.set_page_config(page_title="Latent Recursion Test", layout="centered")

with st.container():
    st.markdown('<div class="main-card">', unsafe_allow_html=True)

    st.title("Latent Recursion Test")
    st.markdown("""
    <p style='text-align:center; font-size:1.25rem; color:#555;'>
        A powerful psychological schema testing tool that reveals hidden patterns dictating your behavior.
    </p>
    <p style='text-align:center; margin-top:1rem;'>
        Brought to you by <a href='http://www.mygipsy.com' target='_blank' style='color:#764ba2; font-weight:600;'>www.mygipsy.com</a>
    </p>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Disclaimer
    st.markdown("""
    <div style="background:#fff; padding:1.5rem; border-radius:12px; border:1px solid #eee; margin:1.5rem 0;">
        <strong>Disclaimer:</strong> This is for educational purposes only • Not a substitute for professional care • All questions required
    </div>
    """, unsafe_allow_html=True)

    questions_per_page = 10
    total_pages = st.session_state.total_pages

    if st.session_state.page < total_pages:
        start = st.session_state.page * questions_per_page
        end = start + questions_per_page
        page_qs = questions_df.iloc[start:end]

        # Progress text
        st.markdown(f"<h2>Section {st.session_state.page + 1} of {total_pages}</h2>", unsafe_allow_html=True)

        for _, q in page_qs.iterrows():
            qid = q['ID']
            text = q['Question Text']

            st.markdown(f'<div class="question-text">Q{qid}: {text}</div>', unsafe_allow_html=True)

            # STAR RATING instead of radio
            cols = st.columns(5)
            selected = st.session_state.answers.get(qid, 3)
            for i, col in enumerate(cols[::-1], 1):  # reverse so checking works naturally
                with col:
                    if st.button("★", key=f"star_{qid}_{i}",
                                help="1=Strongly Disagree → 5=Strongly Agree"):
                        st.session_state.answers[qid] = i
                        st.rerun()
                    if i == selected:
                        st.markdown(f"<script>document.querySelector('[data-testid=\"stButton\"][key=\"star_{qid}_{i}\"] button').style.filter='grayscale(0%)';"
                                    f"document.querySelector('[data-testid=\"stButton\"][key=\"star_{qid}_{i}\"] button').style.transform='scale(1.3)';</script>",
                                    unsafe_allow_html=True)

            # Force selected star to be colored (fallback)
            if selected:
                st.markdown(f"""
                <style>
                [key="star_{qid}_{selected}"] button {{ filter: grayscale(0%) !important; transform: scale(1.3); }}
                [key="star_{qid}_{selected}"] button:hover {{ transform: scale(1.45); }}
                </style>
                """, unsafe_allow_html=True)

        # Navigation
        col1, col2 = st.columns([1, 2])
        if st.session_state.page > 0:
            if col1.button("⬅️ Previous"):
                st.session_state.page -= 1
                st.rerun()

        all_answered = all(q['ID'] in st.session_state.answers for _, q in page_qs.iterrows())
        if col2.button("Next ➡️" if st.session_state.page < total_pages-1 else "See My Results 🎉",
                       disabled=not all_answered):
            if all_answered:
                if st.session_state.page == total_pages - 1:
                    st.session_state.page = total_pages
                else:
                    st.session_state.page += 1
                st.rerun()

    else:
        # === RESULTS PAGE (same logic, just prettier) ===
        scores = calculate_schema_scores(st.session_state.answers)
        top_schemas, root_note, top_scores = get_top_schemas(scores)

        st.header("Your Hidden Patterns Are Revealed")
        st.markdown("<p style='text-align:center; font-size:1.3rem; color:#555;'>Here are the top psychological schemas currently shaping your life — plus a 30-day plan to break free.</p>", unsafe_allow_html=True)

        for sid in top_schemas:
            row = schemas_df[schemas_df['Schema'] == sid].iloc[0]
            name = row['Schema Name']
            score = top_scores[sid]
            root = row['Root Causes (Childhood Drivers)']
            patterns = row['Symptoms & Behavioral Loops']
            plan = ACTION_PLANS.get(sid, "Custom plan coming soon.")

            # Beautiful action plan
            formatted = re.sub(r'(Week \d+:)', r'<br><span class="week-bold">\1</span><br>', plan)
            if formatted.startswith('<br>'): formatted = formatted[4:]

            st.markdown(f"### 🎯 {name} — {score}%")
            st.markdown(f"**Root Cause:** {root}")
            st.markdown(f"**Current Loops:** {patterns}")
            st.markdown(f"""
            <div class="action-plan-card">
                <h4 style="color:#2e7d32; margin-top:0;">30-Day Breakthrough Plan</h4>
                <div style="line-height:1.8;">{formatted}</div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("---")

        if root_note:
            st.warning(root_note)

        # PDF download (unchanged logic)
        # ... keep your generate_pdf + download_button code here

        if st.button("Start Over"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)  # close main-card

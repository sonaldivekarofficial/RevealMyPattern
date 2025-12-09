import streamlit as st
import pandas as pd
from io import BytesIO
import re
from fpdf import FPDF
import streamlit.components.v1 as components

# ============================ PAGE CONFIG & CUSTOM CSS/JS ============================
st.set_page_config(layout="centered", page_title="Latent Recursion Test")

components.html("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@900&display=swap');
    
    body, .stApp { background:#0f172a !important; }
    .main-card { 
        background:#1e293b; 
        max-width:880px; 
        margin:2rem auto; 
        padding:5rem 4rem προβ; 
        border-radius:32px; 
        box-shadow:0 30px 90px rgba(0,0,0,0.7);
    }
    
    /* PERFECTLY CENTERED TITLE */
    h1 { 
        text-align: center !important; 
        font-size: 3.5rem !important; 
        font-weight: 900 !important;
        margin: 0 0 2rem 0 !important;
        font-family: 'Inter', sans-serif !important;
        color: white !important;
    }
    
    /* MUCH BIGGER QUESTION TEXT */
    .big-question {
        font-size: 2.1rem !important;
        color:#ffffff !important;
        text-align:center !important;
        margin: 4.5rem 0 3rem 0 !important;
        line-height:1.5 !important;
        font-weight: 600 !important;
    }
    
    /* GREEN GLOW ON SELECTED RADIO - BULLETPROOF */
    div[data-testid="stRadio"] label {
        background: transparent !important;
        color: #94a3b8 !important;
        padding: 0.9rem 1.4rem !important;
        border-radius: 12px !important;
        transition: all 0.3s ease !important;
        font-size: 1.1rem !important;
    }
    div[data-testid="stRadio"] label[data-checked="true"] {
        background: #10b981 !important;
        color: white !important;
        font-weight: 900 !important;
        box-shadow: 0 0 40px #10b981 !important;
        transform: scale(1.15) !important;
    }
    
    /* HIDE ALL STREAMLIT JUNK + ANSWERED COUNTER + PROGRESS BAR */
    #MainMenu, footer, header, .stAlert, .stProgress { visibility:hidden !important; }
    .answered-counter, [data-testid="stMetric"] { display: none !important; }
</style>

<script>
    // Force scroll to top on EVERY rerun
    window.parent.scrollTo(0, 0);
    setTimeout(() => window.parent.scrollTo(0, 0), 50);
</script>
""", height=0)

# ============================ DATA LOADING ============================
def load_csv_smart(filename):
    encodings = ['utf-8', 'utf-16', 'cp1252', 'latin1', 'iso-8859-1', 'mbcs']
    separators = [',', '\t', ';']
    for enc in encodings:
        for sep in separators:
            try:
                return pd.read_csv(filename, encoding=enc, sep=sep, engine='python', on_bad_lines='skip')
            except:
                pass
    raise ValueError(f"Could not load {filename}")

try:
    questions_df = load_csv_smart("Updated_100Q_Assessment.csv")
    map_df = load_csv_smart("Schema_Weighted_Score_Map.csv")
    schemas_df = load_csv_smart("20_Core_Schemas.csv")
except ValueError as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# ============================ FULL ACTION PLANS DICTIONARY ============================
ACTION_PLANS = {
    1: "Week 1: Keep a 'Perfectionism Log'. Record situations where you felt the urge to be perfect. Note the specific standard you felt you had to meet and rate your anxiety (1-10). Identify if the standard was self-imposed or external.\nWeek 2: Use 'Cost-Benefit Analysis'. List the advantages (e.g., praise, safety) vs. disadvantages (e.g., burnout, time loss) of your high standards. Challenge the 'All-or-Nothing' distortion: 'If I'm not perfect, I'm a failure.'\nWeek 3: The 'B+ Experiment'. Deliberately perform a low-stakes task (e.g., an internal email, a quick chore) to an 80% standard. Resist the urge to fix it. Record the outcome: Did a catastrophe happen?\nWeek 4: Create a 'Good Enough' Mantra card. Schedule mandatory 'Non-Productive Time' where the goal is specifically to achieve nothing, reinforcing worth separate from output.",
    2: "Week 1: Track 'Agency Moments'. Record times during the day when you actually made a choice (even small ones like what to eat). Rate your sense of control (0-10) for each.\nWeek 2: Challenge 'Fortune Telling'. When you think 'It won't matter anyway,' ask: 'What is the evidence for this?' and 'Have I ever influenced an outcome before?' Write down 3 counter-examples.\nWeek 3: Graded Task Assignment. Pick one micro-goal (e.g., wash 3 dishes, send 1 text). Do not focus on the outcome, only the initiation. Treat the action itself as the success.\nWeek 4: Build a 'Success Log'. Every evening, write down 3 things you influenced that day. Review this log whenever the feeling of paralysis returns.",
    3: "Week 1: Identify 'Fixed Triggers'. Notice when you say 'I can't do this' or 'I'm not good at this.' Label these as 'Fixed Mindset Thoughts' rather than facts.\nWeek 2: Reframe 'Failure' to 'Data'. When you make a mistake, complete this sentence: 'This mistake teaches me that I need to adjust X, not that I am Y.'\nWeek 3: The 'Beginner's Mind' Experiment. Engage in a hobby or task you are terrible at for 15 minutes. Observe the discomfort of not being expert. Allow yourself to be clumsy without judgment.\nWeek 4: Establish a 'Yet' Habit. Append the word 'yet' to every inability statement (e.g., 'I don't understand this code... yet'). Schedule one weekly learning session for a new skill.",
    4: "Week 1: The 'Critic Audit'. Give your inner critic a name (e.g., 'The Judge'). Tally how many times 'The Judge' speaks to you daily. Note the tone—is it angry, cold, or mocking?\nWeek 2: Compassionate Re-framing. For every critical thought, write a 'Compassionate Response' as if speaking to a friend or child. Example: Change 'You idiot' to 'You made a human mistake.'\nWeek 3: Mirror Work. Stand in front of a mirror for 2 minutes daily. Look at yourself and say 3 factual, neutral, or positive things. Sit with the discomfort this causes.\nWeek 4: The 'Good Enough' Letter. Write a letter of forgiveness to yourself for a past mistake. Keep a 'Credit List'—daily things you did right, no matter how small.",
    5: "Week 1: Trigger Mapping. Track moments of 'Abandonment Panic'. What triggered it? (e.g., a delayed text, a neutral tone). Rate the intensity.\nWeek 2: Check the Facts. When panic sets in, ask: 'Is this a fact or a fear?' 'Is there an alternative explanation for their behavior (e.g., they are busy)?'\nWeek 3: Response Prevention. When the urge to seek reassurance hits (e.g., double texting), wait 30 minutes. Self-soothe during the gap (deep breathing, walking).\nWeek 4: Self-Soothing Kit. Create a physical or digital list of activities that calm you down *without* involving another person. Practice one daily regardless of anxiety levels.",
    6: "Week 1: Emotion Naming. Set a timer 3 times a day. Ask: 'What am I feeling physically?' and 'What emotion matches this?' (Use an Emotion Wheel).\nWeek 2: Challenge 'Independence'. Examine the belief 'If I need others, I am weak.' Look for evidence where mutual support actually increased strength or efficiency.\nWeek 3: Micro-Vulnerability. Share one small, genuine feeling or opinion with a safe person that you would usually keep to yourself. (e.g., 'I had a hard day' instead of 'I'm fine').\nWeek 4: Connection Scheduling. Schedule 15 minutes of 'undistracted connection' time with a partner or friend weekly. No phones, just presence.",
    7: "Week 1: The 'Yes' Audit. Track every time you said 'Yes' when you wanted to say 'No'. Note the physical sensation (e.g., stomach knot).\nWeek 2: Decatastrophizing 'No'. Write down: 'If I say no, I fear X will happen.' Then write: 'If X happens, I will cope by Y.' Challenge the idea that saying no makes you 'bad'.\nWeek 3: The 'Buy Time' Technique. For one week, do not agree to anything immediately. Use the script: 'Let me check my schedule and get back to you.' Practice sitting with the guilt.\nWeek 4: Boundary Scripting. Write down 3 standard scripts for refusal. Practice saying them out loud. Reward yourself for every boundary set.",
    8: "Week 1: Screen Time Audit. Use an app tracker. Identify the 'Numbing Hour'—the specific time of day you scroll to avoid feeling.\nWeek 2: Identify the Void. When reaching for the phone, pause 5 seconds. Ask: 'What am I avoiding?' (Boredom, loneliness, anxiety). Write it down instead of scrolling.\nWeek 3: Gray Scale Experiment. Turn your phone to Grayscale mode for the week. Leave the phone in another room during meals and sleep. Replace the scrolling time with a physical book or walk.\nWeek 4: Real World Anchoring. Establish 'Tech-Free Zones' (e.g., bedroom, dinner table). Schedule one face-to-face (or voice) interaction per week to replace a digital one.",
    9: "Week 1: Expense Awareness. Track spending without judgment. Notice the emotion attached to buying (guilt, relief, panic).\nWeek 2: Cognitive Restructuring. Challenge 'Catastrophic Poverty' thoughts. Replace 'I will end up homeless' with 'I have skills and resources to manage challenges.'\nWeek 3: Financial Exposure. Open your bank statements/bills that you avoid. Sit with the numbers for 10 minutes until the panic creates a bell curve (rises then falls).\nWeek 4: The 'Abundance' Plan. Automate a very small savings amount (even $5) to prove you have margin. Create a 1-month realistic budget.",
    10: "Week 1: Chaos Scan. Photograph your primary living space. Look at the photo objectively. Identify 3 areas that drain your energy visually.\nWeek 2: Visualization. Visualize a calm, ordered space. Connect the feeling of 'safety' with 'order' rather than 'chaos'. Challenge the belief 'Clutter doesn't affect me' by noting how it impacts focus/mood.\nWeek 3: The 15-Minute Sweep. Do not try to clean the whole house. Set a timer for 15 minutes daily to clear one flat surface. Stop when the timer dings.\nWeek 4: Sanctuary Creation. Designate one corner or room as a 'Chaos-Free Zone'. Maintain this single area strictly as a retreat for your nervous system.",
    11: "Week 1: Threat Log. Note how many times you scan for danger (e.g., checking exits, watching people). Rate the *actual* safety of the environment (0-10).\nWeek 2: Probability Estimation. When you fear a threat, rate the probability (0-100%). Compare this to the probability of safety. Challenge 'Possible vs. Probable'.\nWeek 3: Safety Drop. In a known safe environment (home), deliberately lower your shoulders and unclench your jaw. Close your eyes for 1 minute. Teach the body safety.\nWeek 4: Grounding Routine. Practice 5-4-3-2-1 grounding whenever vigilance spikes. Create a 'Safety Anchor' object to carry.",
    12: "Week 1: Energy Accounting. Treat energy like money. Track deposits (rest, food) vs. withdrawals (work, stress). Identify where you are overdrawn.\nWeek 2: Permission to Rest. Identify the rule 'I must always be productive.' Replace with 'Rest is productive because it repairs me.'\nWeek 3: Pacing Experiment. Break tasks into 20-minute chunks with mandatory 5-minute floor-rests. Stop *before* you are exhausted.\nWeek 4: Sleep Hygiene Reset. Establish a strict wind-down routine. No screens 1 hour before bed. Make the bedroom for sleep only.",
    13: "Week 1: Values Sort. List 5 core values (e.g., creativity, service, freedom). Rate how much your current daily life aligns with them (1-10).\nWeek 2: Challenge 'The Destination'. Restructure the thought 'I will be happy when...' to 'I can find meaning in...'. Focus on process over outcome.\nWeek 3: Novelty Action. Try one activity purely for curiosity, not mastery or profit (e.g., a pottery class, a hike in a new place).\nWeek 4: Service Micro-Dose. Spend 1 hour/week helping someone else or a cause. Observe the impact on your sense of purpose.",
    14: "Week 1: Negativity Bias Log. Track how many times you predict a negative outcome. Mark how many actually came true.\nWeek 2: Alternative Outcomes. For every negative prediction, force yourself to write one positive and one neutral outcome.\nWeek 3: Savoring Practice. Spend 2 minutes daily solely focusing on a positive sensory experience (coffee, sun). Amplify the good feelings.\nWeek 4: Gratitude Discipline. Write 3 specific things that went well today. Explain *why* they went well due to your efforts (internal attribution).",
    15: "Week 1: Body Scan. Since emotions are numb, track physical tension. Where does the grief live? (Chest, throat, stomach). Use an emotion wheel to label feelings before scanning.\nWeek 2: Grief Letters. Write a letter to what/who was lost. Do not send it. Allow yourself to write the angry or sad parts without editing.\nWeek 3: Scheduled Grieving. Set aside 20 minutes to listen to music or view photos that evoke the loss. Allow the wave to hit, then self-soothe.\nWeek 4: Integration. Create a ritual to honor the loss (planting a tree, lighting a candle). Move from 'getting over it' to 'carrying it with you'.",
    16: "Week 1: Time Blindness Track. Estimate how long a task will take, then time it. Note the discrepancy.\nWeek 2: Chunking. Break 'Big Scary Tasks' into 'Nano-Steps' (e.g., 'Open laptop' is step 1). Cognitive reframe: 'I only have to do the first step.'\nWeek 3: The Pomodoro Method. Work 25 mins, rest 5. Use an external timer (not phone). Externalize executive function.\nWeek 4: Visual Systems. Set up a visual kanban board or whiteboard (To Do, Doing, Done). Move physical sticky notes to create dopamine hits.",
    17: "Week 1: Blame Audit. Notice when you say 'It's not my fault' or 'They made me'. Catch the deflection reflex.\nWeek 2: Radical Responsibility. For one small error, practice saying 'I made a mistake, here is how I will fix it.' Observe that the world doesn't end.\nWeek 3: The 'Hard Thing' First. Do the most dreaded task first thing in the morning (Eat the Frog). Build tolerance for discomfort.\nWeek 4: Ownership Language. Change 'I have to' to 'I choose to'. Reclaim agency over your obligations.",
    18: "Week 1: Delegation Log. List tasks you are doing that others could do. Note the thought blocking you (e.g., 'They'll mess it up').\nWeek 2: Trust Testing. Challenge the thought 'No one can do it like me.' Is this fact, or a control mechanism?\nWeek 3: The 'Ask' Experiment. Ask for help with one small, low-risk task (e.g., asking for directions or a small favor).\nWeek 4: Interdependence. Identify one area where collaboration yields better results than solo work. Initiate a collaborative effort.",
    19: "Week 1: Connection Inventory. How many meaningful interactions do you have weekly? Rate your feeling of belonging (1-10).\nWeek 2: Empathy Exercise. When seeing a stranger, practice imagining their life, struggles, and hopes. Humanize the 'other'.\nWeek 3: Contribution. Do one small act for the community (pick up trash, donate, hold a door). Focus on the feeling of being part of the whole.\nWeek 4: Group Participation. Join one local group or online community centered on a shared interest. Attend once.",
    20: "Week 1: Trigger Awareness (Safety First). Identify specific sensory triggers (smells, sounds). Focus on grounding immediately when triggered.\nWeek 2: Cognitive Processing. Work on 'Stuck Points' (e.g., 'The world is unsafe'). Differentiate 'Then' (trauma time) vs. 'Now' (safe time).\nWeek 3: Titrated Exposure. Slowly approach safe situations you avoid due to trauma triggers. Do this only when regulated.\nWeek 4: Maintenance & Care. Build a robust support network (therapy, groups). Prioritize nervous system regulation as a lifestyle, not a fix"
}

standard_options = ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]
ace_options = ["Never", "Rarely", "Sometimes", "Often", "Very Often"]

if 'page' not in st.session_state:
    st.session_state.page = 0
if 'answers' not in st.session_state:
    st.session_state.answers = {}

# ============================ SCORING & RESULTS LOGIC ============================
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
    formatted = re.sub(r'(Week \d+:)', r'<br><span style="font-weight:900;color:#c084fc">\\1</span>', plan_text)
    return formatted

# ============================ MAIN UI ============================
with st.container():
    st.markdown("<div class='main-card'>", unsafe_allow_html=True)

    st.markdown("<h1>Latent Recursion Test</h1>", unsafe_allow_html=True)
    st.markdown("""
    <p style='text-align:center;font-size:1.35rem;color:#94a3b8;margin:2rem 0 5rem;line-height:1.8'>
        A powerful Psychological Schema Testing tool that reveals hidden patterns dictating your behavior, decisions, and life outcomes.<br>
        Brought to you by <a href='http://www.mygipsy.com' style='color:#c084fc;text-decoration:none'>www.mygipsy.com</a>
    </p>
    """, unsafe_allow_html=True)

    questions_per_page = 10
    total_pages = (len(questions_df) + questions_per_page - 1) // questions_per_page

    if st.session_state.page < total_pages:
        start = st.session_state.page * questions_per_page
        end = start + questions_per_page
        page_questions = questions_df.iloc[start:end]

        st.markdown(f"<h2 style='text-align:center;color:#c084fc;margin:4rem 0 3rem;font-size:2.6rem'>Section {st.session_state.page + 1} of {total_pages}</h2>", unsafe_allow_html=True)

        is_ace = 61 <= page_questions.iloc[0]['ID'] <= 70 if not page_questions.empty else False
        options = ace_options if is_ace else standard_options

        for _, q in page_questions.iterrows():
            qid = q['ID']
            text = q['Question Text']
            st.markdown(f"<div class='big-question'>Q{qid}: {text}</div>", unsafe_allow_html=True)

            choice = st.radio(
                "",
                options,
                index=st.session_state.answers.get(qid, 3) - 1,
                key=f"q_{qid}",
                label_visibility="collapsed",
                horizontal=True
            )
            st.session_state.answers[qid] = options.index(choice) + 1

        col1, col2 = st.columns([1, 2])
        if st.session_state.page > 0:
            if col1.button("← Previous", use_container_width=True):
                st.session_state.page -= 1
                st.rerun()

        if all(qid in st.session_state.answers for qid in page_questions['ID']):
            label = "Submit & See Results" if st.session_state.page == total_pages - 1 else "Next →"
            if col2.button(label, type="primary", use_container_width=True):
                st.session_state.page += 1
                st.rerun()
        else:
            col2.button("Next →", disabled=True, use_container_width=True)
            st.markdown("<p style='color:#ef4444;text-align:center;margin-top:1rem;font-size:1.1rem'>Please answer all questions to continue.</p>", unsafe_allow_html=True)

    else:
        scores = calculate_schema_scores(st.session_state.answers)
        top_schemas, root_note, top_scores = get_top_schemas(scores)

        st.markdown("<h1 style='text-align:center;margin-bottom:3rem'>Your Results</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center;font-size:1.5rem;color:#e2e8f0;margin-bottom:4rem'>Your top psychological patterns and personalized 30-day action plans</p>", unsafe_allow_html=True)

        plain_text = "--- Latent Recursion Test Report ---\n\n"
        for sid in top_schemas:
            r = schemas_df[schemas_df['Schema'] == sid].iloc[0]
            st.markdown(f"### {r['Schema Name']} ({top_scores[sid]}%)")
            st.markdown(f"**Root Cause:** {r['Root Causes (Childhood Drivers)']}")
            st.markdown(f"**Patterns:** {r['Symptoms & Behavioral Loops']}")
            st.markdown(f"<div style='background:#1e1b4b;padding:2rem;border-radius:16px;margin:3rem 0;border-left:8px solid #ec4899'><h4 style='color:#ec4899;margin-top:0'>30-Day Action Plan</h4>{format_action_plan_html(ACTION_PLANS[sid])}</div>", unsafe_allow_html=True)
            st.markdown("---")
            plain_text += f"Schema: {r['Schema Name']} ({top_scores[sid]}%)\nRoot: {r['Root Causes (Childhood Drivers)']}\nPatterns: {r['Symptoms & Behavioral Loops']}\nPlan:\n{ACTION_PLANS[sid]}\n\n---\n\n"

        if root_note:
            st.warning(root_note)

        st.download_button(
            "Download Full PDF Report",
            generate_pdf(plain_text),
            "latent_recursion_report.pdf",
            "application/pdf",
            use_container_width=True
        )

        if st.button("Take Test Again", use_container_width=True):
            st.session_state.clear()
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

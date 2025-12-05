import streamlit as st
import pandas as pd
from io import BytesIO
import csv
import codecs
from fpdf import FPDF
import re

# --- GLOBAL CONFIGURATION AND SCALES ---

# Define the two distinct scale option sets (1-5)
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

# --- UTILITY FUNCTIONS ---

# Smart CSV loader to handle encoding issues
def load_csv_smart(filename):
    encodings = ['utf-8', 'utf-16', 'cp1252', 'latin1', 'iso-8859-1', 'mbcs']
    separators = [',', '\t', ';']
    for enc in encodings:
        for sep in separators:
            try:
                # Added 'on_bad_lines=skip' for robustness
                return pd.read_csv(filename, encoding=enc, sep=sep, engine='python', on_bad_lines='skip')
            except:
                pass
    raise ValueError(f"Could not load {filename} with any encoding/separator combo.")

# Load data
try:
    questions_df = load_csv_smart("Updated_100Q_Assessment.csv")
    map_df = load_csv_smart("Schema_Weighted_Score_Map.csv")
    schemas_df = load_csv_smart("20_Core_Schemas.csv")
except ValueError as e:
    st.error(f"Error loading required data files: {e}")
    st.stop()


# Action plans (Data remains the same)
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
    11: "Week 1: Threat Log. Note how many times you scan for danger (e.g., checking exits, watching people). Rate the *actual* safety of the environment (0-10).\nWeek 2: Probability Estimation. When you fear a threat, rate the probability (0-100%). Compare this to the probability of safety. Challenge 'Possible vs. Probable'.\nWeek 3: Safety Drop. In a known safe environment (home), deliberately lower your shoulders and unclench your jaw. Close your eyes for 1 minute. Teach the body safety.\nWeek 4: Grounding Routine. Practice 5-4-3-2-1 grounding (5 things seen, 4 touched, etc.) whenever vigilance spikes. Create a 'Safety Anchor' object to carry.",
    12: "Week 1: Energy Accounting. Treat energy like money. Track deposits (rest, food) vs. withdrawals (work, stress). Identify where you are overdrawn.\nWeek 2: Permission to Rest. Identify the rule 'I must always be productive.' Replace with 'Rest is productive because it repairs me.'\nWeek 3: Pacing Experiment. Break tasks into 20-minute chunks with mandatory 5-minute floor-rests. Stop *before* you are exhausted.\nWeek 4: Sleep Hygiene Reset. Establish a strict wind-down routine. No screens 1 hour before bed. Make the bedroom for sleep only.",
    13: "Week 1: Values Sort. List 5 core values (e.g., creativity, service, freedom). Rate how much your current daily life aligns with them (1-10).\nWeek 2: Challenge 'The Destination'. Restructure the thought 'I will be happy when...' to 'I can find meaning in...'. Focus on process over outcome.\nWeek 3: Novelty Action. Try one activity purely for curiosity, not mastery or profit (e.g., a pottery class, a hike in a new place).\nWeek 4: Service Micro-Dose. Spend 1 hour/week helping someone else or a cause. Observe the impact on your sense of purpose.",
    14: "Week 1: Negativity Bias Log. Track how many times you predict a negative outcome. Mark how many actually came true.\nWeek 2: Alternative Outcomes. For every negative prediction, force yourself to write one positive and one neutral outcome.\nWeek 3: Savoring Practice. Spend 2 minutes daily solely focusing on a positive sensory experience (coffee, sun). Amplify the good feelings.\nWeek 4: Gratitude Discipline. Write 3 specific things that went well today. Explain *why* they went well due to your efforts (internal attribution).",
    15: "Week 1: Body Scan. Since emotions are numb, track physical tension. Where does the grief live? (Chest, throat, stomach). Use an emotion wheel to label feelings before scanning.\nWeek 2: Grief Letters. Write a letter to what/who was lost. Do not send it. Allow yourself to write the angry or sad parts without editing.\nWeek 3: Scheduled Grieving. Set aside 20 minutes to listen to music or view photos that evoke the loss. Allow the wave to hit, then self-soothe.\nWeek 4: Integration. Create a ritual to honor the loss (planting a tree, lighting a candle). Move from 'getting over it' to 'carrying it with you'.",
    16: "Week 1: Time Blindness Track. Estimate how long a task will take, then time it. Note the discrepancy.\nWeek 2: Chunking. Break 'Big Scary Tasks' into 'Nano-Steps' (e.g., 'Open laptop' is step 1). Cognitive reframe: 'I only have to do the first step.'\nWeek 3: The Pomodoro Method. Work 25 mins, rest 5. Use an external timer (not phone). Externalize executive function.\nWeek 4: Visual Systems. Set up a visual kanban board or whiteboard (To Do, Doing, Done). Move physical sticky notes to create dopamine hits.",
    17: "Week 1: Blame Audit. Notice when you say 'It's not my fault' or 'They made me'. Catch the deflection reflex.\nWeek 2: Radical Responsibility. For one small error, practice saying 'I made a mistake, here is how I will fix it.' Observe that the world doesn't end.\nWeek 3: The 'Hard Thing' First. Do the most dreaded task first thing in the morning (Eat the Frog). Build tolerance for discomfort.\nWeek 4: Ownership Language. Change 'I have to' to 'I choose to'. Reclaim agency over your obligations.",
    18: "Week 1: Delegation Log. List tasks you are doing that others could do. Note the thought blocking you (e.g., 'They'll mess it up').\nWeek 2: Trust Testing. Challenge the thought 'No one can do it like me.' Is this fact, or a control mechanism?\nWeek 3: The 'Ask' Experiment. Ask for help with one small, low-risk task (e.g., asking for directions or a small favor).\nWeek 4: Interdependence. Identify one area where collaboration yields better results than solo work. Initiate a collaborative effort.",
    19: "Week 1: Connection Inventory. How many meaningful interactions do you have weekly? Rate your feeling of belonging (1-10).\nWeek 2: Empathy Exercise. When seeing a stranger, practice imagining their life, struggles, and hopes. Humanize the 'other'.\nWeek 3: Contribution. Do one small act for the community (pick up trash, donate, hold a door). Focus on the feeling of being part of the whole.\nWeek 4: Group Participation. Join one local group or online community centered on a shared interest. Attend once.",
    20: "Week 1: Trigger Awareness (Safety First). Identify specific sensory triggers (smells, sounds). Focus on grounding immediately when triggered.\nWeek 2: Cognitive Processing. Work on 'Stuck Points' (e.g., 'The world is unsafe'). Differentiate 'Then' (trauma time) vs. 'Now' (safe time).\nWeek 3: Titrated Exposure. Slowly approach safe situations you avoid due to trauma triggers. Do this only when regulated.\nWeek 4: Maintenance & Care. Build a robust support network (therapy, groups). Prioritize nervous system regulation as a lifestyle, not a fix."
}

# --- SCORING AND REPORT GENERATION ---

# Session state
if 'page' not in st.session_state:
    st.session_state.page = 0
if 'answers' not in st.session_state:
    st.session_state.answers = {}

# Calculate scores with fixes
def calculate_schema_scores(answers):
    # Check if all questions are answered, crucial for 100% completion
    if len(answers) != len(questions_df):
        # This should ideally be caught by the front-end check, but acts as a server-side guard
        # Since question 70 is included in the ACE check and not the main check, we use len()
        st.error("Submission failed: Not all 100 questions were answered.")
        return {}
        
    results = {}
    for schema_id in map_df['Schema_ID'].unique():
        schema_rows = map_df[map_df['Schema_ID'] == schema_id]
        raw_scores = []
        max_possible = 0
        
        for _, row in schema_rows.iterrows():
            qid = row['Question_ID']
            direction = row['Direction']
            
            # Ensure the user value is between 1 and 5
            user_val = min(max(answers.get(qid, 0), 1), 5) 
            
            # ACE questions (61-70) are scored as binary (1 or 0) based on value > 1
            is_ace = 61 <= qid <= 70
            
            if is_ace:
                # Contribution is 1 if score is > 1 ("Never" is 1, so 2-5 give a 1 contribution)
                contrib = 1 if user_val > 1 else 0
                q_max = 1
            else:
                # Standard questions use the 1-5 score directly
                contrib = user_val
                q_max = 5
                
            # Score calculation: if direction=1 (positive), score=contribution. 
            # If direction=0 (reverse), score=max_possible + 1 - contribution
            score = contrib if direction == 1 else (q_max + 1 - contrib)
            
            raw_scores.append(score)
            max_possible += q_max
            
        raw_sum = sum(raw_scores)
        percentage = (raw_sum / max_possible) * 100 if max_possible > 0 else 0
        results[schema_id] = round(percentage, 1)
        
    return results

# Get top schemas
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

# PDF generation using FPDF
def generate_pdf(plain_text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    # Use multi_cell for automatic line breaks
    pdf.multi_cell(0, 10, plain_text.encode('latin-1', 'replace').decode('latin-1')) 
    pdf_bytes = BytesIO(bytes(pdf.output(dest='S')))
    pdf_bytes.seek(0)
    return pdf_bytes

# --- APP LAYOUT ---
st.set_page_config(layout="wide")
st.title("Psychological Schema Assessment MVP")

# Disclaimer
st.markdown("""
<div style="padding: 10px; background-color: #f0f0f5; border-radius: 5px; border-left: 5px solid #ffa500;">
    <strong>Disclaimer:</strong> This assessment is for informational and educational purposes only. It is not a substitute for professional mental health diagnosis or treatment. The results are based on schema therapy principles and should be discussed with a qualified mental health professional. All questions are mandatory.
</div>
""", unsafe_allow_html=True)
st.divider()

questions_per_page = 10
total_pages = (len(questions_df) // questions_per_page)
if len(questions_df) % questions_per_page != 0:
    total_pages += 1
    
if st.session_state.page < total_pages:
    
    start = st.session_state.page * questions_per_page
    end = start + questions_per_page
    page_questions = questions_df.iloc[start:end]
    
    st.progress((st.session_state.page + 1) / total_pages)
    st.subheader(f"Section {st.session_state.page + 1} of {total_pages}")
    
    # --- Display Scale Key based on the first question of the page ---
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
        **SCALE FOR THIS SECTION:** **1** = {scale_min_text} 
        **5** = {scale_max_text}
        """,
        unsafe_allow_html=True
    )
    st.markdown("---")
    
    # --- Question Rendering Loop ---
    for _, q in page_questions.iterrows():
        qid = q['ID']
        question_text = q['Question Text']
        
        # Determine options for the individual question
        if 61 <= qid <= 70:
            current_options_q = ace_options
        else:
            current_options_q = standard_options
            
        # Get stored numerical value (1-5), default to 3 (Neutral/Sometimes)
        previous_val = st.session_state.answers.get(qid, 3)
        # Convert the numerical value back to the corresponding option string for the radio button index
        previous_answer_str = current_options_q[previous_val - 1]
        
        # Use st.radio to display discrete options (text labels)
        selected_option_str = st.radio(
            f"**Q{qid}:** {question_text}", 
            options=current_options_q, 
            index=current_options_q.index(previous_answer_str), # Set default selection
            key=f"q_{qid}",
            horizontal=True 
        )
        
        # Convert the selected string back to the required integer value (1-5)
        # Extracts the number from the string (e.g., "3. Neutral" -> 3)
        try:
            selected_val = int(selected_option_str.split('.')[0])
            st.session_state.answers[qid] = selected_val
        except (ValueError, IndexError):
            # Fallback in case of unexpected string format, defaults to Neutral/Sometimes (3)
            st.session_state.answers[qid] = 3 
            
    st.markdown("---")
    
    # --- Navigation Buttons ---
    col1, col2 = st.columns(2)
    
    if st.session_state.page > 0:
        if col1.button("⬅️ Previous"):
            st.session_state.page -= 1
            st.rerun()
            
    # Check if all questions on the current page have been answered (mandatory check)
    current_page_answered_count = sum(1 for qid in page_questions['ID'] if qid in st.session_state.answers)
    
    if current_page_answered_count < len(page_questions):
        # Display a warning if not all questions on the page are answered
        if col2.button("Next / Submit ➡️"):
            st.error(f"Please answer all {len(page_questions)} questions on this page before continuing.")
    
    else:
        # Proceed logic (Next or Submit)
        button_label = "Submit & See Results 🎉" if st.session_state.page == total_pages - 1 else "Next ➡️"
        
        if col2.button(button_label):
            
            if st.session_state.page < total_pages - 1:
                # Move to next page
                st.session_state.page += 1
                st.rerun()
            else:
                # Submit logic (Final page)
                if len(st.session_state.answers) == len(questions_df):
                    st.session_state.page = total_pages # Move to results page
                    st.rerun()
                else:
                    st.error("Submission failed: Not all 100 questions were answered across the assessment.")
                
else:
    # --- RESULTS PAGE ---
    
    # Run calculation only when all questions are answered
    if len(st.session_state.answers) != len(questions_df):
        st.error("Error: Assessment data is incomplete. Please restart the assessment.")
        if st.button("Restart Assessment"):
            st.session_state.page = 0
            st.session_state.answers = {}
            st.rerun()
        st.stop()
        
    scores = calculate_schema_scores(st.session_state.answers)
    top_schemas, root_note, top_scores = get_top_schemas(scores)
    
    st.header("Your Top Schemas & Insights")
    st.markdown("Below are the top schemas driving your patterns and tailored action plans.")
    st.divider()
    
    plain_text = "--- Psychological Schema Assessment Report ---\n\n"
    
    for sid in top_schemas:
        schema_row = schemas_df[schemas_df['Schema'] == sid].iloc[0]
        name = schema_row['Schema Name']
        score = top_scores[sid]
        root = schema_row['Root Causes (Childhood Drivers)']
        patterns = schema_row['Symptoms & Behavioral Loops']
        plan = ACTION_PLANS.get(sid, 'Custom 30-day plan based on schema therapy principles.')
        
        st.markdown(f"### 🎯 {name} ({score}%)")
        st.markdown(f"**Root Cause:** {root}")
        st.markdown(f"**Patterns Keeping You Stuck:** {patterns}")
        st.markdown(f"**30-Day Action Plan:**\n```\n{plan}\n```")
        st.divider()
        
        plain_text += f"Schema: {name} ({score}%)\n\nRoot Cause: {root}\n\nPatterns Keeping You Stuck: {patterns}\n\n30-Day Action Plan:\n{plan}\n\n---\n"
        
    if root_note:
        st.warning(root_note)
        plain_text += f"Note: {root_note}\n\n"
        
    # PDF Download
    pdf = generate_pdf(plain_text)
    st.download_button("⬇️ Download PDF Report", pdf, "schema_report.pdf", "application/pdf")
    
    if st.button("Restart Assessment"):
        st.session_state.page = 0
        st.session_state.answers = {}
        st.rerun()

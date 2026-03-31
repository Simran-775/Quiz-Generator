# streamlit_app.py

import streamlit as st
from tabulate import tabulate
# Import the functions and variables from logic file
from project import TOPICS, wikipedia_fetch, generate_quiz 

# --- Streamlit State Initialization ---
def init_session_state():
    # 'config': Quiz setup stage
    # 'quiz_in_progress': Displaying questions
    # 'finished': Showing results
    if 'quiz_state' not in st.session_state:
        st.session_state.quiz_state = 'config'
    if 'quiz' not in st.session_state:
        st.session_state.quiz = []
    if 'score' not in st.session_state:
        st.session_state.score = 0
    if 'q_index' not in st.session_state:
        st.session_state.q_index = 0
    if 'show_feedback' not in st.session_state:
        st.session_state.show_feedback = False
    if 'user_answer' not in st.session_state:
        st.session_state.user_answer = None

init_session_state()

# --- Controller Functions ---

def start_quiz_session(topic, num_questions):
    """Fetches text, generates quiz, and moves to quiz state."""
    with st.spinner(f"Fetching content for {topic} and generating {num_questions} questions..."):
        text = wikipedia_fetch(topic)
        if not text:
            st.error("No Wikipedia content found for this topic.")
            return

        generated_quiz = generate_quiz(text, num_questions)
        
    if generated_quiz:
        st.session_state.quiz = generated_quiz
        st.session_state.score = 0
        st.session_state.q_index = 0
        st.session_state.quiz_state = 'quiz_in_progress'
        st.session_state.show_feedback = False
        st.session_state.user_answer = None
        st.rerun()
    else:
        st.error("No quiz could be generated. Try a different topic or fewer questions.")

def check_answer_and_proceed(current_q, user_input):
    """Checks the answer, updates score, and sets up for next step."""
    
    correct = False
    if current_q['type'] == 'mcq':
        # MCQ: Check the selected option value against the answer
        if user_input == current_q['answer']:
            correct = True
    elif current_q['type'] == 'one_word':
        # One-Word: Case-insensitive check
        if user_input.strip().lower() == current_q['answer'].lower():
            correct = True
    elif current_q['type'] == 'true_false':
        # True/False: Check lower-cased input against "True" or "False"
        if (user_input.lower() == "true" and current_q['answer'] == "True") or \
           (user_input.lower() == "false" and current_q['answer'] == "False"):
            correct = True

    if correct:
        st.session_state.score += (2 if current_q['type'] == 'one_word' else 1)

    st.session_state.correct = correct
    st.session_state.show_feedback = True
    st.session_state.user_answer = user_input # Store for feedback

def next_question():
    """Moves to the next question or finishes the quiz."""
    st.session_state.q_index += 1
    st.session_state.show_feedback = False
    st.session_state.user_answer = None
    
    if st.session_state.q_index >= len(st.session_state.quiz):
        st.session_state.quiz_state = 'finished'
    st.rerun()

# --- UI Rendering Functions ---

def render_config_state():
    """Renders the topic and question count selection UI."""
    st.header("Select your Quiz Settings")
    st.markdown("********************************************")

    # Use st.form to group inputs and prevent reruns until submission
    with st.form("quiz_config_form"):
        topic = st.selectbox("1. Choose a topic:", options=TOPICS)
        
        num_questions = st.number_input(
            "2. Enter no of questions (recommended: multiples of 3):",
            min_value=3, max_value=30, value=9, step=3
        )
        
        submitted = st.form_submit_button("Generate Quiz & Start")
        
    if submitted:
        start_quiz_session(topic, int(num_questions))

def render_quiz_in_progress_state():
    """Renders the current question and handles interaction."""
    quiz = st.session_state.quiz
    q_index = st.session_state.q_index
    current_q = quiz[q_index]

    # Calculate total marks to display score metric
    mcq_count = len([q for q in quiz if q['type'] == 'mcq'])
    one_word_count = len([q for q in quiz if q['type'] == 'one_word'])
    true_false_count = len([q for q in quiz if q['type'] == 'true_false'])
    total_marks = mcq_count * 1 + one_word_count * 2 + true_false_count * 1

    st.metric(
        label="Current Score", 
        value=f"{st.session_state.score} / {total_marks}", 
        delta=f"Question {q_index + 1}/{len(quiz)}",
        delta_color="off"
    )

    # Question Display Area
    with st.container(border=True):
        st.subheader(f"Q{q_index + 1}: {current_q['question']}")

        if not st.session_state.show_feedback:
            # --- Input Phase ---
            with st.form(key=f"q_form_{q_index}"):
                user_input = None
                
                if current_q['type'] == 'mcq':
                    user_input = st.radio("Choose an answer:", current_q['options'],index=None)
                elif current_q['type'] == 'one_word':
                    user_input = st.text_input("Your answer (One word):")
                elif current_q['type'] == 'true_false':
                    user_input = st.radio("Your answer:", options=["True", "False"], index=None)

                submit_button = st.form_submit_button("Submit Answer")

            if submit_button and user_input is not None:
                check_answer_and_proceed(current_q, user_input)
                st.rerun() # Rerun to show feedback

        else:
            # --- Feedback Phase ---
            if st.session_state.correct:
                st.success("✅ Correct!")
            else:
                st.error(f"❌ Incorrect! The correct answer was: **{current_q.get('answer')}**")
                
            st.button("Next Question", on_click=next_question, use_container_width=True)

def render_finished_state():
    """Renders the final score UI."""
    quiz = st.session_state.quiz
    total_marks = len([q for q in quiz if q['type'] == 'mcq'])*1 + \
                  len([q for q in quiz if q['type'] == 'one_word'])*2 + \
                  len([q for q in quiz if q['type'] == 'true_false'])*1
                  
    st.balloons()
    st.success("🎉 Quiz Complete!")
    st.subheader(f"📊 Your Final Score: {st.session_state.score} / {total_marks}")
    
    if st.button("Start New Quiz", use_container_width=True):
        st.session_state.quiz_state = 'config'
        st.rerun()

# --- Main App Execution ---
st.title("💡 AI-Powered Coding Quiz Generator")
st.markdown("---")

if st.session_state.quiz_state == 'config':
    render_config_state()
elif st.session_state.quiz_state == 'quiz_in_progress':
    render_quiz_in_progress_state()
elif st.session_state.quiz_state == 'finished':
    render_finished_state()
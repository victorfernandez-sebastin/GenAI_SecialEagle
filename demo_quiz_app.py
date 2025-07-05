import streamlit as st

# Set page config
st.set_page_config(page_title="🧠 Quiz App", layout="centered")

# Quiz data: questions, options, answers
quiz_data = [
    {
        "question": "What is the capital of France?",
        "options": ["Berlin", "Madrid", "Paris", "Rome"],
        "answer": "Paris"
    },
    {
        "question": "Which planet is known as the Red Planet?",
        "options": ["Earth", "Venus", "Mars", "Jupiter"],
        "answer": "Mars"
    },
    {
        "question": "Who developed Python?",
        "options": ["Elon Musk", "Guido van Rossum", "Bill Gates", "Mark Zuckerberg"],
        "answer": "Guido van Rossum"
    },
    {
        "question": "Which is the largest ocean in the world?",
        "options": ["Indian Ocean", "Pacific Ocean", "Atlantic Ocean", "Arctic Ocean"],
        "answer": "Pacific Ocean"
    }
]

# Initialize score
if "score" not in st.session_state:
    st.session_state.score = 0
if "current_q" not in st.session_state:
    st.session_state.current_q = 0
if "quiz_done" not in st.session_state:
    st.session_state.quiz_done = False

# Quiz interface
st.title("🧠 General Knowledge Quiz")

if st.session_state.current_q < len(quiz_data):
    q = quiz_data[st.session_state.current_q]
    st.subheader(f"Q{st.session_state.current_q + 1}: {q['question']}")
    
    selected = st.radio("Choose your answer:", q['options'])

    if st.button("Submit Answer"):
        if selected == q["answer"]:
            st.success("Correct! ✅")
            st.session_state.score += 1
        else:
            st.error(f"Wrong! ❌ The correct answer is: {q['answer']}")
        
        st.session_state.current_q += 1
        st.rerun()
else:
    st.session_state.quiz_done = True

# Final score
if st.session_state.quiz_done:
    st.markdown("---")
    st.subheader("🎉 Quiz Completed!")
    st.success(f"Your Score: **{st.session_state.score} / {len(quiz_data)}**")

    if st.button("Restart Quiz"):
        st.session_state.score = 0
        st.session_state.current_q = 0
        st.session_state.quiz_done = False
        st.rerun()

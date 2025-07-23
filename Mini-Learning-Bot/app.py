from bot.quiz import Quiz
from data_manager import load_words, append_word, load_performance, save_performance
import streamlit as st

st.set_page_config(page_title="Mini Learning Bot", page_icon="🎓")


# ---------- INIT STATE ----------
if "quiz" not in st.session_state:
    st.session_state.quiz = None
if "quiz_started" not in st.session_state:
    st.session_state.quiz_started = False
if "last_feedback" not in st.session_state:
    st.session_state.last_feedback = ""
if "last_correct" not in st.session_state:
    st.session_state.last_correct = False
if "answer_key" not in st.session_state:
    st.session_state.answer_key = 0   # change key to clear input


# ---------- SIDEBAR ----------
def sidebar_ui():
    st.sidebar.title("📚 Mini Learning Bot")

    if st.session_state.quiz_started and st.session_state.quiz:
        q = st.session_state.quiz
        total = q.total()
        idx = min(q.index, total)  # clamp
        st.sidebar.markdown(f"**Progress:** {idx}/{total}")
        pct = (idx / total * 100) if total else 0
        st.sidebar.progress(min(idx / max(total, 1), 1.0))
        st.sidebar.markdown(f"**{pct:.0f}% complete**")
        st.sidebar.markdown(f"**Score:** {q.correct} ✅ / {q.incorrect} ❌")

    st.sidebar.markdown("---")
    st.sidebar.subheader("➕ Add / Update Word")
    term = st.sidebar.text_input("Term", key="sb_term")
    definition = st.sidebar.text_input("Definition", key="sb_def")
    if st.sidebar.button("Save Word"):
        if term and definition:
            append_word(term.strip(), definition.strip())
            st.sidebar.success("Saved!")
            # refresh quiz data if running
            if st.session_state.quiz_started and st.session_state.quiz:
                st.session_state.quiz.items = load_words()
                st.session_state.quiz.reset(shuffle=False)
            st.rerun()
        else:
            st.sidebar.warning("Both fields required.")

    st.sidebar.markdown("---")
    if st.sidebar.button("🔁 Restart Quiz"):
        start_quiz(shuffle=True)
        st.rerun()


# ---------- START QUIZ ----------
def start_quiz(shuffle=True):
    items = load_words()
    st.session_state.quiz = Quiz(items, shuffle=shuffle)
    st.session_state.quiz_started = True
    st.session_state.last_feedback = ""
    st.session_state.last_correct = False
    st.session_state.answer_key += 1  # reset input field


# ---------- QUIZ UI ----------
def quiz_ui():
    q = st.session_state.quiz

    if q.total() == 0:
        st.warning("No words found. Add some in the sidebar to begin.")
        return

    # Are we done?
    if q.index >= q.total():
        st.success(f"🎉 All done! Final score: {q.correct}/{q.total()}")
        # save session summary
        perf = load_performance()
        perf["sessions"].append({
            "correct": q.correct,
            "incorrect": q.incorrect,
            "total": q.total(),
        })
        save_performance(perf)
        if st.button("Start Again"):
            start_quiz(shuffle=False)
            st.rerun()
        return

    # Show current question
    term = q.current_term()
    st.subheader(f"What is the meaning of: **{term}**")

    # Answer input
    user_answer = st.text_input(
        "Your answer:",
        key=f"answer_{st.session_state.answer_key}"
    )

    # Submit
    if st.button("Submit"):
        is_correct = q.check(user_answer)
        st.session_state.last_correct = is_correct
        correct_def = q.current_definition() or ""
        if is_correct:
            st.session_state.last_feedback = "✅ Correct!"
        else:
            st.session_state.last_feedback = f"❌ Incorrect. Correct answer: {correct_def}"
        st.rerun()

    # Feedback
    if st.session_state.last_feedback:
        if st.session_state.last_correct:
            st.success(st.session_state.last_feedback)
        else:
            st.error(st.session_state.last_feedback)

        # Next button after feedback
        if st.button("Next"):
            q.next()
            st.session_state.last_feedback = ""
            st.session_state.answer_key += 1
            st.rerun()


# ---------- MAIN ----------
def main():
    st.title("🎓 Mini Learning Bot")
    sidebar_ui()

    if not st.session_state.quiz_started:
        st.info("Click below to begin!")
        if st.button("Start Quiz"):
            start_quiz()
            st.rerun()
    else:
        quiz_ui()


if __name__ == "__main__":
    main()






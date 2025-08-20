import streamlit as st
import random
import time

st.set_page_config(page_title="영단어 퀴즈", page_icon="📘", layout="centered")

# 고등 모의고사 자주 나오는 단어 샘플 (확장 가능)
word_dict = {
    "abandon": "버리다",
    "abstract": "추상적인",
    "adolescent": "청소년",
    "analyze": "분석하다",
    "assume": "가정하다",
    "collapse": "붕괴하다",
    "contrast": "대조",
    "crucial": "중요한",
    "demonstrate": "증명하다",
    "distinguish": "구별하다",
    "emerge": "나타나다",
    "generate": "생성하다",
    "illustrate": "설명하다",
    "inevitable": "피할 수 없는",
    "interpret": "해석하다",
    "justify": "정당화하다",
    "maintain": "유지하다",
    "notion": "개념",
    "persuade": "설득하다",
    "precise": "정확한",
    "regulate": "규제하다",
    "relevant": "관련 있는",
    "significant": "중요한",
    "sustain": "지속하다",
    "tend": "경향이 있다"
}

if "score" not in st.session_state:
    st.session_state.score = 0
if "question_count" not in st.session_state:
    st.session_state.question_count = 0
if "quiz_word" not in st.session_state:
    st.session_state.quiz_word = None
if "options" not in st.session_state:
    st.session_state.options = []
if "timer_start" not in st.session_state:
    st.session_state.timer_start = None
if "time_limit" not in st.session_state:
    st.session_state.time_limit = 10  # 제한 시간 (초)

def new_question():
    st.session_state.quiz_word = random.choice(list(word_dict.keys()))
    correct_answer = word_dict[st.session_state.quiz_word]

    # 보기 만들기
    options = [correct_answer]
    while len(options) < 4:
        wrong = random.choice(list(word_dict.values()))
        if wrong not in options:
            options.append(wrong)
    random.shuffle(options)

    st.session_state.options = options
    st.session_state.timer_start = time.time()

# 첫 문제 세팅
if st.session_state.quiz_word is None:
    new_question()

st.title("📘 영단어 퀴즈")
st.write(f"점수: {st.session_state.score} | 문제 수: {st.session_state.question_count}")

# 남은 시간 표시
elapsed = time.time() - st.session_state.timer_start
remaining = max(st.session_state.time_limit - int(elapsed), 0)
progress = remaining / st.session_state.time_limit
st.progress(progress)

st.subheader(f"❓ '{st.session_state.quiz_word}' 의 뜻은?")

# 정답 선택
choice = st.radio("보기:", st.session_state.options)

if st.button("제출"):
    if remaining <= 0:
        st.error("⏰ 시간 초과! 정답을 맞히지 못했습니다.")
    elif choice == word_dict[st.session_state.quiz_word]:
        st.success("✅ 정답입니다!")
        st.session_state.score += 1
    else:
        st.error(f"❌ 오답입니다. 정답은 '{word_dict[st.session_state.quiz_word]}' 입니다.")

    st.session_state.question_count += 1
    new_question()
    st.rerun()

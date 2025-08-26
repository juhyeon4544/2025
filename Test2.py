import streamlit as st
import random

# --- 단어장 ---
word_dict = {
    "apple": "사과",
    "banana": "바나나",
    "cat": "고양이",
    "dog": "개",
    "elephant": "코끼리"
}

# --- 세션 상태 초기화 ---
if "score" not in st.session_state:
    st.session_state.score = 0
if "current_word" not in st.session_state:
    st.session_state.current_word = random.choice(list(word_dict.keys()))
if "options" not in st.session_state:
    # 문제 당 선택지 고정
    correct = word_dict[st.session_state.current_word]
    wrong_choices = random.sample([v for v in word_dict.values() if v != correct], 3)
    st.session_state.options = random.sample([correct] + wrong_choices, 4)
if "answered" not in st.session_state:
    st.session_state.answered = False

# --- 앱 제목 ---
st.title("🎯 영단어 객관식 퀴즈")
st.subheader(f"{st.session_state.current_word}")

# --- 객관식 선택지 ---
if not st.session_state.answered:
    user_choice = st.radio("뜻을 선택하세요:", st.session_state.options)

    if st.button("제출"):
        correct_answer = word_dict[st.session_state.current_word]
        if user_choice == correct_answer:
            st.success("✅ 정답!")
            st.session_state.score += 1
        else:
            st.error(f"❌ 틀렸습니다. 정답: {correct_answer}")
        st.session_state.answered = True
else:
    if st.button("다음 문제"):
        # 다음 문제 설정
        st.session_state.current_word = random.choice(list(word_dict.keys()))
        correct = word_dict[st.session_state.current_word]
        wrong_choices = random.sample([v for v in word_dict.values() if v != correct], 3)
        st.session_state.options = random.sample([correct] + wrong_choices, 4)
        st.session_state.answered = False

# --- 점수 표시 ---
st.write(f"현재 점수: {st.session_state.score}")

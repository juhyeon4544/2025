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

# --- 앱 제목 ---
st.title("🎯 영단어 퀴즈 게임")
st.write("다음 단어의 뜻을 입력하세요:")

st.subheader(f"{st.session_state.current_word}")

# --- form 사용 ---
with st.form(key="quiz_form"):
    user_input = st.text_input("뜻을 입력하세요:")
    submit_button = st.form_submit_button("제출")

    if submit_button:
        correct_answer = word_dict[st.session_state.current_word]
        if user_input.strip() == correct_answer:
            st.success("✅ 정답!")
            st.session_state.score += 1
        else:
            st.error(f"❌ 틀렸습니다. 정답: {correct_answer}")

        # 다음 단어로 교체
        st.session_state.current_word = random.choice(list(word_dict.keys()))

# --- 점수 표시 ---
st.write(f"현재 점수: {st.session_state.score}")

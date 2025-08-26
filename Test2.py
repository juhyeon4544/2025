import streamlit as st
import random

# --- 단어장 설정 ---
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
if "input_value" not in st.session_state:
    st.session_state.input_value = ""

# --- 앱 제목 ---
st.title("🎯 영단어 퀴즈 게임")
st.write("다음 단어의 뜻을 입력하세요:")

# --- 문제 표시 ---
st.subheader(f"{st.session_state.current_word}")

# --- 사용자 입력 ---
st.session_state.input_value = st.text_input("뜻을 입력하세요:", value=st.session_state.input_value)

# --- 정답 확인 ---
if st.button("제출"):
    user_answer = st.session_state.input_value.strip()
    correct_answer = word_dict[st.session_state.current_word]

    if user_answer == correct_answer:
        st.success("✅ 정답!")
        st.session_state.score += 1
    else:
        st.error(f"❌ 틀렸습니다. 정답: {correct_answer}")

    # 다음 단어로 교체
    st.session_state.current_word = random.choice(list(word_dict.keys()))
    st.session_state.input_value = ""  # 입력창 초기화

# --- 점수 표시 ---
st.write(f"현재 점수: {st.session_state.score}")

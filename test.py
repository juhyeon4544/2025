import streamlit as st
import random
import pandas as pd

st.set_page_config(page_title="영어 단어 암기 퀴즈", page_icon="📚")

# 초기 세션 설정
if "words" not in st.session_state:
    st.session_state.words = []  # 단어 리스트 저장
if "score" not in st.session_state:
    st.session_state.score = 0
if "history" not in st.session_state:
    st.session_state.history = []

st.title("📚 영어 단어 암기 퀴즈")

# -------------------------------
# 1. 단어 입력
# -------------------------------
with st.expander("단어 추가하기 ✍️"):
    word = st.text_input("단어 입력")
    meaning = st.text_input("뜻 입력")
    example = st.text_input("예문 입력")
    if st.button("추가하기"):
        if word and meaning:
            st.session_state.words.append({"word": word, "meaning": meaning, "example": example})
            st.success(f"{word} 추가 완료!")

# -------------------------------
# 2. 퀴즈 모드
# -------------------------------
st.subheader("🎯 퀴즈 풀기")
if len(st.session_state.words) > 0:
    question_type = random.choice(["뜻 맞추기", "단어 맞추기", "빈칸 맞추기"])
    q = random.choice(st.session_state.words)

    if question_type == "뜻 맞추기":
        st.write(f"❓ 단어: **{q['word']}** 의 뜻은?")
        answer = st.text_input("정답 입력", key="ans1")
        if st.button("제출", key="submit1"):
            if answer.strip().lower() == q['meaning'].lower():


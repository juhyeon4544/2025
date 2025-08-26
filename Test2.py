import streamlit as st
import random

# ==========================
# 단어 리스트 (단어:뜻)
# ==========================
words = {
    "apple": "사과",
    "banana": "바나나",
    "orange": "오렌지",
    "grape": "포도",
    "watermelon": "수박",
    "cherry": "체리",
    "peach": "복숭아",
    "lemon": "레몬",
    "strawberry": "딸기",
    "kiwi": "키위"
}

# ==========================
# 세션 상태 초기화
# ==========================
if "word_list" not in st.session_state:
    st.session_state.word_list = list(words.keys())
    random.shuffle(st.session_state.word_list)
    st.session_state.index = 0
    st.session_state.score = 0

st.title("영어 단어 게임 🎮")
st.write("단어에 맞는 뜻을 선택하세요!")

# ==========================
# 게임 진행
# ==========================
if st.session_state.index < len(st.session_state.word_list):
    current_word = st.session_state.word_list[st.session_state.index]
    correct_meaning = words[current_word]

    # 객관식 보기 4개 만들기
    all_meanings = list(words.values())
    choices = random.sample([m for m in all_meanings if m != correct_meaning], 3)
    choices.append(correct_meaning)
    random.shuffle(choices)

    st.subheader(f"단어: {current_word}")

    user_choice = st.radio("뜻을 선택하세요:", choices)

    if st.button("제출"):
        if user_choice == correct_meaning:
            st.success("정답! 🎉")
            st.session_state.score += 1
        else:
            st.error(f"오답! 정답은 '{correct_meaning}' 입니다.")
        st.session_state.index += 1
        st.experimental_rerun()
else:
    st.balloons()
    st.success(f"게임 종료! 점수: {st.session_state.score}/{len(st.session_state.word_list)}")
    if st.button("다시 시작"):
        st.session_state.index = 0
        st.session_state.score = 0
        random.shuffle(st.session_state.word_list)
        st.experimental_rerun()

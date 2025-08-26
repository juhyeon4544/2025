import streamlit as st
import random

# 단어 데이터
word_list = [
    {"word": "apple", "meaning": "사과"},
    {"word": "banana", "meaning": "바나나"},
    {"word": "cherry", "meaning": "체리"},
    {"word": "dog", "meaning": "개"},
    {"word": "cat", "meaning": "고양이"},
    {"word": "elephant", "meaning": "코끼리"},
    {"word": "house", "meaning": "집"},
    {"word": "car", "meaning": "자동차"},
    {"word": "school", "meaning": "학교"},
    {"word": "teacher", "meaning": "선생님"}
]

# 세션 상태 초기화
if "score" not in st.session_state:
    st.session_state.score = 0
if "question_index" not in st.session_state:
    st.session_state.question_index = 0
if "current_question" not in st.session_state:
    st.session_state.current_question = None
if "quiz_done" not in st.session_state:
    st.session_state.quiz_done = False

# 문제 생성 함수
def generate_question():
    return random.choice(word_list)

# 퀴즈 초기화
def reset_quiz():
    st.session_state.score = 0
    st.session_state.question_index = 0
    st.session_state.quiz_done = False
    st.session_state.current_question = generate_question()
    st.rerun()

# 앱 제목
st.title("영단어 퀴즈 게임 🎮")

# 퀴즈 시작
if st.session_state.current_question is None:
    st.session_state.current_question = generate_question()

if not st.session_state.quiz_done:
    question = st.session_state.current_question
    st.subheader(f"Q{st.session_state.question_index + 1}. {question['word']} 의 뜻은 무엇일까요?")

    answer = st.text_input("정답을 입력하세요:", key=f"answer_{st.session_state.question_index}")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("확인"):
            if answer.strip() == "":
                st.warning("정답을 입력해주세요!")
            else:
                if answer.strip() == question["meaning"]:
                    st.success("정답입니다! ✅")
                    st.session_state.score += 1
                else:
                    st.error(f"오답입니다 ❌ (정답: {question['meaning']})")

                st.session_state.question_index += 1
                if st.session_state.question_index >= 5:  # 5문제만 진행
                    st.session_state.quiz_done = True
                else:
                    st.session_state.current_question = generate_question()

                st.rerun()

    with col2:
        if st.button("건너뛰기"):
            st.session_state.question_index += 1
            if st.session_state.question_index >= 5:
                st.session_state.quiz_done = True
            else:
                st.session_state.current_question = generate_question()
            st.rerun()

else:
    st.header("퀴즈 완료 🎉")
    st.write(f"최종 점수: {st.session_state.score} / 5")

    if st.button("다시하기 🔄"):
        reset_quiz()

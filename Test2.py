# Test2.py
import streamlit as st
import random

# ------------------------------
# Streamlit rerun 호환성 처리
# ------------------------------
if hasattr(st, "rerun"):
    rerun = st.rerun
elif hasattr(st, "experimental_rerun"):
    rerun = st.experimental_rerun
else:
    # 매우 구버전(거의 없음) 대비 안전한 대체 함수
    def rerun():
        # 사용자에게 업그레이드 권장 메시지 출력
        st.warning("현재 Streamlit 버전에서 rerun을 지원하지 않습니다. "
                   "가능하면 `pip install --upgrade streamlit`로 업그레이드하세요.")
        return

# ------------------------------
# 단어 데이터
# ------------------------------
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

# ------------------------------
# 세션 상태 초기화
# ------------------------------
if "score" not in st.session_state:
    st.session_state.score = 0
if "question_index" not in st.session_state:
    st.session_state.question_index = 0
if "current_question" not in st.session_state:
    st.session_state.current_question = None
if "quiz_done" not in st.session_state:
    st.session_state.quiz_done = False
if "total_questions" not in st.session_state:
    st.session_state.total_questions = 5  # 기본 5문제 (원하면 변경 가능)

# ------------------------------
# 문제 생성 함수 및 초기화
# ------------------------------
def generate_question():
    return random.choice(word_list)

def reset_quiz():
    st.session_state.score = 0
    st.session_state.question_index = 0
    st.session_state.quiz_done = False
    st.session_state.current_question = generate_question()
    rerun()

# ------------------------------
# UI
# ------------------------------
st.title("영단어 퀴즈 게임 🎮")
st.caption("텍스트로 뜻을 입력하는 간단한 퀴즈입니다. (한글 뜻 입력)")

# total 조절 (옵션)
total = st.sidebar.number_input("전체 문제 수", min_value=1, max_value=20, value=st.session_state.total_questions, step=1)
st.session_state.total_questions = int(total)

# 퀴즈 시작 준비
if st.session_state.current_question is None:
    st.session_state.current_question = generate_question()

# 진행상황 표시
st.write(f"문제 {st.session_state.question_index + 1} / {st.session_state.total_questions}")
st.progress(min(st.session_state.question_index / max(1, st.session_state.total_questions), 1.0))

if not st.session_state.quiz_done:
    question = st.session_state.current_question
    st.subheader(f"Q{st.session_state.question_index + 1}. **{question['word']}** 의 뜻은 무엇일까요?")

    # 입력 박스에 인덱스를 키로 사용해서 문제별로 입력 필드가 달라지게 함
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
                if st.session_state.question_index >= st.session_state.total_questions:
                    st.session_state.quiz_done = True
                else:
                    st.session_state.current_question = generate_question()

                rerun()

    with col2:
        if st.button("건너뛰기"):
            st.info(f"스킵했습니다. 정답: {question['meaning']}")
            st.session_state.question_index += 1
            if st.session_state.question_index >= st.session

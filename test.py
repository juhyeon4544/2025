import streamlit as st
import random
import time

# ------------------------------
# 고등 모의고사/수능 빈출 단어 50개
# ------------------------------
word_dict = {
    "abandon": "버리다, 포기하다",
    "abstract": "추상적인",
    "accessible": "접근 가능한",
    "accomplish": "완수하다",
    "acquire": "얻다, 습득하다",
    "adapt": "적응하다",
    "adequate": "충분한",
    "affect": "영향을 미치다",
    "alter": "바꾸다",
    "analyze": "분석하다",
    "ancient": "고대의",
    "anticipate": "예상하다",
    "apparent": "분명한",
    "approach": "접근하다",
    "appropriate": "적절한",
    "assume": "가정하다",
    "attempt": "시도하다",
    "benefit": "이익, 혜택",
    "broaden": "넓히다",
    "collapse": "붕괴하다",
    "comprehend": "이해하다",
    "conceal": "숨기다",
    "conclude": "결론짓다",
    "conduct": "수행하다",
    "consequence": "결과",
    "considerable": "상당한",
    "constant": "끊임없는",
    "contribute": "기여하다",
    "convince": "설득하다",
    "critical": "중대한, 비판적인",
    "crucial": "결정적인",
    "decline": "감소하다",
    "demonstrate": "증명하다, 보여주다",
    "determine": "결정하다",
    "distinct": "별개의, 뚜렷한",
    "distribute": "분배하다",
    "emerge": "나타나다",
    "enable": "가능하게 하다",
    "encounter": "마주치다",
    "ensure": "보장하다",
    "evaluate": "평가하다",
    "exceed": "초과하다",
    "expand": "확장하다",
    "explore": "탐험하다, 조사하다",
    "extend": "연장하다",
    "familiar": "익숙한",
    "fundamental": "근본적인",
    "identify": "식별하다",
    "illustrate": "설명하다",
    "imply": "암시하다",
    "indicate": "나타내다"
}

# ------------------------------
# 세션 상태 관리
# ------------------------------
if "score" not in st.session_state:
    st.session_state.score = 0
if "question_num" not in st.session_state:
    st.session_state.question_num = 1
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "time_limit" not in st.session_state:
    st.session_state.time_limit = 15  # 문제당 제한시간 (초)

# ------------------------------
# 문제 생성 함수
# ------------------------------
def generate_question():
    eng_word = random.choice(list(word_dict.keys()))
    correct_meaning = word_dict[eng_word]

    # 보기 만들기
    wrong_answers = random.sample(
        [v for k, v in word_dict.items() if v != correct_meaning], 3
    )
    options = wrong_answers + [correct_meaning]
    random.shuffle(options)

    return eng_word, correct_meaning, options

# ------------------------------
# 앱 UI
# ------------------------------
st.title("📘 고등 영어 단어 퀴즈")
st.write("⏳ 문제당 시간 제한:", st.session_state.time_limit, "초")

# 새로운 문제 생성
if "current_q" not in st.session_state:
    st.session_state.current_q = generate_question()

eng_word, correct_meaning, options = st.session_state.current_q

# 시간 시작
if st.session_state.start_time is None:
    st.session_state.start_time = time.time()

elapsed_time = int(time.time() - st.session_state.start_time)
remaining_time = st.session_state.time_limit - elapsed_time

st.subheader(f"Q{st.session_state.question_num}. '{eng_word}'의 뜻은?")
st.write(f"⏰ 남은 시간: {remaining_time}초")

if remaining_time <= 0:
    st.error("⏰ 시간 초과! 다음 문제로 넘어갑니다.")
    st.session_state.question_num += 1
    st.session_state.current_q = generate_question()
    st.session_state.start_time = time.time()
    st.stop()

# 보기 출력
choice = st.radio("뜻을 고르세요:", options, index=None)

# 제출 버튼
if st.button("제출"):
    if choice == correct_meaning:
        st.success("✅ 정답!")
        st.session_state.score += 1
    else:
        st.error(f"❌ 오답! 정답은: {correct_meaning}")

    st.session_state.question_num += 1
    st.session_state.current_q = generate_question()
    st.session_state.start_time = time.time()

st.write("---")
st.write(f"현재 점수: {st.session_state.score} / {st.session_state.question_num - 1}")

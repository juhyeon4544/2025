import streamlit as st
import random
import time

st.set_page_config(page_title="영단어 퀴즈", layout="wide")

# ---------------------------
# 단어 데이터
# ---------------------------
word_list = {
    "abandon": "버리다",
    "accelerate": "가속하다",
    "acquire": "얻다",
    "adapt": "적응하다",
    "analyze": "분석하다",
    "assume": "가정하다",
    "collapse": "붕괴하다",
    "contrast": "대조",
    "crucial": "중요한",
    "demonstrate": "증명하다"
}

TIME_LIMIT = 10  # 제한 시간(초)

# ---------------------------
# 세션 초기화
# ---------------------------
if "score" not in st.session_state:
    st.session_state.score = 0
if "question_num" not in st.session_state:
    st.session_state.question_num = 0
if "current_question" not in st.session_state:
    st.session_state.current_question = None
if "start_time" not in st.session_state:
    st.session_state.start_time = None

# ---------------------------
# 새 문제 생성 함수
# ---------------------------
def new_question():
    eng_word = random.choice(list(word_list.keys()))
    correct_meaning = word_list[eng_word]
    wrong_options = random.sample([v for k,v in word_list.items() if v != correct_meaning], 3)
    options = wrong_options + [correct_meaning]
    random.shuffle(options)
    st.session_state.current_question = {
        "eng_word": eng_word,
        "correct": correct_meaning,
        "options": options
    }
    st.session_state.start_time = time.time()

# ---------------------------
# 문제 준비
# ---------------------------
if st.session_state.current_question is None:
    new_question()

q = st.session_state.current_question

# ---------------------------
# 남은 시간 계산
# ---------------------------
elapsed = int(time.time() - st.session_state.start_time)
remaining = max(TIME_LIMIT - elapsed, 0)
progress = remaining / TIME_LIMIT

st.title("📝 영단어 퀴즈")
st.subheader(f"문제 {st.session_state.question_num+1}/10")
st.markdown(f"### '{q['eng_word']}' 의 뜻은 무엇일까요?")

# 프로그레스바
st.progress(progress)

# 4개 버튼을 2열로
cols = st.columns(2)
clicked = None

for i, option in enumerate(q["options"]):
    col = cols[i % 2]
    if col.button(option, key=f"opt_{i}"):
        clicked = option

# ---------------------------
# 제출 또는 시간 초과 처리
# ---------------------------
if clicked or remaining == 0:
    if remaining == 0 and clicked is None:
        st.error("⏰ 시간 초과! 오답 처리됩니다.")
    elif clicked == q["correct"]:
        st.success("✅ 정답!")
        st.session_state.score += 1
    else:
        st.error(f"❌ 오답! 정답은 '{q['correct']}'")

    st.session_state.question_num += 1
    if st.session_state.question_num >= 10:
        st.write(f"🏆 퀴즈 완료! 최종 점수: {st.session_state.score}/10")
    else:
        new_question()
        st.experimental_rerun()

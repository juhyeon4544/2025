import streamlit as st
import random
import pandas as pd
import time

st.set_page_config(page_title="고등학생 영어 객관식 퀴즈", page_icon="📚")

# -----------------------------
# 단어 데이터 (수능/모의고사 빈출)
# -----------------------------
word_list = [
    {"word": "accomplishment", "meaning": "달성, 성취"},
    {"word": "assumption", "meaning": "가정, 추정"},
    {"word": "collapse", "meaning": "붕괴하다"},
    {"word": "evaluate", "meaning": "평가하다"},
    {"word": "consequence", "meaning": "결과, 결말"},
    {"word": "derive", "meaning": "유래하다"},
    {"word": "opportunity", "meaning": "기회"},
    {"word": "participate", "meaning": "참여하다"},
]

# -----------------------------
# 세션 초기화
# -----------------------------
if "score" not in st.session_state:
    st.session_state.score = 0
if "history" not in st.session_state:
    st.session_state.history = []
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "question" not in st.session_state:
    st.session_state.question = None
if "options" not in st.session_state:
    st.session_state.options = None
if "qtype" not in st.session_state:
    st.session_state.qtype = None

st.title("📖 고등학생 영어 객관식 퀴즈 (⏱️ 시간제한)")

# -----------------------------
# 문제/보기 생성 함수
# -----------------------------
def make_options(correct, all_options):
    options = [correct]
    while len(options) < 4:
        choice = random.choice(all_options)
        if choice not in options:
            options.append(choice)
    random.shuffle(options)
    return options

# -----------------------------
# 새로운 문제 출제
# -----------------------------
if st.session_state.question is None:
    q = random.choice(word_list)
    qtype = random.choice(["word_to_meaning", "meaning_to_word"])
    if qtype == "word_to_meaning":
        options = make_options(q["meaning"], [w["meaning"] for w in word_list])
    else:
        options = make_options(q["word"], [w["word"] for w in word_list])

    st.session_state.question = q
    st.session_state.qtype = qtype
    st.session_state.options = options
    st.session_state.start_time = time.time()

# -----------------------------
# 문제 표시
# -----------------------------
q = st.session_state.question
qtype = st.session_state.qtype
options = st.session_state.options

time_limit = 10  # 제한 시간 (초)
elapsed = int(time.time() - st.session_state.start_time)
remaining = max(0, time_limit - elapsed)

st.write(f"⏱️ 남은 시간: **{remaining}초**")

if qtype == "word_to_meaning":
    st.write(f"❓ 단어 **{q['word']}** 의 뜻은 무엇일까요?")
else:
    st.write(f"❓ 뜻 **{q['meaning']}** 에 해당하는 단어는 무엇일까요?")

answer = st.radio("정답을 선택하세요:", options, index=None)

# -----------------------------
# 정답 처리
# -----------------------------
if st.button("제출"):
    if elapsed > time_limit:
        st.error("⏰ 시간 초과! 오답 처리됩니다.")
        correct = q["meaning"] if qtype == "word_to_meaning" else q["word"]
        st.error(f"정답은 {correct}")
    else:
        if qtype == "word_to_meaning":
            correct = q["meaning"]
        else:
            correct = q["word"]

        if answer == correct:
            st.session_state.score += 1
            st.success("✅ 정답!")
        else:
            st.error(f"❌ 오답! 정답은 {correct}")

    # 기록 저장
    st.session_state.history.append((qtype, q["word"], answer, "시간초과" if elapsed > time_limit else ""))

    # 다음 문제로 초기화
    st.session_state.question = None

# -----------------------------
# 점수 & 기록
# -----------------------------
st.markdown("---")
st.write(f"📊 현재 점수: **{st.session_state.score}**")

if st.button("기록 저장하기"):
    df = pd.DataFrame(st.session_state.history, columns=["문제 유형", "문제(단어)", "내 답", "비고"])
    df.to_csv("quiz_history.csv", index=False)
    st.success("기록이 저장되었습니다!")


import streamlit as st
import random
import pandas as pd

st.set_page_config(page_title="고등생용 영어 객관식 퀴즈", page_icon="📚")

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

if "score" not in st.session_state:
    st.session_state.score = 0
if "history" not in st.session_state:
    st.session_state.history = []

st.title("📖 고등학생 빈출 단어 객관식 퀴즈")

with st.expander("단어 학습하기 (빈출 단어 목록)"):
    for w in word_list:
        st.write(f"**{w['word']}** : {w['meaning']}")

st.markdown("---")
st.subheader("퀴즈 풀기")

question_type = random.choice(["word_to_meaning", "meaning_to_word"])
q = random.choice(word_list)

def make_options(correct, all_options):
    options = [correct]
    while len(options) < 4:
        choice = random.choice(all_options)
        if choice not in options:
            options.append(choice)
    random.shuffle(options)
    return options

if question_type == "word_to_meaning":
    st.write(f"❓ 단어 **{q['word']}**의 뜻은 무엇일까요?")
    options = make_options(q["meaning"], [w["meaning"] for w in word_list])
    answer = st.radio("정답:", options, key="opt1")
    if st.button("제출", key="submit1"):
        if answer == q["meaning"]:
            st.session_state.score += 1
            st.success("정답!👏")
        else:
            st.error(f"오답… 정답은 **{q['meaning']}**")
        st.session_state.history.append(("단어→뜻", q['word'], answer))

else:
    st.write(f"❓ 뜻 **{q['meaning']}**에 해당하는 단어는 무엇일까요?")
    options = make_options(q["word"], [w["word"] for w in word_list])
    answer = st.radio("정답:", options, key="opt2")
    if st.button("제출", key="submit2"):
        if answer == q["word"]:
            st.session_state.score += 1
            st.success("정답!👏")
        else:
            st.error(f"오답… 정답은 **{q['word']}**")
        st.session_state.history.append(("뜻→단어", q['meaning'], answer))

st.markdown("---")
st.write(f"현재 점수: **{st.session_state.score}**")

if st.button("기록 저장하기"):
    df = pd.DataFrame(st.session_state.history, columns=["문제 유형", "문제", "내 답"])
    df.to_csv("quiz_history.csv", index=False)
    st.success("저장 완료!")

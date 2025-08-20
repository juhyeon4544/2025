import streamlit as st
import random
import pandas as pd

st.set_page_config(page_title="영어 단어 암기 퀴즈", page_icon="📚")

# ------------------------------------
# 0. 단어 데이터 (AI가 제공하는 기본 단어 리스트)
# ------------------------------------
word_list = [
    {"word": "abandon", "meaning": "버리다", "example": "He decided to abandon the project halfway."},
    {"word": "benevolent", "meaning": "자비로운", "example": "The king was known as a benevolent ruler."},
    {"word": "candid", "meaning": "솔직한", "example": "She was candid about her mistakes."},
    {"word": "diligent", "meaning": "부지런한", "example": "He is a diligent student who studies every day."},
    {"word": "emerge", "meaning": "드러나다", "example": "A new idea began to emerge during the discussion."},
]

# ------------------------------------
# 1. 세션 상태 초기화
# ------------------------------------
if "score" not in st.session_state:
    st.session_state.score = 0
if "history" not in st.session_state:
    st.session_state.history = []

st.title("📚 영어 단어 암기 퀴즈")

# ------------------------------------
# 2. 단어 학습 모드
# ------------------------------------
with st.expander("📖 단어 학습하기 (눌러서 보기)"):
    for w in word_list:
        st.write(f"**{w['word']}** : {w['meaning']}")
        if w["example"]:
            st.caption(f"📌 예문: {w['example']}")

st.markdown("---")

# ------------------------------------
# 3. 퀴즈 모드
# ------------------------------------
st.subheader("🎯 퀴즈 풀기")
question_type = random.choice(["뜻 맞추기", "단어 맞추기", "빈칸 맞추기"])
q = random.choice(word_list)

if question_type == "뜻 맞추기":
    st.write(f"❓ 단어: **{q['word']}** 의 뜻은?")
    answer = st.text_input("정답 입력", key="ans1")
    if st.button("제출", key="submit1"):
        if answer.strip().lower() == q['meaning'].lower():
            st.session_state.score += 1
            st.success("✅ 정답!")
        else:
            st.error(f"❌ 오답! 정답은 {q['meaning']}")
        st.session_state.history.append(("뜻 맞추기", q['word'], answer))

elif question_type == "단어 맞추기":
    st.write(f"❓ 뜻: **{q['meaning']}** 인 단어는?")
    answer = st.text_input("정답 입력", key="ans2")
    if st.button("제출", key="submit2"):
        if answer.strip().lower() == q['word'].lower():
            st.session_state.score += 1
            st.success("✅ 정답!")
        else:
            st.error(f"❌ 오답! 정답은 {q['word']}")
        st.session_state.history.append(("단어 맞추기", q['meaning'], answer))

else:  # 빈칸 맞추기
    if q['example']:
        sentence = q['example'].replace(q['word'], "____")
        st.write(f"❓ 빈칸 채우기: {sentence}")
        answer = st.text_input("정답 입력", key="ans3")
        if st.button("제출", key="submit3"):
            if answer.strip().lower() == q['word'].lower():
                st.session_state.score += 1
                st.success("✅ 정답!")
            else:
                st.error(f"❌ 오답! 정답은 {q['word']}")
            st.session_state.history.append(("빈칸 맞추기", sentence, answer))

# ------------------------------------
# 4. 점수 & 기록
# ------------------------------------
st.markdown("---")
st.write(f"📊 현재 점수: **{st.session_state.score}**")

if st.button("기록 저장하기 💾"):
    df = pd.DataFrame(st.session_state.history, columns=["문제 유형", "문제", "내 답"])
    df.to_csv("quiz_history.csv", index=False)
    st.success("기록이 저장되었습니다!")

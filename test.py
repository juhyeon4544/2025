import streamlit as st
import random

st.title("📚 고등학생용 영어 단어 학습 앱")

# -----------------------------
# 난이도별 단어장
# -----------------------------
easy_words = [("apple", "사과"), ("banana", "바나나"), ("school", "학교"), ("teacher", "선생님"), 
              ("book", "책"), ("friend", "친구"), ("water", "물"), ("food", "음식"), 
              ("music", "음악"), ("movie", "영화")]

medium_words = [("environment", "환경"), ("culture", "문화"), ("history", "역사"), ("science", "과학"),
                ("technology", "기술"), ("education", "교육"), ("future", "미래"), ("health", "건강"),
                ("travel", "여행"), ("society", "사회"), ("language", "언어"), ("hobby", "취미"),
                ("success", "성공"), ("failure", "실패"), ("dream", "꿈"), ("freedom", "자유"),
                ("responsibility", "책임"), ("knowledge", "지식"), ("opportunity", "기회"), ("experience", "경험")]

hard_words = [("inevitable", "피할 수 없는"), ("significant", "중요한"), ("consequence", "결과"),
              ("hypothesis", "가설"), ("complicated", "복잡한"), ("achievement", "성취"),
              ("perspective", "관점"), ("contradiction", "모순"), ("comprehensive", "포괄적인"),
              ("transition", "변화")]

# -----------------------------
# 세션 상태 초기화
# -----------------------------
if "step" not in st.session_state:
    st.session_state.step = "난이도"
if "level" not in st.session_state:
    st.session_state.level = "쉬움"
if "quiz_score" not in st.session_state:
    st.session_state.quiz_score = 0
if "quiz_total" not in st.session_state:
    st.session_state.quiz_total = 0
if "current_word" not in st.session_state:
    st.session_state.current_word = None
if "wrong_words" not in st.session_state:
    st.session_state.wrong_words = []
if "quiz_mode" not in st.session_state:
    st.session_state.quiz_mode = "단어→뜻"  # 기본 모드

# -----------------------------
# 단계별 화면
# -----------------------------
# 1️⃣ 난이도 선택
if st.session_state.step == "난이도":
    st.subheader("난이도를 선택하세요")
    st.session_state.level = st.radio(
        "", 
        ["쉬움", "중간", "어려움"],
        index=["쉬움", "중간", "어려움"].index(st.session_state.level)
    )
    if st.button("선택 완료"):
        st.session_state.step = "외우기"

# 2️⃣ 단어 외우기 (모두 표시)
elif st.session_state.step == "외우기":
    if st.session_state.level == "쉬움":
        words = easy_words
    elif st.session_state.level == "중간":
        words = medium_words
    else:
        words = hard_words

    st.subheader(f"{st.session_state.level} 단어 외우기")
    for eng, kor in words:
        st.markdown(f"**{eng}**  👉  {kor}")

    if st.button("퀴즈 시작"):
        st.session_state.step = "퀴즈"
        st.session_state.quiz_score = 0
        st.session_state.quiz_total = len(words)
        st.session_state.wrong_words = []
        st.session_state.quiz_mode = st.radio("퀴즈 모드 선택:", ["단어→뜻", "뜻→단어"])
        st.session_state.current_word = random.choice(words)

# 3️⃣ 퀴즈 단계
elif st.session_state.step == "퀴즈":
    if st.session_state.level == "쉬움":
        words = easy_words
    elif st.session_state.level == "중간":
        words = medium_words
    else:
        words = hard_words

    if st.session_state.current_word is None and st.session_state.quiz_total > 0:
        st.session_state.current_word = random.choice(words)

    if st.session_state.quiz_total > 0:
        eng, kor = st.session_state.current_word
        st.subheader("❓ 퀴즈 시작!")
        if st.session_state.quiz_mode == "단어→뜻":
            st.write(f"'{eng}' 의 뜻은 무엇일까요?")
            answer = st.text_input("정답 입력:", key="quiz_input")
        else:
            st.write(f"'{kor}' 의 단어는 무엇일까요?")
            answer = st.text_input("정답 입력:", key="quiz_input")

        if st.button("확인"):
            correct = kor if st.session_state.quiz_mode == "단어→뜻" else eng
            if answer.strip() == correct:
                st.success("✅ 정답!")
                st.session_state.quiz_score += 1
            else:
                st.error(f"❌ 오답! 정답은 {correct}")
                st.session_state.wrong_words.append(st.session_state.current_word)

            st.session_state.quiz_total -= 1
            if st.session_state.quiz_total > 0:
                st.session_state.current_word = random.choice(words)
            else:
                st.success(f"🎉 퀴즈 완료! 점수: {st.session_state.quiz_score} / {len(words)}")
                st.session_state.current_word = None

        st.write(f"남은 문제: {st.session_state.quiz_total}")
        st.write(f"현재 점수: {st.session_state.quiz_score}")

    else:
        st.success("모든 문제가 완료되었습니다!")
        if st.session_state.wrong_words:
            if st.button("틀린 단어 복습"):
                st.session_state.step = "외우기"
                # 틀린 단어만 외우도록 words 교체
                if st.session_state.level == "쉬움":
                    easy_words = st.session_state.wrong_words
                elif st.session_state.level == "중간":
                    medium_words = st.session_state.wrong_words
                else:
                    hard_words = st.session_state.wrong_words
                st.session_state.wrong_words = []

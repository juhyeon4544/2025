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
    st.session_state.level = None
if "index" not in st.session_state:
    st.session_state.index = 0
if "quiz_score" not in st.session_state:
    st.session_state.quiz_score = 0
if "quiz_total" not in st.session_state:
    st.session_state.quiz_total = 0
if "current_word" not in st.session_state:
    st.session_state.current_word = None

# -----------------------------
# 단계별 화면
# -----------------------------
# 1️⃣ 난이도 선택
if st.session_state.step == "난이도":
    st.subheader("난이도를 선택하세요")

    options = ["쉬움", "중간", "어려움"]
    level_choice = st.selectbox(
        "",
        options,
        index=None,  # 기본 선택 없음
        placeholder="난이도를 골라주세요 🙌"
    )

    if level_choice:
        st.session_state.level = level_choice

    if st.button("선택 완료") and st.session_state.level:
        st.session_state.step = "외우기"
        st.session_state.index = 0
        st.rerun()

# 2️⃣ 단어 외우기
elif st.session_state.step == "외우기":
    if st.session_state.level == "쉬움":
        words = easy_words
    elif st.session_state.level == "중간":
        words = medium_words
    else:
        words = hard_words

    st.subheader(f"{st.session_state.level} 단어 외우기")
    eng, kor = words[st.session_state.index]
    st.markdown(f"**단어:** {eng}  👉  **뜻:** {kor}")
    st.write(f"{st.session_state.index + 1} / {len(words)}")

    if st.button("다음 단어"):
        st.session_state.index += 1
        if st.session_state.index >= len(words):
            st.session_state.step = "퀴즈"
            st.session_state.quiz_score = 0
            st.session_state.quiz_total = len(words)
            st.session_state.quiz_words = random.sample(words, len(words))  # 문제 순서 섞기
            st.session_state.quiz_index = 0
        st.rerun()

# 3️⃣ 퀴즈 단계
elif st.session_state.step == "퀴즈":
    words = (easy_words if st.session_state.level == "쉬움"
             else medium_words if st.session_state.level == "중간"
             else hard_words)

    # 오답 기록 초기화 (처음만)
    if "wrong_answers" not in st.session_state:
        st.session_state.wrong_answers = []

    # 퀴즈 종료 조건 확인
    if st.session_state.quiz_index >= len(st.session_state.quiz_words):
        st.success(f"🎉 퀴즈 완료! 점수: {st.session_state.quiz_score} / {len(st.session_state.quiz_words)}")

        # 틀린 문제 보여주기
        if st.session_state.wrong_answers:
            st.subheader("❌ 틀린 문제 복습")
            for eng, correct, user_answer in st.session_state.wrong_answers:
                st.write(f"- **{eng}** → 정답: {correct} (내 답: {user_answer})")
        else:
            st.info("모든 문제를 맞췄습니다! 🎯")

        # 다시 시작 버튼
        if st.button("처음으로 돌아가기"):
            # 상태 초기화
            st.session_state.step = "난이도"
            st.session_state.level = None
            st.session_state.index = 0
            if "quiz_words" in st.session_state:
                del st.session_state.quiz_words
            if "wrong_answers" in st.session_state:
                del st.session_state.wrong_answers
            st.rerun()

    else:
        # 현재 문제
        eng, kor = st.session_state.quiz_words[st.session_state.quiz_index]

        st.subheader("❓ 퀴즈 시작!")
        st.write(f"'{eng}' 의 뜻은 무엇일까요?")

        # 문제 번호 기반 key → 자동 초기화
        answer = st.text_input("정답 입력:", key=f"quiz_input_{st.session_state.quiz_index}")

        if st.button("확인"):
            if answer.strip() == kor:
                st.success("✅ 정답!")
                st.session_state.quiz_score += 1
            else:
                st.error(f"❌ 오답! 정답은 {kor}")
                # 오답 기록 저장
                st.session_state.wrong_answers.append((eng, kor, answer.strip()))

            st.session_state.quiz_index += 1
            st.rerun()

        st.write(f"진행 상황: {st.session_state.quiz_index + 1} / {len(st.session_state.quiz_words)}")
        st.write(f"현재 점수: {st.session_state.quiz_score}")

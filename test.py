import streamlit as st
import random

st.title("📚 고등학생용 영어 단어 학습 앱")

# 난이도별 단어장
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

# 세션 상태 초기화
if "step" not in st.session_state:
    st.session_state.step = "난이도"  # 난이도 선택 단계
if "level" not in st.session_state:
    st.session_state.level = None
if "index" not in st.session_state:
    st.session_state.index = 0

# 단계별 화면
if st.session_state.step == "난이도":
    st.subheader("난이도를 선택하세요")
    level = st.radio("", ["쉬움", "중간", "어려움"])
    if st.button("선택 완료"):
        st.session_state.level = level
        st.session_state.step = "외우기"
        st.experimental_rerun()

elif st.session_state.step == "외우기":
    # 선택한 난이도 단어 가져오기
    if st.session_state.level == "쉬움":
        words = easy_words
    elif st.session_state.level == "중간":
        words = medium_words
    else:
        words = hard_words

    st.subheader(f"{st.session_state.level} 단어 외우기")
    eng, kor = words[st.session_state.index]
    st.markdown(f"**단어:** {eng}  👉  **뜻:** {kor}")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("다음 단어"):
            st.session_state.index += 1
            if st.session_state.index >= len(words):
                st.session_state.step = "퀴즈"
                st.session_state.index = 0
            st.experimental_rerun()
    with col2:
        st.write(f"{st.session_state.index+1} / {len(words)}")

elif st.session_state.step == "퀴즈":
    # 퀴즈 단계
    if st.session_state.level == "쉬움":
        words = easy_words
    elif st.session_state.level == "중간":
        words = medium_words
    else:
        words = hard_words

    eng, kor = random.choice(words)
    st.subheader("❓ 퀴즈 시작!")
    st.write(f"'{eng}'의 뜻은?")
    answer = st.text_input("정답 입력:")

    if st.button("확인"):
        if answer.strip() == kor:
            st.success("✅ 정답!")
        else:
            st.error(f"❌ 오답! 정답은 {kor}")

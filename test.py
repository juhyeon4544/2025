import streamlit as st
import random
import time

# ---------------------------
# 단어 데이터 (고등 모의고사 빈출 단어)
# ---------------------------
word_list = {
    "abandon": "버리다, 포기하다",
    "accelerate": "가속하다, 촉진하다",
    "acquire": "얻다, 습득하다",
    "adapt": "적응하다",
    "allocate": "할당하다, 배분하다",
    "analyze": "분석하다",
    "anticipate": "예상하다",
    "approximate": "대략의, 근사한",
    "artificial": "인공의, 인위적인",
    "assume": "가정하다, 맡다",
    "attain": "달성하다, 도달하다",
    "beneficial": "유익한, 이로운",
    "collapse": "붕괴하다, 무너지다",
    "concentrate": "집중하다",
    "contribute": "기여하다, 공헌하다",
    "crucial": "중요한, 결정적인",
    "determine": "결정하다, 알아내다",
    "distinguish": "구별하다",
    "eliminate": "제거하다",
    "encounter": "우연히 만나다, 직면하다",
    "exaggerate": "과장하다",
    "expand": "확장하다, 팽창하다",
    "generate": "생산하다, 발생시키다",
    "identify": "식별하다",
    "imply": "암시하다",
    "interpret": "해석하다",
    "maintain": "유지하다, 주장하다",
    "obtain": "얻다, 획득하다",
    "predict": "예측하다",
    "propose": "제안하다",
    "recall": "기억하다, 상기하다",
    "reduce": "줄이다",
    "reinforce": "강화하다",
    "rely": "의지하다",
    "require": "요구하다",
    "resolve": "해결하다, 결심하다",
    "retain": "유지하다",
    "significant": "중요한, 의미있는",
    "transform": "변화시키다",
}

# ---------------------------
# 상태 초기화
# ---------------------------
if "page" not in st.session_state:
    st.session_state.page = "study"  # 시작은 단어 학습 화면
if "score" not in st.session_state:
    st.session_state.score = 0
if "question" not in st.session_state:
    st.session_state.question = 0

# ---------------------------
# 단어 학습 화면
# ---------------------------
if st.session_state.page == "study":
    st.title("📘 단어 학습하기")
    st.write("아래 단어들을 먼저 외워보세요. 준비가 되면 '퀴즈 시작' 버튼을 누르세요.")
    
    # 단어 테이블 표시
    st.table({"영단어": list(word_list.keys()), "뜻": list(word_list.values())})
    
    if st.button("퀴즈 시작 🚀"):
        st.session_state.page = "quiz"
        st.session_state.score = 0
        st.session_state.question = 0
        st.rerun()

# ---------------------------
# 퀴즈 화면
# ---------------------------
elif st.session_state.page == "quiz":
    st.title("📝 단어 퀴즈")
    st.write(f"문제 {st.session_state.question + 1} / 10")

    words = list(word_list.keys())
    answer_word = random.choice(words)
    answer_meaning = word_list[answer_word]

    # 문제 유형 랜덤 선택
    question_type = random.choice(["word_to_meaning", "meaning_to_word"])

    if question_type == "word_to_meaning":
        st.subheader(f"👉 {answer_word} 의 뜻은?")
        options = random.sample(list(word_list.values()), 3)
        if answer_meaning not in options:
            options.append(answer_meaning)
        random.shuffle(options)
        correct_answer = answer_meaning
    else:
        st.subheader(f"👉 '{answer_meaning}' 에 해당하는 단어는?")

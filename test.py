import streamlit as st
import random
import time

st.set_page_config(page_title="영단어 퀴즈", layout="wide")

# ---------------------------
# CSS 스타일
# ---------------------------
st.markdown("""
<style>
.button-style {
    width: 100%;
    height: 70px;
    font-size: 20px;
    font-weight: bold;
    margin: 5px 0;
    border-radius: 12px;
    border: none;
    transition: 0.3s;
    cursor: pointer;
}
.button-style:hover {
    box-shadow: 0 5px 15px rgba(0,0,0,0.3);
    transform: scale(1.05);
}
.button-correct {
    background-color: #4CAF50;
    color: white;
}
.button-wrong {
    background-color: #f44336;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------
# 단어 데이터
# ---------------------------
word_list = {
    "abandon": "버리다, 포기하다",
    "accelerate": "가속하다, 촉진하다",
    "acquire": "얻다, 습득하다",
    "adapt": "적응하다",
    "analyze": "분석하다",
    "assume": "가정하다",
    "collapse": "붕괴하다",
    "contrast": "대조",
    "crucial": "중요한",
    "demonstrate": "증명하다"
}

TIME_LIMIT = 10
TOTAL_QUESTIONS = 10

# ---------------------------
# 세션 초기화
# ---------------------------
if "page" not in st.session_state:
    st.session_state.page = "study"
if "score" not in st.session_state:
    st.session_state.score = 0
if "question_num" not in st.session_state:
    st.session_state.question_num = 0
if "current_question" not in st.session_state:
    st.session_state.current_question = None
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "clicked_option" not in st.session_state:
    st.session_state.clicked_option = None

# ---------------------------
# 새 문제 생성
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
    st.session_state.clicked_option = None

# ---------------------------
# 학습 화면
# ---------------------------
if st.session_state.page == "study":
    st.title("📖 단어 학습하기")
    st.write("먼저 단어를 외워보세요. 준비되면 '퀴즈 시작' 버튼을 누르세요.")
    st.table({"영단어": list(word_list.keys()), "뜻": list(word_list.values())})
    
    if st.button("퀴즈 시작 🚀"):
        st.session_state.page = "quiz"
        st.session_state.score = 0
        st.session_state.question_num = 0
        st.session_state.current_question = None
        st.session_state.start_time = None
        st.session_state.clicked_option = None
        st.rerun()

# ---------------------------
# 퀴즈 화면
# ---------------------------
elif st.session_state.page == "quiz":
    if st.session_state.current_question is None:
        new_question()
    q = st.session_state.current_question

    elapsed = int(time.time() - st.session_state.start_time)
    remaining = max(TIME_LIMIT - elapsed, 0)
    progress = remaining / TIME_LIMIT

    st.title("📝 영단어 퀴즈")
    st.subheader(f"문제 {st.session_state.question_num + 1} / {TOTAL_QUESTIONS}")
    st.markdown(f"### '{q['eng_word']}' 의 뜻은 무엇일까요?")
    st.progress(progress)
    st.write(f"⏳ 남은 시간: {remaining}초")

    # 버튼 표시
    cols = st.columns(2)
    for i, option in enumerate(q["options"]):
        col = cols[i % 2]

        # 색상 결정
        if st.session_state.clicked_option is not None:
            if option == q["correct"]:
                style_class = "button-style button-correct"
            elif option == st.session_state.clicked_option:
                style_class = "button-style button-wrong"
            else:
                style_class = "button-style"
            col.markdown(f"<button class='{style_class}'>{option}</button>", unsafe_allow_html=True)
        else:
            if col.button(option, key=f"opt_{i}"):
                st.session_state.clicked_option = option
                if option == q["correct"]:
                    st.session_state.score += 1
                st.session_state.start_time = time.time()
                st.experimental_rerun()

    # 시간 초과 처리
    if remaining <= 0 and st.session_state.clicked_option is None:
        st.session_state.clicked_option = "timeout"
        st.experimental_rerun()

    # 다음 문제 이동
    if st.session_state.clicked_option is not None:
        if time.time() - st.session_state.start_time >= 1.5:
            st.session_state.question_num += 1
            if st.session_state.question_num >= TOTAL_QUESTIONS:
                st.session_state.page = "result"
            st.session_state.current_question = None
            st.session_state.start_time = None
            st.session_state.clicked_option = None
            st.experimental_rerun()

# ---------------------------
# 결과 화면
# ---------------------------
elif st.session_state.page == "result":
    st.title("🏆 퀴즈 완료!")
    st.write(f"최종 점수: {st.session_state.score} / {TOTAL_QUESTIONS}")
    if st.button("다시하기 🔁"):
        st.session_state.page = "study"
        st.session_state.score = 0
        st.session_state.question_num = 0
        st.session_state.current_question = None
        st.session_state.start_time = None
        st.session_state.clicked_option = None
        st.rerun()

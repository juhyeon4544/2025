import streamlit as st
import random
import time

# ---------------------------
# 단어 데이터 (고등 모의고사 빈출 단어 샘플)
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
    "demonstrate": "증명하다",
    "distinguish": "구별하다",
    "emerge": "나타나다",
    "generate": "생성하다",
    "illustrate": "설명하다",
    "interpret": "해석하다",
    "maintain": "유지하다",
    "predict": "예측하다",
    "rely": "의지하다",
    "resolve": "해결하다",
    "significant": "중요한"
}

TIME_LIMIT = 10  # 제한 시간 (초)

# ---------------------------
# 세션 초기화
# ---------------------------
if "page" not in st.session_state:
    st.session_state.page = "study"  # 시작 화면: 단어 학습
if "score" not in st.session_state:
    st.session_state.score = 0
if "question_num" not in st.session_state:
    st.session_state.question_num = 0
if "current_question" not in st.session_state:
    st.session_state.current_question = None
if "start_time" not in st.session_state:
    st.session_state.start_time = None

# ---------------------------
# 단어 학습 화면
# ---------------------------
if st.session_state.page == "study":
    st.title("📖 단어 학습하기")
    st.write("먼저 단어를 충분히 외우세요. 준비되면 '퀴즈 시작'을 눌러주세요.")
    st.table({"영단어": list(word_list.keys()), "뜻": list(word_list.values())})
    
    if st.button("퀴즈 시작 🚀"):
        st.session_state.page = "quiz"
        st.session_state.score = 0
        st.session_state.question_num = 0
        st.session_state.current_question = None
        st.session_state.start_time = None
        st.rerun()

# ---------------------------
# 퀴즈 화면
# ---------------------------
elif st.session_state.page == "quiz":
    st.title("📝 단어 퀴즈")
    st.write(f"문제 {st.session_state.question_num + 1} / 10")

    # 새로운 문제 생성
    if st.session_state.current_question is None:
        eng_word = random.choice(list(word_list.keys()))
        correct_meaning = word_list[eng_word]

        # 보기 만들기
        wrong_options = random.sample([v for k,v in word_list.items() if v != correct_meaning], 3)
        options = wrong_options + [correct_meaning]
        random.shuffle(options)

        st.session_state.current_question = {
            "eng_word": eng_word,
            "correct": correct_meaning,
            "options": options
        }
        st.session_state.start_time = time.time()

    q = st.session_state.current_question

    # 남은 시간 계산
    elapsed = int(time.time() - st.session_state.start_time)
    remaining = max(TIME_LIMIT - elapsed, 0)
    progress = remaining / TIME_LIMIT
    st.progress(progress)
    st.write(f"⏳ 남은 시간: {remaining}초")

    st.subheader(f"'{q['eng_word']}' 의 뜻은 무엇일까요?")
    choice = st.radio("정답 선택:", q['options'], key="quiz_radio")

    if st.button("제출"):
        if remaining <= 0:
            st.error("⏰ 시간 초과! 오답 처리됩니다.")
        elif choice == q['correct']:
            st.success("✅ 정답!")
            st.session_state.score += 1
        else:
            st.error(f"❌ 오답! 정답은 '{q['correct']}'")

        # 다음 문제 준비
        st.session_state.question_num += 1
        if st.session_state.question_num >= 10:
            st.session_state.page = "result"
        st.session_state.current_question = None
        st.session_state.start_time = None
        st.rerun()

# ---------------------------
# 결과 화면
# ---------------------------
elif st.session_state.page == "result":
    st.title("🏆 퀴즈 완료!")
    st.write(f"최종 점수: {st.session_state.score} / 10")

    if st.button("다시하기 🔁"):
        st.session_state.page = "study"
        st.session_state.score = 0
        st.session_state.question_num = 0
        st.session_state.current_question = None
        st.session_state.start_time = None
        st.rerun()

# vocab_quiz_app.py
import streamlit as st
import random
import pandas as pd
from typing import List, Tuple

st.set_page_config(page_title="영단어 퀴즈 게임", layout="centered")

# ---------- 기본 단어장 (샘플) ----------
DEFAULT_VOCAB = [
    ("apple", "사과"),
    ("banana", "바나나"),
    ("cat", "고양이"),
    ("dog", "개"),
    ("elephant", "코끼리"),
    ("friend", "친구"),
    ("happy", "행복한"),
    ("important", "중요한"),
    ("knowledge", "지식"),
    ("learn", "배우다"),
    ("music", "음악"),
    ("novel", "소설"),
    ("orange", "오렌지"),
    ("planet", "행성"),
    ("quiet", "조용한"),
    ("river", "강"),
    ("school", "학교"),
    ("travel", "여행하다"),
    ("useful", "유용한"),
    ("yellow", "노란색"),
]

# ---------- 유틸리티 ----------
def load_vocab_from_uploaded(file) -> List[Tuple[str,str]]:
    """CSV/TXT 업로드 처리: 각 줄 'word,meaning'"""
    try:
        df = pd.read_csv(file, header=None, names=["word","meaning"])
        pairs = [(str(r["word"]).strip(), str(r["meaning"]).strip()) for _, r in df.iterrows() if pd.notna(r["word"])]
        return pairs
    except Exception:
        # fallback: txt lines
        content = file.getvalue().decode("utf-8").splitlines()
        pairs = []
        for line in content:
            if "," in line:
                w,m = line.split(",",1)
                pairs.append((w.strip(), m.strip()))
        return pairs

def make_mc_choices(correct: Tuple[str,str], pool: List[Tuple[str,str]], k=4):
    """객관식 보기 생성"""
    choices = [correct[1]]
    candidates = [m for (w,m) in pool if m != correct[1]]
    random.shuffle(candidates)
    for c in candidates[:max(0,k-1)]:
        choices.append(c)
    random.shuffle(choices)
    return choices

def init_session():
    if "vocab" not in st.session_state:
        st.session_state.vocab = DEFAULT_VOCAB.copy()
    if "quiz_list" not in st.session_state:
        st.session_state.quiz_list = []
    if "index" not in st.session_state:
        st.session_state.index = 0
    if "score" not in st.session_state:
        st.session_state.score = 0
    if "answers" not in st.session_state:
        st.session_state.answers = []  # (word, user_answer, correct_bool)
    if "streak" not in st.session_state:
        st.session_state.streak = 0
    if "mode" not in st.session_state:
        st.session_state.mode = "객관식"
    if "last_submission" not in st.session_state:
        st.session_state.last_submission = None
    if "show_answer" not in st.session_state:
        st.session_state.show_answer = False

def start_quiz(n_questions: int, shuffle_questions: bool):
    vocab = st.session_state.vocab.copy()
    if shuffle_questions:
        random.shuffle(vocab)
    st.session_state.quiz_list = vocab[:n_questions]
    st.session_state.index = 0
    st.session_state.score = 0
    st.session_state.answers = []
    st.session_state.streak = 0
    st.session_state.last_submission = None
    st.session_state.show_answer = False

# ---------- 레이아웃 ----------
st.title("🇬🇧 영단어 퀴즈 게임")
st.caption("객관식 또는 타이핑으로 실력을 체크해보세요. CSV 업로드 지원 (형식: word,meaning)")

init_session()

with st.sidebar:
    st.header("설정 / 단어장")
    uploaded = st.file_uploader("단어장 업로드 (CSV or TXT, each line: word,meaning)", type=["csv","txt"])
    if uploaded:
        try:
            pairs = load_vocab_from_uploaded(uploaded)
            if pairs:
                st.session_state.vocab = pairs
                st.success(f"업로드 완료: {len(pairs)}개 단어 로드됨")
            else:
                st.warning("유효한 단어를 찾지 못했습니다. 형식: word,meaning")
        except Exception as e:
            st.error("파일 로드 실패: " + str(e))

    st.write("---")
    n_questions = st.number_input("문제 수", min_value=1, max_value=100, value=min(10, max(5, len(st.session_state.vocab))), step=1)
    mc_choices = st.slider("객관식 보기 개수", min_value=2, max_value=6, value=4)
    shuffle_q = st.checkbox("문제 섞기", value=True)
    mode = st.radio("문제 형식 선택", ["객관식", "타이핑"], index=0)
    st.session_state.mode = mode
    st.write("---")
    st.write(f"현재 단어장: {len(st.session_state.vocab)}개")
    if st.button("퀴즈 시작 / 재시작"):
        if len(st.session_state.vocab) == 0:
            st.warning("단어장이 비어있습니다.")
        else:
            start_quiz(int(n_questions), shuffle_q)

# ---------- 메인 화면 ----------
if not st.session_state.quiz_list:
    st.info("왼쪽에서 설정 후 '퀴즈 시작' 버튼을 눌러 시작하세요.")
    st.write("샘플 단어 예시:")
    st.write(pd.DataFrame(st.session_state.vocab[:10], columns=["word","meaning"]))
    st.stop()

# 현재 문제
idx = st.session_state.index
total = len(st.session_state.quiz_list)
current = st.session_state.quiz_list[idx]
st.progress(idx / total)
st.subheader(f"문제 {idx+1} / {total}")
st.markdown("**단어:**")
st.code(current[0], line_numbers=False)

# 힌트 및 정답 보기
col1, col2, col3 = st.columns([1,1,1])
with col1:
    if st.button("힌트 (뜻 일부 공개)"):
        hint = current[1]
        half = max(1, len(hint)//2)
        st.info(hint[:half] + ("*" * (len(hint)-half)))
with col2:
    if st.button("정답 보기"):
        st.session_state.show_answer = True
with col3:
    if st.button("다음 문제 건너뛰기"):
        st.session_state.answers.append((current[0], None, False))
        st.session_state.streak = 0
        st.session_state.index += 1
        st.session_state.show_answer = False
        st.rerun()   # ✅ 변경됨

# 문제 형식별
if st.session_state.mode == "객관식":
    choices = make_mc_choices(current, st.session_state.vocab, k=mc_choices)
    user_choice = st.radio("뜻을 고르세요:", choices, index=0)
    submitted = st.button("확인")
    if submitted:
        correct = (user_choice == current[1])
        st.session_state.answers.append((current[0], user_choice, correct))
        st.session_state.last_submission = user_choice
        if correct:
            st.success("정답이에요! ✅")
            st.session_state.score += 1
            st.session_state.streak += 1
        else:
            st.error(f"오답이에요. 정답: {current[1]}")
            st.session_state.streak = 0
        st.session_state.index += 1
        st.session_state.show_answer = False
        st.rerun()   # ✅ 변경됨

elif st.session_state.mode == "타이핑":
    user_input = st.text_input("뜻(한국어)을 입력하세요:", value="")
    submitted = st.button("제출")
    if submitted:
        normalized_user = user_input.strip().lower()
        correct_answer = current[1].strip().lower()
        correct = (normalized_user == correct_answer) or (normalized_user in correct_answer) or (correct_answer in normalized_user)
        st.session_state.answers.append((current[0], user_input, correct))
        st.session_state.last_submission = user_input
        if correct:
            st.success("정답이에요! ✅")
            st.session_state.score += 1
            st.session_state.streak += 1
        else:
            st.error(f"오답이에요. 정답: {current[1]}")
            st.session_state.streak = 0
        st.session_state.index += 1
        st.session_state.show_answer = False
        st.rerun()   # ✅ 변경됨

# 정답 보기
if st.session_state.show_answer:
    st.info(f"정답: {current[1]}")

# 퀴즈 종료
if st.session_state.index >= total:
    st.markdown("---")
    st.header("🎉 퀴즈 완료!")
    score = st.session_state.score
    st.subheader(f"점수: {score} / {total} ({score/total*100:.1f}%)")
    st.write(f"최대 연속 정답: {st.session_state.streak}")
    df = pd.DataFrame(st.session_state.answers, columns=["word","your_answer","correct"])
    df["correct_meaning"] = [next((m for w,m in st.session_state.vocab if w==row[0]), "") for row in st.session_state.answers]
    st.write("상세 결과")
    st.dataframe(df)

    if st.button("처음으로 돌아가기 / 다시하기"):
        st.session_state.quiz_list = []
        st.session_state.index = 0
        st.session_state.score = 0
        st.session_state.answers = []
        st.session_state.streak = 0
        st.session_state.show_answer = False
        st.rerun()   # ✅ 변경됨

# 상태 요약
st.write("---")
col_a, col_b, col_c = st.columns(3)
col_a.metric("점수", f"{st.session_state.score} / {total}")
col_b.metric("현재 문제", f"{idx+1} / {total}")
col_c.metric("연속 정답", f"{st.session_state.streak}")

st.caption("앱 개선 아이디어: 발음 추가, 정답 유사도 개선, 단어 레벨별 필터, 점수 저장 등")

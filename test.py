import streamlit as st
import random

st.title("📚 고등학생용 영어 단어 학습 앱")

# 난이도별 단어장
easy_words = {
    "apple": "사과",
    "banana": "바나나",
    "school": "학교",
    "teacher": "선생님",
    "book": "책",
    "friend": "친구",
    "water": "물",
    "food": "음식",
    "music": "음악",
    "movie": "영화"
}

medium_words = {
    "environment": "환경",
    "culture": "문화",
    "history": "역사",
    "science": "과학",
    "technology": "기술",
    "education": "교육",
    "future": "미래",
    "health": "건강",
    "travel": "여행",
    "society": "사회",
    "language": "언어",
    "hobby": "취미",
    "success": "성공",
    "failure": "실패",
    "dream": "꿈",
    "freedom": "자유",
    "responsibility": "책임",
    "knowledge": "지식",
    "opportunity": "기회",
    "experience": "경험"
}

hard_words = {
    "inevitable": "피할 수 없는",
    "significant": "중요한",
    "consequence": "결과",
    "hypothesis": "가설",
    "complicated": "복잡한",
    "achievement": "성취",
    "perspective": "관점",
    "contradiction": "모순",
    "comprehensive": "포괄적인",
    "transition": "변화, 전환",
    "alternative": "대안",
    "fundamental": "근본적인",
    "interpretation": "해석",
    "sustainable": "지속 가능한",
    "phenomenon": "현상",
    "reputation": "평판",
    "revolution": "혁명",
    "circumstance": "상황",
    "efficiency": "효율",
    "priority": "우선순위",
    "modification": "수정",
    "composition": "구성, 작문",
    "contribution": "기여",
    "innovation": "혁신",
    "distinction": "차이, 구별",
    "implementation": "실행",
    "investment": "투자",
    "obligation": "의무",
    "participation": "참여",
    "prediction": "예측",
    "preference": "선호",
    "publication": "출판",
    "requirement": "요구 사항",
    "restriction": "제한",
    "significance": "의미, 중요성",
    "speculation": "추측",
    "tendency": "경향",
    "validity": "타당성",
    "variation": "변화",
    "conservation": "보존",
    "determination": "결단력",
    "distinguish": "구별하다",
    "evaluate": "평가하다",
    "generate": "생성하다",
    "identify": "식별하다",
    "maintain": "유지하다",
    "occur": "발생하다",
    "persuade": "설득하다",
    "recommend": "추천하다"
}

# 난이도 선택
level = st.radio("난이도를 선택하세요:", ["쉬움 (10개)", "중간 (20개)", "어려움 (50개)"])

if level == "쉬움 (10개)":
    words = easy_words
elif level == "중간 (20개)":
    words = medium_words
else:
    words = hard_words

# 퀴즈 방향 선택
mode = st.radio("퀴즈 모드 선택:", ["단어 → 뜻", "뜻 → 단어"])

# 퀴즈 출제
eng, kor = random.choice(list(words.items()))

if mode == "단어 → 뜻":
    st.subheader(f"❓ '{eng}' 의 뜻은 무엇일까요?")
    answer = st.text_input("정답 입력:")
    if st.button("정답 확인"):
        if answer.strip() == kor:
            st.success("✅ 정답!")
        else:
            st.error(f"❌ 오답! 정답은 {kor}")

else:  # 뜻 → 단어
    st.subheader(f"❓ '{kor}' 의 영어 단어는 무엇일까요?")
    answer = st.text_input("정답 입력:")
    if st.button("정답 확인"):
        if answer.strip().lower() == eng.lower():
            st.success("✅ 정답!")
        else:
            st.error(f"❌ 오답! 정답은 {eng}")

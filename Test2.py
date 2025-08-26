# simple_word_app.py
import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="심플 영어 단어 암기 앱", layout="centered")

st.title("📚 심플 영어 단어 암기 앱")

# 1. 단어 CSV 업로드
st.sidebar.header("단어 목록 업로드")
uploaded_file = st.sidebar.file_uploader("CSV 파일 선택", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    if '단어' not in df.columns or '뜻' not in df.columns:
        st.error("CSV 파일에 '단어'와 '뜻' 컬럼이 있어야 합니다.")
    else:
        words = df.to_dict('records')

        # 2. 학습 모드 선택
        mode = st.sidebar.radio("모드 선택", ["플래시카드", "퀴즈"])

        if mode == "플래시카드":
            st.header("💡 플래시카드 학습")
            card = random.choice(words)
            st.subheader(card['단어'])
            if st.button("뜻 보기"):
                st.write(f"✅ 뜻: {card['뜻']}")

        elif mode == "퀴즈":
            st.header("📝 단어 퀴즈")
            question = random.choice(words)
            correct = question['뜻']

            # 객관식 4지선다
            options = [correct] + random.sample([w['뜻'] for w in words if w['뜻'] != correct], k=3)
            random.shuffle(options)
            answer = st.radio(f"'{question['단어']}'의 뜻은?", options)
            if st.button("제출"):
                if answer == correct:
                    st.success("🎉 정답입니다!")
                else:
                    st.error(f"❌ 틀렸습니다. 정답은: {correct}")
else:
    st.info("먼저 CSV 파일을 업로드 해주세요.")

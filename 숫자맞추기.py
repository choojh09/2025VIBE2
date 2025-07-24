import streamlit as st
import random

st.set_page_config(page_title="숫자 맞추기 게임", layout="centered")
st.title("🎯 숫자 맞추기 게임")

st.markdown("""
1부터 100 사이의 숫자 중 컴퓨터가 고른 숫자를 맞혀보세요!
""")

# 숫자 저장 및 초기화
if "target" not in st.session_state:
    st.session_state.target = random.randint(1, 100)
    st.session_state.tries = 0

guess = st.number_input("숫자를 입력하세요 (1~100):", min_value=1, max_value=100, step=1)

if st.button("확인"):
    st.session_state.tries += 1
    if guess < st.session_state.target:
        st.warning("너무 작아요!")
    elif guess > st.session_state.target:
        st.warning("너무 커요!")
    else:
        st.success(f"정답입니다! 🎉 {st.session_state.tries}번 만에 맞췄어요!")
        if st.button("다시 시작하기"):
            st.session_state.target = random.randint(1, 100)
            st.session_state.tries = 0

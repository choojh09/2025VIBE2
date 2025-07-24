import streamlit as st
import random

st.set_page_config(page_title="가위바위보 게임", layout="centered")
st.title("✊ ✋ ✌ 🦎 가위바위보도마뱀 게임")

st.markdown("""
가위, 바위, 보, 도마뱀 중 하나를 선택하세요!  
컴퓨터와의 대결에서 이겨보세요!
""")

choices = ["가위", "바위", "보", "도마뱀"]
user_choice = st.radio("당신의 선택은?", choices)

# 승리 규칙 정의
win_rules = {
    "가위": ["보", "도마뱀"],
    "바위": ["가위", "도마뱀"],
    "보": ["바위"],
    "도마뱀": ["보"]
}

if st.button("결과 보기"):
    computer_choice = random.choice(choices)
    st.write(f"컴퓨터의 선택: **{computer_choice}**")

    if user_choice == computer_choice:
        result = "무승부입니다! 😐"
    elif computer_choice in win_rules.get(user_choice, []):
        result = "당신이 이겼습니다! 🎉"
    else:
        result = "컴퓨터가 이겼습니다! 😢"

    st.subheader(result)

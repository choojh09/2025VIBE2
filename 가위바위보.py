import streamlit as st
import random

st.set_page_config(page_title="가위바위보 게임", layout="centered")
st.title("✊ ✋ ✌ 가위바위보 게임")

st.markdown("""
간단한 가위바위보 게임입니다.  
당신의 선택과 컴퓨터의 선택을 비교하여 승부를 가립니다!
""")

choices = ["가위", "바위", "보"]
user_choice = st.radio("당신의 선택은?", choices)

if st.button("결과 보기"):
    computer_choice = random.choice(choices)
    st.write(f"컴퓨터의 선택: **{computer_choice}**")

    if user_choice == computer_choice:
        result = "무승부입니다! 😐"
    elif (
        (user_choice == "가위" and computer_choice == "보") or
        (user_choice == "바위" and computer_choice == "가위") or
        (user_choice == "보" and computer_choice == "바위")
    ):
        result = "당신이 이겼습니다! 🎉"
    else:
        result = "컴퓨터가 이겼습니다! 😢"

    st.subheader(result)

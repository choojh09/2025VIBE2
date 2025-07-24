import streamlit as st
import random

st.set_page_config(page_title="Streamlit 솔리테어", layout="wide")
st.title("🃏 Streamlit 솔리테어 (룰 + 이동 + 색 규칙 포함)")

st.markdown("""
텍스트 기반 솔리테어입니다. 
- 각 열에서 마지막 공개된 카드만 다른 열로 옮길 수 있습니다.
- 파운데이션에는 같은 무늬로 A부터 K까지 순서대로 쌓아야 합니다.
- 카드 이동 시 색이 교차해야 하며, 이동되는 카드는 현재 카드보다 숫자가 1 작아야 합니다.
- 더미(Deck)에서 새로운 카드를 열고, 오픈된 카드를 열 또는 파운데이션으로 이동할 수 있습니다.
""")

suits = ["♠", "♥", "♦", "♣"]
ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
rank_value = {rank: i+1 for i, rank in enumerate(ranks)}
suit_color = {"♠": "black", "♣": "black", "♥": "red", "♦": "red"}
deck_full = [f"{suit}{rank}" for suit in suits for rank in ranks]

# 상태 초기화
if "columns" not in st.session_state:
    random.shuffle(deck_full)
    st.session_state.columns = []
    for i in range(4):
        pile = deck_full[i*7:(i+1)*7]
        hidden = pile[:-1]
        visible = [pile[-1]] if pile else []
        st.session_state.columns.append({"hidden": hidden, "visible": visible})
    st.session_state.foundation = {suit: [] for suit in suits}
    st.session_state.deck = deck_full[28:]
    st.session_state.open_card = []
    st.session_state.discard_pile = []

# 더미에서 카드 열기
if st.button("🔄 더미에서 카드 열기"):
    if st.session_state.deck:
        card = st.session_state.deck.pop(0)
        st.session_state.open_card = [card]
        st.session_state.discard_pile.append(card)
    else:
        st.warning("더미에 남은 카드가 없습니다.")

# 테이블 출력 (줄 정렬 개선)
st.markdown("---")
st.subheader("📍 테이블")
max_height = max(len(p["hidden"] + p["visible"]) for p in st.session_state.columns)
table_rows = []
for i in range(max_height):
    row = []
    for col in st.session_state.columns:
        total = col["hidden"] + col["visible"]
        if i < len(col["hidden"]):
            row.append("[###]")
        elif i < len(total):
            row.append(f"[{total[i]}]")
        else:
            row.append("     ")
    table_rows.append("   ".join(row))

st.text("\n".join(table_rows))

# 오픈 카드와 열 이동 기능
st.markdown("---")
st.subheader("🎴 더미와 오픈 카드")
if st.session_state.open_card:
    open_card = st.session_state.open_card[-1]
    st.markdown(f"열린 카드: [{open_card}]")
    move_target = st.selectbox("오픈 카드를 이동할 열:", [1, 2, 3, 4], key="dummy_target")
    if st.button("📤 오픈 카드 열로 이동"):
        card = st.session_state.open_card[-1]
        suit, rank = card[0], card[1:]
        target = st.session_state.columns[move_target - 1]
        if target["visible"]:
            top = target["visible"][-1]
            top_suit, top_rank = top[0], top[1:]
            if suit_color[suit] != suit_color[top_suit] and rank_value[rank] == rank_value[top_rank] - 1:
                target["visible"].append(card)
                st.session_state.open_card.pop()
                st.success(f"{card} → 열 {move_target} 이동 완료")
            else:
                st.warning("색이 교차하고 숫자가 1 작아야 합니다.")
        else:
            if rank == "K":
                target["visible"].append(card)
                st.session_state.open_card.pop()
                st.success(f"{card} → 빈 열 {move_target} 이동 완료")
            else:
                st.warning("빈 열에는 K만 이동 가능합니다.")
else:
    st.markdown("열린 카드 없음")

st.markdown(f"남은 더미 카드 수: {len(st.session_state.deck)}")
st.markdown(f"버린 카드 수: {len(st.session_state.discard_pile)}")

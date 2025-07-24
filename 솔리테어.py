import streamlit as st
import random

st.set_page_config(page_title="Streamlit 솔리테어", layout="wide")
st.title("🃏 Streamlit 솔리테어 (룰 + 이동 + 색 규칙 포함)")

st.markdown("""
텍스트 기반 솔리테어입니다. 
- 각 열에서 마지막 공개된 카드만 다른 열로 옮길 수 있습니다.
- 파운데이션에는 같은 무늬로 A부터 K까지 순서대로 쌓아야 합니다.
- 카드 이동 시 색이 교차해야 하며, 이동되는 카드는 현재 카드보다 숫자가 1 작아야 합니다.
- 더미(Deck)에서 새로운 카드를 열 수 있습니다.
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

# 더미에서 카드 열기
if st.button("🔄 더미에서 카드 열기"):
    if st.session_state.deck:
        st.session_state.open_card = [st.session_state.deck.pop(0)]
    else:
        st.warning("더미에 남은 카드가 없습니다.")

# 오픈카드를 열로 이동
st.markdown("---")
st.subheader("🎯 오픈 카드 열로 이동")
target_column = st.selectbox("오픈 카드를 이동할 열 (1~4):", [1, 2, 3, 4], key="open_move")
if st.button("⬇️ 오픈 카드 이동"):
    if st.session_state.open_card:
        card = st.session_state.open_card.pop()
        suit, rank = card[0], card[1:]
        target = st.session_state.columns[target_column - 1]
        if target["visible"]:
            top_card = target["visible"][-1]
            top_suit, top_rank = top_card[0], top_card[1:]
            if suit_color[suit] != suit_color[top_suit] and rank_value[rank] == rank_value[top_rank] - 1:
                target["visible"].append(card)
                st.success(f"오픈 카드 {card} → 열 {target_column} 이동 완료")
            else:
                st.warning("색이 교차하고 숫자가 1 작아야 이동할 수 있습니다.")
        else:
            if rank == "K":
                target["visible"].append(card)
                st.success(f"빈 열로 {card} 이동 완료")
            else:
                st.warning("빈 열에는 K만 이동 가능합니다.")
    else:
        st.warning("오픈된 카드가 없습니다.")

# 카드 옮기기: 열에서 열로
st.markdown("---")
st.subheader("⬇️ 카드 옮기기")
from_col = st.selectbox("출발 열 (1~4)", [1, 2, 3, 4], key="from")
to_col = st.selectbox("도착 열 (1~4)", [1, 2, 3, 4], key="to")
if st.button("👉 열에서 열로 이동"):
    source = st.session_state.columns[from_col - 1]
    target = st.session_state.columns[to_col - 1]
    if source["visible"]:
        card = source["visible"][-1]
        suit, rank = card[0], card[1:]
        if target["visible"]:
            top_card = target["visible"][-1]
            top_suit, top_rank = top_card[0], top_card[1:]
            if suit_color[suit] != suit_color[top_suit] and rank_value[rank] == rank_value[top_rank] - 1:
                source["visible"].pop()
                target["visible"].append(card)
                if not source["visible"] and source["hidden"]:
                    source["visible"].append(source["hidden"].pop())
                st.success(f"{card} → 열 {to_col} 이동 완료")
            else:
                st.warning("색이 교차하고 숫자가 1 작아야 이동할 수 있습니다.")
        else:
            if rank == "K":
                source["visible"].pop()
                target["visible"].append(card)
                if not source["visible"] and source["hidden"]:
                    source["visible"].append(source["hidden"].pop())
                st.success(f"{card} → 빈 열 {to_col} 이동 완료")
            else:
                st.warning("빈 열에는 K만 이동 가능합니다.")
    else:
        st.warning("출발 열에 이동 가능한 카드가 없습니다.")

# 카드 파운데이션으로 이동
selected_column = st.selectbox("파운데이션으로 옮길 열:", [1, 2, 3, 4], key="f")
if st.button("⬆️ 파운데이션으로 보내기"):
    col_idx = selected_column - 1
    pile = st.session_state.columns[col_idx]
    if pile["visible"]:
        card = pile["visible"][-1]
        suit, rank = card[0], card[1:]
        foundation = st.session_state.foundation[suit]
        expected = ranks[len(foundation)]
        if rank == expected:
            st.session_state.foundation[suit].append(card)
            pile["visible"].pop()
            if not pile["visible"] and pile["hidden"]:
                pile["visible"].append(pile["hidden"].pop())
            st.success(f"{card} 파운데이션 이동 성공!")
        else:
            st.warning(f"{card}는 {suit}{expected}가 되어야 이동할 수 있습니다.")
    else:
        st.warning("열에 카드가 없습니다.")

# 테이블 출력
st.markdown("---")
st.subheader("📍 테이블")
table_display = ""
max_height = max(len(p["hidden"] + p["visible"]) for p in st.session_state.columns)
for row in range(max_height):
    line = []
    for pile in st.session_state.columns:
        full = pile["hidden"] + pile["visible"]
        if row < len(pile["hidden"]):
            line.append("###")
        elif row < len(full):
            line.append(f"---{full[row]}---")
        else:
            line.append("     ")
    table_display += "  ".join(line) + "\n"
st.text(table_display)

# 파운데이션 출력
st.markdown("---")
st.subheader("✅ 파운데이션")
st.markdown("  ".join([
    f"{suit}: " + (" → ".join(st.session_state.foundation[suit]) if st.session_state.foundation[suit] else "(비어있음)")
    for suit in suits
]))

# 더미 출력
st.markdown("---")
st.subheader("🎴 더미와 오픈 카드")
if st.session_state.open_card:
    st.markdown(f"열린 카드: ---{st.session_state.open_card[0]}---")
else:
    st.markdown("열린 카드 없음")

if st.button("🆕 게임 초기화"):
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
    st.experimental_rerun()

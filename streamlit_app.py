
import streamlit as st
import requests
from collections import defaultdict

API_URL = "https://script.google.com/macros/s/AKfycbzh_Lagq1pXOSCDl6JmiEt0Rmbq5vmlMUd_N-qPq1Txki--JvAqsaaOSvHsVKcD7DZrIQ/exec"

@st.cache_data
def load_data():
    chu_de = requests.get(API_URL).json()
    phan_hoi = requests.get(API_URL, params={"type": "phanhoi"}).json()
    return chu_de, phan_hoi

chu_de_data, phan_hoi_data = load_data()

# Tách dữ liệu ChuDe
all_choices = defaultdict(list)
for row in chu_de_data[1:]:
    category, choice = row
    all_choices[category].append(choice)

# Dữ liệu đã được chọn
used = set()
used_songs = set()
for row in phan_hoi_data[1:]:
    used.update(row[1:5])
    if row[5]:
        used_songs.update([s.strip() for s in row[5].split(",")])

# Lọc dữ liệu chưa được chọn
available = defaultdict(list)
for cat, choices in all_choices.items():
    for c in choices:
        if cat == "Bài hát":
            if c not in used_songs:
                available[cat].append(c)
        else:
            if c not in used:
                available[cat].append(c)

st.title("🎤 Đăng ký Chủ đề & Bài Hát")

with st.form("form"):
    if not available["Team"]: st.warning("❌ Tất cả các Team đã được chọn."); st.stop()
    team = st.radio("Team", available["Team"])

    if not available["Dấu xưa vọng lời"]: st.warning("❌ Chủ đề 1 hết lựa chọn."); st.stop()
    topic1 = st.radio("Dấu xưa vọng lời", available["Dấu xưa vọng lời"])

    if not available["Dòng sử chảy mãi"]: st.warning("❌ Chủ đề 2 hết lựa chọn."); st.stop()
    topic2 = st.radio("Dòng sử chảy mãi", available["Dòng sử chảy mãi"])

    if not available["Debate"]: st.warning("❌ Chủ đề 3 hết lựa chọn."); st.stop()
    topic3 = st.radio("Debate: Góc nhìn hậu thế", available["Debate"])

    st.markdown("🎵 **Bài hát Pool Party (chọn nhiều)**")
    selected_songs = []
    for i, song in enumerate(available["Bài hát"]):
        if st.checkbox(song, key=f"song_{i}"):
            selected_songs.append(song)

    submitted = st.form_submit_button("✅ Gửi đăng ký")

    if submitted:
        payload = {
            "team": team,
            "topic1": topic1,
            "topic2": topic2,
            "topic3": topic3,
            "songs": selected_songs
        }
        try:
            res = requests.post(API_URL, json=payload)
            result = res.json()
            if result.get("success"):
                st.success("✅ Ghi nhận thành công!")
                st.balloons()
            else:
                st.error("❌ " + result.get("message"))
                st.markdown("<script>setTimeout(() => window.location.reload(), 5000);</script>", unsafe_allow_html=True)
        except Exception as e:
            st.warning(f"⚠️ Gửi thất bại: {e}")

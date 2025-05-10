
import streamlit as st
import requests

API_URL = "https://script.google.com/macros/s/AKfycbx2kxoOnhJDZ0rLWxyuybA-1Yp1N8HmDb3PmLNfJcN2H42TNqU01vRfSuO3bGXRiSvyBg/exec"  # <- Thay URL thật

st.set_page_config(page_title="Đăng ký chủ đề", layout="centered")
st.title("🎤 Đăng ký Chủ đề & Bài Hát")

@st.cache_data
def load_data():
    all_choices = requests.get(API_URL).json()
    used_choices = requests.get(API_URL, params={"type": "used"}).json()

    filtered = {}
    for category in all_choices:
        used = set(used_choices.get(category, []))
        filtered[category] = [c for c in all_choices[category] if c not in used]
    return filtered

data = load_data()

with st.form("register"):
    if not data.get("Team"): st.stop()
    team = st.radio("TEAM", data["Team"])
    topic1 = st.radio("DẤU XƯA VỌNG LỜI", data["Dấu xưa vọng lời"])
    topic2 = st.radio("DÒNG SỬ CHẢY MÃI", data["Dòng sử chảy mãi"])
    topic3 = st.radio("DEBATE: GÓC NHÌN HẬU THẾ", data["Debate"])

    st.markdown("🎵 **BÀI HÁT POOL PARTY (chọn nhiều)**")
    selected_songs = []
    for i, song in enumerate(data["Bài hát"]):
        if st.checkbox(song, key=f"song_{i}"):
            selected_songs.append(song)

    submitted = st.form_submit_button("Gửi")

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
                st.error("❌ " + result.get("message", "Lỗi chưa xác định."))
                st.markdown("<script>setTimeout(() => { window.location.reload(); }, 5000);</script>", unsafe_allow_html=True)
        except Exception as e:
            st.warning(f"⚠️ Gửi dữ liệu thất bại: {e}")

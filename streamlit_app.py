import streamlit as st
import requests

API_URL = "https://script.google.com/macros/s/AKfycbwfacrQGO7Dm6A0gnAYDfQX6QuIG5Cf_P8s887UTtCDjpseQc3t6i4DqtWg-zAGojbbNQ/exec"  # Thay bằng Script ID thật

st.set_page_config(page_title="Đăng ký chủ đề & bài hát", layout="centered")
st.title("Đăng ký Chủ đề & Bài hát")

@st.cache_data
def load_choices():
    try:
        res = requests.get(API_URL)
        if res.status_code == 200:
            return res.json()
        else:
            return {}
    except Exception:
        return {}

data = load_choices()

if not data:
    st.error("Không thể tải dữ liệu từ hệ thống. Vui lòng thử lại sau.")
    st.stop()

with st.form("register_form"):
    if not data.get("Team"):
        st.warning("Tất cả các TEAM đã được chọn.")
        st.stop()

    team = st.radio("🔰 Chọn TEAM", options=data.get("Team", []), key="team")

    if not data.get("Dấu xưa vọng lời"):
        st.warning("Không còn chủ đề nào cho DẤU XƯA VỌNG LỜI.")
        st.stop()
    topic1 = st.radio("📜 DẤU XƯA VỌNG LỜI", options=data.get("Dấu xưa vọng lời", []), key="topic1")

    if not data.get("Dòng sử chảy mãi"):
        st.warning("Không còn chủ đề nào cho DÒNG SỬ CHẢY MÃI.")
        st.stop()
    topic2 = st.radio("📖 DÒNG SỬ CHẢY MÃI", options=data.get("Dòng sử chảy mãi", []), key="topic2")

    if not data.get("Debate"):
        st.warning("Không còn chủ đề nào cho DEBATE.")
        st.stop()
    topic3 = st.radio("🤔 DEBATE: GÓC NHÌN HẬU THẾ", options=data.get("Debate", []), key="topic3")

    st.markdown("🎵 **BÀI HÁT POOL PARTY (chọn nhiều)**")
    selected_songs = []
    if data.get("Bài hát"):
        for i, song in enumerate(data["Bài hát"]):
            if st.checkbox(song, key=f"song_{i}"):
                selected_songs.append(song)
    else:
        st.info("Tất cả bài hát đã được chọn.")

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
                st.error("❌ " + result.get("message", "Lỗi chưa xác định."))
                st.markdown("""
                    <script>
                        setTimeout(() => { window.location.reload(); }, 5000);
                    </script>
                """, unsafe_allow_html=True)
        except Exception as e:
            st.warning(f"⚠️ Gửi dữ liệu thất bại: {e}")

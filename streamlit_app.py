
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
    team = st.radio("Chọn TEAM", data.get("Team", []), key="team")
    topic1 = st.radio("Chủ đề: DẤU XƯA VỌNG LỜI", data.get("Dấu xưa vọng lời", []), key="topic1")
    topic2 = st.radio("Chủ đề: DÒNG SỬ CHẢY MÃI", data.get("Dòng sử chảy mãi", []), key="topic2")
    topic3 = st.radio("Chủ đề: DEBATE: GÓC NHÌN HẬU THẾ", data.get("Debate", []), key="topic3")

    st.markdown("**BÀI HÁT POOL PARTY (chọn nhiều)**")
    selected_songs = []
    for idx, song in enumerate(data.get("Bài hát", [])):
        if st.checkbox(song, key=f"song_{idx}"):
            selected_songs.append(song)

    submitted = st.form_submit_button("Gửi đăng ký")

    if submitted:
        payload = {
            "team": team,
            "topic1": topic1,
            "topic2": topic2,
            "topic3": topic3,
            "songs": selected_songs
        }

        try:
            response = requests.post(API_URL, json=payload)
            result = response.json()

            if result.get("success"):
                st.success("✅ Ghi nhận thành công.")
            else:
                st.error("❌ " + result.get("message", "Lỗi chưa xác định."))
                st.info("Trang sẽ tải lại sau 5 giây.")
                # st.rerun()
        except Exception as e:
            st.warning(f"⚠️ Gửi dữ liệu thất bại: {e}")
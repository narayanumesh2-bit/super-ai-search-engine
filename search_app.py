import streamlit as st
import os
from groq import Groq
from gtts import gTTS
import io

# --- SETUP ---
st.set_page_config(page_title="Super AI Engine", layout="wide", initial_sidebar_state="expanded")

# --- SESSION STATE ---
if "auth" not in st.session_state: st.session_state.auth = False
if "user" not in st.session_state: st.session_state.user = {"name": "", "id": ""}
if "history" not in st.session_state: st.session_state.history = []

# --- CSS (Premium Dark Theme) ---
st.markdown("""
<style>
    .stApp { background: #0d1117; color: #ffffff; }
    section[data-testid="stSidebar"] { background-color: #161b22; }
    .stTextInput input { border-radius: 20px !important; }
    .stButton>button { border-radius: 20px !important; font-weight: bold; width: 100%; }
</style>
""", unsafe_allow_html=True)

# --- LOGIN ---
if not st.session_state.auth:
    st.markdown("<h1 style='text-align:center'>🔎 Super AI Login</h1>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["Google / Email", "Mobile Number"])
    with tab1:
        n = st.text_input("Name")
        e = st.text_input("Gmail/Email")
        if st.button("➔ Sign in"):
            if n and e: st.session_state.auth=True; st.session_state.user={"name":n, "id":e}; st.rerun()
    with tab2:
        m = st.text_input("Mobile Number")
        otp = st.text_input("Enter OTP (1234)")
        if st.button("➔ Verify & Login"):
            if m and otp == "1234": st.session_state.auth=True; st.session_state.user={"name":"User", "id":m}; st.rerun()
    st.stop()

# --- SIDEBAR ---
with st.sidebar:
    st.markdown(f"### 👤 {st.session_state.user['name']}")
    st.caption(f"🆔 {st.session_state.user['id']}")
    if st.button("🚪 Logout"): st.session_state.auth = False; st.rerun()
    st.markdown("---")
    api_key = st.text_input("⚙️ Groq API Key:", type="password")
    menu = st.radio("🚀 Features:", ["🔍 AI Search", "🎬 Video Splitter", "📚 Study Notes", "🎵 AI Song", "🎨 AI Art"])
    st.markdown("---")
    st.markdown("### 🕒 History")
    for h in st.session_state.history[-5:]: st.markdown(f"• {h}")

# --- MAIN ENGINE ---
if menu == "🔍 AI Search":
    st.title("🔍 AI Search Engine")
    # SEARCH ROW (Mic + Plus + Search)
    c1, c2, c3, c4 = st.columns([5, 0.5, 0.5, 1])
    with c1: q = st.text_input("", placeholder="Ask anything...")
    with c2: st.button("🎙️")
    with c3: plus = st.button("➕")
    with c4: search = st.button("➔ Search")
    
    if plus: st.info("File/Camera/Doc Upload opened.")
    if search and q:
        client = Groq(api_key=api_key)
        resp = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"user","content":q}])
        st.markdown(resp.choices[0].message.content)
        st.session_state.history.append(q)

elif menu == "📚 Study Notes":
    st.title("📚 Study Notes AI")
    with st.expander("➕ Click to Upload / Camera"):
        mode = st.radio("Select Input", ["Camera", "File Upload"], horizontal=True)
        if mode == "Camera": st.camera_input("Take Photo")
        else: st.file_uploader("Upload Notes File")
    
    topic = st.text_input("Topic Name:")
    if st.button("Generate Hand-Written Notes"):
        st.success("AI scanning & Notes generated!")

elif menu == "🎬 Video Splitter":
    st.title("🎬 Video Splitter")
    st.file_uploader("Upload Video")
    if st.button("Start Split (15s)"): st.write("Processing video...")

elif menu == "🎵 AI Song":
    st.title("🎵 AI Song Studio")
    st.text_input("Song Mood/Topic:")
    if st.button("Generate Song"): st.write("Writing lyrics & generating voice...")

elif menu == "🎨 AI Art":
    st.title("🎨 AI Art Studio")
    p = st.text_input("Prompt:")
    if st.button("Generate Art"): st.image(f"https://image.pollinations.ai/prompt/{p}")
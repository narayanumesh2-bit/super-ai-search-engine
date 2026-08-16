import streamlit as st
from groq import Groq
import urllib.parse

# Page Setup
st.set_page_config(page_title="Super AI Studio", layout="wide")

# CSS Styling (Handwritten & Notebook look)
st.markdown("""
<style>
    .notebook-sheet {
        background: repeating-linear-gradient(#fdfbf7, #fdfbf7 28px, #e2e8f0 29px, #fdfbf7 30px);
        font-family: 'Caveat', cursive; color: #1e3a8a; padding: 40px; border-radius: 8px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1); font-size: 20px; line-height: 35px; border-left: 5px solid #ef4444;
    }
    .main-title { color: #1e293b; font-weight: 800; }
</style>
""", unsafe_allow_html=True)

# Session State
if "logged_in" not in st.session_state: st.session_state.logged_in = False

# Login Flow
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align:center;'>⚡ Super AI Studio</h1>", unsafe_allow_html=True)
    if st.button("🔴 Google से सुरक्षित प्रवेश करें (Sign-In)", use_container_width=True, type="primary"):
        st.session_state.logged_in = True
        st.rerun()
else:
    # Sidebar
    st.sidebar.markdown("### 🛠️ स्टूडियो टूल्स")
    tool = st.sidebar.radio("फीचर्स चुनें:", ["🎬 Shorts Gen", "📝 Notes & Diagrams", "🎨 Image Gen", "🎵 Music Gen", "🔍 AI Search"])
    groq_api = st.sidebar.text_input("Groq API Key:", type="password")

    def call_ai(prompt):
        if not groq_api: return "⚠️ कृपया साइडबार में Groq API Key डालें।"
        client = Groq(api_key=groq_api)
        return client.chat.completions.create(messages=[{"role":"user", "content": prompt}], model="llama-3.3-70b-versatile").choices[0].message.content

    # FEATURE 1 & 2: Shorts Generator (YouTube Link or Upload)
    if tool == "🎬 Shorts Gen":
        st.header("🎬 YouTube/Video Shorts Generator")
        mode = st.radio("इनपुट:", ["🔗 YouTube Link", "📁 Upload Video (1-2 Hours)"])
        source = st.text_input("लिंक पेस्ट करें या फाइल पाथ:")
        
        # User Defined Settings
        part_duration = st.number_input("एक पार्ट कितने सेकंड का होना चाहिए?", value=20)
        num_parts = st.number_input("कुल कितने पार्ट्स में बाँटना है?", value=20)
        
        if st.button("🚀 शॉर्ट्स में कन्वर्ट करें"):
            prompt = f"Analyze video: {source}. Split it into {num_parts} parts, each {part_duration} seconds. For each part, give me the exact timestamp, a viral hook, and a script."
            st.markdown(call_ai(prompt))

    # FEATURE 3: Handwritten Notes & Diagrams
    elif tool == "📝 Notes & Diagrams":
        st.header("📝 Handwritten Notes & Diagrams")
        topic = st.text_input("टॉपिक का नाम:")
        uploaded_img = st.file_uploader("टॉपिक का फोटो अपलोड करें (ऑप्शनल):", type=["jpg", "png"])
        
        if st.button("🖋️ हैंड-रिटन नोट्स बनाएँ"):
            prompt = f"Create handwritten-style detailed notes for '{topic}'. Explain the diagram structure clearly. Use bullet points and headers."
            content = call_ai(prompt)
            st.markdown(f"<div class='notebook-sheet'>{content.replace(chr(10), '<br>')}</div>", unsafe_allow_html=True)
            st.info("💡 प्रो टिप: अगर फोटो दी है, तो मैं उसे देख कर डायग्राम समझा सकता हूँ।")

    # FEATURE 4: Image Gen
    elif tool == "🎨 Image Gen":
        st.header("🎨 AI Image Generator")
        prompt = st.text_input("क्या बनाना है?")
        if st.button("इमेज बनाएँ"):
            st.image(f"https://image.pollinations.ai/prompt/{urllib.parse.quote(prompt)}")

    # FEATURE 5: Music Gen
    elif tool == "🎵 Music Gen":
        st.header("🎵 AI Music/Anthem Generator")
        topic = st.text_input("गाने का विषय:")
        if st.button("गीत और म्यूजिक कम्पोज करें"):
            st.write(call_ai(f"Compose a complete song/anthem about '{topic}' with beats and lyrics."))

    # FEATURE 6: Main Search
    elif tool == "🔍 AI Search":
        st.header("🔍 Super AI Search")
        query = st.text_input("कुछ भी पूछें...")
        if st.button("सर्च करें"):
            st.markdown(call_ai(query))

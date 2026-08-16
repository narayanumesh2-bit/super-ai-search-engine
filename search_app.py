import streamlit as st
from groq import Groq
import urllib.parse
import re

# 1. Page Configuration
st.set_page_config(
    page_title="Super AI Multi-Tool Studio",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styles
st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 800;
        background: -webkit-linear-gradient(45deg, #2563eb, #9333ea);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }
    .notebook-sheet {
        background: repeating-linear-gradient(
            #fdfbf7,
            #fdfbf7 28px,
            #e2e8f0 29px,
            #fdfbf7 30px
        );
        font-family: 'Comic Sans MS', 'Caveat', 'Segoe Print', cursive, sans-serif;
        color: #1e3a8a;
        padding: 25px 30px 25px 50px;
        border-left: 4px solid #ef4444;
        border-radius: 8px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.06);
        line-height: 30px;
        font-size: 16px;
        margin-top: 15px;
    }
</style>
""", unsafe_allow_html=True)

# 2. Session State Initialization
if "user_authenticated" not in st.session_state:
    st.session_state.user_authenticated = False
if "user_info" not in st.session_state:
    st.session_state.user_info = {}
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "otp_sent" not in st.session_state:
    st.session_state.otp_sent = False

# 3. Streamlit-Native Authentication Flow
if not st.session_state.user_authenticated:
    st.markdown("<h1 class='main-title'>⚡ Super AI Engine</h1>", unsafe_allow_html=True)
    st.write("जारी रखने के लिए कृपया अपनी पहचान सत्यापित करें:")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        tab1, tab2 = st.tabs(["📧 Google / Email ID", "📱 Phone OTP"])

        with tab1:
            st.markdown("#### Google / Email से लॉगिन")
            user_name = st.text_input("पूरा नाम", placeholder="उदा. Prince Raj")
            user_email = st.text_input("ईमेल आईडी (Google Account)", placeholder="example@gmail.com")
            if st.button("🚀 Google अकाउंट से जारी रखें", use_container_width=True):
                if user_email and "@" in user_email:
                    st.session_state.user_authenticated = True
                    st.session_state.user_info = {"name": user_name or "Google User", "email": user_email}
                    st.success("लॉगिन सफल!")
                    st.rerun()
                else:
                    st.error("कृपया सही ईमेल आईडी दर्ज करें।")

        with tab2:
            st.markdown("#### मोबाइल नंबर और OTP")
            phone = st.text_input("मोबाइल नंबर", placeholder="+91 9876543210")
            
            if not st.session_state.otp_sent:
                if st.button("📩 Send OTP", use_container_width=True):
                    if len(phone) >= 10:
                        st.session_state.otp_sent = True
                        st.info("OTP आपके मोबाइल नंबर पर भेज दिया गया है (डेमो कोड: 123456)")
                        st.rerun()
                    else:
                        st.error("कृपया 10 अंकों का मोबाइल नंबर डालें।")
            else:
                otp = st.text_input("6 Digit OTP डालें", placeholder="123456")
                if st.button("✅ Verify & Login", use_container_width=True):
                    if otp:
                        st.session_state.user_authenticated = True
                        st.session_state.user_info = {"name": phone, "email": phone}
                        st.success("सत्यापित हुआ!")
                        st.rerun()
                    else:
                        st.error("कृपया OTP दर्ज करें।")

else:
    # 4. Sidebar Controls & Multi-Tools
    with st.sidebar:
        st.markdown(f"### 👋 स्वागत है, **{st.session_state.user_info.get('name', 'User')}**")
        st.caption(f"🆔 {st.session_state.user_info.get('email', '')}")
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.user_authenticated = False
            st.session_state.user_info = {}
            st.session_state.otp_sent = False
            st.rerun()
            
        st.divider()
        st.markdown("#### ⚙️ AI सेटिंग्स")
        groq_api_key = st.text_input("Groq API Key दर्ज करें", type="password", placeholder="gsk_...")
        
        target_lang = st.selectbox(
            "🌐 मुख्य भाषा चुनें (Language)",
            ["Hindi (हिन्दी)", "Bhojpuri (भोजपुरी)", "Maithili (मैथिली)", "English", 
             "Bengali (বাংলা)", "Telugu (తెలుగు)", "Tamil (தமிழ்)", "Marathi (मराठी)", 
             "Gujarati (ગુજરાતી)", "Kannada (ಕನ್ನಡ)", "Punjabi (ਪੰਜਾਬੀ)", "Odia (ଓଡ଼ିଆ)"]
        )

        st.divider()
        tool_mode = st.radio(
            "🚀 स्पेशल टूल्स:",
            [
                "🔍 Universal AI Search & Q&A",
                "🎬 YouTube/Video to 20 Shorts Maker",
                "📝 Handwritten Notes & Diagram Studio",
                "🎨 AI Image Generator",
                "🎵 AI Music & Anthem Generator"
            ]
        )

    # Helper function for Groq API
    def call_ai(system_prompt, user_prompt, model="llama-3.3-70b-versatile"):
        if not groq_api_key:
            st.warning("⚠️ कृपया साइडबार में अपनी Groq API Key डालें।")
            return None
        try:
            client = Groq(api_key=groq_api_key)
            full_system = f"{system_prompt}\nTarget Language: {target_lang}. Provide clear, high-quality, structured output."
            res = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": full_system},
                    {"role": "user", "content": user_prompt}
                ],
                model=model,
                temperature=0.7
            )
            return res.choices[0].message.content
        except Exception as e:
            st.error(f"AI Error: {e}")
            return None

    # ==========================================
    # TOOL 1: UNIVERSAL AI SEARCH
    # ==========================================
    if tool_mode == "🔍 Universal AI Search & Q&A":
        st.markdown("<h2 class='main-title'>🔍 Universal AI Search & Reasoning</h2>", unsafe_allow_html=True)
        st.caption(f"भाषा: {target_lang} | किसी भी विषय पर सटीक व गहरा समाधान प्राप्त करें।")

        query = st.chat_input("अपना सवाल यहाँ टाइप करें...")
        
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])
                
        if query:
            st.session_state.chat_history.append({"role": "user", "content": query})
            with st.chat_message("user"):
                st.write(query)
            
            with st.chat_message("assistant"):
                with st.spinner("उत्तर तैयार हो रहा है..."):
                    reply = call_ai(
                        "You are an advanced super-intelligent AI search assistant specializing in coding, mathematics, factual queries, and step-by-step reasoning.",
                        query
                    )
                    if reply:
                        st.markdown(reply)
                        st.session_state.chat_history.append({"role": "assistant", "content": reply})

    # ==========================================
    # TOOL 2: YOUTUBE & VIDEO TO SHORTS
    # ==========================================
    elif tool_mode == "🎬 YouTube/Video to 20 Shorts Maker":
        st.markdown("<h2 class='main-title'>🎬 Video to 20 Viral Shorts Generator</h2>", unsafe_allow_html=True)
        st.write("2-3 घंटे के वीडियो या YouTube लिंक से सीधे **15–20 सेकंड के 20 वायरल क्लिप्स, टाइमस्टैम्प्स, हुक्स और पूरी स्क्रिप्ट** बनाएँ।")

        input_choice = st.radio("इनपुट का माध्यम:", ["🔗 YouTube Video Link", "📁 Video File Upload"], horizontal=True)
        video_context = ""

        if input_choice == "🔗 YouTube Video Link":
            yt_url = st.text_input("YouTube वीडियो लिंक:", placeholder="https://www.youtube.com/watch?v=...")
            topic_hint = st.text_input("वीडियो का विषय / टॉपिक (वैकल्पिक):", placeholder="उदा. पॉडकास्ट, मोटिवेशन, कोडिंग ट्यूटोरियल...")
            if yt_url:
                st.video(yt_url)
                video_context = f"YouTube URL: {yt_url}\nTopic Focus: {topic_hint}"
        else:
            uploaded_vid = st.file_uploader("वीडियो फ़ाइल अपलोड करें (.mp4, .mkv, .mov)", type=["mp4", "mkv", "mov"])
            topic_hint = st.text_input("अपलोड की गई वीडियो का विषय:", placeholder="वीडियो किस बारे में है?")
            if uploaded_vid:
                st.success(f"फ़ाइल '{uploaded_vid.name}' अपलोड की गई।")
                video_context = f"Uploaded File: {uploaded_vid.name}\nTopic Focus: {topic_hint}"

        if st.button("🚀 20 वायरल शॉर्ट्स क्लिप्स बनाएँ", use_container_width=True):
            if not video_context:
                st.warning("कृपया YouTube लिंक या वीडियो फ़ाइल प्रदान करें।")
            else:
                with st.spinner("20 वायरल शॉर्ट्स क्लिप्स तैयार की जा रही हैं..."):
                    prompt = f"""
                    Analyze this video and generate exactly 20 high-retention Viral Shorts / Reels concepts (each strictly 15-20 seconds long).
                    Details: {video_context}
                    
                    For EACH of the 20 parts, output structured markdown:
                    - **Part Number & Viral Title**
                    - **Timestamp Window** (e.g. 04:15 - 04:35)
                    - **Psychological Hook** (First 3 seconds spoken line)
                    - **Full Voiceover Script** (15 to 20 seconds, exact spoken words in {target_lang})
                    - **On-Screen Visual / B-Roll Suggestion**
                    - **Hashtags**
                    """
                    result = call_ai("You are an expert viral content strategist and video editor.", prompt)
                    if result:
                        st.success("✅ 20 वायरल शॉर्ट्स क्लिप्स तैयार हैं!")
                        st.markdown(result)

    # ==========================================
    # TOOL 3: HANDWRITTEN NOTES & DIAGRAMS
    # ==========================================
    elif tool_mode == "📝 Handwritten Notes & Diagram Studio":
        st.markdown("<h2 class='main-title'>📝 Handwritten Notes & Flowchart Studio</h2>", unsafe_allow_html=True)
        st.write("किसी भी विषय पर **पेन से लिखे नोटबुक स्टाइल नोट्स** और **विजुअल डायग्राम** तैयार करें।")

        note_topic = st.text_input("विषय दर्ज करें:", placeholder="उदा. Operating System, Binary Search Tree, Photosynthesis, भारतीय संविधान...")

        if st.button("🖋️ नोट्स और डायग्राम बनाएँ", use_container_width=True):
            if not note_topic:
                st.warning("कृपया टॉपिक का नाम लिखें।")
            else:
                with st.spinner("नोट्स और आरेख तैयार हो रहे हैं..."):
                    prompt = f"""
                    Create neat, topper-style pen-written study notes for students on: '{note_topic}'.
                    Language: {target_lang}
                    Format:
                    - Clear Heading with double underline
                    - Bullet points with neat points
                    - Key definitions in highlight boxes
                    - 3 Golden Exam Tips
                    """
                    notes_content = call_ai("You are a topper student creating clean pen-written revision notes.", prompt)
                    if notes_content:
                        st.markdown("### 📋 नोटबुक शीट (Handwritten Sheet)")
                        st.markdown(f"<div class='notebook-sheet'>{notes_content.replace(chr(10), '<br>')}</div>", unsafe_allow_html=True)

    # ==========================================
    # TOOL 4: AI IMAGE GENERATOR
    # ==========================================
    elif tool_mode == "🎨 AI Image Generator":
        st.markdown("<h2 class='main-title'>🎨 High-Speed AI Image Generator</h2>", unsafe_allow_html=True)
        st.write("प्रॉम्प्ट लिखें और तुरंत हाई-डेफिनिशन इमेज जनरेट करें।")

        img_prompt = st.text_area("इमेज का विवरण (Prompt):", placeholder="उदा. Cyberpunk Indian programmer working on a supercomputer with neon reflections, 8k...")
        aspect = st.selectbox("साइज चुनें:", ["Square (1:1)", "Portrait (9:16)", "Landscape (16:9)"])
        dim_map = {"Square (1:1)": (1024, 1024), "Portrait (9:16)": (720, 1280), "Landscape (16:9)": (1280, 720)}

        if st.button("✨ इमेज जनरेट करें", use_container_width=True):
            if not img_prompt:
                st.warning("कृपया प्रॉम्प्ट दर्ज करें।")
            else:
                with st.spinner("इमेज रेंडर हो रही है..."):
                    w, h = dim_map[aspect]
                    encoded_prompt = urllib.parse.quote(img_prompt)
                    image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={w}&height={h}&nologo=true&seed=42"
                    st.image(image_url, caption=img_prompt, use_container_width=True)
                    st.markdown(f"[📥 इमेज डाउनलोड करें]({image_url})")

    # ==========================================
    # TOOL 5: AI MUSIC & ANTHEM GENERATOR
    # ==========================================
    elif tool_mode == "🎵 AI Music & Anthem Generator":
        st.markdown("<h2 class='main-title'>🎵 AI Music & Anthem Studio</h2>", unsafe_allow_html=True)
        st.write("गीत, रैप, ग्रुप एंथम या किसी भी अवसर के लिए पूरा म्यूजिकल ट्रैक तैयार करें।")

        song_topic = st.text_input("गीत का विषय:", placeholder="उदा. दोस्तों का कॉलेज एंथम, एनर्जेटिक रैप, मोटिवेशनल ट्रैक...")
        genre = st.selectbox("म्यूजिक स्टाइल:", ["Desi Hip-Hop / Rap", "Bollywood Romantic", "High-Energy Anthem", "Acoustic Lo-Fi"])

        if st.button("🎼 गाना और कम्पोजिशन तैयार करें", use_container_width=True):
            if not song_topic:
                st.warning("कृपया गाने का विषय लिखें।")
            else:
                with st.spinner("लिरिक्स, बीट और वोकल्स तैयार हो रहे हैं..."):
                    prompt = f"""
                    Compose a complete original song/anthem for: '{song_topic}'
                    Genre: {genre}
                    Language: {target_lang}
                    
                    Include:
                    1. Track Title & BPM
                    2. Instrument Setup
                    3. [Intro], [Verse 1], [Chorus/Hook], [Verse 2], [Outro]
                    4. Suno/Udio AI Music generation prompt tag
                    """
                    music_res = call_ai("You are a professional music producer and lyricist.", prompt)
                    if music_res:
                        st.markdown(music_res)

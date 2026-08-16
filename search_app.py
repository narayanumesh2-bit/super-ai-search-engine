import streamlit as st
import streamlit.components.v1 as components
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
        margin-bottom: 5px;
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

# 2. Session States
if "user_authenticated" not in st.session_state:
    st.session_state.user_authenticated = False
if "user_info" not in st.session_state:
    st.session_state.user_info = {}
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# URL से असली Google लॉगिन टोकन पकड़ना
params = st.query_params
if "user_email" in params and "user_name" in params:
    st.session_state.user_authenticated = True
    st.session_state.user_info = {
        "name": params.get("user_name"),
        "email": params.get("user_email")
    }

# 3. REAL FIREBASE GOOGLE POPUP COMPONENT
def render_real_firebase_google_auth():
    auth_html = """
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <script src="https://www.gstatic.com/firebasejs/9.23.0/firebase-app-compat.js"></script>
      <script src="https://www.gstatic.com/firebasejs/9.23.0/firebase-auth-compat.js"></script>
      <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 10px;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .card {
            background: #ffffff;
            border-radius: 16px;
            padding: 30px 25px;
            max-width: 400px;
            width: 100%;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
            text-align: center;
            border: 1px solid #e2e8f0;
        }
        .btn-google {
            background: #ffffff;
            color: #374151;
            border: 1px solid #d1d5db;
            padding: 14px 20px;
            border-radius: 24px;
            width: 100%;
            font-size: 15px;
            font-weight: 600;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 12px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.08);
            transition: all 0.2s ease;
        }
        .btn-google:hover {
            background: #f8fafc;
            border-color: #9ca3af;
            box-shadow: 0 4px 10px rgba(0,0,0,0.12);
        }
        .status { margin-top: 15px; font-size: 14px; font-weight: 500; }
        .success { color: #059669; }
        .error { color: #dc2626; }
      </style>
    </head>
    <body>
      <div class="card">
        <h2 style="margin: 0 0 8px 0; color: #1e293b; font-size: 22px;">Super AI Studio</h2>
        <p style="color: #64748b; font-size: 14px; margin-bottom: 25px;">
          अपने असली Google खाते से सुरक्षित लॉगिन करें
        </p>

        <button class="btn-google" onclick="signInWithGoogle()">
          <svg width="20" height="20" viewBox="0 0 24 24"><path fill="#EA4335" d="M12 5c1.6 0 3 .6 4.1 1.6l3.1-3.1C17.3 1.7 14.8 1 12 1 7.4 1 3.5 3.6 1.6 7.4l3.7 2.9C6.2 7.1 8.9 5 12 5z"/><path fill="#4285F4" d="M23.5 12.3c0-.8-.1-1.6-.2-2.3H12v4.6h6.5c-.3 1.5-1.1 2.8-2.4 3.7l3.7 2.9c2.2-2 3.7-5 3.7-8.9z"/><path fill="#FBBC05" d="M5.3 14.7c-.2-.7-.4-1.5-.4-2.3s.2-1.6.4-2.3L1.6 7.2C.6 9.2 0 11.5 0 14s.6 4.8 1.6 6.8l3.7-2.9z"/><path fill="#34A853" d="M12 23c3.2 0 6-1.1 8-3l-3.7-2.9c-1.1.7-2.5 1.2-4.3 1.2-3.1 0-5.8-2.1-6.7-5.3L1.6 16c1.9 3.8 5.8 6.4 10.4 6.4z"/></svg>
          Google से Sign In करें
        </button>

        <div id="status-box" class="status"></div>
      </div>

      <script>
        const firebaseConfig = {
            apiKey: "AIzaSyDz0N-bxSTYDAk0ygQNjbRX-a0shIl8Pw8",
            authDomain: "super-ai-search-engine.firebaseapp.com",
            projectId: "super-ai-search-engine",
            storageBucket: "super-ai-search-engine.firebasestorage.app",
            messagingSenderId: "703150781255",
            appId: "1:703150781255:web:22866e05bee00ec8c5d262"
        };

        if (!firebase.apps.length) {
            firebase.initializeApp(firebaseConfig);
        }

        const auth = firebase.auth();

        function setMsg(msg, isError=false) {
            const el = document.getElementById('status-box');
            el.innerText = msg;
            el.className = isError ? 'status error' : 'status success';
        }

        function signInWithGoogle() {
            setMsg("Google लॉगिन विंडो खुल रही है...");
            const provider = new firebase.auth.GoogleAuthProvider();
            provider.setCustomParameters({ prompt: 'select_account' });

            auth.signInWithPopup(provider)
                .then((result) => {
                    const user = result.user;
                    setMsg("लॉगिन सफल! रीडायरेक्ट हो रहा है...");
                    const base = window.top.location.origin + window.top.location.pathname;
                    const redirectUrl = `${base}?user_email=${encodeURIComponent(user.email)}&user_name=${encodeURIComponent(user.displayName || 'Google User')}`;
                    window.top.location.href = redirectUrl;
                })
                .catch((error) => {
                    console.error("Popup error:", error);
                    // If popup is blocked by browser, open external auth redirect
                    if (error.code === 'auth/operation-not-supported-in-this-environment' || error.code === 'auth/popup-blocked') {
                        setMsg("बाहरी विंडो में Google साइन-इन खोला जा रहा है...");
                        auth.signInWithRedirect(provider);
                    } else {
                        setMsg("Error: " + error.message, true);
                    }
                });
        }
      </script>
    </body>
    </html>
    """
    components.html(auth_html, height=300)

# 4. Authentication Barrier
if not st.session_state.user_authenticated:
    st.markdown("<h1 class='main-title'>⚡ Super AI Engine</h1>", unsafe_allow_html=True)
    render_real_firebase_google_auth()

else:
    # 5. Sidebar Navigation & Special Features
    with st.sidebar:
        user = st.session_state.user_info
        st.markdown(f"### 👋 स्वागत है, **{user.get('name', 'User')}**")
        st.caption(f"🔒 {user.get('email', '')}")
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.user_authenticated = False
            st.session_state.user_info = {}
            st.query_params.clear()
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
            "🚀 स्पेशल टूल्स (Special Features):",
            [
                "🔍 Universal AI Search & Q&A",
                "🎬 YouTube/Video to 20 Shorts Maker",
                "📝 Handwritten Notes & Diagram Studio",
                "🎨 AI Image Generator",
                "🎵 AI Music & Anthem Generator"
            ]
        )

    # Groq Helper
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
        st.caption(f"भाषा: {target_lang} | किसी भी प्रश्न का सटीक और गहरा समाधान प्राप्त करें।")

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
                    reply = call_ai("You are an advanced super-intelligent AI search assistant specializing in coding, mathematics, science and reasoning.", query)
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
            topic_hint = st.text_input("वीडियो का विषय / टॉपिक (वैकल्पिक):", placeholder="उदा. पॉडकास्ट, मोटिवेशन, ट्यूटोरियल...")
            if yt_url:
                st.video(yt_url)
                video_context = f"YouTube URL: {yt_url}\nTopic Focus: {topic_hint}"
        else:
            uploaded_vid = st.file_uploader("वीडियो फ़ाइल अपलोड करें (.mp4, .mkv, .mov)", type=["mp4", "mkv", "mov"])
            topic_hint = st.text_input("अपलोड की गई वीडियो का विषय:", placeholder="वीडियो किस बारे में है?")
            if uploaded_vid:
                st.success(f"फ़ाइल '{uploaded_vid.name}' अपलोड की गई।")
                video_context = f"Uploaded File: {uploaded_vid.name}\nTopic Focus: {topic_hint}"

        if st.button("🚀 20 वायरल शॉर्ट्स क्लिप्स बनाएँ", use_container_width=True, type="primary"):
            if not video_context:
                st.warning("कृपया YouTube लिंक या वीडियो फ़ाइल प्रदान करें।")
            else:
                with st.spinner("20 वायरल शॉर्ट्स क्लिप्स तैयार की जा रही हैं..."):
                    prompt = f"""
                    Analyze this video and generate exactly 20 high-retention Viral Shorts / Reels concepts (strictly 15-20 seconds each).
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
                        st.success("✅ 20 वायरल शॉर्ट्स तैयार हैं!")
                        st.markdown(result)

    # ==========================================
    # TOOL 3: HANDWRITTEN NOTES & DIAGRAMS
    # ==========================================
    elif tool_mode == "📝 Handwritten Notes & Diagram Studio":
        st.markdown("<h2 class='main-title'>📝 Handwritten Notes & Flowchart Studio</h2>", unsafe_allow_html=True)
        st.write("किसी भी विषय पर **पेन से लिखे नोटबुक स्टाइल नोट्स** और **विजुअल डायग्राम** तैयार करें।")

        note_topic = st.text_input("विषय दर्ज करें:", placeholder="उदा. Operating System, Binary Search Tree, Photosynthesis, भारतीय संविधान...")

        if st.button("🖋️ नोट्स और डायग्राम बनाएँ", use_container_width=True, type="primary"):
            if not note_topic:
                st.warning("कृपया टॉपिक का नाम लिखें।")
            else:
                with st.spinner("नोट्स और आरेख तैयार हो रहे हैं..."):
                    prompt = f"""
                    Create neat, topper-style pen-written study notes for students on: '{note_topic}'.
                    Language: {target_lang}
                    Format:
                    - Clear Heading with double underline
                    - Bullet points with stars or dashes
                    - Key definitions in highlight boxes
                    - 3 Golden Exam Tips
                    """
                    notes_content = call_ai("You are a topper student creating clean pen-written revision notes.", prompt)
                    if notes_content:
                        st.markdown("### 📋 नोटबुक शीट (Handwritten Look)")
                        st.markdown(f"<div class='notebook-sheet'>{notes_content.replace(chr(10), '<br>')}</div>", unsafe_allow_html=True)

    # ==========================================
    # TOOL 4: AI IMAGE GENERATOR
    # ==========================================
    elif tool_mode == "🎨 AI Image Generator":
        st.markdown("<h2 class='main-title'>🎨 High-Speed AI Image Generator</h2>", unsafe_allow_html=True)
        st.write("प्रॉम्प्ट लिखें और तुरंत हाई-डेफिनिशन इमेज जनरेट करें।")

        img_prompt = st.text_area("इमेज का विवरण (Prompt):", placeholder="उदा. Futuristic Indian coder working in a cyber room with neon lights, 8k...")
        aspect = st.selectbox("साइज चुनें:", ["Square (1:1)", "Portrait (9:16)", "Landscape (16:9)"])
        dim_map = {"Square (1:1)": (1024, 1024), "Portrait (9:16)": (720, 1280), "Landscape (16:9)": (1280, 720)}

        if st.button("✨ इमेज जनरेट करें", use_container_width=True, type="primary"):
            if not img_prompt:
                st.warning("कृपया प्रॉम्प्ट दर्ज करें।")
            else:
                with st.spinner("इमेज रेंडर हो रही है..."):
                    w, h = dim_map[aspect]
                    encoded_prompt = urllib.parse.quote(img_prompt)
                    image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={w}&height={h}&nologo=true&seed=42"
                    st.image(image_url, caption=img_prompt, use_container_width=True)
                    st.markdown(f"[📥 पूरी इमेज यहाँ से डाउनलोड करें]({image_url})")

    # ==========================================
    # TOOL 5: AI MUSIC & ANTHEM GENERATOR
    # ==========================================
    elif tool_mode == "🎵 AI Music & Anthem Generator":
        st.markdown("<h2 class='main-title'>🎵 AI Music & Anthem Studio</h2>", unsafe_allow_html=True)
        st.write("गीत, रैप, ग्रुप एंथम या किसी भी अवसर के लिए पूरा म्यूजिकल ट्रैक तैयार करें।")

        song_topic = st.text_input("गीत का विषय:", placeholder="उदा. दोस्तों का कॉलेज एंथम, एनर्जेटिक रैप, मोटिवेशनल ट्रैक...")
        genre = st.selectbox("म्यूजिक स्टाइल:", ["Desi Hip-Hop / Rap", "Bollywood Romantic", "High-Energy Anthem", "Acoustic Lo-Fi"])

        if st.button("🎼 गाना और कम्पोजिशन तैयार करें", use_container_width=True, type="primary"):
            if not song_topic:
                st.warning("कृपया गाने का विषय लिखें।")
            else:
                with st.spinner("लिरिक्स और वोकल्स तैयार हो रहे हैं..."):
                    prompt = f"""
                    Compose an original song/anthem for: '{song_topic}'
                    Genre: {genre}
                    Language: {target_lang}
                    
                    Include:
                    1. Track Title & BPM
                    2. Instrument Setup
                    3. [Intro], [Verse 1], [Chorus/Hook], [Verse 2], [Outro]
                    4. AI Music generator prompt tag
                    """
                    music_res = call_ai("You are a professional music producer and lyricist.", prompt)
                    if music_res:
                        st.markdown(music_res)

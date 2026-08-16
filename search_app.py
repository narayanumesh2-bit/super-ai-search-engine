import streamlit as st
import streamlit.components.v1 as components
from groq import Groq
import json
import re
import urllib.parse

# 1. Page Configuration
st.set_page_config(
    page_title="Super AI Multi-Tool Studio",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Sleek Theme & Handwritten Look
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
    .clip-card {
        background: #ffffff;
        border-radius: 10px;
        border-left: 5px solid #2563eb;
        padding: 15px;
        margin-bottom: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)

# 2. State Management
if "user_authenticated" not in st.session_state:
    st.session_state.user_authenticated = False
if "user_info" not in st.session_state:
    st.session_state.user_info = {}
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 3. Firebase Auth Component
FIREBASE_CONFIG = {
    "apiKey": "AIzaSyDz0N-bxSTYDAk0ygQNjbRX-a0shIl8Pw8",
    "authDomain": "super-ai-search-engine.firebaseapp.com",
    "projectId": "super-ai-search-engine",
    "storageBucket": "super-ai-search-engine.firebasestorage.app",
    "messagingSenderId": "703150781255",
    "appId": "1:703150781255:web:22866e05bee00ec8c5d262"
}

def render_firebase_auth():
    auth_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <script src="https://www.gstatic.com/firebasejs/9.23.0/firebase-app-compat.js"></script>
      <script src="https://www.gstatic.com/firebasejs/9.23.0/firebase-auth-compat.js"></script>
      <style>
        body {{
            font-family: 'Segoe UI', sans-serif;
            background: transparent;
            margin: 0;
            display: flex;
            justify-content: center;
        }}
        .card {{
            background: #ffffff;
            border-radius: 12px;
            padding: 24px;
            max-width: 420px;
            width: 100%;
            box-shadow: 0 4px 14px rgba(0,0,0,0.1);
            text-align: center;
            border: 1px solid #e2e8f0;
        }}
        .btn-google {{
            background: #ffffff;
            color: #374151;
            border: 1px solid #d1d5db;
            padding: 12px 18px;
            border-radius: 8px;
            width: 100%;
            font-size: 15px;
            font-weight: 600;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
        }}
        .divider {{
            display: flex;
            align-items: center;
            margin: 18px 0;
            color: #94a3b8;
            font-size: 13px;
        }}
        .divider::before, .divider::after {{
            content: '';
            flex: 1;
            border-bottom: 1px solid #e2e8f0;
        }}
        input[type="tel"], input[type="text"] {{
            width: 100%;
            padding: 10px;
            border: 1px solid #cbd5e1;
            border-radius: 6px;
            margin-bottom: 10px;
            box-sizing: border-box;
        }}
        .btn-phone {{
            background: #2563eb;
            color: white;
            border: none;
            padding: 10px;
            border-radius: 6px;
            width: 100%;
            font-weight: 600;
            cursor: pointer;
        }}
        .status {{ margin-top: 10px; font-size: 13px; color: #059669; }}
        .error {{ color: #dc2626; }}
      </style>
    </head>
    <body>
      <div class="card">
        <h2 style="margin-top:0; color:#1e293b;">Super AI Login</h2>
        <p style="color:#64748b; font-size:14px;">जारी रखने के लिए लॉगिन करें</p>
        
        <button class="btn-google" onclick="loginWithGoogle()">
          <svg width="18" height="18" viewBox="0 0 24 24"><path fill="#EA4335" d="M12 5c1.6 0 3 .6 4.1 1.6l3.1-3.1C17.3 1.7 14.8 1 12 1 7.4 1 3.5 3.6 1.6 7.4l3.7 2.9C6.2 7.1 8.9 5 12 5z"/><path fill="#4285F4" d="M23.5 12.3c0-.8-.1-1.6-.2-2.3H12v4.6h6.5c-.3 1.5-1.1 2.8-2.4 3.7l3.7 2.9c2.2-2 3.7-5 3.7-8.9z"/><path fill="#FBBC05" d="M5.3 14.7c-.2-.7-.4-1.5-.4-2.3s.2-1.6.4-2.3L1.6 7.2C.6 9.2 0 11.5 0 14s.6 4.8 1.6 6.8l3.7-2.9z"/><path fill="#34A853" d="M12 23c3.2 0 6-1.1 8-3l-3.7-2.9c-1.1.7-2.5 1.2-4.3 1.2-3.1 0-5.8-2.1-6.7-5.3L1.6 16c1.9 3.8 5.8 6.4 10.4 6.4z"/></svg>
          Google से Sign In करें
        </button>

        <div class="divider">या Phone OTP</div>

        <div id="recaptcha-container"></div>
        <input type="tel" id="phone-number" placeholder="+91 9876543210" />
        <button class="btn-phone" id="send-otp-btn" onclick="sendOTP()">Send OTP</button>

        <div id="otp-section" style="display: none; margin-top: 10px;">
            <input type="text" id="otp-code" placeholder="6 Digit OTP" />
            <button class="btn-phone" onclick="verifyOTP()">Verify OTP</button>
        </div>
        <div id="status-msg" class="status"></div>
      </div>

      <script>
        const firebaseConfig = {json.dumps(FIREBASE_CONFIG)};
        if (!firebase.apps.length) {{ firebase.initializeApp(firebaseConfig); }}
        const auth = firebase.auth();

        function setStatus(msg, isError=false) {{
            const el = document.getElementById('status-msg');
            el.innerText = msg;
            el.className = isError ? 'status error' : 'status';
        }}

        function loginWithGoogle() {{
            const provider = new firebase.auth.GoogleAuthProvider();
            auth.signInWithPopup(provider).then((result) => {{
                setStatus("लॉगिन सफल!");
            }}).catch((e) => setStatus(e.message, true));
        }}

        window.recaptchaVerifier = new firebase.auth.RecaptchaVerifier('recaptcha-container', {{ 'size': 'invisible' }});
        let confirmationObj = null;

        function sendOTP() {{
            const phone = document.getElementById('phone-number').value.trim();
            if (!phone.startsWith('+')) {{
                setStatus("Country code (+91) लगाएँ", true);
                return;
            }}
            auth.signInWithPhoneNumber(phone, window.recaptchaVerifier).then((res) => {{
                confirmationObj = res;
                document.getElementById('otp-section').style.display = 'block';
                document.getElementById('send-otp-btn').style.display = 'none';
                setStatus("OTP भेजा गया!");
            }}).catch((e) => setStatus(e.message, true));
        }}

        function verifyOTP() {{
            const code = document.getElementById('otp-code').value.trim();
            if(confirmationObj) {{
                confirmationObj.confirm(code).then(() => {{
                    setStatus("सत्यापित हुआ!");
                }}).catch((e) => setStatus("गलत OTP", true));
            }}
        }}
      </script>
    </body>
    </html>
    """
    components.html(auth_html, height=440)

# Helper: Mermaid Diagram Renderer
def render_mermaid(diagram_code):
    html_code = f"""
    <script type="module">
      import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
      mermaid.initialize({{ startOnLoad: true, theme: 'neutral' }});
    </script>
    <div class="mermaid" style="background:#ffffff; padding:15px; border-radius:8px; border:1px solid #cbd5e1;">
    {diagram_code}
    </div>
    """
    components.html(html_code, height=350, scrolling=True)

# 4. Authentication Barrier
if not st.session_state.user_authenticated:
    st.markdown("<h1 class='main-title'>⚡ Super AI Engine</h1>", unsafe_allow_html=True)
    st.info("सुरक्षित लॉगिन करें या नीचे तुरंत Guest रूप में जारी रखें:")
    
    render_firebase_auth()
    
    with st.expander("⚡ तुरंत टेस्ट लॉगिन (Guest Mode)"):
        guest_name = st.text_input("अपना नाम", "Prince Raj")
        if st.button("Guest रूप में ऐप खोलें 🚀", use_container_width=True):
            st.session_state.user_authenticated = True
            st.session_state.user_info = {"name": guest_name, "email": "user@superai.com"}
            st.rerun()

else:
    # 5. Sidebar Navigation & Global Controls
    with st.sidebar:
        st.markdown(f"### 👤 {st.session_state.user_info.get('name', 'User')}")
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.user_authenticated = False
            st.session_state.user_info = {}
            st.rerun()
            
        st.divider()
        st.markdown("#### ⚙️ सेटिंग्स")
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

    # Helper function for Groq API call
    def call_ai(system_prompt, user_prompt, model="llama-3.3-70b-versatile"):
        if not groq_api_key:
            st.warning("⚠️ कृपया बाईं तरफ साइडबार में अपनी Groq API Key डालें।")
            return None
        try:
            client = Groq(api_key=groq_api_key)
            full_system = f"{system_prompt}\nTarget Language: {target_lang}. Always respond directly in the selected language unless specified otherwise."
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
        st.caption(f"भाषा: {target_lang} | किसी भी विषय पर सटीक व गहरा विश्लेषण प्राप्त करें।")

        query = st.chat_input("अपना सवाल यहाँ पूछें...")
        
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])
                
        if query:
            st.session_state.chat_history.append({"role": "user", "content": query})
            with st.chat_message("user"):
                st.write(query)
            
            with st.chat_message("assistant"):
                with st.spinner("सोच रहा हूँ..."):
                    reply = call_ai(
                        "You are an advanced super-intelligent AI search engine capable of deep research, step-by-step reasoning, coding, science, mathematics, and regional queries.",
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
        st.write("2-3 घंटे के वीडियो या YouTube लिंक से सीधे **15–20 सेकंड के 20 वायरल क्लिप्स, टाइमस्टैम्प्स, कैची हुक्स और वॉयसओवर स्क्रिप्ट** तैयार करें।")

        input_choice = st.radio("इनपुट का माध्यम चुनें:", ["🔗 YouTube Video Link", "📁 Video File Upload"], horizontal=True)
        
        video_context = ""
        topic_hint = ""

        if input_choice == "🔗 YouTube Video Link":
            yt_url = st.text_input("YouTube वीडियो का पूरा लिंक यहाँ पेस्ट करें:", placeholder="https://www.youtube.com/watch?v=...")
            topic_hint = st.text_input("वीडियो का मुख्य विषय / टॉपिक (वैकल्पिक):", placeholder="उदा. BCA गाइड, मोटिवेशन, पॉडकास्ट, साइंस...")
            if yt_url:
                st.video(yt_url)
                video_context = f"YouTube URL: {yt_url}\nTopic Focus: {topic_hint}"
        else:
            uploaded_vid = st.file_uploader("वीडियो फ़ाइल अपलोड करें (.mp4, .mkv, .mov)", type=["mp4", "mkv", "mov"])
            topic_hint = st.text_input("अपलोड की गई वीडियो का मुख्य विषय:", placeholder="वीडियो किस बारे में है?")
            if uploaded_vid:
                st.success(f"फ़ाइल '{uploaded_vid.name}' चुनी गई।")
                video_context = f"Uploaded File: {uploaded_vid.name}\nTopic: {topic_hint}"

        if st.button("🚀 20 वायरल शॉर्ट्स क्लिप्स बनाएँ (Generate 20 Shorts)", use_container_width=True):
            if not video_context:
                st.warning("कृपया YouTube लिंक या वीडियो का विवरण प्रदान करें।")
            else:
                with st.spinner("पूरे वीडियो का विश्लेषण और 20 वायरल शॉर्ट्स तैयार किए जा रहे हैं..."):
                    prompt = f"""
                    Analyze this video and generate exactly 20 high-retention Viral Shorts / Reels concepts (each strictly 15-20 seconds long).
                    Details: {video_context}
                    
                    For EACH of the 20 parts, provide in structured markdown:
                    - **Part Number & Viral Title**
                    - **Estimated Timestamp Window** (e.g. 04:15 - 04:35)
                    - **Psychological Hook** (First 3 seconds line)
                    - **Full Voiceover / Narration Script** (15 to 20 seconds, exact spoken words in {target_lang})
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
        st.write("किसी भी टॉपिक पर **पेन से लिखे नोट्स (Handwritten Sheet)** और **विजुअल फ्लोचार्ट / माइंडमैप** प्राप्त करें।")

        note_topic = st.text_input("जिस टॉपिक पर नोट्स चाहिए लिखें:", placeholder="उदा. Data Structures, Photosynthesis, BCA Syllabus, संविधान के मौलिक अधिकार...")
        detail_level = st.select_slider("नोट्स का विस्तार:", options=["संक्षिप्त (Quick Points)", "विस्तृत (Full Exam Notes)", "माइंड-मैप व डायग्राम केंद्रित"])

        if st.button("🖋️ हैंड-रिटन नोट्स और डायग्राम बनाएँ", use_container_width=True):
            if not note_topic:
                st.warning("कृपया टॉपिक का नाम लिखें।")
            else:
                with st.spinner("नोट्स और डायग्राम तैयार हो रहे हैं..."):
                    # 1. Notes generation
                    prompt = f"""
                    Create neat, beautiful handwritten-style study notes for students on: '{note_topic}'.
                    Level: {detail_level}
                    Language: {target_lang}
                    Format:
                    - Heading with Underline style
                    - Bullet points with stars or dashes
                    - Key definitions in highlighted boxes
                    - 3 Exam Tips / Short Formulae
                    """
                    notes_content = call_ai("You are a topper student creating clean pen-written revision notes.", prompt)

                    # 2. Mermaid Diagram code generation
                    diagram_prompt = f"""
                    Generate a Mermaid.js flowchart or mindmap diagram representing '{note_topic}'.
                    Return ONLY valid Mermaid code starting with `graph TD` or `mindmap`.
                    Do NOT wrap in backticks or markdown, just the raw mermaid code text.
                    """
                    mermaid_code = call_ai("You are a diagram and workflow specialist. Output only valid raw mermaid code.", diagram_prompt)

                    # Display Ruled Notebook Page
                    if notes_content:
                        st.markdown("### 📋 नोटबुक शीट (Handwritten Look)")
                        st.markdown(f"<div class='notebook-sheet'>{notes_content.replace(chr(10), '<br>')}</div>", unsafe_allow_html=True)

                    # Display Diagram
                    if mermaid_code:
                        clean_mermaid = re.sub(r"```mermaid|```", "", mermaid_code).strip()
                        st.markdown("### 📊 विजुअल फ्लोचार्ट / माइंड-मैप")
                        render_mermaid(clean_mermaid)

    # ==========================================
    # TOOL 4: AI IMAGE GENERATOR
    # ==========================================
    elif tool_mode == "🎨 AI Image Generator":
        st.markdown("<h2 class='main-title'>🎨 High-Speed AI Image Generator</h2>", unsafe_allow_html=True)
        st.write("अपनी कल्पना को शब्दों में लिखें और तुरंत HD इमेज जनरेट करें।")

        img_prompt = st.text_area("इमेज का विवरण (Prompt):", placeholder="उदा. A futuristic Indian college student coding in a cyber room with neon lights, 8k render, hyper-realistic...")
        aspect = st.selectbox("साइज / अनुपात (Aspect Ratio):", ["Square (1:1)", "Portrait / Phone Wallpaper (9:16)", "Landscape / YouTube Thumbnail (16:9)"])

        dim_map = {
            "Square (1:1)": (1024, 1024),
            "Portrait / Phone Wallpaper (9:16)": (720, 1280),
            "Landscape / YouTube Thumbnail (16:9)": (1280, 720)
        }

        if st.button("✨ इमेज जनरेट करें", use_container_width=True):
            if not img_prompt:
                st.warning("कृपया इमेज का विवरण दर्ज करें।")
            else:
                with st.spinner("AI इमेज तैयार कर रहा है..."):
                    w, h = dim_map[aspect]
                    encoded_prompt = urllib.parse.quote(img_prompt)
                    image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={w}&height={h}&nologo=true&seed=42"
                    
                    st.image(image_url, caption=f"Generated: {img_prompt}", use_container_width=True)
                    st.markdown(f"[📥 पूरी इमेज यहाँ से डाउनलोड करें]({image_url})")

    # ==========================================
    # TOOL 5: AI MUSIC & ANTHEM GENERATOR
    # ==========================================
    elif tool_mode == "🎵 AI Music & Anthem Generator":
        st.markdown("<h2 class='main-title'>🎵 AI Music & Anthem Studio</h2>", unsafe_allow_html=True)
        st.write("गीत, रैप, ग्रुप एंथम, जन्मदिन या किसी भी अवसर के लिए म्यूजिकल ट्रैक तैयार करें।")

        song_topic = st.text_input("गीत का विषय / अवसर:", placeholder="उदा. कॉलेज दोस्तों का ग्रुप एंथम, बिहार की मिट्टी का रैप, मोटिवेशनल सॉन्ग...")
        genre = st.selectbox("म्यूजिक स्टाइल / जॉनर:", ["Desi Hip-Hop / Rap", "Bollywood Melodic Romantic", "High-Energy Anthem", "Acoustic Lo-Fi", "Folk Fusion"])

        if st.button("🎼 गाना और म्यूजिक कम्पोजिशन बनाएँ", use_container_width=True):
            if not song_topic:
                st.warning("कृपया गाने का विषय दर्ज करें।")
            else:
                with st.spinner("म्यूजिक, लिरिक्स और बीट तैयार हो रही है..."):
                    prompt = f"""
                    Compose a complete original song/anthem for: '{song_topic}'
                    Genre: {genre}
                    Language: {target_lang}
                    
                    Include:
                    1. **Track Title & BPM (Tempo)**
                    2. **Vibe & Instrument Guide** (Guitar, 808 Bass, Flute, Dholak etc.)
                    3. **[Intro]** (Beat buildup)
                    4. **[Verse 1]** (Rhyming lyrics)
                    5. **[Chorus / Hook]** (Catchy repeating punchline)
                    6. **[Verse 2]**
                    7. **[Drop / Bridge]**
                    8. **[Outro]**
                    9. **AI Music Prompt Tag** (formatted for Suno/Udio text-to-music engines)
                    """
                    music_res = call_ai("You are a professional music producer, lyricist and sound engineer.", prompt)
                    if music_res:
                        st.markdown(music_res)

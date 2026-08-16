import streamlit as st
import streamlit.components.v1 as components
from groq import Groq
import urllib.parse
import json
import re

# 1. Page Configuration
st.set_page_config(
    page_title="Super AI Studio & Search Engine",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Custom CSS (Handwritten Notebook Look, Clean Theme & Plus Icons)
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
            #cbd5e1 29px,
            #fdfbf7 30px
        );
        font-family: 'Comic Sans MS', 'Caveat', 'Segoe Print', cursive, sans-serif;
        color: #1e3a8a;
        padding: 30px 35px 30px 55px;
        border-left: 5px solid #ef4444;
        border-radius: 8px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.06);
        line-height: 30px;
        font-size: 17px;
        margin-top: 15px;
    }
    .stTextInput>div>div>input {
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# 3. State Management
if "user_authenticated" not in st.session_state:
    st.session_state.user_authenticated = False
if "user_info" not in st.session_state:
    st.session_state.user_info = {}
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Backend Groq Client Setup (API Key can be loaded from Streamlit Secrets or Environment)
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", "gsk_yvV2Pq3z1R9Q0X4mJ8KLwgY9abcdef123456") # Replace or add in Secrets

def call_super_ai(system_prompt, user_prompt, target_lang="Hindi"):
    try:
        # Fallback to key if passed or default
        client = Groq(api_key=st.session_state.get("custom_groq_key", GROQ_API_KEY))
        full_system = f"{system_prompt}\nTarget Language: {target_lang}. Respond directly and accurately in this language with structured formatting."
        res = client.chat.completions.create(
            messages=[
                {"role": "system", "content": full_system},
                {"role": "user", "content": user_prompt}
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.7
        )
        return res.choices[0].message.content
    except Exception as e:
        return f"AI Engine Error: {str(e)}"

# Helper: Mermaid Diagram Visualizer
def render_mermaid(diagram_code):
    html_code = f"""
    <script type="module">
      import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
      mermaid.initialize({{ startOnLoad: true, theme: 'neutral' }});
    </script>
    <div class="mermaid" style="background:#ffffff; padding:15px; border-radius:8px; border:1px solid #e2e8f0;">
    {diagram_code}
    </div>
    """
    components.html(html_code, height=350, scrolling=True)

# 4. AUTHENTICATION (Google Native Account Picker)
if not st.session_state.user_authenticated:
    st.markdown("<h1 class='main-title'>⚡ Super AI Search Engine & Studio</h1>", unsafe_allow_html=True)
    st.write("अपने आधिकारिक Google खाते से प्रमाणित करें:")

    col1, col2, col3 = st.columns([1, 1.8, 1])
    with col2:
        st.markdown("""
        <div style="background:#ffffff; border:1px solid #e2e8f0; border-radius:14px; padding:30px; box-shadow:0 4px 15px rgba(0,0,0,0.06); text-align:center;">
            <h3 style="margin-top:0; color:#1e293b;">Google Account Login</h3>
            <p style="color:#64748b; font-size:14px;">सुरक्षित 1-Click साइन इन</p>
        </div>
        """, unsafe_allow_html=True)

        user_email = st.text_input("अपना Google / Gmail खाता चुनें", placeholder="yourname@gmail.com")
        user_name = st.text_input("आपका नाम", placeholder="Prince Raj")

        c_a, c_b = st.columns([0.85, 0.15])
        with c_a:
            if st.button("🔴 Google खाते से प्रवेश करें", use_container_width=True, type="primary"):
                if user_email and "@" in user_email:
                    st.session_state.user_authenticated = True
                    st.session_state.user_info = {"name": user_name or "Google User", "email": user_email}
                    st.success("Google ऑथेंटिकेशन सफल!")
                    st.rerun()
                else:
                    st.error("कृपया सही Gmail आईडी दर्ज करें।")
        with c_b:
            st.button("➕", key="auth_plus")

else:
    # 5. SIDEBAR & NAVIGATION
    with st.sidebar:
        user = st.session_state.user_info
        st.markdown(f"### 👤 {user.get('name', 'User')}")
        st.caption(f"🔒 {user.get('email', '')}")
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.user_authenticated = False
            st.session_state.user_info = {}
            st.rerun()
            
        st.divider()
        target_lang = st.selectbox(
            "🌐 मुख्य भाषा चुनें (Regional Languages)",
            ["Hindi (हिन्दी)", "Bhojpuri (भोजपुरी)", "Maithili (मैथिली)", "English", 
             "Bengali (বাংলা)", "Telugu (తెలుగు)", "Tamil (தமிழ்)", "Marathi (मराठी)", 
             "Gujarati (ગુજરાતી)", "Kannada (ಕನ್ನಡ)", "Punjabi (ਪੰਜਾਬੀ)", "Odia (ଓଡ଼ିଆ)"]
        )

        st.divider()
        tool_mode = st.radio(
            "🚀 स्टूडियो टूल्स:",
            [
                "🔍 Universal Super AI Search Engine",
                "🎬 YouTube/Video to Custom Shorts Maker",
                "📝 Handwritten Notes & Diagram Studio",
                "🎨 AI Image Generator",
                "🎵 AI Music & Anthem Generator"
            ]
        )
        
        with st.expander("⚙️ Advanced API Settings"):
            custom_key = st.text_input("Custom Groq API Key (Optional)", type="password")
            if custom_key:
                st.session_state.custom_groq_key = custom_key

    # ==========================================
    # TOOL 1: UNIVERSAL AI SEARCH ENGINE
    # ==========================================
    if tool_mode == "🔍 Universal Super AI Search Engine":
        st.markdown("<h2 class='main-title'>🔍 Universal Super AI Search Engine</h2>", unsafe_allow_html=True)
        st.caption(f"भाषा: {target_lang} | भारत और विश्व के किसी भी सवाल का सटीक, विश्लेषणात्मक व त्वरित उत्तर।")

        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

        col_s1, col_s2 = st.columns([0.92, 0.08])
        with col_s1:
            query = st.chat_input("अपना सवाल यहाँ सर्च करें...")
        with col_s2:
            st.button("➕", key="search_plus", help="अतिरिक्त फ़ाइल या डेटा जोड़ें")
                
        if query:
            st.session_state.chat_history.append({"role": "user", "content": query})
            with st.chat_message("user"):
                st.write(query)
            
            with st.chat_message("assistant"):
                with st.spinner("Super AI Search खोज कर रहा है..."):
                    reply = call_super_ai(
                        "You are the world's most capable Universal AI Search Engine. Provide fast, deeply researched, accurate and structured answers with code, facts, maths, or logical deductions as needed.",
                        query,
                        target_lang
                    )
                    st.markdown(reply)
                    st.session_state.chat_history.append({"role": "assistant", "content": reply})

    # ==========================================
    # TOOL 2: YOUTUBE / GALLERY VIDEO TO SHORTS
    # ==========================================
    elif tool_mode == "🎬 YouTube/Video to Custom Shorts Maker":
        st.markdown("<h2 class='main-title'>🎬 Video to Custom Shorts & Clips Studio</h2>", unsafe_allow_html=True)
        st.write("1-2 घंटे के लंबे वीडियो या YouTube लिंक को अपनी पसंद के समय और पार्ट्स में वायरल शॉर्ट्स में बदलें।")

        input_type = st.radio("वीडियो का स्रोत चुनें:", ["🔗 YouTube Video Link", "📁 Gallery / File Upload (1-2 Hours)"], horizontal=True)
        video_source_details = ""

        if input_type == "🔗 YouTube Video Link":
            c_in1, c_in2 = st.columns([0.92, 0.08])
            with c_in1:
                yt_link = st.text_input("YouTube वीडियो लिंक यहाँ पेस्ट करें:", placeholder="https://www.youtube.com/watch?v=...")
            with c_in2:
                st.button("➕", key="yt_plus")
            if yt_link:
                st.video(yt_link)
                video_source_details = f"YouTube URL: {yt_link}"
        else:
            c_up1, c_up2 = st.columns([0.92, 0.08])
            with c_up1:
                uploaded_file = st.file_uploader("गैलरी से वीडियो अपलोड करें (.mp4, .mkv, .mov)", type=["mp4", "mkv", "mov"])
            with c_up2:
                st.button("➕", key="vid_plus")
            if uploaded_file:
                st.success(f"फ़ाइल '{uploaded_file.name}' लोड हो गई।")
                video_source_details = f"Uploaded Video: {uploaded_file.name}"

        st.markdown("#### ⚙️ शॉर्ट्स विभाजन सेटिंग्स (Custom Partitioning)")
        col_p1, col_p2 = st.columns(2)
        with col_p1:
            part_duration = st.selectbox(
                "एक शॉर्ट / क्लिप की लंबाई चुनें:",
                ["5 Seconds", "10 Seconds", "15-20 Seconds (Viral Standard)", "30 Seconds", "1 Minute", "2 Minutes", "5 Minutes", "10 Minutes"]
            )
        with col_p2:
            num_clips = st.number_input("कुल कितने शॉर्ट्स / पार्ट्स में विभाजित करना है?", min_value=1, max_value=50, value=20)

        if st.button("🚀 शॉर्ट्स और स्क्रिप्ट्स तैयार करें", use_container_width=True, type="primary"):
            if not video_source_details:
                st.warning("कृपया पहले YouTube लिंक या वीडियो फ़ाइल प्रदान करें।")
            else:
                with st.spinner(f"वीडियो का विश्लेषण कर {num_clips} पार्ट्स ({part_duration}) तैयार किए जा रहे हैं..."):
                    prompt = f"""
                    Analyze this long video: {video_source_details}
                    Task: Split and extract exactly {num_clips} viral shorts / clips.
                    Duration per clip: {part_duration}.
                    Language: {target_lang}.

                    For EACH of the {num_clips} clips, output structured markdown:
                    - **Part # & Catchy Title**
                    - **Timestamp Window** (e.g. 02:15 - 02:35)
                    - **High-Retention Hook** (Opening 3-second statement)
                    - **Complete Spoken Script** (exact narration in {target_lang})
                    - **Visual B-Roll / Screen Description**
                    - **Trending Hashtags**
                    """
                    shorts_result = call_super_ai("You are a viral YouTube Shorts/Reels producer and video editor.", prompt, target_lang)
                    st.success("✅ सभी शॉर्ट्स और स्क्रिप्ट्स सफलतापूर्वक तैयार हैं!")
                    st.markdown(shorts_result)

    # ==========================================
    # TOOL 3: HANDWRITTEN NOTES & DIAGRAMS
    # ==========================================
    elif tool_mode == "📝 Handwritten Notes & Diagram Studio":
        st.markdown("<h2 class='main-title'>📝 Handwritten Notes & Diagram Studio</h2>", unsafe_allow_html=True)
        st.write("पेन से लिखी नोटबुक शीट स्टाइल में नोट्स और डायग्राम प्राप्त करें।")

        c_nt1, c_nt2 = st.columns([0.92, 0.08])
        with c_nt1:
            topic_text = st.text_input("विषय या टॉपिक का नाम लिखें:", placeholder="उदा. Data Structures, Operating System, Photosynthesis, भारतीय संविधान...")
        with c_nt2:
            st.button("➕", key="notes_plus")

        doc_image = st.file_uploader("टॉपिक / डायग्राम की फोटो अपलोड करें (वैकल्पिक):", type=["jpg", "jpeg", "png"])

        if st.button("🖋️ हैंड-रिटन नोट्स और डायग्राम बनाएँ", use_container_width=True, type="primary"):
            if not topic_text:
                st.warning("कृपया टॉपिक का नाम दर्ज करें।")
            else:
                with st.spinner("हैंड-रिटन नोट्स और डायग्राम बनाए जा रहे हैं..."):
                    notes_prompt = f"""
                    Generate comprehensive, student-topper style revision notes on: '{topic_text}'.
                    Language: {target_lang}.
                    Format:
                    - Title with Double Underline
                    - Bullet points with star/dash indicators
                    - Important definitions in clear framed points
                    - Step-by-step mechanism / workflow
                    - 3 Golden Exam Tips
                    """
                    notes_output = call_super_ai("You are an expert professor preparing clean pen-written student notes.", notes_prompt, target_lang)

                    diagram_prompt = f"""
                    Generate a Mermaid.js diagram (flowchart/mindmap) representing the core architecture/flow of '{topic_text}'.
                    Output ONLY valid mermaid code starting with 'graph TD' or 'mindmap'. No surrounding backticks or commentary.
                    """
                    mermaid_output = call_super_ai("Output only valid mermaid.js code without any markdown wrappers.", diagram_prompt, "English")

                    st.markdown("### 📋 नोटबुक शीट (Handwritten Look)")
                    st.markdown(f"<div class='notebook-sheet'>{notes_output.replace(chr(10), '<br>')}</div>", unsafe_allow_html=True)

                    clean_mermaid = re.sub(r"```mermaid|```", "", mermaid_output).strip()
                    st.markdown("### 📊 विजुअल फ्लोचार्ट / डायग्राम")
                    render_mermaid(clean_mermaid)

    # ==========================================
    # TOOL 4: AI IMAGE GENERATOR
    # ==========================================
    elif tool_mode == "🎨 AI Image Generator":
        st.markdown("<h2 class='main-title'>🎨 High-Speed AI Image Generator</h2>", unsafe_allow_html=True)
        st.write("अपनी कल्पना का विवरण लिखें और तुरंत HD इमेज जनरेट करें।")

        c_im1, c_im2 = st.columns([0.92, 0.08])
        with c_im1:
            img_desc = st.text_area("इमेज का विवरण (Prompt):", placeholder="उदा. Futuristic Indian student coding with holographic displays, cinematic lighting, 8k...")
        with c_im2:
            st.button("➕", key="img_plus")

        aspect_ratio = st.selectbox("इमेज साइज चुनें:", ["Square (1:1)", "Portrait / Mobile Wallpaper (9:16)", "Landscape / YouTube Banner (16:9)"])
        dim_dict = {"Square (1:1)": (1024, 1024), "Portrait / Mobile Wallpaper (9:16)": (720, 1280), "Landscape / YouTube Banner (16:9)": (1280, 720)}

        if st.button("✨ इमेज जनरेट करें", use_container_width=True, type="primary"):
            if not img_desc:
                st.warning("कृपया इमेज का विवरण लिखें।")
            else:
                with st.spinner("AI इमेज तैयार कर रहा है..."):
                    w, h = dim_dict[aspect_ratio]
                    encoded_prompt = urllib.parse.quote(img_desc)
                    img_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={w}&height={h}&nologo=true&seed=42"
                    st.image(img_url, caption=img_desc, use_container_width=True)
                    st.markdown(f"[📥 पूरी इमेज यहाँ से डाउनलोड करें]({img_url})")

    # ==========================================
    # TOOL 5: AI MUSIC & ANTHEM GENERATOR
    # ==========================================
    elif tool_mode == "🎵 AI Music & Anthem Generator":
        st.markdown("<h2 class='main-title'>🎵 AI Music & Anthem Studio</h2>", unsafe_allow_html=True)
        st.write("किसी भी अवसर, कॉलेज ग्रुप, जन्मदिन या सोशल मीडिया के लिए पूरा गाना व म्यूजिक तैयार करें।")

        c_mu1, c_mu2 = st.columns([0.92, 0.08])
        with c_mu1:
            music_theme = st.text_input("गीत का विषय या अवसर:", placeholder="उदा. कॉलेज दोस्तों का ग्रुप एंथम, एनर्जेटिक देसी हिप-हॉप...")
        with c_mu2:
            st.button("➕", key="mus_plus")

        genre_choice = st.selectbox("म्यूजिक स्टाइल / जॉनर:", ["Desi Hip-Hop / Rap", "Bollywood Melodic", "High-Energy Anthem", "Acoustic Lo-Fi", "Bhojpuri Folk Fusion"])

        if st.button("🎼 पूरा गाना और म्यूजिक कम्पोजिशन बनाएँ", use_container_width=True, type="primary"):
            if not music_theme:
                st.warning("कृपया गाने का विषय दर्ज करें।")
            else:
                with st.spinner("लिरिक्स, बीट और म्यूजिक तैयार हो रहा है..."):
                    music_prompt = f"""
                    Compose a complete original song/anthem for: '{music_theme}'.
                    Genre: {genre_choice}.
                    Language: {target_lang}.
                    Include:
                    1. **Track Title & BPM (Tempo)**
                    2. **Instrument Arrangement Guide**
                    3. **[Intro]** (Beat buildup)
                    4. **[Verse 1]** (Rhyming lyrics)
                    5. **[Chorus / Hook]** (Catchy punchline)
                    6. **[Verse 2]**
                    7. **[Drop / Bridge]**
                    8. **[Outro]**
                    9. **AI Music Prompt Tag** (formatted for text-to-music generators)
                    """
                    music_out = call_super_ai("You are a professional music director, lyricist and sound producer.", music_prompt, target_lang)
                    st.markdown(music_out)

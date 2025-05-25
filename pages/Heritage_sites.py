import streamlit as st
import pandas as pd
import folium
import snowflake.connector
from streamlit_folium import st_folium
from folium import IFrame
from folium.plugins import MarkerCluster
import os

# Page Config
st.set_page_config(page_title="The Chronicles of India: A Heritage Odyssey", layout="wide")

# Enhanced Glassmorphism CSS
st.markdown("""
    <style>
    /* Cinematic background with enhanced depth */
    .stApp {
        background: 
            radial-gradient(circle at 20% 80%, rgba(120, 119, 198, 0.3), transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(255, 119, 198, 0.15), transparent 50%),
            radial-gradient(circle at 40% 40%, rgba(120, 219, 226, 0.15), transparent 50%),
            linear-gradient(135deg, #0c0c0c 0%, #1a0f0f 25%, #2d1b1f 50%, #1a0f0f 75%, #0c0c0c 100%);
        background-size: 400% 400%, 400% 400%, 400% 400%, 400% 400%;
        animation: gradientShift 20s ease infinite;
        color: #f5f5f5;
        font-family: 'Crimson Text', serif;
        min-height: 100vh;
    }

    @keyframes gradientShift {
        0% { background-position: 0% 50%, 0% 50%, 0% 50%, 0% 50%; }
        50% { background-position: 100% 50%, 100% 50%, 100% 50%, 100% 50%; }
        100% { background-position: 0% 50%, 0% 50%, 0% 50%, 0% 50%; }
    }

    /* Cinematic title with enhanced glassmorphism */
    .chronicles-title {
        text-align: center;
        background: linear-gradient(45deg, #FFD700, #FFA500, #FF6347, #FFD700);
        background-size: 400% 400%;
        animation: goldShimmer 3s ease-in-out infinite;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 4rem;
        font-weight: bold;
        margin: 2rem 0;
        text-shadow: 0 0 30px rgba(255, 215, 0, 0.5);
        letter-spacing: 2px;
        position: relative;
        padding: 30px;
    }

    .chronicles-title::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px);
        border-radius: 25px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        z-index: -1;
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
    }

    @keyframes goldShimmer {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }

    /* Enhanced glassmorphism story chapter */
    .story-chapter {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(25px);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 25px;
        padding: 35px;
        margin: 35px 0;
        box-shadow: 
            0 12px 40px rgba(0, 0, 0, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.15),
            inset 0 -1px 0 rgba(255, 255, 255, 0.05);
        position: relative;
        overflow: hidden;
        transition: all 0.4s ease;
    }

    .story-chapter:hover {
        background: rgba(255, 255, 255, 0.12);
        border: 1px solid rgba(255, 255, 255, 0.18);
        transform: translateY(-5px);
        box-shadow: 
            0 20px 50px rgba(0, 0, 0, 0.5),
            inset 0 1px 0 rgba(255, 255, 255, 0.2);
    }

    .story-chapter::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, transparent, rgba(255, 215, 0, 0.8), transparent);
        animation: shimmer 3s linear infinite;
    }

    .story-chapter::after {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255, 255, 255, 0.03) 0%, transparent 70%);
        opacity: 0;
        transition: opacity 0.3s ease;
        pointer-events: none;
    }

    .story-chapter:hover::after {
        opacity: 1;
    }

    @keyframes shimmer {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }

    /* Enhanced narrator voice */
    .narrator-voice {
        font-size: 1.3rem;
        line-height: 1.8;
        color: #e8e8e8;
        text-align: justify;
        margin-bottom: 25px;
        position: relative;
        padding-left: 30px;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
    }

    .narrator-voice::before {
        content: '"';
        position: absolute;
        left: 0;
        top: -10px;
        font-size: 4rem;
        color: #FFD700;
        opacity: 0.6;
        text-shadow: 0 0 20px rgba(255, 215, 0, 0.5);
    }

    /* Enhanced chapter headers with glassmorphism */
    .chapter-title {
        color: #FFD700;
        font-size: 2.5rem;
        text-align: center;
        margin-bottom: 30px;
        font-weight: bold;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.7);
        position: relative;
        padding: 20px;
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    .chapter-title::after {
        content: '';
        position: absolute;
        bottom: -5px;
        left: 50%;
        transform: translateX(-50%);
        width: 100px;
        height: 3px;
        background: linear-gradient(90deg, transparent, #FFD700, transparent);
        border-radius: 2px;
    }

    /* Enhanced glassmorphism controls */
    .story-controls {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 30px;
        margin: 30px 0;
        border: 1px solid rgba(255, 255, 255, 0.12);
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        transition: all 0.3s ease;
    }

    .story-controls:hover {
        background: rgba(255, 255, 255, 0.12);
        border: 1px solid rgba(255, 255, 255, 0.18);
    }

    .story-controls h3 {
        color: #FFD700;
        text-align: center;
        margin-bottom: 25px;
        font-size: 1.8rem;
        text-shadow: 0 0 20px rgba(255, 215, 0, 0.3);
    }

    /* Enhanced ancient map with glassmorphism */
    .ancient-map {
        background: rgba(139, 69, 19, 0.08);
        backdrop-filter: blur(25px);
        border-radius: 25px;
        padding: 35px;
        margin: 35px 0;
        border: 1px solid rgba(255, 255, 255, 0.12);
        box-shadow: 
            0 12px 40px rgba(0, 0, 0, 0.4),
            0 0 80px rgba(255, 215, 0, 0.1),
            inset 0 1px 0 rgba(255, 255, 255, 0.15);
        position: relative;
        transition: all 0.4s ease;
    }

    .ancient-map:hover {
        background: rgba(139, 69, 19, 0.12);
        box-shadow: 
            0 20px 60px rgba(0, 0, 0, 0.5),
            0 0 100px rgba(255, 215, 0, 0.15),
            inset 0 1px 0 rgba(255, 255, 255, 0.2);
    }

    .ancient-map::before {
        content: '🗺️';
        position: absolute;
        top: -20px;
        left: 50%;
        transform: translateX(-50%);
        font-size: 2.5rem;
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        padding: 15px;
        border-radius: 50%;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }

    /* Enhanced ancient tome with glassmorphism */
    .ancient-tome {
        background: rgba(139, 69, 19, 0.08);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 30px;
        margin: 30px 0;
        border: 1px solid rgba(255, 255, 255, 0.12);
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        transition: all 0.3s ease;
    }

    .ancient-tome:hover {
        background: rgba(139, 69, 19, 0.12);
        border: 1px solid rgba(255, 255, 255, 0.18);
    }

    /* Enhanced selectbox with glassmorphism */
    div.stSelectbox label {
        color: #FFD700 !important;
        font-weight: bold;
        font-size: 1.1rem;
        text-shadow: 0 0 10px rgba(255, 215, 0, 0.3);
    }

    .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.08) !important;
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 15px !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }

    .stSelectbox > div > div:hover {
        background: rgba(255, 255, 255, 0.12) !important;
        border: 1px solid rgba(255, 255, 255, 0.18) !important;
    }

    /* Enhanced download button with glassmorphism */
    .stDownloadButton button {
        background: rgba(139, 69, 19, 0.3) !important;
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 215, 0, 0.4) !important;
        border-radius: 20px !important;
        color: #FFD700 !important;
        font-weight: bold;
        padding: 15px 30px !important;
        transition: all 0.4s ease;
        box-shadow: 
            0 8px 25px rgba(0, 0, 0, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        position: relative;
        overflow: hidden;
    }

    .stDownloadButton button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transition: left 0.5s ease;
    }

    .stDownloadButton button:hover {
        background: rgba(139, 69, 19, 0.5) !important;
        border: 1px solid rgba(255, 215, 0, 0.6) !important;
        transform: translateY(-3px);
        box-shadow: 
            0 12px 35px rgba(0, 0, 0, 0.5),
            0 0 40px rgba(255, 215, 0, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.2);
    }

    .stDownloadButton button:hover::before {
        left: 100%;
    }

    /* Enhanced dataframe with glassmorphism */
    .dataframe {
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(15px);
        border-radius: 15px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }

    /* Enhanced epilogue with glassmorphism */
    .epilogue {
        background: rgba(255, 215, 0, 0.08);
        backdrop-filter: blur(30px);
        border-radius: 30px;
        padding: 50px;
        margin: 50px 0;
        border: 1px solid rgba(255, 255, 255, 0.15);
        text-align: center;
        box-shadow: 
            0 20px 60px rgba(0, 0, 0, 0.4),
            0 0 100px rgba(255, 215, 0, 0.1),
            inset 0 1px 0 rgba(255, 255, 255, 0.2);
        position: relative;
        overflow: hidden;
        transition: all 0.4s ease;
    }

    .epilogue::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 100%;
        background: radial-gradient(circle at center, rgba(255, 215, 0, 0.05) 0%, transparent 70%);
        pointer-events: none;
    }

    .epilogue:hover {
        background: rgba(255, 215, 0, 0.12);
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 
            0 30px 80px rgba(0, 0, 0, 0.5),
            0 0 120px rgba(255, 215, 0, 0.15),
            inset 0 1px 0 rgba(255, 255, 255, 0.25);
    }

    /* Enhanced warning messages with glassmorphism */
    .stWarning {
        background: rgba(255, 193, 7, 0.1) !important;
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 193, 7, 0.3) !important;
        border-radius: 20px !important;
        box-shadow: 0 4px 20px rgba(255, 193, 7, 0.1);
    }

    /* Enhanced streamlit components */
    .stApp > header {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px);
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* Image enhancements */
    .stImage > div {
        border-radius: 20px;
        overflow: hidden;
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* Column enhancements */
    .stColumn > div {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        margin: 10px 5px;
    }

    /* Floating elements effect */
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }

    .story-chapter:nth-child(odd) {
        animation: float 6s ease-in-out infinite;
    }

    .story-chapter:nth-child(even) {
        animation: float 6s ease-in-out infinite reverse;
    }
    </style>
""", unsafe_allow_html=True)

# ---------- 📖 PROLOGUE: The Chronicles Begin ----------
st.markdown('<h1 class="chronicles-title">The Chronicles of India</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; font-size: 1.5rem; color: #FFD700; font-style: italic;">A Heritage Odyssey Through Time</p>', unsafe_allow_html=True)

# Language Selection with Story Context
language = st.selectbox("🌐 Choose the Language of Your Chronicle", ["English", "Hindi"])

# Enhanced Multilingual Storytelling Content
texts = {
    "English": {
        "prologue": """In the heart of ancient Bharat, where the whispers of time dance with the winds, lie scattered the jewels of our civilization. Each temple stone holds prayers of a thousand devotees, each fort wall echoes with tales of valor and sacrifice.

Today, dear traveler, you embark on a mystical journey through the corridors of time. You shall walk where kings once ruled, where sages once meditated, and where artisans carved dreams into stone.

This is not merely a map—it is a portal to India's soul.""",
        
        "chapter1_title": "Chapter I: Choose Your Destiny",
        "chapter1_story": """The ancient scriptures speak of two sacred paths that weave through our land:

**The Path of Devotion** - Following the sacred temples where divine energy flows through carved pillars and ancient prayers still echo in hallowed halls.

**The Path of Valor** - Tracing the mighty fortresses where brave hearts defended their motherland, where strategy met courage, and where legends were born.

Which path calls to your soul, wanderer?""",
        
        "path_choice": "Choose Your Sacred Path",
        "realm_choice": "Select Your Realm of Exploration",
        
        "chapter2_title": "Chapter II: The Sacred Map Unveiled",
        "chapter2_story": """Behold! The mystical map materializes before your eyes, revealing the hidden treasures scattered across our beloved motherland. Each glowing marker holds within it centuries of stories, waiting to be discovered.

Click upon any marker, and let the ancient voices guide you through their tales...""",
        
        "no_sites": "The mists of time have hidden the treasures in this realm. Choose another path, brave explorer.",
        
        "chapter3_title": "Chapter III: The Chronicle Records",
        "chapter3_story": """Here lie the detailed chronicles of each sacred site - their names whispered by pilgrims, their stories etched in the annals of history. Study these records well, for they hold the keys to understanding our glorious past.""",
        
        "treasure_download": "📜 Preserve This Chronicle",
        
        "epilogue": """
**Thus concludes your journey through the Chronicles of India...**

You have walked the sacred paths where saints found enlightenment and warriors found glory. You have touched the very essence of our civilization—carved in stone, preserved in prayers, and alive in the hearts of our people.

Remember, dear traveler: Every temple you've discovered pulses with divine energy. Every fort you've explored resonates with the courage of our ancestors.

*The chronicles await your return...*

🙏 *May the wisdom of ages guide your path* 🙏"""
    },
    
    "Hindi": {
        "prologue": """प्राचीन भारत के हृदय में, जहाँ समय की फुसफुसाहट हवाओं के साथ नृत्य करती है, वहाँ हमारी सभ्यता के रत्न बिखरे पड़े हैं। प्रत्येक मंदिर का पत्थर हजारों भक्तों की प्रार्थनाओं को समेटे है, प्रत्येक किले की दीवार वीरता और बलिदान की गाथाओं से गूंजती है।

आज, प्रिय यात्री, आप समय के गलियारों से होकर एक रहस्यमय यात्रा पर निकल रहे हैं। आप वहाँ चलेंगे जहाँ कभी राजा शासन करते थे, जहाँ ऋषि तपस्या करते थे, और जहाँ कारीगरों ने सपनों को पत्थर में उकेरा था।

यह केवल एक नक्शा नहीं है—यह भारत की आत्मा का द्वार है।""",
        
        "chapter1_title": "अध्याय I: अपनी नियति चुनें",
        "chapter1_story": """प्राचीन शास्त्र हमारी भूमि से होकर गुजरते दो पवित्र मार्गों की चर्चा करते हैं:

**भक्ति का मार्ग** - उन पवित्र मंदिरों का अनुसरण जहाँ दिव्य ऊर्जा नक्काशीदार स्तंभों से प्रवाहित होती है और प्राचीन प्रार्थनाएं अभी भी पवित्र कक्षों में गूंजती हैं।

**वीरता का मार्ग** - उन शक्तिशाली किलों का पता लगाना जहाँ बहादुर दिलों ने अपनी मातृभूमि की रक्षा की, जहाँ रणनीति साहस से मिली, और जहाँ किंवदंतियों का जन्म हुआ।

कौन सा मार्ग आपकी आत्मा को पुकारता है, यात्री?""",
        
        "path_choice": "अपना पवित्र मार्ग चुनें",
        "realm_choice": "अन्वेषण का क्षेत्र चुनें",
        
        "chapter2_title": "अध्याय II: पवित्र मानचित्र का अनावरण",
        "chapter2_story": """देखिए! रहस्यमय मानचित्र आपकी आंखों के सामने प्रकट हो रहा है, हमारी प्रिय मातृभूमि में बिखरे छुपे खजानों को प्रकट कर रहा है। प्रत्येक चमकता चिह्न अपने भीतर सदियों की कहानियाँ समेटे है, खोजे जाने की प्रतीक्षा में।

किसी भी चिह्न पर क्लिक करें, और प्राचीन आवाजों को अपनी कहानियों के माध्यम से आपका मार्गदर्शन करने दें...""",
        
        "no_sites": "समय की धुंध ने इस क्षेत्र में खजानों को छुपा दिया है। दूसरा मार्ग चुनें, बहादुर खोजकर्ता।",
        
        "chapter3_title": "अध्याय III: इतिहास के अभिलेख",
        "chapter3_story": """यहाँ प्रत्येक पवित्र स्थल के विस्तृत इतिहास हैं - उनके नाम तीर्थयात्रियों द्वारा फुसफुसाए गए, उनकी कहानियाँ इतिहास के पन्नों में अंकित। इन अभिलेखों का अच्छी तरह अध्ययन करें, क्योंकि ये हमारे गौरवशाली अतीत को समझने की चाबी रखते हैं।""",
        
        "treasure_download": "📜 इस इतिहास को संरक्षित करें",
        
        "epilogue": """
**इस प्रकार भारत के इतिहास के माध्यम से आपकी यात्रा समाप्त होती है...**

आपने उन पवित्र मार्गों पर चला है जहाँ संतों ने ज्ञान पाया और योद्धाओं ने महिमा पाई। आपने हमारी सभ्यता के सार को छुआ है—पत्थर में उकेरा गया, प्रार्थनाओं में संरक्षित, और हमारे लोगों के दिलों में जीवित।

याद रखें, प्रिय यात्री: आपके द्वारा खोजा गया प्रत्येक मंदिर दिव्य ऊर्जा से स्पंदित होता है। आपके द्वारा खोजा गया प्रत्येक किला हमारे पूर्वजों के साहस से गूंजता है।

*इतिहास आपकी वापसी की प्रतीक्षा कर रहा है...*

🙏 *युगों की बुद्धि आपके मार्ग का मार्गदर्शन करे* 🙏"""
    }
}
# ---------- 📖 PROLOGUE ----------
st.markdown(f"""
<div class="story-chapter">
    <div class="narrator-voice">
        {texts[language]["prologue"]}
    </div>
</div>
""", unsafe_allow_html=True)

# Hero Image with Story Context
st.image(
    "https://www.indianluxurytrains.com/wp-content/uploads/2011/07/Hampi_virupaksha_temple-1.jpg",
    caption="The eternal stones of Hampi whisper tales of the mighty Vijayanagara Empire...",
    use_column_width=True
)

# ---------- 🧭 Data Loading (Hidden in Story) ----------
@st.cache_data(ttl=600)
def load_data_from_snowflake():
    conn = snowflake.connector.connect(
        user=st.secrets["snowflake"]["user"],
        password=st.secrets["snowflake"]["password"],
        account=st.secrets["snowflake"]["account"],
        warehouse=st.secrets["snowflake"]["warehouse"],
        database=st.secrets["snowflake"]["database"],
        schema=st.secrets["snowflake"]["schema"]
    )
    
    temples_query = "SELECT * FROM DATASET_TEMPLES"
    temples = pd.read_sql(temples_query, conn)

    forts_query = "SELECT * FROM DATASET_FORTS"
    forts = pd.read_sql(forts_query, conn)
    
    conn.close()
    return temples, forts

try:
    temples, forts = load_data_from_snowflake()
except Exception as e:
    st.error(f"❌ The ancient scrolls could not be retrieved: {e}")
    st.stop()

# Data Preparation
for df_, label in [(temples, "Temples"), (forts, "Forts")]:
    df_["LATITUDE"] = pd.to_numeric(df_["LATITUDE"], errors="coerce")
    df_["LONGITUDE"] = pd.to_numeric(df_["LONGITUDE"], errors="coerce")
    df_.dropna(subset=["LATITUDE", "LONGITUDE"], inplace=True)
    df_["Type"] = label

df = pd.concat([temples, forts], ignore_index=True)

# ---------- 📖 CHAPTER I: Choose Your Path ----------
st.markdown(f"""
<div class="story-chapter">
    <h2 class="chapter-title">{texts[language]["chapter1_title"]}</h2>
    <div class="narrator-voice">
        {texts[language]["chapter1_story"]}
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="story-controls">', unsafe_allow_html=True)
st.markdown(f'<h3>{texts[language]["path_choice"]}</h3>', unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    type_filter = st.selectbox(
        "🏛️ Sacred Path", 
        ["All Paths", "Temples", "Forts"],
        help="Choose between the path of devotion (Temples) or valor (Forts)"
    )
with col2:
    state_filter = st.selectbox(
        f"🗺️ {texts[language]['realm_choice']}", 
        ["All Realms"] + sorted(df["STATE"].dropna().unique()),
        help="Select a specific region to explore"
    )
st.markdown('</div>', unsafe_allow_html=True)

# Filter Logic
filtered_df = df.copy()
if type_filter == "Temples":
    filtered_df = filtered_df[filtered_df["Type"] == "Temples"]
elif type_filter == "Forts":
    filtered_df = filtered_df[filtered_df["Type"] == "Forts"]

if state_filter != "All Realms":
    filtered_df = filtered_df[filtered_df["STATE"] == state_filter]

# ---------- 📖 CHAPTER II: The Sacred Map ----------
st.markdown(f"""
<div class="story-chapter">
    <h2 class="chapter-title">{texts[language]["chapter2_title"]}</h2>
    <div class="narrator-voice">
        {texts[language]["chapter2_story"]}
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="ancient-map">', unsafe_allow_html=True)

if not filtered_df.empty:
    center_lat = filtered_df["LATITUDE"].mean()
    center_lon = filtered_df["LONGITUDE"].mean()
    m = folium.Map(location=[center_lat, center_lon], zoom_start=6, tiles="CartoDB positron")
else:
    m = folium.Map(location=[22.9734, 78.6569], zoom_start=4.5, tiles="CartoDB positron")
    st.warning(texts[language]["no_sites"])

marker_cluster = MarkerCluster().add_to(m)

for _, row in filtered_df.iterrows():
    name = row["NAME"]
    desc = str(row.get("DESCRIPTION", ""))[:150] + "..."
    state = row["STATE"]
    url = row.get("URL", "#")
    img_url = row.get("C8", "")

    if img_url:
        html = f"""
        <div style="width:280px; background: linear-gradient(135deg, rgba(0,0,0,0.9), rgba(139,69,19,0.8)); 
                    color: #f5f5f5; padding: 20px; border-radius: 15px; border: 2px solid #FFD700;">
            <h4 style="color: #FFD700; margin-bottom: 15px; text-align: center; font-size: 1.3rem;">{name}</h4>
            <img src="{img_url}" width="250" style="margin-bottom:15px; border-radius: 10px; border: 1px solid #FFD700;"><br>
            <p style="color: #FFA500;"><b>📍 Realm:</b> {state}</p>
            <p style="margin-bottom: 15px; font-style: italic; color: #e8e8e8;">{desc}</p>
            <a href="{url}" target="_blank" 
               style="color: #FFD700; text-decoration: none; font-weight: bold; 
                      padding: 8px 16px; border: 1px solid #FFD700; border-radius: 8px; 
                      display: inline-block; transition: all 0.3s;">
               📖 Discover the Tale
            </a>
        </div>
        """
    else:
        html = f"""
        <div style="width:280px; background: linear-gradient(135deg, rgba(0,0,0,0.9), rgba(139,69,19,0.8)); 
                    color: #f5f5f5; padding: 20px; border-radius: 15px; border: 2px solid #FFD700;">
            <h4 style="color: #FFD700; margin-bottom: 15px; text-align: center; font-size: 1.3rem;">{name}</h4>
            <p style="color: #FFA500;"><b>📍 Realm:</b> {state}</p>
            <p style="margin-bottom: 15px; font-style: italic; color: #e8e8e8;">{desc}</p>
            <a href="{url}" target="_blank" 
               style="color: #FFD700; text-decoration: none; font-weight: bold; 
                      padding: 8px 16px; border: 1px solid #FFD700; border-radius: 8px; 
                      display: inline-block;">
               📖 Discover the Tale
            </a>
        </div>
        """

    iframe = IFrame(html, width=300, height=350)
    popup = folium.Popup(iframe, max_width=320)

    folium.Marker(
        location=[row["LATITUDE"], row["LONGITUDE"]],
        popup=popup,
        tooltip=f"🏛️ {name}",
        icon=folium.Icon(
            color="red" if row["Type"] == "Temples" else "green", 
            icon="star" if row["Type"] == "Temples" else "tower",
            prefix='fa'
        )
    ).add_to(marker_cluster)

st_folium(m, width=1200, height=600)
st.markdown('</div>', unsafe_allow_html=True)

# ---------- 📖 CHAPTER III: The Chronicle Records ----------
st.markdown(f"""
<div class="story-chapter">
    <h2 class="chapter-title">{texts[language]["chapter3_title"]}</h2>
    <div class="narrator-voice">
        {texts[language]["chapter3_story"]}
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="ancient-tome">', unsafe_allow_html=True)
st.dataframe(
    filtered_df[["NAME", "STATE", "Type", "DESCRIPTION"]].reset_index(drop=True),
    use_container_width=True
)
st.markdown('</div>', unsafe_allow_html=True)

# Download as Treasure
csv = filtered_df.to_csv(index=False).encode("utf-8")
st.download_button(
    texts[language]["treasure_download"], 
    csv, 
    "heritage_chronicles.csv", 
    "text/csv",
    help="Download your chronicle to preserve this journey"
)

# ---------- 📖 EPILOGUE ----------
st.markdown(f"""
<div class="epilogue">
    {texts[language]["epilogue"]}
</div>
""", unsafe_allow_html=True)
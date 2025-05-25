import streamlit as st
import pandas as pd
import base64
import snowflake.connector

# Set page configuration
st.set_page_config(
    page_title="Journey to Responsible Tourism", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# Background image path
image_path = "Responsible_Tourism/images/main2.png"

# Convert image to base64
def get_base64_image(img_path):
    with open(img_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Encode and set as background with storytelling atmosphere
encoded_bg = get_base64_image(image_path)

# Enhanced Beautiful Styling
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Inter:wght@300;400;500;600&display=swap');
    
    .stApp {{
        background: 
            radial-gradient(circle at 20% 80%, rgba(120, 119, 198, 0.3) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(255, 119, 198, 0.3) 0%, transparent 50%),
            linear-gradient(135deg, rgba(15, 23, 42, 0.95) 0%, rgba(30, 41, 59, 0.9) 50%, rgba(51, 65, 85, 0.85) 100%),
            url("data:image/jpg;base64,{encoded_bg}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        font-family: 'Inter', sans-serif;
    }}
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {{
        width: 8px;
    }}
    ::-webkit-scrollbar-track {{
        background: rgba(15, 23, 42, 0.5);
    }}
    ::-webkit-scrollbar-thumb {{
        background: linear-gradient(45deg, #f9c74f, #f8961e);
        border-radius: 10px;
    }}
    
    /* Main Headers */
    .stMarkdown h1 {{
        font-family: 'Playfair Display', serif !important;
        font-size: 3.5rem !important;
        font-weight: 700 !important;
        background: linear-gradient(135deg, #fbbf24, #f59e0b, #d97706) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
        text-align: center !important;
        margin-bottom: 0.5rem !important;
        text-shadow: 0 4px 20px rgba(251, 191, 36, 0.3) !important;
        animation: glow 2s ease-in-out infinite alternate !important;
    }}
    
    @keyframes glow {{
        from {{ text-shadow: 0 0 10px rgba(251, 191, 36, 0.3), 0 0 20px rgba(251, 191, 36, 0.2); }}
        to {{ text-shadow: 0 0 20px rgba(251, 191, 36, 0.5), 0 0 30px rgba(251, 191, 36, 0.3); }}
    }}
    
    .stMarkdown h3:first-of-type {{
        font-family: 'Playfair Display', serif !important;
        font-size: 1.8rem !important;
        color: #cbd5e1 !important;
        text-align: center !important;
        font-style: italic !important;
        margin-top: -1rem !important;
        margin-bottom: 3rem !important;
        opacity: 0.9 !important;
    }}
    
    /* Chapter Headers */
    .stMarkdown h2 {{
        font-family: 'Playfair Display', serif !important;
        font-size: 2.2rem !important;
        color: #fbbf24 !important;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.8) !important;
        margin-bottom: 1.5rem !important;
        position: relative !important;
        padding-left: 20px !important;
    }}
    
    .stMarkdown h2::before {{
        content: '';
        position: absolute;
        left: 0;
        top: 50%;
        transform: translateY(-50%);
        width: 4px;
        height: 100%;
        background: linear-gradient(to bottom, #fbbf24, #f59e0b);
        border-radius: 2px;
    }}
    
    .stMarkdown h3 {{
        font-family: 'Inter', sans-serif !important;
        font-size: 1.5rem !important;
        color: #f1c40f !important;
        text-align: center !important;
        margin: 3rem 0 2rem 0 !important;
        font-weight: 500 !important;
        text-shadow: 1px 1px 4px rgba(0,0,0,0.6) !important;
    }}
    
    /* Paragraph and Text Styling */
    .stMarkdown p {{
        color: #e2e8f0 !important;
        font-size: 1.15rem !important;
        line-height: 1.8 !important;
        font-weight: 400 !important;
        text-align: justify !important;
        margin-bottom: 1.5rem !important;
    }}
    
    .stMarkdown em {{
        color: #fbbf24 !important;
        font-style: italic !important;
        font-weight: 500 !important;
    }}
    
    .stMarkdown strong {{
        color: #ffffff !important;
        font-weight: 600 !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.5) !important;
    }}
    
    /* Container Styling with Glass Morphism */
    .stContainer {{
        background: linear-gradient(135deg, 
            rgba(255, 255, 255, 0.1) 0%, 
            rgba(255, 255, 255, 0.05) 100%) !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 24px !important;
        padding: 2.5rem !important;
        margin: 2rem 0 !important;
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
        position: relative !important;
        overflow: hidden !important;
        transition: all 0.3s ease !important;
    }}
    
    .stContainer::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: linear-gradient(90deg, 
            transparent, 
            rgba(255, 255, 255, 0.4), 
            transparent);
    }}
    
    .stContainer:hover {{
        transform: translateY(-4px) !important;
        box-shadow: 
            0 12px 48px rgba(0, 0, 0, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.3) !important;
    }}
    
    /* Button Styling */
    .stButton > button {{
        background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 50%, #d97706 100%) !important;
        color: #1e293b !important;
        font-weight: 600 !important;
        font-size: 1.2rem !important;
        border: none !important;
        border-radius: 50px !important;
        padding: 1rem 3rem !important;
        box-shadow: 
            0 8px 25px rgba(251, 191, 36, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.3) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        position: relative !important;
        overflow: hidden !important;
    }}
    
    .stButton > button::before {{
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, 
            transparent, 
            rgba(255, 255, 255, 0.3), 
            transparent);
        transition: left 0.5s;
    }}
    
    .stButton > button:hover::before {{
        left: 100%;
    }}
    
    .stButton > button:hover {{
        transform: translateY(-2px) scale(1.05) !important;
        box-shadow: 
            0 12px 35px rgba(251, 191, 36, 0.6),
            inset 0 1px 0 rgba(255, 255, 255, 0.4) !important;
    }}
    
    .stButton > button:active {{
        transform: translateY(0) scale(1) !important;
    }}
    
    /* Divider Styling */
    hr {{
        border: none !important;
        height: 2px !important;
        background: linear-gradient(90deg, 
            transparent, 
            rgba(251, 191, 36, 0.6), 
            transparent) !important;
        margin: 3rem 0 !important;
    }}
    
    /* Special styling for intro and conclusion sections */
    .stMarkdown:has(h2:contains("Once Upon")) {{
        background: linear-gradient(135deg, 
            rgba(251, 191, 36, 0.1) 0%, 
            rgba(245, 158, 11, 0.05) 100%) !important;
        border: 1px solid rgba(251, 191, 36, 0.3) !important;
        border-radius: 20px !important;
        padding: 2.5rem !important;
        margin: 2rem 0 !important;
        position: relative !important;
    }}
    
    /* Animation for elements */
    .stContainer, .stMarkdown {{
        animation: fadeInUp 0.6s ease-out !important;
    }}
    
    @keyframes fadeInUp {{
        from {{
            opacity: 0;
            transform: translateY(30px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}
    
    /* Responsive Design */
    @media (max-width: 768px) {{
        .stMarkdown h1 {{
            font-size: 2.5rem !important;
        }}
        .stMarkdown h2 {{
            font-size: 1.8rem !important;
        }}
        .stContainer {{
            padding: 1.5rem !important;
        }}
    }}
    
    /* Custom list styling */
    .stMarkdown ul {{
        list-style: none !important;
        padding-left: 0 !important;
    }}
    
    .stMarkdown li {{
        background: rgba(255, 255, 255, 0.05) !important;
        margin: 1rem 0 !important;
        padding: 1rem 1.5rem !important;
        border-radius: 12px !important;
        border-left: 4px solid #fbbf24 !important;
        transition: all 0.3s ease !important;
        backdrop-filter: blur(10px) !important;
    }}
    
    .stMarkdown li:hover {{
        background: rgba(255, 255, 255, 0.1) !important;
        transform: translateX(5px) !important;
        border-left-color: #f59e0b !important;
    }}
</style>
""", unsafe_allow_html=True)

# Storytelling Header with enhanced presentation
st.markdown("# 🌍 The Traveler's Guide to Responsible Adventures")
st.markdown("### *A Journey Through Conscious Exploration*")

# Enhanced Narrative Introduction
st.markdown("""
---
## 📖 Once Upon a Journey...

In a world where wanderlust calls to every curious soul, there lived travelers who discovered 
that the most meaningful adventures were those that honored both the places they visited and 
the communities that welcomed them. This is their story—a collection of wisdom gathered from 
paths well-traveled and hearts well-intentioned.

*Each chapter of this guide reveals the secrets of traveling with purpose, 
leaving footprints of kindness rather than harm...*

---
""")

# Connect to Snowflake using secrets
conn = snowflake.connector.connect(
    user=st.secrets["snowflake"]["user"],
    password=st.secrets["snowflake"]["password"],
    account=st.secrets["snowflake"]["account"],
    warehouse=st.secrets["snowflake"]["warehouse"],
    database=st.secrets["snowflake"]["database"],
    schema=st.secrets["snowflake"]["schema"]
)

# Query data
query = "SELECT CATEGORY, TIP FROM RESPONSIBLE_TOURISM_TIPS"
tips_df = pd.read_sql(query, conn)
conn.close()

# Unique categories
categories = tips_df['CATEGORY'].unique()

# Story chapter transition
st.markdown("### ✨ *And so, our tale unfolds through these sacred chapters of wisdom...* ✨")

# Display chapters in storytelling format using Streamlit containers
cols = st.columns(2)

# Enhanced story elements for each chapter
chapter_icons = ["🌱", "🏛️", "🤝", "🌊"]

for i, category in enumerate(categories):
    with cols[i % 2]:
        tips = tips_df[tips_df['CATEGORY'] == category]['TIP'].tolist()
        
        # Create enhanced storytelling container
        with st.container():
            st.markdown(f"## {chapter_icons[i % len(chapter_icons)]} Chapter {i + 1}: The Tale of {category}")
            
            st.markdown("*Our wise travelers discovered these sacred principles:*")
            
            # Display tips as beautifully formatted story elements
            for tip in tips:
                st.markdown(f"✨ **{tip}**")
            
            st.markdown("---")

# Enhanced Story conclusion
st.markdown("""
## 🌟 The Journey Continues...

And so, dear traveler, armed with this ancient wisdom, you are ready to embark 
on adventures that will not only fill your soul but also nurture the world around you. 
The next chapter of your story awaits...

*May your journeys be filled with wonder, respect, and the joy of discovery that enriches both you and the world you explore.*
""")

# Enhanced Navigation with storytelling theme
st.markdown("<br>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("🗺️ Continue Your Journey →", use_container_width=True):
        st.markdown(
            '<meta http-equiv="refresh" content="0; url=/Info_tips">',
            unsafe_allow_html=True
        )

# Enhanced storytelling footer
st.markdown("""
---
*"The world is a book, and those who do not travel read only one page."*  
*— But those who travel responsibly, write beautiful chapters for future generations.*

**✨ Safe travels, conscious explorer. ✨**
""")

st.markdown("<br><br>", unsafe_allow_html=True)
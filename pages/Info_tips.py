import streamlit as st
import base64

# Set page configuration
st.set_page_config(
    page_title="Chronicles of Mindful Wandering", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# Background image path
image_path = "Responsible_Tourism/images/main2.png"

# Convert image to base64
def get_base64_image(img_path):
    try:
        with open(img_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except:
        return ""

# Encode and set as background with storytelling atmosphere
encoded_bg = get_base64_image(image_path)

# Enhanced Beautiful Styling matching the first file
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
    
    /* Custom Story Card Styling */
    .story-card {{
        background: linear-gradient(135deg, 
            rgba(255, 255, 255, 0.15) 0%,
            rgba(255, 255, 255, 0.08) 50%,
            rgba(255, 255, 255, 0.05) 100%) !important;
        backdrop-filter: blur(25px) !important;
        -webkit-backdrop-filter: blur(25px) !important;
        border: 1px solid rgba(255, 255, 255, 0.25) !important;
        border-radius: 28px !important;
        padding: 2.5rem !important;
        margin: 1.5rem 0 !important;
        box-shadow: 
            0 12px 40px rgba(0, 0, 0, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.3),
            inset 0 -1px 0 rgba(0, 0, 0, 0.1) !important;
        position: relative !important;
        overflow: hidden !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        transform-style: preserve-3d !important;
    }}
    
    .story-card::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, 
            transparent, 
            rgba(251, 191, 36, 0.6),
            rgba(245, 158, 11, 0.6),
            transparent);
        animation: shimmer 3s ease-in-out infinite;
    }}
    
    @keyframes shimmer {{
        0% {{ transform: translateX(-100%); }}
        100% {{ transform: translateX(100%); }}
    }}
    
    .story-card:hover {{
        transform: translateY(-8px) rotateX(2deg) !important;
        box-shadow: 
            0 20px 60px rgba(0, 0, 0, 0.5),
            inset 0 1px 0 rgba(255, 255, 255, 0.4),
            0 0 0 1px rgba(251, 191, 36, 0.3) !important;
    }}
    
    .story-card h3 {{
        font-family: 'Playfair Display', serif !important;
        font-size: 1.8rem !important;
        color: #fbbf24 !important;
        text-align: center !important;
        margin-bottom: 1.5rem !important;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.6) !important;
        font-weight: 600 !important;
    }}
    
    .story-card p {{
        color: #e2e8f0 !important;
        font-size: 1.1rem !important;
        line-height: 1.7 !important;
        text-align: center !important;
        margin-bottom: 1.5rem !important;
        font-style: italic !important;
    }}
    
    .story-card img {{
        border-radius: 20px !important;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3) !important;
        margin-bottom: 1.5rem !important;
        transition: all 0.3s ease !important;
    }}
    
    .story-card:hover img {{
        transform: scale(1.05) !important;
        box-shadow: 0 12px 35px rgba(0, 0, 0, 0.4) !important;
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
    
    /* Custom list styling */
    .stMarkdown ul {{
        list-style: none !important;
        padding-left: 0 !important;
    }}
    
    .stMarkdown li {{
        background: rgba(255, 255, 255, 0.08) !important;
        margin: 0.8rem 0 !important;
        padding: 1rem 1.5rem !important;
        border-radius: 12px !important;
        border-left: 4px solid #fbbf24 !important;
        transition: all 0.3s ease !important;
        backdrop-filter: blur(10px) !important;
        color: #e2e8f0 !important;
        font-size: 1rem !important;
        line-height: 1.6 !important;
    }}
    
    .stMarkdown li:hover {{
        background: rgba(255, 255, 255, 0.12) !important;
        transform: translateX(8px) !important;
        border-left-color: #f59e0b !important;
        box-shadow: 0 4px 15px rgba(251, 191, 36, 0.2) !important;
    }}
    
    /* Animation for elements */
    .story-card, .stMarkdown {{
        animation: fadeInUp 0.8s ease-out !important;
    }}
    
    @keyframes fadeInUp {{
        from {{
            opacity: 0;
            transform: translateY(40px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}
</style>
""", unsafe_allow_html=True)

# Storytelling Header with enhanced presentation
st.markdown("# 📚 Chronicles of Mindful Wandering")
st.markdown("### *Ancient Wisdom for the Modern Explorer*")

# Enhanced Narrative Introduction
st.markdown("""
---
## 🌟 The Deeper Tales Unfold...

Beyond the first whispers of wisdom lies a treasury of ancient knowledge, 
passed down through generations of mindful wanderers. These are the deeper stories—
the sacred practices that transform ordinary travelers into guardians of culture, 
protectors of nature, and bridges between worlds.

*Let us delve deeper into the chronicles of conscious exploration, 
where every choice becomes a story worth telling...*

---
""")

# Define the story card data with enhanced narrative
story_chapters = [
    {
        "title": "🌱 The Guardian's Path",
        "subtitle": "Chapter of Sustainable Harmony",
        "story_intro": "In lands where ancient trees whispered secrets to the wind, the wise travelers learned to walk without leaving scars upon the earth...",
        "content": """Choose eco-friendly transportation, pack light, and stay in green-certified accommodations to reduce your environmental footprint.""",
        "sacred_practices": [
            "🚌 Journey by public transport, walk with intention, or cycle with the breeze",
            "🏨 Seek shelter in eco-certified sanctuaries that honor Mother Earth", 
            "♻️ Carry sacred vessels—reusable bottles, bags, and utensils of renewal",
            "🌍 Offer carbon prayers to the sky, offsetting the breath of your flights"
        ],
        "image": "Responsible_Tourism/images/sustainable_travel.png",
        "mystical_quote": "*\"Leave nothing but footprints, take nothing but memories, kill nothing but time.\"*"
    },
    {
        "title": "🤝 The Bridge Builder's Tale",
        "subtitle": "Chapter of Community Bonds",
        "story_intro": "Where strangers became family and every meal shared was a celebration of human connection...",
        "content": """Support local communities by booking local guides, eating at family-run restaurants, and staying in homestays or locally owned lodges.""",
        "sacred_practices": [
            "🍽️ Feast at tables where grandmothers cook with love and local stories",
            "👥 Walk with local guides who carry the wisdom of their ancestors",
            "🏠 Rest in homestays where every room echoes with authentic laughter",
            "🎭 Dance at cultural celebrations, joining the rhythm of local hearts"
        ],
        "image": "Responsible_Tourism/images/community.png",
        "mystical_quote": "*\"A stranger is just a friend whose story you haven't heard yet.\"*"
    },
    {
        "title": "🧶 The Artisan's Legacy",
        "subtitle": "Chapter of Handcrafted Dreams", 
        "story_intro": "In workshops where skilled hands breathed life into clay, thread, and wood, travelers discovered the soul of creation...",
        "content": """Purchase handmade crafts and souvenirs directly from local artisans to promote traditional skills and boost the local economy.""",
        "sacred_practices": [
            "🎨 Buy treasures directly from the hands that shaped them with love",
            "🌿 Choose handmade, earth-friendly goods that tell ancient stories",
            "🦋 Protect endangered species by refusing their exploitation",
            "✋ Learn the ancient arts in workshops, becoming part of the legacy"
        ],
        "image": "Responsible_Tourism/images/handicrafts.png",
        "mystical_quote": "*\"Every handmade creation carries the heartbeat of its maker.\"*"
    }
]

# Story chapter transition
st.markdown("### ✨ *The sacred scrolls of wisdom await your discovery...* ✨")

# Display chapters in enhanced storytelling format
for i, chapter in enumerate(story_chapters):
    # Create story card with enhanced styling
    story_card_html = f"""
    <div class="story-card">
        <h3>{chapter['title']}</h3>
        <h4 style="color: #cbd5e1; font-family: 'Playfair Display', serif; font-style: italic; text-align: center; margin-bottom: 2rem; font-size: 1.2rem;">{chapter['subtitle']}</h4>
        <p style="color: #fbbf24; font-size: 1.1rem; text-align: center; margin-bottom: 2rem; font-weight: 500;">{chapter['story_intro']}</p>
    </div>
    """
    
    st.markdown(story_card_html, unsafe_allow_html=True)
    
    # Display the image with storytelling context
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            try:
                st.image(chapter["image"], use_container_width=True, caption=f"✨ {chapter['subtitle']} ✨")
            except:
                st.markdown(f"*📸 Vision of {chapter['title']} awaits...*")
    
    # Display the story content and practices
    st.markdown(f"""
    ### 📖 The Sacred Teachings
    
    *{chapter['content']}*
    
    **The Ancient Practices Revealed:**
    """)
    
    # Display practices as enhanced list items
    for practice in chapter['sacred_practices']:
        st.markdown(f"- {practice}")
    
    # Add mystical quote
    st.markdown(f"""
    <div style="text-align: center; margin: 2rem 0; padding: 1.5rem; 
    background: linear-gradient(135deg, rgba(251, 191, 36, 0.1), rgba(245, 158, 11, 0.05)); 
    border-radius: 20px; border: 1px solid rgba(251, 191, 36, 0.3);">
        <p style="color: #fbbf24; font-style: italic; font-size: 1.1rem; margin: 0;">{chapter['mystical_quote']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")

# Enhanced Story conclusion
st.markdown("""
## 🌟 The Chronicle Closes, But Your Story Begins...

With these deeper wisdoms etched upon your traveler's heart, you now possess 
the complete tapestry of conscious exploration. Each thread represents a choice, 
each pattern a path toward harmony between wanderlust and wisdom.

*Go forth, noble traveler, and let your journeys become legends 
that inspire future generations to walk the path of mindful discovery.*

**✨ May your adventures write the most beautiful chapters in the book of conscious travel. ✨**
""")

# Enhanced Navigation with storytelling theme
st.markdown("<br>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("🏠 Return to Your Journey's Beginning", use_container_width=True):
        st.markdown(
            '<meta http-equiv="refresh" content="0; url=/">',
            unsafe_allow_html=True
        )

# Enhanced storytelling footer
st.markdown("""
---
*"We travel, initially, to lose ourselves; and we travel, next, to find ourselves."*  
*— But the wisest travelers know that we journey to become ourselves.*

**🌍 Until we meet again on the paths of wonder, dear explorer. 🌍**
""")

st.markdown("<br><br>", unsafe_allow_html=True)
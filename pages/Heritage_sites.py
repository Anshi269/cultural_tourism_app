import streamlit as st
import pandas as pd
import folium
import snowflake.connector
from streamlit_folium import st_folium
from folium import IFrame
from folium.plugins import MarkerCluster
import os

# Page Config
st.set_page_config(page_title="Heritage Explorer: Temples & Forts of India", layout="wide")

# Custom CSS - Matching the endangered art forms styling
st.markdown("""
    <style>
    /* Set background image or gradient */
    .stApp {
        background-image: linear-gradient(to bottom, #1b0b0d, #3a1c1f);
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: white;
    }

    /* Remove default padding */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    /* Card styling */
    .heritage-card {
        background: rgba(255, 255, 255, 0.05); /* glassy white */
        backdrop-filter: blur(6px);
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 8px 20px rgba(255, 0, 0, 0.3);
        margin-bottom: 20px;
        transition: transform 0.3s ease;
        height: auto;
        min-height: 200px;
    }

    .heritage-card:hover {
        transform: scale(1.02);
        filter: brightness(1.4);
    }

    /* General card styling for components */
    .card {
        background: rgba(255, 255, 255, 0.05); /* glassy white */
        backdrop-filter: blur(6px);
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 8px 20px rgba(255, 0, 0, 0.3);
        margin-bottom: 30px;
        margin-top: 20px;
        transition: transform 0.3s ease;
    }

    .card:hover {
        transform: scale(1.02);
        filter: brightness(1.4);
    }

    /* Image styling */
    .element-container img {
        border-radius: 12px;
        margin-bottom: 10px;
        transition: transform 0.3s ease;
    } 
    
    .element-container img:hover {
        transform: scale(1.05); /* Slight zoom effect on hover */
        filter: brightness(1.2); /* Slightly brighten the image on hover */
    }

    /* Selectbox styling */
    div.stSelectbox label {
        color: white !important;
    }

    /* Header styling */
    header {
        background-color: transparent !important;
        box-shadow: none !important;
    }

    /* Title styling */
    .main-title {
        text-align: center;
        color: #FFD700;
        font-size: 3rem;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }

    /* Intro text styling */
    .intro-text {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 25px;
        margin: 20px 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }

    /* Map container styling */
    .map-container {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(6px);
        border-radius: 15px;
        padding: 20px;
        margin: 20px 0;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
    }

    /* Filter section styling */
    .filter-section {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(8px);
        border-radius: 15px;
        padding: 20px;
        margin: 20px 0;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* Table styling */
    .dataframe {
        background: rgba(255, 255, 255, 0.1) !important;
        border-radius: 10px;
    }

    /* Warning and info messages */
    .stWarning {
        background: rgba(255, 193, 7, 0.2) !important;
        border: 1px solid rgba(255, 193, 7, 0.5) !important;
        border-radius: 10px !important;
    }

    /* Download button styling */
    .stDownloadButton button {
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.3);
        border-radius: 10px;
        color: white;
        transition: all 0.3s ease;
    }

    .stDownloadButton button:hover {
        background: rgba(255, 255, 255, 0.2);
        transform: translateY(-2px);
    }

    /* Section headers */
    .section-header {
        color: #FFD700;
        font-size: 1.8rem;
        margin: 30px 0 20px 0;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
    }
    </style>
""", unsafe_allow_html=True)

# ---------- 🏁 Story Start: Introduction ----------
st.markdown('<h1 class="main-title">🇮🇳 Heritage Explorer: Temples & Forts of India</h1>', unsafe_allow_html=True)

# ---------- 🌐 Language Selection ----------
language = st.selectbox("🌐 Language", ["English", "Hindi"])

# ---------- 🌐 Multilingual Content ----------
texts = {
    "English": {
        "intro": """Welcome to the <b>Heritage Explorer<b>, a journey across the sacred temples and majestic forts that echo the timeless soul of India.  
From the granite cliffs of Rajasthan to the spiritual heartlands of Tamil Nadu — this interactive map lets you <b>discover, learn, and explore<b> the jewels of our rich history.""",
        "choose_path": "🔎 Choose Your Path",
        "site_type": "Select Type of Site",
        "state": "Select a State to Explore",
        "map_title": "🗺️ Explore the Sites on Map",
        "no_sites": "No sites match the selected filters.",
        "table_title": "📋 Discover the Stories Behind the Sites",
        "download": "📥 Download This Journey (CSV)",
        "thank_you": """
<br>🧡 Thank you for exploring India's timeless marvels!<br>
Every fort has witnessed battles and bravery.  
Every temple echoes with centuries of devotion.

Keep exploring, Keep preserving! 🙏"""

    },
    "Hindi": {
        "intro": """**हेरिटेज एक्सप्लोरर** में आपका स्वागत है — भारत के पवित्र मंदिरों और भव्य किलों की एक अद्भुत यात्रा।  
राजस्थान की चट्टानों से लेकर तमिलनाडु की आध्यात्मिक भूमि तक — यह इंटरेक्टिव मैप आपको हमारे समृद्ध इतिहास के रत्नों को **खोजने, जानने और समझने** की अनुमति देता है।""",
        "choose_path": "🔎 अपनी यात्रा चुनें",
        "site_type": "स्थल का प्रकार चुनें",
        "state": "राज्य चुनें",
        "map_title": "🗺️ नक्शे पर स्थलों का अन्वेषण करें",
        "no_sites": "चयनित फ़िल्टर के अनुसार कोई स्थल नहीं मिला।",
        "table_title": "📋 स्थलों की कहानियाँ जानें",
        "download": "📥 इस यात्रा को डाउनलोड करें (CSV)",
        "thank_you": """---
### 🧡 भारत की शाश्वत धरोहरों को एक्सप्लोर करने के लिए धन्यवाद!
हर किला वीरता की कहानियाँ कहता है।  
हर मंदिर भक्ति की सदियों पुरानी गूंज है।

खोजते रहें, संरक्षित करते रहें! 🙏"""
    }
}

# ---------- 📜 Intro ----------
st.markdown(f"""
<div class="intro-text">
{texts[language]["intro"]}
</div>
""", unsafe_allow_html=True)

st.image(
    "https://www.indianluxurytrains.com/wp-content/uploads/2011/07/Hampi_virupaksha_temple-1.jpg",
    caption="Group of Monuments at Hampi",
    use_column_width=True
)

# ---------- 🧭 Step 1: Load Data ----------
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
    
    # Query temples
    temples_query = "SELECT * FROM DATASET_TEMPLES"
    temples = pd.read_sql(temples_query, conn)

    # Query forts
    forts_query = "SELECT * FROM DATASET_FORTS"
    forts = pd.read_sql(forts_query, conn)
    
    conn.close()
    return temples, forts

try:
    temples, forts = load_data_from_snowflake()
except Exception as e:
    st.error(f"❌ Snowflake connection failed: {e}")
    st.stop()

# ---------- 🧹 Step 2: Clean + Tag Data ----------
for df_, label in [(temples, "Temples"), (forts, "Forts")]:
    df_["Latitude"] = pd.to_numeric(df_["Latitude"], errors="coerce")
    df_["Longitude"] = pd.to_numeric(df_["Longitude"], errors="coerce")
    df_.dropna(subset=["Latitude", "Longitude"], inplace=True)
    df_["Type"] = label

df = pd.concat([temples, forts], ignore_index=True)

# ---------- 🔍 Step 3: Filter Your Journey ----------
st.markdown(f'<h2 class="section-header">{texts[language]["choose_path"]}</h2>', unsafe_allow_html=True)

st.markdown('<div class="filter-section">', unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    type_filter = st.selectbox(texts[language]["site_type"], ["All", "Temples", "Forts"])
with col2:
    state_filter = st.selectbox(texts[language]["state"], ["All"] + sorted(df["State"].dropna().unique()))
st.markdown('</div>', unsafe_allow_html=True)

filtered_df = df.copy()
if type_filter != "All":
    filtered_df = filtered_df[filtered_df["Type"] == type_filter]
if state_filter != "All":
    filtered_df = filtered_df[filtered_df["State"] == state_filter]

# ---------- 🗺️ Step 4: Journey on the Map ----------
st.markdown(f'<h2 class="section-header">{texts[language]["map_title"]}</h2>', unsafe_allow_html=True)

st.markdown('<div class="map-container">', unsafe_allow_html=True)

if not filtered_df.empty:
    center_lat = filtered_df["Latitude"].mean()
    center_lon = filtered_df["Longitude"].mean()
    m = folium.Map(location=[center_lat, center_lon], zoom_start=6, tiles="CartoDB positron")
else:
    m = folium.Map(location=[22.9734, 78.6569], zoom_start=4.5, tiles="CartoDB positron")
    st.warning(texts[language]["no_sites"])

marker_cluster = MarkerCluster().add_to(m)

for _, row in filtered_df.iterrows():
    name = row["Name"]
    desc = str(row.get("Description", ""))[:150] + "..."
    state = row["State"]
    url = row.get("URL", "#")
    img_url = row.get("ImageURL", "")

    if img_url:
        html = f"""
        <div style="width:240px; background: rgba(0,0,0,0.8); color: white; padding: 15px; border-radius: 10px;">
            <h4 style="color: #FFD700; margin-bottom: 15px;">{name}</h4>
            <img src="{img_url}" width="230" style="margin-bottom:10px; border-radius: 8px;"><br>
            <p><b>State:</b> {state}</p>
            <p style="margin-bottom: 15px;">{desc}</p>
            <a href="{url}" target="_blank" style="color: #FFD700; text-decoration: none;">🔗 Read More</a>
        </div>
        """
    else:
        html = f"""
        <div style="width:240px; background: rgba(0,0,0,0.8); color: white; padding: 15px; border-radius: 10px;">
            <h4 style="color: #FFD700; margin-bottom: 15px;">{name}</h4>
            <p><b>State:</b> {state}</p>
            <p style="margin-bottom: 15px;">{desc}</p>
            <a href="{url}" target="_blank" style="color: #FFD700; text-decoration: none;">🔗 Read More</a>
        </div>
        """

    iframe = IFrame(html, width=250, height=300)
    popup = folium.Popup(iframe, max_width=300)

    # Using different colors and icons for better visibility on dark map
    folium.Marker(
        location=[row["Latitude"], row["Longitude"]],
        popup=popup,
        tooltip=name,
        icon=folium.Icon(
            color="red" if row["Type"] == "Temples" else "green", 
            icon="info-sign",
            prefix='fa'
        )
    ).add_to(marker_cluster)

st_folium(m, width=1200, height=600)
st.markdown('</div>', unsafe_allow_html=True)

# ---------- 📜 Step 5: Details in Table ----------
st.markdown(f'<h2 class="section-header">{texts[language]["table_title"]}</h2>', unsafe_allow_html=True)

st.dataframe(
    filtered_df[["Name", "State", "Type", "Description"]].reset_index(drop=True),
    use_container_width=True
)

# ---------- 📥 Step 6: Let Others Explore Too ----------
csv = filtered_df.to_csv(index=False).encode("utf-8")
st.download_button(texts[language]["download"], csv, "heritage_sites_filtered.csv", "text/csv")

# ---------- 📖 Outro ----------
st.markdown(f"""
<div class="card">
{texts[language]["thank_you"]}
</div>
""", unsafe_allow_html=True)
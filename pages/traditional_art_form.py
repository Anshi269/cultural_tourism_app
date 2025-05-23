import streamlit as st
import pandas as pd
import os
from PIL import Image
import snowflake.connector

# Page configuration
st.set_page_config(page_title="Endangered Art Cards", layout="wide")
# Custom CSS
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
    .card {
        background: rgba(255, 255, 255, 0.05); /* glassy white */
        backdrop-filter: blur(6px);
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 8px 20px rgba(255, 0, 0, 0.3);
        margin-bottom: 30px;
        margin-top: 100px;
        transition: transform 0.3s ease;
    }

    .card:hover {
        transform: scale(1.02);
        filter: brightness(1.4);
    }

    /* Image styling */
    .element-container img {
        object-fit: cover;
        width: 335px !important;
        height: 475px !important;
        border-radius: 12px;
        margin-bottom: 10px;
    } 
            .element-container img:hover {
    transform: scale(1.05); /* Slight zoom effect on hover */
    filter: brightness(1.2); /* Slightly brighten the image on hover */
}
div.stSelectbox label {
    color: white !important;
}
 header {
    background-color: transparent !important;
    box-shadow: none !important;
}
    </style>
""", unsafe_allow_html=True)


st.title("Endangered Indian Art Forms")

# File paths

images_path = os.path.join("Traditional_art", 'images')

# Load data
SNOWFLAKE_CONFIG = {
    'user': 'YOUR_USER',
    'password': 'YOUR_PASSWORD',
    'account': 'YOUR_ACCOUNT',
    'warehouse': 'YOUR_WAREHOUSE',
    'database': 'YOUR_DATABASE',
    'schema': 'YOUR_SCHEMA',
    'role': 'YOUR_ROLE'  # Optional
}

# Function to get a Snowflake connection
def get_snowflake_connection():
    return snowflake.connector.connect(
        user=st.secrets["snowflake"]["user"],
        password=st.secrets["snowflake"]["password"],
        account=st.secrets["snowflake"]["account"],
        warehouse=st.secrets["snowflake"]["warehouse"],
        database=st.secrets["snowflake"]["database"],
        schema=st.secrets["snowflake"]["schema"]
    )

def load_endangered_art_forms():
    conn = get_snowflake_connection()
    query = "SELECT * FROM ENDANGERED_ART_FORMS"
    df = pd.read_sql(query, conn)
    df.columns = df.columns.str.strip()
    conn.close()
    return df

df = load_endangered_art_forms()

# Classify art
def classify_art(art_form):
    dance = ['Kathakali', 'Chhau Dance', 'Khon', 'Birhor Dance', 'Pung Cholom']
    music = ['Taiko Drumming']
    theatre = ['Bhavai', 'Kutiyattam', 'Tholu Bommalata']
    painting = ['Warli Painting', 'Phad Painting', 'Kalighat Paintings', 'Saora Art', 'Gond Art', 'Chitrakathi', 'Pattachitra']
    handicraft = ['Patola Weaving', 'Channapatna Toys', 'Kalamkari', 'Charkha Weaving']

    if art_form in dance:
        return 'Dance'
    elif art_form in music:
        return 'Music'
    elif art_form in theatre:
        return 'Theatre'
    elif art_form in painting:
        return 'Painting'
    elif art_form in handicraft:
        return 'Handicraft'
    else:
        return 'Others'

df['art_category'] = df['ART FORM'].apply(classify_art)

# Art descriptions
art_descriptions = {
    "Kathakali": "<b>🎭 Eyes that speak, colors that roar — Kathakali weaves stories like never before.</b><br> Originating from Kerala, this classical dance-drama is characterized by elaborate costumes, intricate movements, and expressive gestures that bring ancient epics to life. It's a grand spectacle of storytelling through dance and theatre.</br>",
    "Chhau Dance": "<b>💃 A martial grace, masked in lore — Chhau echoes tribal myths and more.</b><br> This vibrant dance form from the tribal regions of India combines elements of martial arts, acrobatics, and storytelling. Dancers wear expressive masks and perform highly energetic movements to depict mythological tales.</br>",
    "Khon": "<b>🎭 Thai-Indian blend of mask and might — Khon brings Ramayana into light.</b><br> A classical Thai dance-drama performed with ornate costumes and elaborate masks, Khon is a captivating portrayal of the Ramayana epic through intricate movements and vibrant stage designs. The performance is a beautiful blend of dance, music, and drama.</br>",
    "Birhor Dance": "<b>🌿 From forest beats and tribal ties, Birhor’s rhythm never dies.</b><br> This dance form is part of the rituals of the Birhor tribe, one of the indigenous groups of India. Known for its earthy beats and vibrant movements, it reflects their deep connection to nature and their spiritual beliefs.</br>",
    "Pung Cholom": "<b>🥁 Dance and drum in perfect flight — Pung Cholom is Manipur’s delight.</b><br> A spectacular dance form from Manipur, it involves rhythmic drumming and synchronized movements. The dancers, who are male performers, drum while balancing on one foot, creating a captivating performance that blends music and dance.</br>",
    "Taiko Drumming": "<b>🥁 Thunder roars in rhythmic flow — Taiko’s beat is ancient glow.</b><br> This traditional Japanese drum performance is known for its powerful, thunderous rhythms. Played on large drums, the Taiko performance is often accompanied by synchronized choreography, making it a visually stunning and exhilarating experience.</br>",
    "Bhavai": "<b>🎭 Village theatre with comic soul — Bhavai plays its humorous role.</b><br> Originating in Gujarat, Bhavai is a folk theatre form that combines music, dance, and drama. It is a humorous and often satirical performance, telling stories of social issues, love, and morality, while engaging the audience with its witty dialogue and lively tunes.</br>",
    "Kutiyattam":"<b>🕉 Sanskrit stage in temple air — Kutiyattam is Kerala’s rare flair.</b><br> Known as one of the oldest living theatre traditions in India, Kutiyattam is a classical Sanskrit drama performed in Kerala's temples. This highly stylized form of theatre uses elaborate gestures, expressions, and rhythmic movements to perform sacred texts.</br>",
    "Tholu Bommalata": "<b>🖼 Shadows dance with leather grace — Tholu Bommalata, an illuminated space.</b><br> A traditional shadow puppetry art form from Andhra Pradesh, Tholu Bommalata uses intricately crafted leather puppets to perform epic stories. The puppets are held against a backlit screen, creating beautiful shadow plays that are both visual and auditory spectacles.</br>",
    "Warli Painting": "<b>🎨 Circles of life in tribal art — Warli tells tales close to heart.</b><br> A tribal art form from Maharashtra, Warli paintings are known for their simple geometric shapes and depictions of nature, animals, and daily life. These paintings tell the stories of the Warli tribe, reflecting their close bond with nature and their agricultural lifestyle.</br>",
    "Phad Painting": "<b>📜 Scrolls unfold heroic streams — Phad flows with Rajput dreams.</b><br> A traditional scroll painting from Rajasthan, Phad paintings depict the heroic tales of local deities and warriors. These intricate paintings are created on cloth or paper and are accompanied by folk songs narrating the stories of gods and their divine acts.</br>",
    "Kalighat Paintings": "<b>🖌 Satire and grace in every stroke — Kalighat’s brush never broke.</b><br> Originating from Kolkata, Kalighat paintings are known for their vibrant, expressive, and satirical style. These paintings often depict religious and mythological figures, as well as social and political themes, and are characterized by bold lines and minimalistic yet striking forms.</br>",
    "Saora Art": "<b>🌾 Symbols speak in Saora style — A tribal tale in every mile.</b><br> Originating from the Saora tribe in Odisha, Saora art is created using natural dyes and features intricate patterns that symbolize their connection to nature. These paintings often depict animals, birds, and trees, showcasing the tribe’s reverence for their environment and its spiritual significance.</br>",
    "Gond Art": "<b>🌳 Trees that talk and dreams that fly — Gond art paints the forest sky.</b><br> This tribal art form from Madhya Pradesh is known for its vibrant colors and intricate patterns. Gond paintings often depict animals, birds, and the forces of nature, telling stories from the artists' dreams and spiritual beliefs.</br>",
    "Chitrakathi": "<b>📖 Epics sung with brush in hand — Chitrakathi brings myths to land.</b><br> A traditional art form from Maharashtra, Chitrakathi is a form of narrative painting that depicts mythological stories. The paintings are often accompanied by storytelling through song, bringing the ancient tales to life with vibrant colors and dynamic compositions.</br>",
    "Pattachitra": "<b>🎨 Silk of tales and gods divine — Pattachitra’s lines entwine.</b><br> Originating from Odisha, Pattachitra paintings are known for their intricate details and religious themes. These paintings often depict Hindu deities, mythological stories, and temples, and are created on cloth or dried palm leaves, showcasing a unique blend of art and spirituality.</br>",
    "Patola Weaving": "<b>🧵 Double ikat, a woven spell — Patola’s precision is hard to tell.</b><br> A traditional form of silk weaving from Gujarat, Patola is famous for its intricate double ikat technique. The art of creating these beautiful woven patterns requires immense skill, and the resulting fabric is known for its vivid colors and complex geometric designs.</br>",
    "Channapatna Toys": "<b>🪀 Wooden joy from Karnataka’s core — Channapatna smiles in folklore.</b><br> A traditional craft from Karnataka, Channapatna toys are made from wood and feature vibrant colors. The craft involves a unique process of creating toys using the lathe machine, and the designs are often inspired by nature and folk traditions.</br>",
    "Kalamkari": "<b>✒️ Pen and plant dye draw the divine — Kalamkari tells stories in design.</b><br> A traditional art form from Andhra Pradesh, Kalamkari is a method of painting on fabric using natural dyes. The artwork often depicts mythological stories, divine beings, and scenes from Hindu epics, and the intricate designs are created with a bamboo pen.</br>",
    "Charkha Weaving": "<b>🧶 Spin the thread of swadeshi pride — Charkha weaves a soulful stride.</b><br> Popularized by Mahatma Gandhi during the Indian freedom struggle, Charkha weaving is a symbol of self-reliance and nationalism. The craft involves spinning cotton yarn into thread and has been revived as a symbol of sustainable living and the fight for independence.</br>"
}


# Filters
col1, col2 = st.columns(2)

with col1:
    selected_category = st.selectbox("Select Category", ['All'] + sorted(df['art_category'].unique()))
with col2:
    selected_state = st.selectbox("Select State", ['All'] + sorted(df['LOCATION (STATE)'].unique()))

# Apply filters
filtered_df = df.copy()

if selected_category != 'All':
    filtered_df = filtered_df[filtered_df['art_category'] == selected_category]

if selected_state != 'All':
    filtered_df = filtered_df[filtered_df['LOCATION (STATE)'] == selected_state]

# Display cards
if filtered_df.empty:
    st.warning("No results match your filters.")
else:
    for i in range(0, len(filtered_df), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(filtered_df):
                row = filtered_df.iloc[i + j]
                art_name = row['ART FORM']
                image_name = art_name.lower().replace(" ", "").replace("/", "") + ".jpg"
                image_file = os.path.join(images_path, image_name)

                with cols[j]:
                   with cols[j]:
                    st.markdown(f"""
                        <div class="card">
                    <h4>{art_name}</h4>
                    """, unsafe_allow_html=True)

                    if os.path.exists(image_file):
                     st.image(image_file, use_container_width=True)
                    else:
                        st.image("https://via.placeholder.com/300x200?text=No+Image", use_container_width=True)

                    st.markdown(f"""
                    <p><b>📍 State(s):</b> {row['LOCATION (STATE)']}</p>
                    <p><b>🎨 Category:</b> {row['art_category']}</p>
                    <em>{art_descriptions.get(art_name, "🌟 A forgotten gem in India’s cultural crown.")}</em>
                    </div>
                    """, unsafe_allow_html=True)
                    st.markdown("<div style='margin-bottom: 2rem;'></div>", unsafe_allow_html=True)
# --- Festival Section ---
st.title("Indian Festivals")


def load_festivals():
    conn = get_snowflake_connection()
    query = "SELECT * FROM INDIAN_FESTIVALS"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

festivals_df = load_festivals()


# Filters for festivals
col3, col4 = st.columns(2)
with col3:
    unique_states = sorted(festivals_df['Location (State)'].unique())
    if 'PAN India' not in unique_states:
        unique_states.append('PAN India')
    selected_festival_state = st.selectbox("Select Festival State", ['All'] + unique_states)
with col4:
    selected_festival_month = st.selectbox("Select Festival Month", ['All'] + sorted(festivals_df['MONTH'].unique()))

# Apply festival filters
filtered_festivals = festivals_df.copy()
if selected_festival_state != 'All':
    filtered_festivals = filtered_festivals[filtered_festivals['Location (State)'] == selected_festival_state]
if selected_festival_month != 'All':
    filtered_festivals = filtered_festivals[filtered_festivals['MONTH'] == selected_festival_month]

# Display festival cards
if selected_festival_state == 'PAN India':
    st.subheader("🎉 National Festivals Celebrated Across India")
elif selected_festival_state == 'All':
    st.subheader("🎊 All Festivals (State-specific and National)")

if filtered_festivals.empty:
    st.warning("No festivals match your filters.")
else:
    for i in range(0, len(filtered_festivals), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(filtered_festivals):
                fest = filtered_festivals.iloc[i + j]
                with cols[j]:
                    st.markdown(f"""
                    <div class="card" style="background: rgba(255, 255, 255, 0.08); padding: 10px; border-radius: 8px;">
                        <h4>{fest['FESTIVAL']}</h4>
                        <p><b>📍 State:</b> {fest['Location (State)']}</p>
                        <p><b>🗓 Month:</b> {fest['MONTH']}</p>
                        <p>{fest['DESCRIPTION']}</p>
                    </div>
                    """, unsafe_allow_html=True)
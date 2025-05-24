import streamlit as st
import pandas as pd
import os
from PIL import Image
import snowflake.connector

# Page configuration
st.set_page_config(page_title="Journey Through India's Cultural Tapestry", layout="wide")

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
    
    /* Storytelling elements */
    .story-intro {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 30px;
        margin: 20px 0;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .chapter-title {
        font-size: 2.5rem;
        background: linear-gradient(45deg, #ff6b6b, #ffd93d);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin: 40px 0 20px 0;
        font-weight: bold;
    }
    
    .narrative-text {
        font-size: 1.2rem;
        line-height: 1.8;
        margin: 20px 0;
        font-style: italic;
        text-align: center;
        color: #f0f0f0;
    }
    </style>
""", unsafe_allow_html=True)

# Storytelling Introduction
st.markdown("""
<div class="story-intro">
    <h1 style="color: #ffd93d; font-size: 3rem; margin-bottom: 20px;">📚 Once Upon a Time in India...</h1>
    <p class="narrative-text">
        In a land where every village whispers ancient tales and every street corner echoes with forgotten melodies, 
        we embark on a magical journey through India's living heritage. Come, let us unveil the stories that time forgot, 
        but the heart remembers...
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="chapter-title">Chapter I: The Endangered Treasures</div>', unsafe_allow_html=True)

st.markdown("""
<div class="narrative-text">
    Deep in the heart of our motherland lie art forms so precious, so rare, that they flutter like endangered butterflies 
    on the edge of oblivion. Each one carries the soul of generations, the dreams of our ancestors, and the hope that 
    someone, somewhere, will remember their beauty...
</div>
""", unsafe_allow_html=True)

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
    "Birhor Dance": "<b>🌿 From forest beats and tribal ties, Birhor's rhythm never dies.</b><br> This dance form is part of the rituals of the Birhor tribe, one of the indigenous groups of India. Known for its earthy beats and vibrant movements, it reflects their deep connection to nature and their spiritual beliefs.</br>",
    "Pung Cholom": "<b>🥁 Dance and drum in perfect flight — Pung Cholom is Manipur's delight.</b><br> A spectacular dance form from Manipur, it involves rhythmic drumming and synchronized movements. The dancers, who are male performers, drum while balancing on one foot, creating a captivating performance that blends music and dance.</br>",
    "Taiko Drumming": "<b>🥁 Thunder roars in rhythmic flow — Taiko's beat is ancient glow.</b><br> This traditional Japanese drum performance is known for its powerful, thunderous rhythms. Played on large drums, the Taiko performance is often accompanied by synchronized choreography, making it a visually stunning and exhilarating experience.</br>",
    "Bhavai": "<b>🎭 Village theatre with comic soul — Bhavai plays its humorous role.</b><br> Originating in Gujarat, Bhavai is a folk theatre form that combines music, dance, and drama. It is a humorous and often satirical performance, telling stories of social issues, love, and morality, while engaging the audience with its witty dialogue and lively tunes.</br>",
    "Kutiyattam":"<b>🕉 Sanskrit stage in temple air — Kutiyattam is Kerala's rare flair.</b><br> Known as one of the oldest living theatre traditions in India, Kutiyattam is a classical Sanskrit drama performed in Kerala's temples. This highly stylized form of theatre uses elaborate gestures, expressions, and rhythmic movements to perform sacred texts.</br>",
    "Tholu Bommalata": "<b>🖼 Shadows dance with leather grace — Tholu Bommalata, an illuminated space.</b><br> A traditional shadow puppetry art form from Andhra Pradesh, Tholu Bommalata uses intricately crafted leather puppets to perform epic stories. The puppets are held against a backlit screen, creating beautiful shadow plays that are both visual and auditory spectacles.</br>",
    "Warli Painting": "<b>🎨 Circles of life in tribal art — Warli tells tales close to heart.</b><br> A tribal art form from Maharashtra, Warli paintings are known for their simple geometric shapes and depictions of nature, animals, and daily life. These paintings tell the stories of the Warli tribe, reflecting their close bond with nature and their agricultural lifestyle.</br>",
    "Phad Painting": "<b>📜 Scrolls unfold heroic streams — Phad flows with Rajput dreams.</b><br> A traditional scroll painting from Rajasthan, Phad paintings depict the heroic tales of local deities and warriors. These intricate paintings are created on cloth or paper and are accompanied by folk songs narrating the stories of gods and their divine acts.</br>",
    "Kalighat Paintings": "<b>🖌 Satire and grace in every stroke — Kalighat's brush never broke.</b><br> Originating from Kolkata, Kalighat paintings are known for their vibrant, expressive, and satirical style. These paintings often depict religious and mythological figures, as well as social and political themes, and are characterized by bold lines and minimalistic yet striking forms.</br>",
    "Saora Art": "<b>🌾 Symbols speak in Saora style — A tribal tale in every mile.</b><br> Originating from the Saora tribe in Odisha, Saora art is created using natural dyes and features intricate patterns that symbolize their connection to nature. These paintings often depict animals, birds, and trees, showcasing the tribe's reverence for their environment and its spiritual significance.</br>",
    "Gond Art": "<b>🌳 Trees that talk and dreams that fly — Gond art paints the forest sky.</b><br> This tribal art form from Madhya Pradesh is known for its vibrant colors and intricate patterns. Gond paintings often depict animals, birds, and the forces of nature, telling stories from the artists' dreams and spiritual beliefs.</br>",
    "Chitrakathi": "<b>📖 Epics sung with brush in hand — Chitrakathi brings myths to land.</b><br> A traditional art form from Maharashtra, Chitrakathi is a form of narrative painting that depicts mythological stories. The paintings are often accompanied by storytelling through song, bringing the ancient tales to life with vibrant colors and dynamic compositions.</br>",
    "Pattachitra": "<b>🎨 Silk of tales and gods divine — Pattachitra's lines entwine.</b><br> Originating from Odisha, Pattachitra paintings are known for their intricate details and religious themes. These paintings often depict Hindu deities, mythological stories, and temples, and are created on cloth or dried palm leaves, showcasing a unique blend of art and spirituality.</br>",
    "Patola Weaving": "<b>🧵 Double ikat, a woven spell — Patola's precision is hard to tell.</b><br> A traditional form of silk weaving from Gujarat, Patola is famous for its intricate double ikat technique. The art of creating these beautiful woven patterns requires immense skill, and the resulting fabric is known for its vivid colors and complex geometric designs.</br>",
    "Channapatna Toys": "<b>🪀 Wooden joy from Karnataka's core — Channapatna smiles in folklore.</b><br> A traditional craft from Karnataka, Channapatna toys are made from wood and feature vibrant colors. The craft involves a unique process of creating toys using the lathe machine, and the designs are often inspired by nature and folk traditions.</br>",
    "Kalamkari": "<b>✒️ Pen and plant dye draw the divine — Kalamkari tells stories in design.</b><br> A traditional art form from Andhra Pradesh, Kalamkari is a method of painting on fabric using natural dyes. The artwork often depicts mythological stories, divine beings, and scenes from Hindu epics, and the intricate designs are created with a bamboo pen.</br>",
    "Charkha Weaving": "<b>🧶 Spin the thread of swadeshi pride — Charkha weaves a soulful stride.</b><br> Popularized by Mahatma Gandhi during the Indian freedom struggle, Charkha weaving is a symbol of self-reliance and nationalism. The craft involves spinning cotton yarn into thread and has been revived as a symbol of sustainable living and the fight for independence.</br>"
}

st.markdown("""
<div class="narrative-text">
    🔍 Choose your path, dear traveler. Which realm of our cultural kingdom calls to your heart? 
    Perhaps the graceful dance forms that make gods weep with joy? Or the paintings that capture 
    the very essence of village life? Let the filters below guide your journey...
</div>
""", unsafe_allow_html=True)

# Filters
col1, col2 = st.columns(2)

with col1:
    selected_category = st.selectbox("🎨 Choose Your Art Realm", ['All'] + sorted(df['art_category'].unique()))
with col2:
    selected_state = st.selectbox("🗺️ Select Your Destination", ['All'] + sorted(df['LOCATION (STATE)'].unique()))

# Apply filters
filtered_df = df.copy()

if selected_category != 'All':
    filtered_df = filtered_df[filtered_df['art_category'] == selected_category]

if selected_state != 'All':
    filtered_df = filtered_df[filtered_df['LOCATION (STATE)'] == selected_state]

# Display cards with storytelling context
if filtered_df.empty:
    st.markdown("""
    <div class="narrative-text" style="color: #ff6b6b;">
        😔 Alas! The combination you seek exists only in dreams. Try a different path, dear explorer, 
        for there are many stories yet to be told...
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown(f"""
    <div class="narrative-text">
        ✨ Behold! Your journey reveals <strong>{len(filtered_df)}</strong> magnificent treasures. 
        Each card below holds a universe of stories, waiting for someone like you to discover their magic...
    </div>
    """, unsafe_allow_html=True)
    
    for i in range(0, len(filtered_df), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(filtered_df):
                row = filtered_df.iloc[i + j]
                art_name = row['ART FORM']
                image_name = art_name.lower().replace(" ", "").replace("/", "") + ".jpg"
                image_file = os.path.join(images_path, image_name)

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
                    <em>{art_descriptions.get(art_name, "🌟 A forgotten gem in India's cultural crown.")}</em>
                    </div>
                    """, unsafe_allow_html=True)
                    st.markdown("<div style='margin-bottom: 2rem;'></div>", unsafe_allow_html=True)

# --- Festival Section ---
st.markdown('<div class="chapter-title">Chapter II: The Calendar of Joy</div>', unsafe_allow_html=True)

st.markdown("""
<div class="narrative-text">
    As our first tale draws to a close, another chapter unfolds... In India, every month is a celebration, 
    every season a festival of colors, lights, and unending joy. These are not just dates on a calendar, 
    but moments when the entire soul of our nation dances in unison. Come, let us walk through this 
    calendar of eternal happiness...
</div>
""", unsafe_allow_html=True)
def display_image_from_url(url, placeholder_text="No Image Available"):
    """
    Display image from URL or show placeholder
    """
    try:
        if url and url.strip() and url.startswith(('http://', 'https://')):
            st.image(url.strip(), use_container_width=True)
        else:
            st.image(f"https://via.placeholder.com/300x200?text={placeholder_text.replace(' ', '+')}", 
                    use_container_width=True)
    except Exception as e:
        st.image(f"https://via.placeholder.com/300x200?text={placeholder_text.replace(' ', '+')}", 
                use_container_width=True)

def load_festivals():
    conn = get_snowflake_connection()
    # Updated query to include image URL column - adjust column name as needed
    query = "SELECT * FROM INDIAN_FESTIVALS"  
    df = pd.read_sql(query, conn)
    df.columns = df.columns.str.strip()
    conn.close()
    return df

festivals_df = load_festivals()

st.markdown("""
<div class="narrative-text">
    🎪 Which celebration calls to your spirit? The grand festivals that unite all of India, 
    or the intimate regional celebrations that make each state unique? Let your heart choose...
</div>
""", unsafe_allow_html=True)

# Filters for festivals
col3, col4 = st.columns(2)
with col3:
    unique_states = sorted(festivals_df['Location (State)'].unique())
    if 'PAN India' not in unique_states:
        unique_states.append('PAN India')
    selected_festival_state = st.selectbox("🏛️ Choose Your Festival Realm", ['All'] + unique_states)
with col4:
    selected_festival_month = st.selectbox("📅 Pick Your Celebratory MONTH", ['All'] + sorted(festivals_df['MONTH'].unique()))

# Apply festival filters
filtered_festivals = festivals_df.copy()
if selected_festival_state != 'All':
    filtered_festivals = filtered_festivals[filtered_festivals['Location (State)'] == selected_festival_state]
if selected_festival_month != 'All':
    filtered_festivals = filtered_festivals[filtered_festivals['MONTH'] == selected_festival_month]

# Display festival cards with storytelling context
if selected_festival_state == 'PAN India':
    st.markdown("""
    <div class="narrative-text">
        🇮🇳 Ah, you've chosen the festivals that bind our entire nation in celebration! 
        These are the moments when from Kashmir to Kanyakumari, every heart beats as one...
    </div>
    """, unsafe_allow_html=True)
elif selected_festival_state == 'All':
    st.markdown("""
    <div class="narrative-text">
        🌈 You wish to witness the complete tapestry of our celebrations! From intimate village 
        gatherings to grand national festivities, here lies the full spectrum of Indian joy...
    </div>
    """, unsafe_allow_html=True)

if filtered_festivals.empty:
    st.markdown("""
    <div class="narrative-text" style="color: #ff6b6b;">
        💫 The stars have not aligned for this combination, dear seeker. Perhaps try another 
        time or place, for festivals are everywhere in our magical land...
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown(f"""
    <div class="narrative-text">
        🎊 Your quest reveals <strong>{len(filtered_festivals)}</strong> celebrations of pure joy! 
        Each festival below is a doorway to understanding the heart and soul of India...
    </div>
    """, unsafe_allow_html=True)
    
    # Modified festival cards display with URL images
    for i in range(0, len(filtered_festivals), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(filtered_festivals):
                fest = filtered_festivals.iloc[i + j]
                with cols[j]:
                    st.markdown(f"""
                        <div class="card">
                    <h4>{fest['FESTIVAL']}</h4>
                    """, unsafe_allow_html=True)

                    # Display festival image from URL - Replace 'IMAGE_URL' with your actual column name
                    festival_image_url = fest.get('image_path', '')  # Replace 'IMAGE_URL' with your actual column name
                    display_image_from_url(festival_image_url, "Festival+Image")

                    st.markdown(f"""
                    <p><b>📍 State:</b> {fest['Location (State)']}</p>
                    <p><b>🗓 Month:</b> {fest['MONTH']}</p>
                    <p>{fest['DESCRIPTION']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    st.markdown("<div style='margin-bottom: 2rem;'></div>", unsafe_allow_html=True)

# Storytelling Conclusion
st.markdown("""
<div class="story-intro" style="margin-top: 50px;">
    <h2 style="color: #ffd93d; margin-bottom: 20px;">🌅 The Story Continues...</h2>
    <p class="narrative-text">
        And so, dear traveler, our journey through the enchanted realms of Indian culture draws to a pause, 
        but never to an end. For every art form you've discovered holds a thousand untold stories, 
        and every festival carries the dreams of millions. Take these treasures with you, 
        and perhaps... just perhaps... you too will become a guardian of these beautiful traditions.
    </p>
    <p class="narrative-text" style="color: #ff6b6b; font-weight: bold;">
        Remember: Every time you share these stories, a dying art form gains another breath of life. ✨
    </p>
</div>
""", unsafe_allow_html=True)
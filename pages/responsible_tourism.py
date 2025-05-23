import streamlit as st
import pandas as pd
import base64
import snowflake.connector

# Set page configuration
st.set_page_config(page_title="Responsible Tourism", layout="wide", initial_sidebar_state="collapsed")

# Background image path
image_path = "Responsible_Tourism/images/main2.png"

# Convert image to base64
def get_base64_image(img_path):
    with open(img_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Encode and set as background with white overlay (reduced transparency)
encoded_bg = get_base64_image(image_path)
st.markdown(
    f"""
    <style>
        .stApp {{
            background: 
                linear-gradient(rgba(255, 255, 255, 0.75), rgba(255, 255, 255, 0.1)),
                url("data:image/jpg;base64,{encoded_bg}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
    </style>
    """,
    unsafe_allow_html=True
)

# Title with black font color
st.markdown(
    "<h1 style='color: black;'>🌿 Responsible Tourism Tips</h1>",
    unsafe_allow_html=True
)

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

# Define card style with light black background
card_styles = {
    "background": "rgba(0, 0, 0, 0.6)",  # Light black background
    "text_color": "#FFFFFF",
    "border_radius": "15px",
    "padding": "20px",
    "box_shadow": "0 4px 8px rgba(0,0,0,0.3)",
}

# Display in two columns
cols = st.columns(2)

for i, category in enumerate(categories):
    with cols[i % 2]:
        tips = tips_df[tips_df['CATEGORY'] == category]['TIP'].tolist()
        with st.container():
            st.markdown(
                f"""
                <div style="
                    background-color:{card_styles['background']};
                    padding:{card_styles['padding']};
                    border-radius:{card_styles['border_radius']};
                    box-shadow:{card_styles['box_shadow']};
                    margin-bottom:20px;
                    min-height: 320px;
                    display: flex;
                    flex-direction: column;
                    justify-content: space-between;
                ">
                    <h3 style="color:#f9c74f;">📋 {category}</h3>
                    <ul style="color:{card_styles['text_color']}; font-size:18px; font-weight:bold;">
                        {''.join([f"<li>{tip}</li>" for tip in tips])}
                    </ul>
                </div>
                """,
                unsafe_allow_html=True
            )

# Spacer
st.markdown("<br><br><br>", unsafe_allow_html=True)

# Centered forward button
col = st.columns([1])[0]
with col:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style="display: flex; justify-content: center; margin-top: 30px;">
        <a href="/Info_tips" target="_self">
        <button style="background-color:#f9c74f; border:none; border-radius:50%; 
        padding:15px 20px; font-size:20px; font-weight:bold; color:#262730; 
        cursor:pointer; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);">➡</button>
        </a>
        </div>
        """,
        unsafe_allow_html=True
    )
import streamlit as st
import pandas as pd
import pydeck as pdk
import os

# Page config
st.set_page_config(page_title="Heritage Sites of India", layout="wide")

# Title
st.title("🏰 Heritage Sites of India")

# Load temple and fort data
temple_csv_path = os.path.join("data1", "Dataset_Temples.csv")
fort_csv_path = os.path.join("data1", "Dataset_Forts.csv")

# Check if files exist
if not os.path.exists(temple_csv_path) or not os.path.exists(fort_csv_path):
    st.error("❌ One or both datasets not found. Please check the paths.")
    st.stop()

# Read datasets
temple_df = pd.read_csv(temple_csv_path)
fort_df = pd.read_csv(fort_csv_path)

# Clean and convert coordinates
temple_df['Latitude'] = pd.to_numeric(temple_df['Latitude'], errors='coerce')
temple_df['Longitude'] = pd.to_numeric(temple_df['Longitude'], errors='coerce')
fort_df['Latitude'] = pd.to_numeric(fort_df['Latitude'], errors='coerce')
fort_df['Longitude'] = pd.to_numeric(fort_df['Longitude'], errors='coerce')
temple_df.dropna(subset=['Latitude', 'Longitude'], inplace=True)
fort_df.dropna(subset=['Latitude', 'Longitude'], inplace=True)

# Add type columns
temple_df['Type'] = 'Temples'
fort_df['Type'] = 'Forts'

# Combine data
df = pd.concat([temple_df, fort_df], ignore_index=True)

# Filter section
col1, col2 = st.columns(2)
with col1:
    heritage_types = ["All", "Temples", "Forts"]
    selected_type = st.selectbox("Select Heritage Type", heritage_types)

with col2:
    states = ["All"] + sorted(df['State'].unique())
    selected_state = st.selectbox("Select a State", states)

# Apply filters
filtered_df = df.copy()
if selected_type != "All":
    filtered_df = filtered_df[filtered_df['Type'] == selected_type]
if selected_state != "All":
    filtered_df = filtered_df[filtered_df['State'] == selected_state]

# Highlight only selected state markers brightly; dim others
df['is_highlight'] = 1
if selected_state != "All":
    df['is_highlight'] = df['State'].apply(lambda x: 255 if x == selected_state else 60)
else:
    df['is_highlight'] = 255

# Map layer with brightness control
layer = pdk.Layer(
    "ScatterplotLayer",
    data=df,
    get_position='[Longitude, Latitude]',
    get_radius=5000,
    get_fill_color='[255, 0, 0, is_highlight]',  # Alpha controls visibility
    pickable=True
)

# Tooltip
tooltip = {
    "html": "<b>{Name}</b><br/>{State}",
    "style": {
        "backgroundColor": "black",
        "color": "white"
    }
}

# View state — transition to selected state
if selected_state != "All":
    focus_df = df[df['State'] == selected_state]
    latitude = focus_df['Latitude'].mean()
    longitude = focus_df['Longitude'].mean()
    zoom = 6
else:
    latitude = 22.9734  # Center of India
    longitude = 78.6569
    zoom = 4.5

view_state = pdk.ViewState(
    latitude=latitude,
    longitude=longitude,
    zoom=zoom,
    pitch=0,
    transition_duration=1000  # Smooth transition
)

# Render the map
st.pydeck_chart(pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v10",
    initial_view_state=view_state,
    layers=[layer],
    tooltip=tooltip
))
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from folium import IFrame
import os

# Config
st.set_page_config(page_title="Heritage Sites of India", layout="wide")
st.title("🏰 Heritage Sites of India")

# Load datasets
temple_path = os.path.join("Datasets", "Dataset_Temples.csv")
fort_path = os.path.join("Datasets", "Dataset_Forts.csv")

# Check files
if not os.path.exists(temple_path) or not os.path.exists(fort_path):
    st.error("❌ Dataset not found!")
    st.stop()

temples = pd.read_csv(temple_path)
forts = pd.read_csv(fort_path)

# Clean and add type
for df, label in [(temples, "Temples"), (forts, "Forts")]:
    df["Latitude"] = pd.to_numeric(df["Latitude"], errors="coerce")
    df["Longitude"] = pd.to_numeric(df["Longitude"], errors="coerce")
    df.dropna(subset=["Latitude", "Longitude"], inplace=True)
    df["Type"] = label

# Combine
df = pd.concat([temples, forts], ignore_index=True)

# Main Page Filters
st.markdown("### 🔍 Filter Sites")
col1, col2 = st.columns(2)
with col1:
    type_filter = st.selectbox("Select Type", ["All", "Temples", "Forts"])
with col2:
    state_filter = st.selectbox("Select State", ["All"] + sorted(df["State"].dropna().unique()))

# Apply Filters
filtered_df = df.copy()
if type_filter != "All":
    filtered_df = filtered_df[filtered_df["Type"] == type_filter]
if state_filter != "All":
    filtered_df = filtered_df[filtered_df["State"] == state_filter]

# Create Map
if not filtered_df.empty:
    center_lat = filtered_df["Latitude"].mean()
    center_lon = filtered_df["Longitude"].mean()
    m = folium.Map(location=[center_lat, center_lon], zoom_start=6, tiles="CartoDB positron")
else:
    m = folium.Map(location=[22.9734, 78.6569], zoom_start=4.5, tiles="CartoDB positron")
    st.warning("No sites found with selected filters.")

# Add markers with popup using IFrame for images
for _, row in filtered_df.iterrows():
    name = row["Name"]
    desc = str(row.get("Description", ""))[:150] + "..."
    state = row["State"]
    url = row.get("URL", "#")
    img_url = row.get("ImageURL", "")

    if img_url:
        html = f"""
        <div style="width:240px">
            <h4>{name}</h4>
            <img src="{img_url}" width="230" style="margin-bottom:10px;"><br>
            <p><b>State:</b> {state}</p>
            <p>{desc}</p>
            <a href="{url}" target="_blank">🔗 Read More</a>
        </div>
        """
    else:
        html = f"""
        <div style="width:240px">
            <h4>{name}</h4>
            <p><b>State:</b> {state}</p>
            <p>{desc}</p>
            <a href="{url}" target="_blank">🔗 Read More</a>
        </div>
        """

    iframe = IFrame(html, width=250, height=300)
    popup = folium.Popup(iframe, max_width=300)

    folium.Marker(
        location=[row["Latitude"], row["Longitude"]],
        popup=popup,
        tooltip=name,
        icon=folium.Icon(color="blue" if row["Type"] == "Temples" else "green", icon="info-sign")
    ).add_to(m)

# Display map
st_data = st_folium(m, width=1200, height=600)

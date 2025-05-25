import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import base64
import snowflake.connector
import os

st.set_page_config(page_title="Tourism Trends", layout="wide")

# ----------- Function to encode image to base64 -----------
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# ----------- Encode background image -----------
img_path = "Tourism_trends/assets/image.png"
img_base64 = get_base64_of_bin_file(img_path)

# ----------- Custom CSS with Witching Hour gradient background -----------
st.markdown(
    f"""
    <style>
    .stApp {{
        /* Witching Hour gradient background */
        background: linear-gradient(135deg, #200122, #6f0000);
        color: #eee;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        min-height: 100vh;
    }}
    /* Hide hamburger menu and footer if needed */
    .css-1d391kg {{ display: none; }}

    /* Content padding */
    .css-18e3th9 {{ padding-left: 2rem; padding-right: 2rem; }}

    /* Text colors */
    .css-10trblm, .css-1v0mbdj {{ color: #eee !important; }}

    /* Make plotly background transparent */
    .js-plotly-plot {{ background-color: transparent !important; }}

    /* Heading with background image */
    .heading-bg {{
        position: relative;
        height: 150px;
        display: flex;
        justify-content: center;
        align-items: center;
        color: white;
        font-size: 2.5em;
        font-weight: bold;
        text-shadow: 2px 2px 6px rgba(0,0,0,0.7);
        border-radius: 10px;
        margin-bottom: 1rem;
        overflow: hidden;
    }}
    .heading-bg::before {{
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background-image: url("data:image/png;base64,{img_base64}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        opacity: 0.3;
        z-index: 0;
        border-radius: 10px;
    }}
    .heading-bg > * {{ position: relative; z-index: 1; }}

    /* Form inputs styling */
    div[role="listbox"] > div,
    div[role="combobox"] > div > input,
    div[role="combobox"] > div > div,
    label,
    input, select, textarea,
    .stCheckbox > label > div,
    .stRadio > label > div,
    button {{
        color: #eee !important;
        background-color: #3b2c2c !important;
        border: 1px solid #666;
        border-radius: 4px;
    }}

    /* Placeholder color */
    ::placeholder {{ color: #bbb !important; opacity: 1; }}

    /* Link color */
    a {{ color: #ffa726 !important; }}

    /* Matplotlib figure background */
    .stPlotlyChart > div > div > div svg {{
        background: transparent !important;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# ----------- Heading with Background Image -----------
st.markdown(
    """
    <div class="heading-bg">
        📊 Tourism Trends in India
    </div>
    """,
    unsafe_allow_html=True
)

# ----------- Load Data from Snowflake -----------
@st.cache_data
def load_data_from_snowflake():
    conn = snowflake.connector.connect(
        user=st.secrets["snowflake"]["user"],
        password=st.secrets["snowflake"]["password"],
        account=st.secrets["snowflake"]["account"],
        warehouse=st.secrets["snowflake"]["warehouse"],
        database=st.secrets["snowflake"]["database"],
        schema=st.secrets["snowflake"]["schema"]
    )
    footfall_query = "SELECT * FROM FOOTFALL_ALL_INDIA"
    culture_query = "SELECT * FROM CULTURAL_RICHNESS_ALL_INDIA"
    footfall_df = pd.read_sql(footfall_query, conn)
    culture_df = pd.read_sql(culture_query, conn)
    conn.close()
    return footfall_df, culture_df

footfall_df, culture_df = load_data_from_snowflake()
footfall_df['STATE'] = footfall_df['STATE'].str.strip()
culture_df['STATE'] = culture_df['STATE'].str.strip()

month_order = ['January', 'February', 'March', 'April', 'May', 'June',
               'July', 'August', 'September', 'October', 'November', 'December']
footfall_df['MONTH'] = pd.Categorical(footfall_df['MONTH'], categories=month_order, ordered=True)

# ----------- Intro -----------
st.markdown("""
Namaste! 🙏 Welcome to the India Tourism Trends Dashboard – your interactive travel compass 🧭.

Here you’ll find:
- 📈 Trends in tourist footfall
- 🌡 Seasonal insights with heatmaps
- 🥧 State-specific tourist composition
- 🛤 Suggested tourist circuits
""")

# ----------- Filters -----------
st.markdown("### 🔍 Filter Data")
states = st.selectbox("🗺 Select State", sorted(footfall_df['STATE'].unique()))
years = st.selectbox("📅 Select Year", sorted(footfall_df['YEAR'].unique()))
filtered_df = footfall_df[(footfall_df['STATE'] == states) & (footfall_df['YEAR'] == years)].copy()
filtered_df['TOTAL'] = filtered_df['DOMESTIC'] + filtered_df['FOREIGN']

# ----------- Line Chart -----------
st.subheader("📈 Monthly Tourist Footfall (Domestic & International)")
line_data = filtered_df.groupby(['MONTH'])[['DOMESTIC', 'FOREIGN']].sum().reset_index().sort_values('MONTH')
fig_line = px.line(line_data, x='MONTH', y=['DOMESTIC', 'FOREIGN'],
                   labels={'value': 'Tourist Count', 'variable': 'Tourist Type'},
                   markers=True, title="Monthly Tourist Trends")
st.plotly_chart(fig_line, use_container_width=True)

# ----------- Heatmap -----------
st.subheader("🌡 Seasonality Heatmap")
st.markdown(f"""
Compare {states} across multiple years to discover recurring patterns 📊.  
This helps with forecasting and understanding how tourism reacts to seasons 🌦 or external events 🦠.
""")

state_df = footfall_df[footfall_df['STATE'] == states].copy()
state_df['TOTAL'] = state_df['DOMESTIC'] + state_df['FOREIGN']
heatmap_data = state_df.groupby(['YEAR', 'MONTH'], as_index=False)['TOTAL'].sum()
heatmap_pivot = heatmap_data.pivot(index='MONTH', columns='YEAR', values='TOTAL')
heatmap_pivot = heatmap_pivot.reindex(month_order).fillna(0)
fig, ax = plt.subplots(figsize=(12, 7))
sns.heatmap(heatmap_pivot, cmap="YlOrRd", annot=True, fmt=".0f", linewidths=0.5, ax=ax)
ax.set_title(f"Seasonality Heatmap for {states}", color="#eee")
ax.tick_params(colors='#eee', rotation=45)
plt.yticks(rotation=0)
st.pyplot(fig)

# ----------- Heatmap Explanation -----------
st.markdown(f"""
#### 🔍 What the Heatmap Tells You:
- Darker shades represent months with higher tourist numbers 📈.
- Spot seasonal patterns like winters, festivals, or school holidays.
- Detect outliers like dips during lockdowns or boosts from campaigns 🧭.
- Use insights to plan marketing strategies or forecast infrastructure needs 🚧.
""")



# ----------- Pie Chart -----------
st.subheader("🥧 Domestic vs Foreign Tourists")

st.markdown(f"""
Understand the tourist mix in {states} for {years}.  
This pie chart gives quick insights on how to balance marketing efforts 🎯 between local explorers and global travelers.
""")

totals = filtered_df[['DOMESTIC', 'FOREIGN']].sum()
fig_pie = px.pie(values=totals, names=totals.index,
                 title="Proportion of Domestic and Foreign Tourists",
                 color_discrete_sequence=px.colors.sequential.RdBu)
st.plotly_chart(fig_pie, use_container_width=True)

# ----------- Tourist Circuit Suggestions -----------
st.subheader("🛤 Suggested Tourist Circuits")

st.markdown("""
Why visit just one destination when you can experience a journey of discovery? ✨  
These curated multi-destination circuits combine culture, climate, and geography for unforgettable travel adventures 🚂.

Explore sample 3–5 day circuits below. Ideal for both tourists and travel planners!
""")


assets_path = os.path.join("Tourism_trends", "assets")

# Encode all circuit images
circuit_images = {
    "golden_triangle": get_base64_of_bin_file(os.path.join(assets_path, "golden_triangle.png")),
    "eastern_explorer": get_base64_of_bin_file(os.path.join(assets_path, "eastern_explorer.png")),
    "himalayan_heritage": get_base64_of_bin_file(os.path.join(assets_path, "himalayan_heritage.png")),
    "southern_spice_trail": get_base64_of_bin_file(os.path.join(assets_path, "southern_spice_trail.png")),
    "cultural_karnataka": get_base64_of_bin_file(os.path.join(assets_path, "cultural_karnataka.png")),
}

circuits = {
    "🟡 Golden Triangle": {
        "States": "Delhi → Agra → Jaipur",
        "Highlights": "Taj Mahal, Red Fort, Amber Palace, local bazaars 🕌",
        "Best Time": "October to March ❄",
        "Image": circuit_images["golden_triangle"]
    },
    "🌿 Eastern Explorer": {
        "States": "Kolkata → Bhubaneswar → Puri → Konark",
        "Highlights": "Jagannath Temple, Sun Temple, Chilika Lake 🐬",
        "Best Time": "November to February",
        "Image": circuit_images["eastern_explorer"]
    },
    "🏞 Himalayan Heritage": {
        "States": "Shimla → Manali → Dharamshala",
        "Highlights": "Snow peaks, monasteries, rivers, apple orchards 🍎",
        "Best Time": "April to June & October",
        "Image": circuit_images["himalayan_heritage"]
    },
    "🌺 Southern Spice Trail": {
        "States": "Kochi → Munnar → Thekkady → Alleppey",
        "Highlights": "Backwaters, tea estates, wildlife sanctuaries 🐘",
        "Best Time": "September to March",
        "Image": circuit_images["southern_spice_trail"]
    },
    "🎨 Cultural Karnataka": {
        "States": "Hampi → Badami → Pattadakal → Aihole",
        "Highlights": "UNESCO temples, rock-cut architecture ⛩",
        "Best Time": "October to February",
        "Image": circuit_images["cultural_karnataka"]
    }
}

selected_circuit = st.selectbox("📌 Select a Tourist Circuit", list(circuits.keys()))
info = circuits[selected_circuit]

st.markdown(
    f"""
    <style>
    .tourist-card:hover {{
        transform: scale(1.02) perspective(1000px) rotateX(1deg) rotateY(-1deg);
    }}
    </style>

    <div class="tourist-card" style="
        display: flex;
        flex-direction: row;
        flex-wrap: wrap;
        align-items: center;
        justify-content: center;
        background-color: #ffffff10;
        border-radius: 20px;
        box-shadow: 0 12px 24px rgba(0, 0, 0, 0.25);
        padding: 20px;
        margin-top: 30px;
        backdrop-filter: blur(6px);
        max-width: 1000px;
        margin-left: auto;
        margin-right: auto;
    ">
        <img src="data:image/png;base64,{info['Image']}" alt="Circuit Map" style="max-width: 300px; border-radius: 12px; margin: 10px;">
        <div style="flex: 1 1 300px; color: #f0f0f0; padding: 10px; max-width: 600px;">
            <h2 style="margin-top: 0;">{selected_circuit}</h2>
            <p style="font-size: 16px; line-height: 1.6;">
                <b>🗺 States Covered:</b> {info['States']}<br>
                <b>📸 Highlights:</b> {info['Highlights']}<br>
                <b>📅 Best Time to Visit:</b> {info['Best Time']}
            </p>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# ----------- Monthly Travel Suggestions -----------
st.subheader("🗓 Best Places to Visit by Month")

st.markdown("""
No matter the month, India has magic waiting for you ✨  
Pick a month to see tailored recommendations based on festivals, climate, and regional culture.
""")

recommendations = pd.DataFrame({
    "Month": month_order,
    "Recommended Places": [
        "Rajasthan, Gujarat, Kerala",
        "Goa, Tamil Nadu, Punjab",
        "Varanasi, Mathura, West Bengal",
        "Himachal Pradesh, Uttarakhand, Kerala",
        "Sikkim, Northeast, Ladakh",
        "Kerala, Goa, Odisha",
        "Leh-Ladakh, Rajasthan, Gujarat",
        "Himachal Pradesh, Jammu & Kashmir, Assam",
        "Kashmir, Himachal, Rajasthan",
        "Delhi, Uttar Pradesh, Punjab",
        "Goa, Rajasthan, Karnataka",
        "Kerala, Tamil Nadu, Gujarat"
    ]
})
month_sel = st.selectbox("Select Month for Travel Recommendations", month_order)
rec_place = recommendations[recommendations['Month'] == month_sel]['Recommended Places'].values[0]
st.markdown(f"### Places recommended in {month_sel}: {rec_place}")


# ----------- Download filtered footfall data -----------
def convert_df_to_csv(df):
    return df.to_csv(index=False).encode('utf-8')

csv_data = convert_df_to_csv(filtered_df)
st.download_button(label="⬇ Download Filtered Footfall Data as CSV",
                   data=csv_data,
                   file_name=f"footfall_{states}_{years}.csv",
                   mime='text/csv')

# ----------- Footer -----------
st.markdown("""
---
Tourism_trends
""")
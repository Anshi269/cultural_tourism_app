import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import base64

st.set_page_config(page_title="Tourism Trends", layout="wide")

# ----------- Function to encode image to base64 -----------
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# ----------- Encode your background image -----------
img_path = "data/image.png"  # Change path if needed
img_base64 = get_base64_of_bin_file(img_path)

# ----------- Custom CSS with base64 image background and opacity -----------
st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: #1a0b0b;  /* cherry black */
        color: #eee;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }}
    .css-1d391kg {{
        display: none;
    }}
    .css-18e3th9 {{
        padding-left: 2rem;
        padding-right: 2rem;
    }}
    .css-10trblm, .css-1v0mbdj {{
        color: #eee;
    }}
    .js-plotly-plot {{
        background-color: transparent !important;
    }}
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
        opacity: 0.3;  /* Decrease this for more transparency */
        z-index: 0;
        border-radius: 10px;
    }}
    .heading-bg > * {{
        position: relative;
        z-index: 1;
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

# ----------- Load Data -----------
@st.cache_data
def load_data():
    footfall_df = pd.read_csv("data/footfall_all_india.csv")
    culture_df = pd.read_csv("data/cultural_richness_all_india.csv")
    return footfall_df, culture_df

footfall_df, culture_df = load_data()
footfall_df['State'] = footfall_df['State'].str.strip()
culture_df['State'] = culture_df['State'].str.strip()
footfall_df = footfall_df.copy()

# Month order for sorting
month_order = ['January', 'February', 'March', 'April', 'May', 'June',
               'July', 'August', 'September', 'October', 'November', 'December']
footfall_df['Month'] = pd.Categorical(footfall_df['Month'], categories=month_order, ordered=True)

# ----------- Intro -----------
st.markdown("""
Namaste! 🙏 Welcome to the **India Tourism Trends Dashboard** – your interactive travel compass 🧭 for understanding where, when, and how people explore this incredible country 🇮🇳.

Here you’ll find:
- 📈 Trends in tourist footfall (domestic vs foreign)
- 🌡️ Seasonal insights with heatmaps
- 🥧 State-specific tourist composition
- 🛤️ Suggested tourist circuits to elevate travel plans

Use the filters below to begin your journey of exploration! ✨
""")

# ----------- Filters -----------
st.markdown("### 🔍 Filter Data")
states = st.selectbox("🗺️ Select State", sorted(footfall_df['State'].unique()))
years = st.selectbox("📅 Select Year", sorted(footfall_df['Year'].unique()))

filtered_df = footfall_df[(footfall_df['State'] == states) & (footfall_df['Year'] == years)].copy()
filtered_df['Total'] = filtered_df['Domestic'] + filtered_df['Foreign']

# ----------- Line Chart -----------
st.subheader("📈 Monthly Tourist Footfall (Domestic & International)")
st.markdown(f"""
Explore how tourist footfall in **{states}** varies month-to-month.  
Look for seasonal spikes, festival peaks 🎉, or off-season dips 💤 to plan or market travel efficiently.
""")

line_data = filtered_df.groupby(['Month'])[['Domestic', 'Foreign']].sum().reset_index().sort_values('Month')
fig_line = px.line(line_data, x='Month', y=['Domestic', 'Foreign'],
                   labels={'value': 'Tourist Count', 'variable': 'Tourist Type'},
                   markers=True, title="Monthly Tourist Trends")
st.plotly_chart(fig_line, use_container_width=True)

# ----------- Heatmap -----------
st.subheader("🌡️ Seasonality Heatmap")
st.markdown(f"""
Compare **{states}** across multiple years to discover recurring patterns 📊.  
This helps with forecasting and understanding how tourism reacts to seasons 🌦️ or external events 🦠.
""")

state_df = footfall_df[footfall_df['State'] == states].copy()
state_df['Total'] = state_df['Domestic'] + state_df['Foreign']
heatmap_data = state_df.groupby(['Year', 'Month'], as_index=False)['Total'].sum()
heatmap_pivot = heatmap_data.pivot(index='Month', columns='Year', values='Total')
heatmap_pivot = heatmap_pivot.reindex(month_order).fillna(0)

fig, ax = plt.subplots(figsize=(12, 7))
sns.heatmap(heatmap_pivot, cmap="YlOrRd", annot=True, fmt=".0f", linewidths=0.5, ax=ax)
ax.set_title(f"Seasonality Heatmap for {states}")
ax.set_ylabel("Month")
ax.set_xlabel("Year")
st.pyplot(fig)

# ----------- Heatmap Explanation -----------
st.markdown(f"""
#### 🔍 What the Heatmap Tells You:
- **Darker shades** represent months with higher tourist numbers 📈.
- Spot **seasonal patterns** like winters, festivals, or school holidays.
- Detect **outliers** like dips during lockdowns or boosts from campaigns 🧭.
- Use insights to plan **marketing strategies** or forecast infrastructure needs 🚧.
""")

# ----------- Pie Chart -----------
st.subheader("🥧 Domestic vs Foreign Tourists")
st.markdown(f"""
Understand the tourist mix in **{states}** for **{years}**.  
This pie chart gives quick insights on how to balance marketing efforts 🎯 between **local explorers** and **global travelers**.
""")

totals = filtered_df[['Domestic', 'Foreign']].sum()
fig_pie = px.pie(values=totals, names=totals.index,
                 title="Proportion of Domestic and Foreign Tourists",
                 color_discrete_sequence=px.colors.sequential.RdBu)
st.plotly_chart(fig_pie, use_container_width=True)

# ----------- Tourist Circuit Suggestions -----------
st.subheader("🛤️ Suggested Tourist Circuits")
st.markdown("""
Why visit just one destination when you can experience **a journey of discovery**? ✨  
These curated **multi-destination circuits** combine culture, climate, and geography for unforgettable travel adventures 🚂.

Explore sample 3–5 day circuits below. Ideal for both tourists and travel planners!
""")

circuits = {
    "🟡 Golden Triangle": {
        "States": "Delhi → Agra → Jaipur",
        "Highlights": "Taj Mahal, Red Fort, Amber Palace, local bazaars 🕌",
        "Best Time": "October to March ❄️"
    },
    "🌿 Eastern Explorer": {
        "States": "Kolkata → Bhubaneswar → Puri → Konark",
        "Highlights": "Jagannath Temple, Sun Temple, Chilika Lake 🐬",
        "Best Time": "November to February"
    },
    "🏞️ Himalayan Heritage": {
        "States": "Shimla → Manali → Dharamshala",
        "Highlights": "Snow peaks, monasteries, rivers, apple orchards 🍎",
        "Best Time": "April to June & October"
    },
    "🌺 Southern Spice Trail": {
        "States": "Kochi → Munnar → Thekkady → Alleppey",
        "Highlights": "Backwaters, tea estates, wildlife sanctuaries 🐘",
        "Best Time": "September to March"
    },
    "🎨 Cultural Karnataka": {
        "States": "Hampi → Badami → Pattadakal → Aihole",
        "Highlights": "UNESCO temples, rock-cut architecture ⛩️",
        "Best Time": "October to February"
    }
}

selected_circuit = st.selectbox("📌 Select a Tourist Circuit", list(circuits.keys()))
info = circuits[selected_circuit]

st.markdown(f"""
### {selected_circuit}

**States Covered:** {info["States"]}  
**Highlights:** {info["Highlights"]}  
**Best Time to Visit:** {info["Best Time"]}
""")

# ----------- Monthly Travel Suggestions -----------
st.subheader("🗓️ Best Places to Visit by Month")
st.markdown("""
No matter the month, **India has magic waiting for you** ✨  
Pick a month to see **tailored recommendations** based on festivals, climate, and regional culture.
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

month_sel = st.selectbox("Select Month", month_order)
rec_places = recommendations.loc[recommendations['Month'] == month_sel, 'Recommended Places'].values[0]

st.markdown(f"**Best Places to Visit in {month_sel}:** {rec_places}")

# ----------- Footer -----------
st.markdown("""
---
Developed by 🇮🇳 Tourism Insights Team | Data Source: Govt. of India | © 2025  
""")

import streamlit as st
import pandas as pd
import plotly.express as px
import base64

# --------------------- SETUP ---------------------

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background():
    cherry_black = "#2E1A1A"

    img_file = "data/image.jpg"
    img_base64 = get_base64_of_bin_file(img_file)

    st.markdown(
        f"""
        <style>
            .stApp {{
                background-color: {cherry_black};
                color: white;
                font-family: 'Segoe UI', sans-serif;
                padding: 0;
            }}
            .stMetric label {{
                color: #ffffff;
            }}
            h1, h2, h3, .stSubheader {{
                color: #F5CBA7;
            }}
            .block-container {{
                padding: 0 2rem;
                max-width: 100%;
            }}
            .main > div {{
                padding-top: 20px;
            }}
            .header-container {{
                position: relative;
                text-align: center;
                color: white;
                background-image: url("data:image/jpg;base64,{img_base64}");
                background-size: cover;
                background-position: center;
                padding: 60px 20px;
                border-radius: 12px;
                overflow: hidden;
            }}
            /* Overlay with opacity */
            .header-container::before {{
                content: "";
                position: absolute;
                top: 0; left: 0; right: 0; bottom: 0;
                background-color: rgba(0, 0, 0, 0.5); /* black with 50% opacity */
                z-index: 0;
                border-radius: 12px;
            }}
            /* Ensure text is above overlay */
            .header-container > * {{
                position: relative;
                z-index: 1;
            }}
            .header-container h1 {{
                font-size: 48px;
                margin: 0;
                color: #ffffff;
                text-shadow: 2px 2px 4px #000000;
            }}
            .header-container p {{
                font-size: 20px;
                margin-top: 10px;
                color: #f0f0f0;
                text-shadow: 1px 1px 2px #000000;
            }}
        </style>
        """,
        unsafe_allow_html=True
    )

# --------------------- LOAD DATA ---------------------

@st.cache_data
def load_data():
    sites_df = pd.read_csv("data/heritage_sites.csv")
    footfall_df = pd.read_csv("data/footfall_tourism.csv")
    endangered_df = pd.read_csv("data/endangered_art_forms.csv")
    budget_df = pd.read_csv("data/art_culture_budget.csv")
    return sites_df, footfall_df, endangered_df, budget_df

# --------------------- VISUAL COMPONENTS ---------------------

def display_metrics(sites_df, footfall_df, endangered_df):
    total_sites = len(sites_df)

    footfall_cols = [col for col in footfall_df.columns if col.lower() in ['total', 'footfall', 'visitors', 'count']]
    if footfall_cols:
        total_footfall = footfall_df[footfall_cols[0]].sum()
    else:
        numeric_cols = footfall_df.select_dtypes(include='number').columns
        total_footfall = footfall_df[numeric_cols].sum().sum()

    endangered_total = len(endangered_df)

    col1, col2, col3 = st.columns(3)
    col1.metric("🏛 Cultural Sites", total_sites)
    col2.metric("👣 Tourist Footfall", f"{int(total_footfall):,}")
    col3.metric("🎭 Endangered Art Forms", endangered_total)

def convert_coord(coord_str):
    if pd.isnull(coord_str):
        return None
    coord_str = str(coord_str).strip().replace('°', '')
    if coord_str[-1] in ['N', 'E']:
        return float(coord_str[:-1])
    elif coord_str[-1] in ['S', 'W']:
        return -float(coord_str[:-1])
    else:
        return float(coord_str)

def cultural_hotspots_map(sites_df):
    st.subheader("🗺 Cultural Hotspots in India")

    state_filter = st.selectbox("📍 Select a State", ["All States"] + sorted(sites_df["LOCATION (STATE)"].dropna().unique()))
    
    if state_filter == "All States":
        filtered_sites = sites_df
    else:
        filtered_sites = sites_df[sites_df["LOCATION (STATE)"] == state_filter]

    filtered_sites["LATITUDE"] = filtered_sites["LATITUDE"].apply(convert_coord)
    filtered_sites["LONGITUDE"] = filtered_sites["LONGITUDE"].apply(convert_coord)

    # Adaptive zoom
    if len(filtered_sites) == 1:
        zoom_level = 10
    elif state_filter != "All States":
        zoom_level = 5
    else:
        zoom_level = 4

    fig = px.scatter_mapbox(
        filtered_sites,
        lat="LATITUDE",
        lon="LONGITUDE",
        hover_name="SITE NAME",
        hover_data=["LOCATION (STATE)", "YEAR LISTED"],
        zoom=zoom_level,
        height=500
    )
    fig.update_layout(mapbox_style="open-street-map", margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig, use_container_width=True)


def budget_chart(budget_df):
    st.subheader("💰 Cultural Budget Over the Years")

    budget_long = budget_df.melt(id_vars='State/UT', var_name='Year', value_name='Budget_Allocation_Crore')
    budget_summary = budget_long.groupby('Year')['Budget_Allocation_Crore'].sum().reset_index()

    fig = px.bar(
        budget_summary,
        x="Year",
        y="Budget_Allocation_Crore",
        text="Budget_Allocation_Crore",
        labels={"Budget_Allocation_Crore": "Budget (₹ Cr)"},
        height=400,
        color_discrete_sequence=["#F1948A"]
    )
    fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig.update_layout(yaxis_tickprefix="₹", xaxis_title="Year", plot_bgcolor="#2E1A1A", paper_bgcolor="#2E1A1A")
    st.plotly_chart(fig, use_container_width=True)

# --------------------- MAIN DASHBOARD ---------------------

def run_dashboard():
    set_background()

    # Custom greeting header with background image
    st.markdown(
        """
        <div class="header-container">
            <h1>Namaste!! Welcome to Cultural Vista </h1>
            <p>Celebrate India's heritage, traditions, and tourism through insightful visuals and stories.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Load data
    sites_df, footfall_df, endangered_df, budget_df = load_data()

    st.markdown(
    """
    ### 🪔 A Journey Through Timeless Traditions

    🇮🇳 *India is not just a country – it’s a living museum* where every street hums with stories,  
    every festival 🎉 bursts with meaning, and every region guards a piece of humanity’s oldest cultural memory.  

    From the rhythmic beats of *Kathak* 🥁 in Uttar Pradesh, to the delicate strokes of *Pattachitra* 🎨 in Odisha,  
    from the sacred chants 📿 echoing in Himalayan monasteries 🏔, to the vibrant colors of *Rajasthan's folk art* 🐫 —  
    *each expression tells a tale of resilience, faith, and identity.*

    ✨ Travel here isn't about ticking off destinations — it's about immersing in centuries-old legacies that still thrive today.  
    Let’s dive into this cultural canvas and explore the soul of India.

    ---
    """
)

    st.markdown("### 🧭 Summary at a Glance")
    st.markdown("🔍 A snapshot of key indicators representing India's cultural ecosystem.")
    display_metrics(sites_df, footfall_df, endangered_df)

    st.markdown("---")

    st.markdown("### 🌍 Discover Heritage Across States")
    st.markdown("🧱 From forts and temples to monasteries and museums – every dot on the map is a window into history.")
    cultural_hotspots_map(sites_df)

    st.markdown("---")

    st.markdown("### 📈 Tracking Cultural Investment")
    st.markdown("💸 Government investment fuels preservation and growth of heritage. Here's how the art & culture budget evolved.")
    budget_chart(budget_df)

    st.markdown("---")
    st.markdown(
        """
        ### 🧠 Key Insight:
        As tourism expands 📈, the need to protect *diverse traditions and art forms* becomes even more critical.  
        🎉 Let’s celebrate responsibly and preserve what makes India timeless. 🇮🇳
        """
    )

# --------------------- RUN ---------------------

if __name__ == "__main__":
    run_dashboard()
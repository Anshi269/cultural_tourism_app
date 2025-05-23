import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import os
import base64

from govt_initiative.load_data import DATA_PATHS

# Use dark background for all plots
plt.style.use('dark_background')
plt.rcParams.update({
    'text.color': 'white',
    'axes.labelcolor': 'white',
    'xtick.color': 'white',
    'ytick.color': 'white',
})

def plot_pie_with_legend(data, title, figsize=(6, 6), dpi=100):
    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
    fig.patch.set_facecolor('#1a1a1a')
    ax.set_facecolor('#1a1a1a')

    # High-contrast pie chart colors
    colors = plt.cm.tab20.colors  # vibrant and varied color set

    wedges, texts, autotexts = ax.pie(
        data.values,
        labels=None,
        colors=colors,
        autopct='%1.1f%%',
        startangle=140,
        textprops={'fontsize': 10, 'color': 'black'}  # dark text for better contrast
    )
    for autotext in autotexts:
        autotext.set_color('white')  # make percentage text white for visibility

    ax.legend(wedges, data.index, title="Categories", loc="center left", bbox_to_anchor=(1, 0.5))
    ax.set_title(title, fontsize=14)
    ax.axis('equal')
    st.pyplot(fig)

def load_and_display(path, selection):
    try:
        df = pd.read_csv(path)
        st.success(f"📂 Loaded: {path}")
        st.markdown("### 🔍 Quick Preview")
        st.dataframe(df, use_container_width=True, height=500)

        num_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
        cat_cols = df.select_dtypes(include=['object']).columns.tolist()

        if selection == "Heritage Sites" and len(cat_cols) > 0:
            st.markdown("## 🏩 India's Cultural Gems")
            pie_col = st.selectbox("🎨 Choose a column to visualize", cat_cols, key="heritage_pie")
            if pie_col and len(num_cols) > 0:
                value_col = st.selectbox("📊 Select a numeric column to sum", num_cols, key="heritage_value")
                pie_data = df.groupby(pie_col)[value_col].sum().sort_values(ascending=False).head(10)
                plot_pie_with_legend(pie_data, f"Top 10 {pie_col} Distribution", figsize=(8, 8), dpi=120)

        elif selection == "Tourism Trends Statewise" and len(cat_cols) > 0:
            st.markdown("## 🧭 State-wise Tourism Trends")
            pie_col = st.selectbox("📍 Select a state/group column", cat_cols, key="statewise_pie")
            if pie_col and len(num_cols) > 0:
                value_col = st.selectbox("📊 Select numeric column to sum", num_cols, key="statewise_value")
                pie_data = df.groupby(pie_col)[value_col].sum().sort_values(ascending=False).head(10)
                plot_pie_with_legend(pie_data, f"Top 10 {pie_col} by {value_col}")

        elif selection == "Tourism Trends Yearly" and "Year" in df.columns:
            st.markdown("## 📈 Tourism Trends Over the Years")

            df['Year'] = pd.to_numeric(df['Year'], errors='coerce').dropna().astype(int)
            df = df.sort_values(by="Year")

            trend_cols = df.select_dtypes(include=['float64', 'int64']).columns.drop('Year', errors='ignore')

            if len(trend_cols) >= 1:
                selected_metrics = st.multiselect("📊 Select metric(s) to plot", trend_cols, default=list(trend_cols))
                if selected_metrics:
                    st.markdown(f"### 📊 Selected Metrics: {', '.join(selected_metrics)}")
                    fig, ax1 = plt.subplots(figsize=(8, 5))
                    fig.patch.set_facecolor('#1a1a1a')
                    ax1.set_facecolor('#1a1a1a')

                    if "Domestic Tourists (millions)" in selected_metrics:
                        ax1.set_xlabel("Year")
                        ax1.set_ylabel("Domestic Tourists (millions)", color='tab:blue')
                        ax1.plot(df["Year"], df["Domestic Tourists (millions)"], marker='o', color='tab:blue', label="Domestic")
                        ax1.tick_params(axis='y', labelcolor='tab:blue')

                    if "Foreign Tourists (millions)" in selected_metrics:
                        ax2 = ax1.twinx()
                        ax2.set_ylabel("Foreign Tourists (millions)", color='tab:orange')
                        ax2.plot(df["Year"], df["Foreign Tourists (millions)"], marker='o', color='tab:orange', label="Foreign")
                        ax2.tick_params(axis='y', labelcolor='tab:orange')

                    plt.title("Yearly Tourism Trends")
                    fig.tight_layout()
                    st.pyplot(fig)
                else:
                    st.warning("⚠ Select at least one metric to display.")
            else:
                st.warning("⚠ No numeric data to visualize.")

        if selection not in ["Tourism Trends Yearly"]:
            if len(num_cols) > 0:
                st.markdown("## 📊 Data Insights at a Glance")
                selected_num = st.selectbox("📈 Select a numeric column", num_cols)
                if len(cat_cols) > 0:
                    selected_cat = st.selectbox("📂 Group data by category", cat_cols)
                    chart_data = df.groupby(selected_cat)[selected_num].sum().sort_values(ascending=False).head(10)
                    fig, ax = plt.subplots()
                    fig.patch.set_facecolor('#1a1a1a')
                    ax.set_facecolor('#1a1a1a')
                    chart_data.plot(kind='bar', color='teal', ax=ax)
                    ax.set_ylabel(selected_num)
                    ax.set_title(f"{selected_num} by {selected_cat}")
                    st.pyplot(fig)

            if len(cat_cols) > 0:
                st.markdown("## 🥧 Pie Chart Breakdown")
                pie_col = st.selectbox("🔘 Choose a category column", cat_cols, key="generic_pie")
                if pie_col:
                    if len(num_cols) > 0:
                        value_col = st.selectbox("📊 Choose a numeric column to sum", num_cols, key="generic_value")
                        pie_data = df.groupby(pie_col)[value_col].sum().sort_values(ascending=False).head(10)
                    else:
                        pie_data = df[pie_col].value_counts().head(10)
                    plot_pie_with_legend(pie_data, f"Top 10 Distribution of {pie_col}")

    except Exception as e:
        st.error(f"⚠ Error loading data from {path}: {e}")

def main():
    st.set_page_config(page_title="Govt Initiatives & Budget", layout="wide")

    st.markdown("""
        <style>
            body, .stApp {
                background-color: #1a1a1a;
                color: #f5f5f5;
            }
            h1, h2, h3, h4, h5, h6, p, .markdown-text-container, .css-1d391kg, .stSelectbox label, .stMultiSelect label {
                color: #f5f5f5 !important;
            }
            .css-1offfwp {
                background-color: #2b2b2b !important;
                color: #f5f5f5 !important;
            }
            .stDataFrame, .stTable {
                background-color: #2b2b2b !important;
                color: #f5f5f5 !important;
            }
            .stSelectbox > div {
                background-color: #2b2b2b !important;
            }
        </style>
    """, unsafe_allow_html=True)

    try:
        img_path = "govt_initiative/images/image.jpg"
        if os.path.exists(img_path):
            with open(img_path, "rb") as f:
                img_bytes = f.read()
            encoded = base64.b64encode(img_bytes).decode()
            html = f"""
                <div class="banner-container" style="position: relative; text-align: center; margin-bottom: 2rem;">
                    <img src="data:image/jpg;base64,{encoded}" style="width: 100%; height: 350px; object-fit: cover; opacity: 0.8; border-radius: 10px;" />
                    <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); color: #ffe6e6; font-size: 2.5rem; font-weight: bold; text-shadow: 2px 2px 8px #000;">
                        Government Initiatives & Cultural Budget Dashboard
                    </div>
                </div>
            """
            st.markdown(html, unsafe_allow_html=True)
        else:
            st.warning("⚠ Banner image not found.")
    except Exception as e:
        st.warning(f"⚠ Could not load banner image: {e}")

    st.markdown("""
    Welcome to the Govt Initiatives & Budget dashboard 🇮🇳

    This interactive tool brings to light how state and central governments invest in:
    - 🏩 Preserving our rich heritage  
    - 💰 Boosting the cultural economy  
    - 📈 Driving employment through tourism

    Dive into datasets, explore patterns, and uncover how India is shaping its cultural future! 🌟
    """)

    st.markdown("### 📂 Choose a dataset to explore")
    selection = st.selectbox("Dataset", list(DATA_PATHS.keys()))
    load_and_display(DATA_PATHS[selection], selection)

if __name__ == "__main__":
    main()

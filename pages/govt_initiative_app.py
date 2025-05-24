import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import base64
import os
import snowflake.connector

# Use secrets to protect credentials
SNOWFLAKE_CONFIG = {
    "user": st.secrets["snowflake"]["user"],
    "password": st.secrets["snowflake"]["password"],
    "account": st.secrets["snowflake"]["account"],
    "warehouse": st.secrets["snowflake"]["warehouse"],
    "database": st.secrets["snowflake"]["database"],
    "schema": st.secrets["snowflake"]["schema"]
}

DATA_TABLES = {
    "Heritage Sites": "HERITAGE_SITES",
    "Tourism Trends Statewise": "TOURISM_TRENDS_STATE_WISE",
    "Tourism Trends Yearly": "TOURISM_TRENDS_COUNTRY",
    "Employment from Tourism": "EMPLOYMENT_TOURISM",
    "Footfall in Tourism": "FOOTFALL_TOURISM",
    "Endangered Art Forms": "ENDANGERED_ART_FORMS",
    "Art & Culture Budget": "ART_CULTURE_BUDGET"
}

# Matplotlib dark styling
plt.style.use('dark_background')
plt.rcParams.update({
    'text.color': 'white',
    'axes.labelcolor': 'white',
    'xtick.color': 'white',
    'ytick.color': 'white',
})

def get_snowflake_connection():
    return snowflake.connector.connect(
        user=SNOWFLAKE_CONFIG['user'],
        password=SNOWFLAKE_CONFIG['password'],
        account=SNOWFLAKE_CONFIG['account'],
        warehouse=SNOWFLAKE_CONFIG['warehouse'],
        database=SNOWFLAKE_CONFIG['database'],
        schema=SNOWFLAKE_CONFIG['schema'],
    )

def fetch_data_from_snowflake(table_name):
    try:
        conn = get_snowflake_connection()
        query = f"SELECT * FROM {table_name}"
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"⚠ Error fetching data from Snowflake: {e}")
        return pd.DataFrame()

def plot_pie_with_legend(data, title, figsize=(6, 6), dpi=100):
    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
    fig.patch.set_facecolor('#2e0f0f')
    ax.set_facecolor('#2e0f0f')
    colors = plt.cm.tab20.colors

    wedges, texts, autotexts = ax.pie(
        data.values,
        labels=None,
        colors=colors,
        autopct='%1.1f%%',
        startangle=140,
        textprops={'fontsize': 10, 'color': 'black'}
    )
    for autotext in autotexts:
        autotext.set_color('white')

    ax.legend(wedges, data.index, title="Categories", loc="center left", bbox_to_anchor=(1, 0.5))
    ax.set_title(title, fontsize=14)
    ax.axis('equal')
    st.pyplot(fig)

def load_and_display(table_name, selection):
    df = fetch_data_from_snowflake(table_name)
    if df.empty:
        st.warning(f"No data available for {selection}")
        return

    st.success(f"📊 Data loaded from Snowflake table: {table_name}")
    st.markdown("### 🔍 Quick Preview")
    st.dataframe(df, use_container_width=True, height=500)

    df.columns = [col.strip().upper() for col in df.columns]
    num_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
    cat_cols = df.select_dtypes(include=['object']).columns.tolist()

    if selection == "Tourism Trends Yearly":
        st.markdown("## 📈 Tourism Trends Over the Years")

        df.rename(columns={
            "YEAR": "Year",
            "DOMESTIC_TOURISTS_MILLIONS_": "Domestic Tourists (Millions)",
            "FOREIGN_TOURISTS_MILLIONS_": "Foreign Tourists (Millions)"
        }, inplace=True)

        if "Year" not in df.columns:
            st.warning("⚠ 'Year' column not found in the dataset.")
            return

        df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
        df = df.dropna(subset=['Year'])
        df['Year'] = df['Year'].astype(int)
        df = df.sort_values(by='Year')

        trend_cols = df.select_dtypes(include=['float64', 'int64']).columns.drop('Year', errors='ignore')

        if trend_cols.empty:
            st.warning("⚠ No numeric trend columns found.")
            return

        selected_metrics = st.multiselect("📊 Select metrics to plot", trend_cols.tolist(), default=trend_cols.tolist())
        if selected_metrics:
            st.markdown(f"### 📊 Selected Metrics: {', '.join(selected_metrics)}")

            fig, axes = plt.subplots(nrows=len(selected_metrics), ncols=1, figsize=(10, 6 * len(selected_metrics)), sharex=True)
            fig.patch.set_facecolor('#2e0f0f')

            if len(selected_metrics) == 1:
                axes = [axes]

            for ax, col in zip(axes, selected_metrics):
                ax.set_facecolor('#2e0f0f')
                ax.plot(df['Year'], df[col], marker='o', label=col)
                ax.set_ylabel("Value (in Millions)")
                ax.set_title(col)
                ax.legend()

            axes[-1].set_xlabel("Year")
            st.pyplot(fig)
        else:
            st.warning("⚠ Select at least one metric to display.")

    elif selection == "Heritage Sites" and len(cat_cols) > 0:
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

    if selection != "Tourism Trends Yearly":
        if len(num_cols) > 0:
            st.markdown("## 📊 Data Insights at a Glance")
            selected_num = st.selectbox("📈 Select a numeric column", num_cols)
            if len(cat_cols) > 0:
                selected_cat = st.selectbox("📂 Group data by category", cat_cols)
                chart_data = df.groupby(selected_cat)[selected_num].sum().sort_values(ascending=False).head(10)
                fig, ax = plt.subplots()
                fig.patch.set_facecolor('#2e0f0f')
                ax.set_facecolor('#2e0f0f')
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

def main():
    st.set_page_config(page_title="Govt Initiatives & Budget", layout="wide")

    st.markdown("""<style>
        body, .stApp { background-color: #2e0f0f; color: #f5f5f5; }
        h1, h2, h3, h4, h5, h6, p, .markdown-text-container, .stSelectbox label, .stMultiSelect label {
            color: #f5f5f5 !important;
        }
        .css-1offfwp, .stDataFrame, .stTable {
            background-color: #3a1a1a !important;
            color: #f5f5f5 !important;
        }
    </style>""", unsafe_allow_html=True)

    try:
        img_path = "govt_initiative/images/image.jpg"
        if os.path.exists(img_path):
            with open(img_path, "rb") as f:
                img_bytes = f.read()
            encoded = base64.b64encode(img_bytes).decode()
            st.markdown(f"""
                <div style="position: relative; text-align: center; margin-bottom: 2rem;">
                    <img src="data:image/jpg;base64,{encoded}" style="width: 100%; height: 350px; object-fit: cover; opacity: 0.8; border-radius: 10px;" />
                    <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
                                color: #ffe6e6; font-size: 2.5rem; font-weight: bold; text-shadow: 2px 2px 8px #000;">
                        Government Initiatives & Cultural Budget Dashboard
                    </div>
                </div>
            """, unsafe_allow_html=True)
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
    selection = st.selectbox("Dataset", list(DATA_TABLES.keys()))
    load_and_display(DATA_TABLES[selection], selection)

if __name__ == "__main__":
    main()

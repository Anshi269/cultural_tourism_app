import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import snowflake.connector

# -------------------- Snowflake Config --------------------
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

# -------------------- Matplotlib Dark Styling --------------------
plt.style.use('dark_background')
plt.rcParams.update({
    'text.color': 'white',
    'axes.labelcolor': 'white',
    'xtick.color': 'white',
    'ytick.color': 'white',
})

# -------------------- Snowflake Connection --------------------
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

# -------------------- Pie Chart with Legend --------------------
def plot_pie_with_legend(data, title, figsize=(6, 6), dpi=100):
    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
    fig.patch.set_facecolor('#1a1a1a')
    ax.set_facecolor('#1a1a1a')
    colors = plt.cm.tab20.colors

    wedges, _, autotexts = ax.pie(
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

# -------------------- Display Handler --------------------
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
            st.warning("⚠ 'Year' column not found.")
            return

        df['Year'] = pd.to_numeric(df['Year'], errors='coerce').dropna().astype(int)
        df = df.sort_values(by='Year')

        trend_cols = df.select_dtypes(include=['float64', 'int64']).columns.drop('Year', errors='ignore')

        selected_metrics = st.multiselect("📊 Select metrics to plot", trend_cols.tolist(), default=trend_cols.tolist())
        if selected_metrics:
            fig, axes = plt.subplots(nrows=len(selected_metrics), ncols=1, figsize=(10, 6 * len(selected_metrics)), sharex=True)
            fig.patch.set_facecolor('#1a1a1a')

            if len(selected_metrics) == 1:
                axes = [axes]

            for ax, col in zip(axes, selected_metrics):
                ax.set_facecolor('#1a1a1a')
                ax.plot(df['Year'], df[col], marker='o', label=col)
                ax.set_ylabel("Value")
                ax.set_title(col)
                ax.legend()

            axes[-1].set_xlabel("Year")
            st.pyplot(fig)
        else:
            st.warning("⚠ Select at least one metric.")

    elif selection == "Heritage Sites" and cat_cols:
        st.markdown("## 🏩 India's Cultural Gems")
        pie_col = st.selectbox("🎨 Choose a category column", cat_cols, key="heritage_pie")
        if pie_col and num_cols:
            value_col = st.selectbox("📊 Numeric column to sum", num_cols, key="heritage_value")
            pie_data = df.groupby(pie_col)[value_col].sum().sort_values(ascending=False).head(10)
            plot_pie_with_legend(pie_data, f"Top 10 {pie_col}")

    elif selection == "Tourism Trends Statewise" and cat_cols:
        st.markdown("## 🧭 State-wise Tourism Trends")
        pie_col = st.selectbox("📍 State/Group Column", cat_cols, key="statewise_pie")
        if pie_col and num_cols:
            value_col = st.selectbox("📊 Numeric column to sum", num_cols, key="statewise_value")
            pie_data = df.groupby(pie_col)[value_col].sum().sort_values(ascending=False).head(10)
            plot_pie_with_legend(pie_data, f"Top 10 {pie_col} by {value_col}")

    # Generic bar and pie insights for other tables
    if selection not in ["Tourism Trends Yearly"]:
        if num_cols:
            st.markdown("## 📊 Top Categories by Numeric Column")
            selected_num = st.selectbox("📈 Numeric Column", num_cols)
            if cat_cols:
                selected_cat = st.selectbox("📂 Group by", cat_cols)
                bar_data = df.groupby(selected_cat)[selected_num].sum().sort_values(ascending=False).head(10)
                fig, ax = plt.subplots()
                fig.patch.set_facecolor('#1a1a1a')
                ax.set_facecolor('#1a1a1a')
                bar_data.plot(kind='bar', color='teal', ax=ax)
                ax.set_ylabel(selected_num)
                ax.set_title(f"{selected_num} by {selected_cat}")
                st.pyplot(fig)

        if cat_cols:
            st.markdown("## 🥧 Pie Chart Breakdown")
            pie_col = st.selectbox("🔘 Category Column", cat_cols, key="generic_pie")
            if pie_col:
                if num_cols:
                    value_col = st.selectbox("📊 Numeric column to sum", num_cols, key="generic_value")
                    pie_data = df.groupby(pie_col)[value_col].sum().sort_values(ascending=False).head(10)
                else:
                    pie_data = df[pie_col].value_counts().head(10)
                plot_pie_with_legend(pie_data, f"Top 10 Distribution of {pie_col}")

# -------------------- Main App --------------------
def main():
    st.set_page_config(page_title="Cultural Tourism Dashboard", layout="wide")
    st.title("🧭 Cultural Tourism Dashboard (via Snowflake)")

    selection = st.sidebar.selectbox("📁 Select Dataset", list(DATA_TABLES.keys()))
    if selection:
        table_name = DATA_TABLES[selection]
        load_and_display(table_name, selection)

if __name__ == "__main__":
    main()

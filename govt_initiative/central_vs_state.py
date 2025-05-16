import streamlit as st
import plotly.express as px

def show(df):
    summary = df.groupby("Year")[["State Budget", "Central Budget"]].sum().reset_index()

    st.markdown("### 📎 Stacked Bar Chart of Central vs State Budget")
    fig_bar = px.bar(
        summary,
        x="Year",
        y=["State Budget", "Central Budget"],
        barmode="stack",
        title="Central vs State Budget Over Years",
        labels={"value": "Budget (Cr)", "variable": "Type"},
        color_discrete_map={"State Budget": "lightblue", "Central Budget": "orange"}
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown("### 🥧 Pie Chart of Latest Year Allocation")
    latest = df[df["Year"] == df["Year"].max()]
    totals = latest[["State Budget", "Central Budget"]].sum()
    pie_df = totals.reset_index().rename(columns={"index": "Type", 0: "Budget"})

    fig_pie = px.pie(
        pie_df,
        names="Type",
        values="Budget",
        title=f"Budget Allocation for {df['Year'].max()}",
        color_discrete_sequence=["lightblue", "orange"]
    )
    st.plotly_chart(fig_pie, use_container_width=True)
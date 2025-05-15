import streamlit as st
import plotly.express as px
import pandas as pd

def show(budget_df, tourism_df):
    # Merge on State and Year
    merged = pd.merge(budget_df, tourism_df, on=["State", "Year"], how="inner")
    merged = merged.dropna(subset=["State Budget", "Total Tourists"])

    fig = px.scatter(
        merged,
        x="State Budget",
        y="Total Tourists",
        color="State",
        size="Total Tourists",
        title="State Budget vs Tourist Footfall",
        labels={"State Budget": "Cultural Budget (Cr)", "Total Tourists": "Tourist Footfall"}
    )
    st.plotly_chart(fig, use_container_width=True)
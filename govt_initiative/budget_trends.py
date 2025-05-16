import streamlit as st
import plotly.express as px

def show(df):
    fig = px.bar(
        df,
        x="Year",
        y="Total Budget",
        color="Type",
        barmode="group",
        title="Total Cultural Budget by Type Over Years"
    )
    st.plotly_chart(fig, use_container_width=True)